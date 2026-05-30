#!/usr/bin/env python3
"""Public disclosure safety scanner for documentation repositories."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


BLOCKER = "BLOCKER"
WARNING = "WARNING"
OK = "OK"

IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

SCAN_SUFFIXES = {
    ".md",
    ".txt",
    ".rst",
    ".adoc",
    ".json",
    ".yaml",
    ".yml",
}

MAX_FILE_BYTES = 2 * 1024 * 1024

DIVIPER_STACK_NAME = "diviper" + "-stack"
DIVIPER_STACK_PATH = "/opt/" + DIVIPER_STACK_NAME
PRIVATE_IP_PREFIX = "90" + ".156"

TOKEN_VALUE_RE = re.compile(
    r"\b(?:OPENAI_API_KEY|API_KEY|TOKEN|SECRET|PASSWORD|PRIVATE_KEY|COOKIE|AUTH)"
    r"[A-Z0-9_-]*\s*(?:=|:)\s*[\"']?(?!<)[A-Za-z0-9_./:+\-]{6,}",
    re.IGNORECASE,
)
CHAT_THREAD_VALUE_RE = re.compile(
    r"\b(?:chat_id|thread_id)\s*(?:=|:)\s*[\"']?-?\d{4,}",
    re.IGNORECASE,
)
COMMON_TOKEN_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{12,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)
IPV4_RE = re.compile(
    r"(?<![\d.])"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}"
    r"(?![\d.])"
)
WINDOWS_PRIVATE_PATH_RE = re.compile(
    r"\b[A-Za-z]:\\(?:Users|Codex|ServerDi|ProgramData|Windows)\\[^\s`'\"\])>]+",
    re.IGNORECASE,
)
UNIX_PRIVATE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])/(?:home|root|etc|var|srv|opt)/[^\s`'\"\])>]+",
    re.IGNORECASE,
)
RAW_LOG_RE = re.compile(
    r"^\s*(?:"
    r"\d{4}-\d{2}-\d{2}[T ][0-2]\d:[0-5]\d:[0-5]\d"
    r"|\[[A-Z][A-Z0-9_-]{2,}\]"
    r"|(?:TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b"
    r")"
)

DANGEROUS_TERM_RES = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\btoken(s)?\b",
        r"\bsecret(s)?\b",
        r"\bapi[_ -]?key(s)?\b",
        r"\bopenai_api_key\b",
        r"\bchat[_ -]?id\b",
        r"\bthread[_ -]?id\b",
        r"(?<![A-Za-z0-9_])\.env(?:\.[A-Za-z0-9_-]+)?",
        r"\bcookie(s)?\b",
        r"\bauth\b",
        r"\bpassword(s)?\b",
        r"\bprivate[_ -]?key(s)?\b",
        r"\bmedication\b",
        r"\bmedicine\b",
        r"\bbilling\b",
        r"\braw log(s)?\b",
        r"\bprivate path(s)?\b",
    )
]

GUIDANCE_SUPPRESSED_PATHS = {
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    line: int
    marker: str
    message: str
    excerpt: str


@dataclass(frozen=True)
class ScanResult:
    status: str
    scanned_files: int
    skipped_files: int
    blockers: int
    warnings: int
    findings: list[Finding]


def is_ignored_dir(name: str) -> bool:
    lowered = name.lower()
    return lowered in IGNORED_DIRS or "pycache" in lowered


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return

    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if not is_ignored_dir(name)]
        for filename in filenames:
            yield Path(current_root) / filename


def to_relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def should_scan_contents(path: Path) -> bool:
    return path.suffix.lower() in SCAN_SUFFIXES


def is_env_file_path(relative_path: str) -> bool:
    parts = Path(relative_path).parts
    return any(part == ".env" or part.startswith(".env.") for part in parts)


def is_serverdi_topic_os_root(root: Path) -> bool:
    return (
        (root / "README.md").is_file()
        and (root / "docs" / "SERVERDI_AGENT_OPERATING_MANUAL.md").is_file()
        and (root / "docs" / "COSTGATE_APPROVAL_POLICY.md").is_file()
    )


def is_guidance_suppressed(relative_path: str, suppress_baseline_guidance: bool) -> bool:
    if not suppress_baseline_guidance:
        return False
    normalized = relative_path.replace("\\", "/")
    return (
        normalized in GUIDANCE_SUPPRESSED_PATHS
        or normalized.startswith("docs/")
        or normalized.startswith("examples/")
    )


def clean_excerpt(line: str) -> str:
    stripped = line.strip()
    if len(stripped) <= 140:
        return stripped
    return stripped[:137] + "..."


def blocker_patterns(line: str) -> Sequence[tuple[str, str]]:
    checks: list[tuple[re.Pattern[str] | str, str, str]] = [
        (TOKEN_VALUE_RE, "token-like value", "likely real credential-style value"),
        (CHAT_THREAD_VALUE_RE, "telegram id value", "likely real Telegram chat or topic identifier"),
        (COMMON_TOKEN_RE, "token-like value", "likely real token-shaped value"),
        (WINDOWS_PRIVATE_PATH_RE, "private path", "likely real private Windows path"),
        (UNIX_PRIVATE_PATH_RE, "private path", "likely real private Unix path"),
        (RAW_LOG_RE, "raw log marker", "raw log-style line"),
        (DIVIPER_STACK_PATH, "private path marker", "unsafe literal private stack path"),
        (DIVIPER_STACK_NAME, "private path marker", "unsafe literal private stack marker"),
        (PRIVATE_IP_PREFIX, "private IP marker", "unsafe literal IP prefix"),
    ]

    findings: list[tuple[str, str]] = []
    for pattern, marker, message in checks:
        if isinstance(pattern, str):
            if pattern.lower() in line.lower():
                findings.append((marker, message))
        elif pattern.search(line):
            findings.append((marker, message))

    if IPV4_RE.search(line) and "<" not in line:
        findings.append(("ip address", "likely real IP address"))

    return findings


def dangerous_terms(line: str) -> list[str]:
    markers: list[str] = []
    for pattern in DANGEROUS_TERM_RES:
        match = pattern.search(line)
        if match:
            markers.append(match.group(0))
    return markers


def scan_line(
    relative_path: str,
    line_number: int,
    line: str,
    suppress_baseline_guidance: bool = False,
) -> list[Finding]:
    findings: list[Finding] = []
    excerpt = clean_excerpt(line)

    for marker, message in blocker_patterns(line):
        findings.append(
            Finding(
                severity=BLOCKER,
                path=relative_path,
                line=line_number,
                marker=marker,
                message=message,
                excerpt=excerpt,
            )
        )

    if findings:
        return findings

    if is_guidance_suppressed(relative_path, suppress_baseline_guidance):
        return []

    for marker in dangerous_terms(line):
        findings.append(
            Finding(
                severity=WARNING,
                path=relative_path,
                line=line_number,
                marker=marker,
                message="dangerous term appears in documentation or safety guidance",
                excerpt=excerpt,
            )
        )

    return findings


def scan_file(
    path: Path,
    root: Path,
    suppress_baseline_guidance: bool = False,
) -> tuple[list[Finding], bool]:
    relative_path = to_relative(path, root)
    findings: list[Finding] = []

    if is_env_file_path(relative_path):
        findings.append(
            Finding(
                severity=BLOCKER,
                path=relative_path,
                line=0,
                marker=".env file",
                message="env files must not be committed to public documentation repositories",
                excerpt=relative_path,
            )
        )
        return findings, False

    if not should_scan_contents(path):
        return findings, True

    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return findings, True
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings, True

    for line_number, line in enumerate(text.splitlines(), start=1):
        findings.extend(
            scan_line(relative_path, line_number, line, suppress_baseline_guidance)
        )

    return findings, False


def scan_path(root: Path) -> ScanResult:
    root = root.resolve()
    findings: list[Finding] = []
    scanned_files = 0
    skipped_files = 0
    suppress_baseline_guidance = is_serverdi_topic_os_root(root)

    for path in iter_files(root):
        file_findings, skipped = scan_file(path, root, suppress_baseline_guidance)
        findings.extend(file_findings)
        if skipped:
            skipped_files += 1
        else:
            scanned_files += 1

    blockers = sum(1 for finding in findings if finding.severity == BLOCKER)
    warnings = sum(1 for finding in findings if finding.severity == WARNING)
    if blockers:
        status = BLOCKER
    elif warnings:
        status = WARNING
    else:
        status = OK

    return ScanResult(
        status=status,
        scanned_files=scanned_files,
        skipped_files=skipped_files,
        blockers=blockers,
        warnings=warnings,
        findings=findings,
    )


def result_to_json(result: ScanResult) -> str:
    payload = asdict(result)
    return json.dumps(payload, indent=2, sort_keys=True)


def print_human_report(result: ScanResult, root: Path, strict: bool) -> None:
    print("Public safety scan")
    print(f"Root: {root}")
    print(f"Status: {result.status}")
    print(f"Scanned files: {result.scanned_files}")
    print(f"Skipped files: {result.skipped_files}")
    print(f"Blockers: {result.blockers}")
    print(f"Warnings: {result.warnings}")
    print(f"Strict: {'yes' if strict else 'no'}")

    if not result.findings:
        print("No findings.")
        return

    print()
    print("Findings:")
    for finding in result.findings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"- {location} [{finding.severity}] {finding.marker}: {finding.message}")
        if finding.excerpt:
            print(f"  {finding.excerpt}")


def exit_code(result: ScanResult, strict: bool) -> int:
    if result.blockers:
        return 1
    if strict and result.warnings:
        return 1
    return 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan public docs and prompt templates for disclosure-risk markers."
    )
    parser.add_argument("path", help="file or directory to scan")
    parser.add_argument("--json", action="store_true", help="output JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failure",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(args.path)
    result = scan_path(root)

    if args.json:
        print(result_to_json(result))
    else:
        print_human_report(result, root, args.strict)

    return exit_code(result, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
