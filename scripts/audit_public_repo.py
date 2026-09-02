#!/usr/bin/env python3
"""Fail when a public repository contains common secrets or unsafe artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "coverage", "__pycache__"}
BLOCKED_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json", "service-account.json"}
TEXT_LIMIT = 2_000_000
FILE_LIMIT = 10_000_000
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{40,})"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Windows user path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--deny-term", action="append", default=[], help="Local confidential term; repeat as needed")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[str] = []

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
