# Cursor vs VS Code + GitHub Copilot: Comparison and File Inventory

## 1. What Happened to Skills and Subagents?

### Cursor (native)

| Concept | How it works |
|---------|--------------|
| **Skills** | Stored in `.cursor/skills/<name>/SKILL.md`. Procedural playbooks with YAML frontmatter. Auto-discovered by Cursor. Subagents are instructed to "read SKILL.md" as their procedure. |
| **Subagents** | Defined in `.cursor/agents/<name>.md` with `name`, `description`, `model`, `readonly`. Invoked via slash commands (e.g. `/researcher-mslearn`). Run in **isolated context** — they start fresh and only receive what the parent passes. |
| **Orchestration** | Commands (`.cursor/commands/*.md`) define execution order: "Run subagent X, then Y, then Z." The main agent delegates; subagents report back. |

### VS Code + GitHub Copilot (mimic)

| Concept | Equivalent |
|---------|------------|
| **Skills** | **Prompt packs** in `docs/prompts/*.md`. Human copies prompt into Copilot Chat and runs it. No auto-discovery; no "read SKILL" instruction — you paste the prompt. |
| **Subagents** | **Role prompts** — same files. Each prompt defines a specialist role. No isolated context; Copilot Chat uses a single shared conversation. You must **manually switch** prompts per stage. |
| **Orchestration** | `scripts/orchestrate.ps1` guides you step-by-step. You run each stage yourself by pasting the right prompt. CI (`research-orchestration-gates.yml`) enforces stage order and coupling. |

**Summary**: Skills and subagents are **not native** in VS Code + Copilot. They are **simulated** via prompt files + guided script + CI. You lose automatic delegation and context isolation.

---

## 2. Can Concurrent Subagent Execution Still Be Possible?

### Cursor

- **Yes.** Cursor can launch multiple subagents in parallel (e.g. researcher + validator in separate contexts). Each subagent has its own context window. Parent aggregates results.

### VS Code + GitHub Copilot

- **No.** Copilot Chat is a single conversation. You cannot run multiple "subagents" concurrently in the same session. Options:
  - **Sequential only**: Run stage 1, paste output, run stage 2, etc.
  - **Parallel workaround**: Open multiple Copilot Chat sessions (e.g. different VS Code windows or split panels) and run different prompts in each — but handoff between them is manual (copy/paste artifacts). No native aggregation.

**Summary**: Concurrent subagent execution is **not supported** in the VS Code + Copilot setup. You must run stages sequentially or manually manage multiple chat sessions.

---

## 3. How Can I Keep My Context Clean/Clear?

### Cursor

| Technique | How |
|-----------|-----|
| **Subagent isolation** | Each subagent starts with a clean context. Only receives: parent instructions + explicit file references. |
| **Intent gates** | Pipeline rule says "only run when user asks for research/deck/PPTX." Reduces irrelevant activation. |
| **File-based handoff** | Artifacts on disk are the contract. Subagents read/write files; parent doesn't need to hold full history. |
| **Command scope** | Each command defines a bounded workflow. Limits what gets pulled into context. |

### VS Code + GitHub Copilot

| Technique | How |
|-----------|-----|
| **One prompt per stage** | Use a single, focused prompt per stage. Don't mix roles in one chat. |
| **Start new chat per stage** | After each stage, start a **new chat** and paste the next prompt + reference to the artifact. Avoids context pollution. |
| **File-based handoff** | Same as Cursor: artifacts are source of truth. Always say "Read `artifacts/research/research.md`" in the prompt. Don't paste huge blocks of text. |
| **Orchestrator script** | `scripts/orchestrate.ps1` enforces "complete stage N before stage N+1." Reduces ad-hoc mixing. |
| **Copilot instructions** | `.github/copilot-instructions.md` sets repo-wide behavior. Keep it focused; avoid long, sprawling instructions. |
| **Issue as input** | Use issue template as the single input spec. Paste issue link/body into chat. Don't re-explain; reference the issue. |

**Summary**: To keep context clean in VS Code + Copilot:
1. One role per chat; start a new chat per stage.
2. Reference files, don't paste them.
3. Use the orchestrator to enforce stage boundaries.
4. Keep `.github/copilot-instructions.md` concise.

---

## File Inventory: Cursor vs VS Code + GitHub Copilot

| Path | Cursor | VS Code + Copilot | Notes |
|------|--------|-------------------|-------|
| **`.cursor/`** | | | |
| `.cursor/rules/pipeline.mdc` | ✅ Primary | ❌ | Replaced by `docs/orchestration/pipeline.md` + `.github/copilot-instructions.md` |
| `.cursor/commands/mslearn-research.md` | ✅ Primary | ❌ | Replaced by issue template + `scripts/orchestrate.ps1` |
| `.cursor/commands/research-to-pptx.md` | ✅ Primary | ❌ | Replaced by orchestration script + optional deck stage |
| `.cursor/agents/researcher-mslearn.md` | ✅ Primary | ❌ | Replaced by `docs/prompts/researcher-mslearn.md` |
| `.cursor/agents/validator-gotchas.md` | ✅ Primary | ❌ | Replaced by `docs/prompts/validator-gotchas.md` |
| `.cursor/agents/security-reviewer.md` | ✅ Primary | ❌ | Replaced by `docs/prompts/security-reviewer.md` |
| `.cursor/agents/deck-writer.md` | ✅ Primary | ❌ | Replaced by `docs/prompts/deck-writer.md` |
| `.cursor/agents/pptx-builder.md` | ✅ Primary | ❌ | No direct equivalent (PPTX MCP not in VS Code) |
| `.cursor/skills/mslearn-research/SKILL.md` | ✅ Primary | ❌ | Logic folded into `docs/prompts/researcher-mslearn.md` |
| `.cursor/skills/validate-and-gotchas/SKILL.md` | ✅ Primary | ❌ | Logic folded into `docs/prompts/validator-gotchas.md` |
| `.cursor/skills/security-assessment/SKILL.md` | ✅ Primary | ❌ | Logic folded into `docs/prompts/security-reviewer.md` |
| `.cursor/skills/deck-authoring/SKILL.md` | ✅ Primary | ❌ | Logic folded into `docs/prompts/deck-writer.md` |
| `.cursor/skills/pptx-generation/SKILL.md` | ✅ Primary | ❌ | No equivalent (MCP-based) |
| `.cursor/mcp.template.json` | ✅ Primary | ❌ | MCP is Cursor-specific; VS Code has different extension model |
| **`.vscode/`** | | | |
| `.vscode/settings.json` | ❌ | ✅ Primary | Workspace settings for VS Code |
| `.vscode/tasks.json` | ❌ | ✅ Primary | Task bindings for orchestration and validation |
| `.vscode/extensions.json` | ❌ | ✅ Primary | Recommended extensions (Copilot, markdown, etc.) |
| **`.github/`** | | | |
| `.github/copilot-instructions.md` | ❌ | ✅ Primary | Repo-wide AI instructions for Copilot |
| `.github/PULL_REQUEST_TEMPLATE.md` | ❌ | ✅ Primary | PR checklist and quality gates |
| `.github/ISSUE_TEMPLATE/research-request.yml` | ❌ | ✅ Primary | Structured research request form |
| `.github/ISSUE_TEMPLATE/security-assessment.yml` | ❌ | ✅ Primary | Structured security request form |
| `.github/CODEOWNERS` | ❌ | ✅ Primary | Review ownership and branch protection |
| `.github/scripts/validate_research.py` | ❌ | ✅ Primary | Validation script (used by both CI and local tasks) |
| `.github/workflows/research-orchestration-gates.yml` | ❌ | ✅ Primary | Stage-dependent CI gates |
| **`docs/`** | | | |
| `docs/orchestration/pipeline.md` | ❌ | ✅ Primary | Orchestration contract (Cursor equivalent: rules + commands) |
| `docs/prompts/researcher-mslearn.md` | ❌ | ✅ Primary | Specialist prompt for research stage |
| `docs/prompts/validator-gotchas.md` | ❌ | ✅ Primary | Specialist prompt for validation stage |
| `docs/prompts/security-reviewer.md` | ❌ | ✅ Primary | Specialist prompt for security stage |
| `docs/prompts/deck-writer.md` | ❌ | ✅ Primary | Specialist prompt for deck stage |
| `docs/architecture/Instructions.txt` | ⚪ Shared | ⚪ Shared | Original setup guide; reference for both |
| `docs/architecture/CursorResearchPresentationPlaybook.md` | ⚪ Shared | ⚪ Shared | Playbook; applies to both setups |
| `docs/architecture/Cursor-vs-VSCode-Comparison-and-Inventory.md` | ⚪ Shared | ⚪ Shared | This document |
| **`scripts/`** | | | |
| `scripts/orchestrate.ps1` | ❌ | ✅ Primary | Guided stage-by-stage orchestration |
| **`artifacts/`** | | | |
| `artifacts/research/research.md` | ✅ Primary | ✅ Primary | Output artifact; used by both |
| `artifacts/security/securityassessment.md` | ✅ Primary | ✅ Primary | Output artifact; used by both |
| `artifacts/deck/presentation.md` | ✅ Primary | ✅ Primary | Output artifact; used by both |
| `artifacts/research/research - Copy*.md` | ⚪ Temp | ⚪ Temp | Likely duplicates; can be removed |
| `artifacts/security/securityassessment - Copy*.md` | ⚪ Temp | ⚪ Temp | Likely duplicates; can be removed |
| `artifacts/deck/presentation - Copy.md` | ⚪ Temp | ⚪ Temp | Likely duplicate; can be removed |

---

## Legend

- **✅ Primary**: Core to that setup; required for workflow
- **❌**: Not used by that setup
- **⚪ Shared**: Used or relevant to both
- **⚪ Temp**: Temporary/duplicate; safe to delete

---

## Quick Reference: What to Use Where

| If you use… | Keep these |
|-------------|------------|
| **Cursor only** | `.cursor/**`, `artifacts/**`, `docs/architecture/Instructions.txt` |
| **VS Code + Copilot only** | `.vscode/**`, `.github/**`, `docs/orchestration/**`, `docs/prompts/**`, `scripts/**`, `artifacts/**` |
| **Both** | `artifacts/**`, `docs/architecture/**`, shared playbook |
