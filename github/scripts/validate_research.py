#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path


RESEARCH_PATH = Path("artifacts/research/research.md")
SECURITY_PATH = Path("artifacts/security/securityassessment.md")
PIPELINE_PATH = Path("docs/orchestration/pipeline.md")


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def changed_files(base_ref: str) -> set[str]:
    out = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    if not out:
        return set()
    return {line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()}


def count_mslearn_refs(text: str) -> int:
    return len(re.findall(r"https?://learn\.microsoft\.com[^\s\)]*", text, flags=re.IGNORECASE))


def has_required_sections(text: str, sections: list[str]) -> list[str]:
    missing = []
    for section in sections:
        if section.lower() not in text.lower():
            missing.append(section)
    return missing


def validate(
    research_required: bool,
    security_required: bool,
    pipeline_required: bool = False,
) -> list[str]:
    errors: list[str] = []

    if research_required and not RESEARCH_PATH.exists():
        errors.append(f"Missing required file: {RESEARCH_PATH.as_posix()}")
    if security_required and not SECURITY_PATH.exists():
        errors.append(f"Missing required file: {SECURITY_PATH.as_posix()}")
    if pipeline_required and not PIPELINE_PATH.exists():
        errors.append(f"Missing orchestration contract: {PIPELINE_PATH.as_posix()}")

    if RESEARCH_PATH.exists():
        research = RESEARCH_PATH.read_text(encoding="utf-8")
        required = [
            "## Assumptions",
            "## Known gotchas",
            "## Open questions",
            "## References",
        ]
        missing = has_required_sections(research, required)
        if missing:
            errors.append(
                "Research file is missing required sections: " + ", ".join(missing)
            )

        refs = count_mslearn_refs(research)
        if refs < 5:
            errors.append(
                f"Research file has only {refs} Microsoft Learn references; expected at least 5."
            )

        for key in ["Source URL", "Access date", "Confidence"]:
            if key.lower() not in research.lower():
                errors.append(f"Research references should include '{key}'.")

    if SECURITY_PATH.exists():
        security = SECURITY_PATH.read_text(encoding="utf-8")
        required = [
            "## Threat model summary",
            "## Risk register",
            "## Residual risks",
            "## References",
        ]
        missing = has_required_sections(security, required)
        if missing:
            errors.append(
                "Security file is missing required sections: " + ", ".join(missing)
            )

    if PIPELINE_PATH.exists():
        pipeline = PIPELINE_PATH.read_text(encoding="utf-8")
        for required in ["Research", "Validate", "Security"]:
            if required.lower() not in pipeline.lower():
                errors.append(
                    f"Pipeline contract should include stage '{required}' in {PIPELINE_PATH.as_posix()}."
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument(
        "--stage",
        choices=["research", "security", "pipeline", "full"],
        default="full",
    )
    args = parser.parse_args()

    changed = set()
    if args.changed_only:
        changed = changed_files(args.base_ref)

    research_changed = RESEARCH_PATH.as_posix() in changed if changed else RESEARCH_PATH.exists()
    security_changed = SECURITY_PATH.as_posix() in changed if changed else SECURITY_PATH.exists()

    # If research changes, security must be updated in the same PR by policy.
    if args.changed_only and research_changed and not security_changed:
        print(
            "ERROR: Research artifact changed but security artifact was not changed in this PR.",
            file=sys.stderr,
        )
        return 1

    if args.stage == "research":
        errors = validate(
            research_required=True,
            security_required=False,
            pipeline_required=False,
        )
    elif args.stage == "security":
        errors = validate(
            research_required=False,
            security_required=True,
            pipeline_required=False,
        )
    elif args.stage == "pipeline":
        errors = validate(
            research_required=False,
            security_required=False,
            pipeline_required=True,
        )
    else:
        errors = validate(
            research_required=research_changed or not args.changed_only,
            security_required=security_changed or not args.changed_only,
            pipeline_required=not args.changed_only,
        )

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

