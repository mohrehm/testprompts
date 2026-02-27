# Repository AI Instructions

Use these instructions when generating or modifying research/security artifacts.

## Scope
- This repository uses a research-first workflow with security assessment always required.
- Use this workflow when user intent is research, analysis, architecture guidance, or decision support.

## Required Workflow
1. Research and draft in `artifacts/research/research.md`
2. Validate and refine with practical gotchas
3. Produce/update `artifacts/security/securityassessment.md` (mandatory)
4. Optional deck/presentation generation

## Modes
- `quick`: concise but complete recommendations
- `deep`: comprehensive analysis (default when unspecified)

## Quality Bar
- Microsoft-related topics must use Microsoft Learn as primary baseline.
- Include at least 5 Microsoft Learn references when available.
- For key claims, include source URL, access date, and confidence.
- Preserve sections:
  - Assumptions
  - Known gotchas
  - Open questions
- Include Mermaid diagrams and configuration snippets where useful.

## File Conventions
- Update existing artifacts in place.
- Keep a short `Change log` section.
- Use clear headings and checklists for implementation and troubleshooting.

## Security Expectations
- Security assessment is always required with:
  - threat model summary
  - risk register
  - mitigations and residual risks
  - security checklist

