# TourOps Documentation

**Last Updated:** 2026-03-03
**System Owner:** Todd Abrams
**Source of Truth:** This directory. When in doubt, these files win.

21 files. Every file has a job. Nothing is duplicated.

---

## Document Map

### Governance
| File | What it is |
|------|-----------|
| [governance/master_rules.md](governance/master_rules.md) | The constitution. Operating principles, non-negotiables, change control, document tiers, decision authority. **Read this first.** |

### System — Architecture & Technical Specs
| File | What it is |
|------|-----------|
| [system/canonical_schema.md](system/canonical_schema.md) | **Schema Contract 3.** All canonical field names and enum values. The authoritative data contract. Nothing overrides this. |
| [system/technical_spec.md](system/technical_spec.md) | Architecture: dual AI channels, persona system, workflow definitions, platform integrations. |
| [system/conversation_design.md](system/conversation_design.md) | Behavioral spec for all AI conversation systems. Intent buckets, script plays, 15 behavioral standards. |
| [system/prompt_compiler.md](system/prompt_compiler.md) | Prompt Compiler v1.1. Generates operator-specific prompts from intake data in ~5 minutes. |
| [system/n8n_spec.md](system/n8n_spec.md) | GHL → n8n → Airtable data flow. Reusable template architecture + full flow logic. |
| [system/ghl_platform_notes.md](system/ghl_platform_notes.md) | Running log of GHL UI changes, navigation paths, and platform constraints. |

### Product — Build, Roadmap & Tracking
| File | What it is |
|------|-----------|
| [product/roadmap.md](product/roadmap.md) | 90-day roadmap Q1–Q3 2026. Major releases, dependencies, capacity limits. |
| [product/backlog.md](product/backlog.md) | Build backlog (P1–P3) + product gap tracker (Tier 1–3 feature readiness vs. current state). |
| [product/build_log.md](product/build_log.md) | Append-only deployment history. Every change, risk level, rollback status. |

### Operations — Running the System Day-to-Day
| File | What it is |
|------|-----------|
| [operations/operations_manual.md](operations/operations_manual.md) | Core SOPs, task schedule, weekly review template, performance dashboard, new team member training. |
| [operations/escalation_playbook.md](operations/escalation_playbook.md) | Escalation handling by priority (P0 safety, P0b legal, DayOf, Human Request, Standard). SLAs and scripts. |
| [operations/quality.md](operations/quality.md) | 6-category 1–5 scoring rubric + quality thresholds, red flags, and prompt trigger conditions. |

### QA & Testing
| File | What it is |
|------|-----------|
| [qa-testing/regression_test_suite.md](qa-testing/regression_test_suite.md) | Pre-deployment checklist + all 19 regression tests + failure handling. 19/19 required before any deploy. |

### Operators
| File | What it is |
|------|-----------|
| [operators/onboarding_plan.md](operators/onboarding_plan.md) | 8-phase operator onboarding pipeline, Day 0 through 30-day impact report. |
| [operators/deployment_playbook.md](operators/deployment_playbook.md) | Deployment playbooks A (prompt), B (new operator), C (schema change). Includes rollback procedures. |
| [operators/barley_bus.md](operators/barley_bus.md) | Barley Bus complete operator file. Profile, AI system config, current live state. Single source of truth for BB. |

### Prompts
| File | What it is |
|------|-----------|
| [prompts/vai_production_prompt.md](prompts/vai_production_prompt.md) | Hope V5.0 Voice AI production prompt (legacy, pre-Schema v2). Migration to Compiler v1.1 planned Q2 2026. |

### State
| File | What it is |
|------|-----------|
| [state/active_state.md](state/active_state.md) | Current system snapshot: open loops, active conflicts, build state, decisions log, issues log. Read at every session start. |

### Reference
| File | What it is |
|------|-----------|
| [reference/ai_command_center.md](reference/ai_command_center.md) | User guide for Claude AI Command Center (Tim/Mike). Use cases, ground rules, quick reference commands. |

---

## Authority Hierarchy

When files conflict, higher tier wins.

```
Tier 0 — Constitution
  governance/master_rules.md

Tier 1 — System Contracts
  system/canonical_schema.md

Tier 2 — Production Behavior
  system/conversation_design.md
  system/technical_spec.md
  prompts/vai_production_prompt.md
  operators/barley_bus.md

Tier 3 — QA & Operations
  qa-testing/regression_test_suite.md
  operations/quality.md
  operations/operations_manual.md
  (all other ops and product files)
```

All changes require Todd Abrams approval per [governance/master_rules.md](governance/master_rules.md).

---

## Session Start Checklist

1. Read `state/active_state.md` — know what's open and blocked
2. Read the file(s) relevant to today's work
3. Update `state/active_state.md` before closing the session
