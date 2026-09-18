#!/usr/bin/env python3
"""Fail when a public repository contains common secrets or unsafe artifacts."""

from __future__ import annotations

import argparse
import re
import sys
import subprocess
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "coverage", "__pycache__"}
BLOCKED_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json", "service-account.json"}
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
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Windows user path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+"),
}


def history_findings(root: Path, revision: str) -> list[str]:
    """Check commit identities/messages and patches, including deleted text.

    Only report commit hashes and rule names; never print the matched value.
    """
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
            findings.extend(history_findings(root, args.history))
        except subprocess.CalledProcessError:
            findings.append("cannot read requested Git history")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts) or not path.is_file():
            continue
        lowered = path.name.lower()
        if lowered in BLOCKED_NAMES or (lowered.startswith(".env.") and lowered != ".env.example"):
            findings.append(f"blocked filename: {relative}")
        size = path.stat().st_size
        if size > FILE_LIMIT:
            findings.append(f"file larger than {FILE_LIMIT} bytes: {relative}")
        if size > TEXT_LIMIT:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append(f"{label}: {relative}")
        haystack = f"{relative}\n{content}".casefold()
        for term in args.deny_term:
            if term and term.casefold() in haystack:
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
