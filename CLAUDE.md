# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A collection of **GitHub Copilot plugins** for BBVA APX projects. These are not applications—they are reusable AI assistant assets (agents, skills, commands, hooks, instructions) installed into consuming repos. The primary plugin is `plugins/apx/`.

## Validation Commands

```bash
# Validate a skill's structure
python3 plugins/apx/skills/apx-html-docs-generator/scripts/validate-skill.py plugins/apx/skills/apx-html-docs-generator

# Run the HTML docs generator (when testing inside a consuming repo)
python3 .agents/skills/apx-html-docs-generator/scripts/generate-html-docs.py --verbose

# Generate unit test report (from a consuming APX repo)
python3 .agents/skills/apx-unit-test-v2/scripts/generate_test_report.py \
  --project "PROJECT" --total 10 --passed 10 --failed 0 --errors 0 \
  --cov-classes 85 --cov-methods 80 --cov-lines 82 --output testresults.md
```

## Architecture

### Plugin Registry

The authoritative plugin catalog is `.github/plugin/marketplace.json`. It references `plugins/apx` as a plugin entry. The `.claude-plugin/marketplace.json` at root is a legacy/local copy.

### Component Types in `plugins/apx/`

**Agents** (`agents/*.agent.md`) — AI personas with YAML frontmatter (`name`, `description`, `tools`) followed by behavior instructions. Each agent has a clearly scoped responsibility:
- `agent-orchestrator-parallel.agent.md` — Orchestrates full APX development lifecycle: Plan → Docs → Code → (SonarQube + Tests in **parallel**) → Finalize. Has mandatory pause points before commit.
- `apx_code_generator-local.agent.md` — Generates Java/Spring Boot code following APX framework patterns. Reads style guide and security guide from the BBVA internal GitHub before coding.
- `apx_doc_generator.agent.md` — Generates functional/architecture documentation. **Requires** consulting BBVA Copilot Spaces (`BBVA-SPACE-APX-FC` and `POC-SECURITY BY DESIGN`) before writing any documentation.
- `quality-sonar.agent.md` — SonarQube analysis and reporting only. Never modifies code.

**Skills** (`skills/*/`) — Self-contained knowledge modules that consumers install. Each has a `SKILL.md` entry point, `references/` (static Markdown knowledge), `scripts/` (Python utilities), and optionally `agents/openai.yaml`.
- `apx-unit-test-v2` — JUnit 5 + Mockito + JaCoCo testing (min 80% coverage). Pattern: AAA + `@DisplayName` Given-When-Then.
- `apx-html-docs-generator` — Converts `docs/` Markdown to HTML with BBVA corporate styling. Edit `.md` sources, never the generated `html/`.

**Commands** (`commands/*.md`) — Slash commands with YAML frontmatter (`description`, `argument-hint`). Referenced via `/apx:<command-name>`.

**Instructions** (`instructions/*.instructions.md`) — Applied to files in consuming repos. Define naming conventions, templates, and quality gates.

**Hooks** (`hooks/copilot-hooks.json`) — Wires shell scripts to Copilot lifecycle events (`PreCompact`, `SubagentStart`, `SubagentStop`).

### Adding a New Agent

1. Create `plugins/apx/agents/<name>.agent.md`
2. Add YAML frontmatter with `name`, `description`, and `tools` list
3. Write behavior instructions as Markdown body
4. Agents that only analyze (never modify code) should include explicit stopping rules like the `quality-sonar` agent does

### Adding a New Skill

1. Create `plugins/apx/skills/<skill-name>/SKILL.md` — this is the entry point agents read
2. Add `references/` for static knowledge, `scripts/` for Python utilities
3. If the skill has an OpenAI-compatible agent definition, add `agents/openai.yaml`
4. Validate: `python3 scripts/validate-skill.py plugins/apx/skills/<skill-name>`

### Plan File Conventions (used by orchestrator)

Plans are written to `plans/<task-name>-plan.md` in the consuming repo. They include a Mermaid `flowchart LR` diagram tracking phase status (CSS classes: `pending`, `inProgress`, `completed`, `failed`). The orchestrator **must** update the plan file after each phase—updating both the Mermaid class assignments and the `Estado:` field in the phase detail section.

### Commit Message Style

```
fix/feat/chore/test/refactor: Short description (max 50 chars)

- Concise bullet 1
- Concise bullet 2
```

No references to plan files or phase numbers in commit messages.
