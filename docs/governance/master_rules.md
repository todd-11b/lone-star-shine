# TourOps — Governance & Project Rules

**Version:** v1.1
**Last Updated:** 2026-02-26
**Owner:** Todd Abrams (System Owner)
**Change Authority:** Todd Abrams only
**Consolidated from:** TO_Governance_Master_Rules.md, TO_Governance_Change_Control_Policy.md, TO_Build_Contract.md

---

## System Overview

**System:** TourOps Voice AI — AI-powered booking inquiry system for tour and activity operators
**Primary KPI:** Voice AI Conversation Quality Score ≥ 4.0 average across all operators

Every build decision must tie back to this KPI. If it doesn't, it doesn't belong in the build.

**Scope:** Voice AI prompt architecture, Conversation AI modules and routing, Canonical Schema, GHL workflows, Snapshot architecture, Prompt Compiler, QA Grader workflows, regression testing, operator onboarding pipeline.

**Out of Scope:** Day-to-day QA reviews → TO_Run. Strategic priorities → TO_Lead. Operator business decisions (tours, pricing, policies) → operator's responsibility.

---

## Operating Principles

1. **Claude proposes. Humans confirm. Always.** No build, deploy, or schema change executes without explicit human approval.
2. **The Schema is the contract.** `system/canonical_schema.md` is the sole data contract authority. No field exists outside it. No enum value deviates from it.
3. **One doc per concept. No duplicates. Ever.** If a doc exists, update it. Do not create a parallel version.
4. **Test before deploy. Always.** 19/19 regression tests required. No exceptions. No "we'll monitor it."
5. **Operators never touch system fields.** Operators complete tasks. Automation handles all field writes.
6. **Build once. Document forever.** Every build change logged in `product/build_log.md` before it goes live.
7. **Every priority replaces one.** No net WIP increase across BUILD, RUN, or LEAD.
8. **No feature may be added if it increases system complexity without reducing an existing bottleneck.** Adding a workflow requires retiring or consolidating an existing workflow where possible.

---

## Non-Negotiables

These rules are absolute. They cannot be overridden by any operator, project, or individual.

1. **`tourops_work_state` is the authoritative AI suppression control.** Tags are visibility-only. Any build that uses tags for AI suppression is non-compliant.
2. **Transfer Bot is banned.** All intent handling occurs within a single bot via Router + Module architecture.
3. **Bot Goals action toggles (Stop Bot, Human Handover) are banned.** Escalation is handled via field writes only.
4. **Enum values are case-sensitive and closed-set.** No value may be used that is not explicitly listed in the current Schema Contract. Enum mismatch blocks deployment.
5. **Disposition writes are required at the end of every module path.** No conversation ends without stamped fields.
6. **Hardcoded operator names/URLs in flow logic are banned.** All operator-specific values live in Custom Values only.
7. **19/19 regression tests required before any production deployment.** Non-negotiable.
8. **Agent persona (name, tone, intro) is defined in the operator overlay only.** Never hardcoded in Platform files.

---

## Standing Architecture Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| `tourops_work_state` is authoritative AI suppression control | Tags proved unreliable; field-level control is deterministic | 2026-02-14 |
| Schema enums are case-sensitive and closed-set | Prevents routing failures from casing drift | 2026-02-14 |
| Disposition writes happen at end of every module path | Ensures no contact leaves a conversation without stamped state | 2026-02-14 |
| Narrative memory fields (summaries) are context-only, not authoritative | Prevents summary drift from overriding accurate canonical state | 2026-02-17 |
| Regression suite must be 19/19 before any production deployment | Zero tolerance for known regressions | 2026-02-14 |
| Agent persona is operator-defined via OP_Profile.md only | Keeps Platform name-agnostic; enables multi-operator persona differentiation without prompt forks | 2026-02-26 |
| n8n flow is a reusable template — operator name passed as variable | Per-operator data infrastructure setup under 20 minutes; no new n8n build per operator | 2026-02-28 |

---

## Change Control

### Approval Requirements

| Change Type | Approval Required | Process | Risk |
|------------|------------------|---------|------|
| Schema field add/modify | Todd only | Design → approve → BUILD implements → 19/19 → deploy | High |
| Schema enum change | Todd only | Design → approve → audit usages → update tests → deploy | High |
| Prompt change (any operator) | Todd sign-off | BUILD builds → 19/19 → Todd approves → deploy | Med |
| Workflow change (GHL) | Todd review | BUILD builds → test → Todd reviews → deploy | Med |
| New operator deployment | Todd sign-off | Intake → KB build → snapshot → compiler → 19/19 → Todd sign-off → go live | Med |
| Snapshot update | Todd approval | BUILD designs → tests → Todd approves → exports | Med |
| KB content change | Mike (operator-level) | Operator submits → Mike reviews → update → spot-check | Low |
| Tier 3 doc update | Mike / Tim | Update → flag if changes SOP behavior | Low |
| Tier 2 doc update | Todd or delegated | Update → re-upload to project knowledge | Med |
| Tier 0/1 doc update | Todd only | Update → re-upload → notify team | High |
| GHL agency-level change | Todd only | Flag in Governance → approve → deploy | High |

### Schema Change Protocol (Highest Risk)

Schema changes are breaking changes by definition. Follow exactly:

1. Todd drafts proposed field/enum change with rationale and KPI justification
2. Impact analysis: which workflows, prompts, and tests are affected? Document all.
3. Update regression tests to reflect new schema BEFORE deploying
4. Write and test rollback plan in sandbox (required, no exceptions)
5. Create `product/build_log.md` entry before any production change
6. Deploy: fields first → workflows second → prompts last
7. Run 19/19 regression suite post-deploy
8. Update `system/canonical_schema.md` and re-upload to project knowledge
9. Todd sign-off: "Schema Contract [N] active in production — [date]"

**Contract increment rules:**
- Adding new fields → increment Contract number (e.g. Contract 3 → Contract 4)
- Modifying existing enum values → increment Contract number
- Editorial/clarification changes → increment Doc revision (r06 → r07)
- Removing deprecated fields → increment Contract number + 30-day notice to operators

### Prompt Change Protocol

1. BUILD drafts prompt change with before/after text
2. Run regression suite (19/19 required) on sandbox with new prompt
3. Mike notifies Todd: "Prompt [version] ready for review — 19/19 pass"
4. Todd reviews and approves in writing
5. Deploy per `operators/deployment_playbook.md` (Playbook A)
6. Mike monitors first 5 live conversations, reports to Todd at 24h and 48h

### Anti-Pattern Ban List (Immutable)

The following cannot be introduced via any change, regardless of rationale:
- Transfer Bot usage in any Conv AI flow
- Tags as AI suppression mechanism
- Bot Goals action toggles (Stop Bot, Human Handover) for escalation control
- Hardcoded operator names/URLs in flow logic
- Hardcoded agent persona (name, tone, intro) in any Platform-layer file
- Any field outside `system/canonical_schema.md` without schema change approval

---

## Document Tiers

| Tier | Type | Example | Who Can Change |
|------|------|---------|----------------|
| Tier 0 | Constitution | This file | Todd only |
| Tier 1 | Standards/Contracts | `system/canonical_schema.md` | Todd only |
| Tier 2 | Production Behavior | `prompts/vai_production_prompt.md` | Todd (or delegated) |
| Tier 3 | Operating Docs | SOPs, checklists, logs | Mike / Tim |

**Tier 0/1:** No version in filename. Version in header only. Overwrite. Never duplicate.
**Tier 2/3:** Version in filename required where rollback matters.

---

## Decision Authority

| Decision Type | Authority | Escalates To |
|--------------|-----------|--------------|
| Tier 0/1 doc changes | Todd only | N/A |
| Tier 2 doc changes | Todd or delegated | Todd if disputed |
| Tier 3 doc changes | Mike / Tim | Todd if disputed |
| Schema changes (any) | Todd only | N/A |
| New operator onboarding | Todd approval required | N/A |
| Prompt deployment | Todd sign-off required | N/A |
| GHL agency-level changes | Todd only | N/A |
| Rollback execution | Mike (notifies Todd immediately) | Todd |

---

## AI Usage Rules

- Claude recommends. Todd or designated owner confirms all execution.
- Claude never changes production without explicit human approval.
- Claude flags cross-project impacts before acting (e.g., schema change affects BUILD + RUN + LEAD).
- Claude requests missing docs rather than inferring from gaps.
- Claude AI Command Center is the QA and analysis layer — not the deployment layer.

---

## Operator Overlay — Persona Configuration

Each operator defines a custom agent persona via their operator profile. The Platform layer is name-agnostic. All persona values live in the operator overlay only.

```
Agent_Name: [e.g. "Hope", "Jade", "Alex"]
Agent_Tone: [e.g. "Friendly and professional"]
Agent_Intro: [e.g. "Hi, I'm [Agent_Name] with [Company]!"]
```

No agent name, tone, or intro may be hardcoded in any Platform-layer file. All persona references in prompts must use the `Agent_Name` variable from the operator overlay.

---

## WIP Limits

| Layer | WIP Limit | Rule |
|-------|-----------|------|
| TO_Build P1 items | Max 3 active | No new P1 without closing one |
| TO_Run improvement initiatives | Max 3 active | No 4th without pausing one |
| TO_Lead strategic initiatives | Max 3 active | Adding 4th requires killing or pausing one |

---

## Change Freeze Periods

- **Peak booking weekends** (operator-defined, typically Fri–Sun): No prompt or schema changes. Emergency rollbacks only.
- **New operator go-live week:** No changes to shared platform components (schema, snapshot) during a new operator's first 7 days live.

---

## Work Continuity Rule

- Every session starts by reading `state/active_state.md`
- Unfinished work logged before ending any session
- `state/active_state.md` older than 14 days = governance audit flag
- Open loops not closed in 14 days → Todd decides immediately

---

## Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| GHL (GoHighLevel) | Primary platform | Voice AI, Conversation AI, workflows, contacts, SMS |
| n8n | Automation layer | Reusable operator data flow template |
| Google Sheets | Data ledger | QA tracking |
| Claude AI Command Center | QA and analysis | Review, test generation, prompt analysis |
| Anthropic API | Grader AI calls | Via webhook |
| `system/canonical_schema.md` | System data contract | Must match production at all times |
| `system/conversation_design.md` | Behavioral standard | Consulted before building any new AI module |
| `system/ghl_platform_notes.md` | Platform constraint ledger | Consulted before building any new automation |
