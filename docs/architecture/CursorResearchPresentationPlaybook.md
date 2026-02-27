# Cursor Research and Presentation Playbook

## Purpose
This playbook operationalizes a repeatable workflow for:
- Deep research
- Validation and practical gotchas
- Security assessment
- Deck authoring
- Optional PPTX generation

## What Was Improved
- Clear intent gates so deck/PPTX steps run only when requested
- Stronger evidence quality (sources, dates, confidence)
- Comprehensive content requirements (code snippets, Mermaid diagrams, image references)
- Artifact templates for consistent output shape and depth
- Specialist skills and agents for reusable execution
- Single command entry point for orchestration

## Implemented Components
- Rule: `.cursor/rules/pipeline.mdc`
- Command: `.cursor/commands/research-to-pptx.md`
- Command (research-only): `.cursor/commands/mslearn-research.md`
- Skills:
  - `.cursor/skills/mslearn-research/SKILL.md`
  - `.cursor/skills/validate-and-gotchas/SKILL.md`
  - `.cursor/skills/security-assessment/SKILL.md`
  - `.cursor/skills/deck-authoring/SKILL.md`
  - `.cursor/skills/pptx-generation/SKILL.md`
- Agents:
  - `.cursor/agents/researcher-mslearn.md`
  - `.cursor/agents/validator-gotchas.md`
  - `.cursor/agents/security-reviewer.md`
  - `.cursor/agents/deck-writer.md`
  - `.cursor/agents/pptx-builder.md`
- Artifact templates:
  - `artifacts/research/research.md`
  - `artifacts/security/securityassessment.md`
  - `artifacts/deck/presentation.md`
- MCP template: `.cursor/mcp.template.json`

## One-Time Setup
1. Copy `.cursor/mcp.template.json` to `.cursor/mcp.json`.
2. Adjust `command` and `args` for your actual PowerPoint MCP server.
3. In Cursor chat, enable the server if needed:
   - `/mcp enable pptxLocal`
4. Verify available tools:
   - `/mcp list`

## Daily Usage
1. In chat, run:
   - `/research-to-pptx <your topic>`
   - or `/mslearn-research <your topic>` for research-only flow
2. Specify output depth:
   - research only (or use `/mslearn-research`)
   - research + deck
   - research + deck + PPTX
3. Specify mode:
   - `quick` for concise output
   - `deep` for comprehensive output (default)
4. Review generated artifacts in `artifacts/**`.

## Quality Checklist
- Research includes assumptions, gotchas, references, and confidence
- Security assessment contains risks, mitigations, and residual risks
- Deck has clear narrative and speaker notes
- Visuals are included or explicitly called out when missing
