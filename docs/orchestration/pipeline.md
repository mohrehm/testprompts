# Research Orchestration Pipeline

## Purpose
Mimic Cursor-native orchestration behavior in a VS Code + GitHub workflow by using:
- a controller contract
- specialist prompt packs
- file-based state handoff
- CI quality gates

## Stage Contract (must run in order)
1. **Research**
   - Input: issue/request scope, architecture context
   - Output: `artifacts/research/research.md`
2. **Validate/Gotchas**
   - Input: `artifacts/research/research.md`, local architecture docs
   - Output: update `artifacts/research/research.md`
3. **Security Assessment (required)**
   - Input: `artifacts/research/research.md`
   - Output: `artifacts/security/securityassessment.md`
4. **Deck (optional)**
   - Input: research and security artifacts
   - Output: `artifacts/deck/presentation.md`

## Rules
- Never skip stage 3 (Security Assessment).
- Use Microsoft Learn as baseline for Microsoft topics.
- Include at least 5 Microsoft Learn references when available.
- Include source URL, access date, and confidence for key claims.
- Preserve `Assumptions`, `Known gotchas`, and `Open questions`.

## Handoff Model
- Treat artifact files as the only source of truth between stages.
- Do not rely on chat memory for stage context.
- Append a short change note under `Change log` for each stage update.

## Local Execution
- Run `scripts/orchestrate.ps1` for guided stage progression.
- Run VS Code tasks for validation before opening PR.

## CI Enforcement
- PRs to `main` run stage-aware validation checks.
- If research changes, security artifact must also change.
- CODEOWNERS and branch protection enforce review gates.

