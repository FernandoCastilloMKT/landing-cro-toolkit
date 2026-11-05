#!/usr/bin/env python3
"""Fail when a public repository contains common secrets or unsafe artifacts."""

from __future__ import annotations

import argparse
import re
import sys
import subprocess
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "coverage", "__pycache__"}
BLOCKED_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json", "service-account.json",
                 ".clasp.json", ".clasprc.json", ".webapp-deployment.json"}
BLOCKED_DIRS = {"credentials", ".secrets", ".ssh", ".openai", ".playwright-cli"}
BLOCKED_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".har", ".sqlite", ".7z", ".zip"}
TEXT_LIMIT = 2_000_000
FILE_LIMIT = 10_000_000
PATTERNS = {
    "personal email": re.compile(
        r"\b[A-Z0-9._%+-]+@(?!(?:users\.noreply\.github\.com|example\.invalid)\b)"
        r"(?!noreply\.github\.com\b)[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I
    ),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{40,})"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "Google OAuth secret": re.compile(r"\bGOCSPX-[A-Za-z0-9_-]{20,}\b"),
    "Google refresh token": re.compile(r"(?<!\w)1//[A-Za-z0-9_-]{30,}"),
    "Google OAuth client": re.compile(r"\b\d{8,}-[a-z0-9_-]{16,}\.apps\.googleusercontent\.com\b", re.I),
    "Meta access token": re.compile(r"\bEA[A-Za-z0-9]{60,}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "advertising identifier": re.compile(r"(?<!\d)(?!000-000-0000)\d{3}-\d{3}-\d{4}(?!\d)"),
    "measurement identifier": re.compile(r"\b(?:GTM-[A-Z0-9]{6,}|G-[A-Z0-9]{10})\b"),
    "spreadsheet URL": re.compile(r"/spreadsheets/d/(?!EXAMPLE_)[A-Za-z0-9_-]{24,}"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Windows user path": re.compile(r"(?i)[A-Z]:[\\/]Users[\\/][^\\/\s]+"),
}


def blocked_path(path: Path) -> bool:
    name = path.name.lower()
    return (name in BLOCKED_NAMES or (name.startswith('.env.') and name != '.env.example')
            or bool(set(path.parts) & BLOCKED_DIRS) or path.suffix.lower() in BLOCKED_SUFFIXES)


def confidential_match(text: str, terms) -> bool:
    return any(re.search(r'[\s_.-]*'.join(re.escape(p) for p in term.split()), text, re.I)
               for term in terms if term.strip())


def history_findings(root: Path, revision: str, deny_terms=()) -> list[str]:
    """Check commit identities/messages and patches, including deleted text.

    Only report commit hashes and rule names; never print the matched value.
    """
    actual_root = subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', '--show-toplevel'], text=True,
    ).strip()
    if Path(actual_root).resolve() != root.resolve():
        return ['history root is not an independent Git checkout']
    shallow = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--is-shallow-repository"], text=True
    ).strip()
    if shallow == "true":
        return ["history incomplete: fetch full history before auditing"]
    commits = subprocess.check_output(
        ["git", "-C", str(root), "rev-list", revision], text=True
    ).split()
    findings = []
    for commit in commits:
        text = subprocess.check_output(
            ["git", "-C", str(root), "show", "--format=fuller", "--root", "-m",
             "--no-ext-diff", "--no-textconv", "--no-color", commit],
        ).decode("utf-8", errors="replace")
        # GitHub's own committer address is not a private mailbox.
        text = text.replace("<noreply" + "@" + "github.com>", "<github-system>")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: commit {commit}")
        if confidential_match(text, deny_terms):
            findings.append(f"confidential deny-term: commit {commit}")
        names = subprocess.check_output(
            ['git', '-C', str(root), 'ls-tree', '-r', '--name-only', commit], text=True,
        ).splitlines()
        if any(blocked_path(Path(name)) for name in names):
            findings.append(f"blocked historical path: commit {commit}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--deny-term", action="append", default=[], help="Local confidential term; repeat as needed")
    parser.add_argument("--history", metavar="REV", help="Audit complete reachable history, e.g. HEAD or --all")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[str] = []
    if args.history:
        try:
            findings.extend(history_findings(root, args.history, args.deny_term))
        except subprocess.CalledProcessError:
            findings.append("cannot read requested Git history")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts) or (not path.is_file() and not path.is_symlink()):
            continue
        if blocked_path(relative):
            findings.append(f"blocked filename: {relative}")
        if path.is_symlink():
            findings.append(f"symlink not allowed: {relative}")
            continue
        size = path.stat().st_size
        if size > FILE_LIMIT:
            findings.append(f"file larger than {FILE_LIMIT} bytes: {relative}")
        if size > TEXT_LIMIT:
            findings.append(f"file too large for text audit: {relative}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico', '.woff', '.woff2'}:
                findings.append(f"unreadable non-media file: {relative}")
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append(f"{label}: {relative}")
        haystack = f"{relative}\n{content}".casefold()
        if confidential_match(haystack, args.deny_term):
            findings.append(f"confidential deny-term: {relative}")

    if findings:
        print("Audit failed:")
        for finding in sorted(set(findings)):
            print(f"- {finding}")
        return 1
    print("Audit passed: no blocked patterns or artifacts found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
