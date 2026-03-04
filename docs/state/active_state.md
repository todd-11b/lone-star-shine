# TourOps — Active State

**Rule:** Read this at the start of every session. Update it before you close. One file, one source of truth.
**Last Updated:** 2026-02-28
**Updated By:** Todd Abrams
**Consolidated from:** TourOps_Active_State.md, TO_Governance_Conflicts_Register.md, TO_Run_Issues_Log.md

---

## WHERE WE ARE

**Stage:** Testing — Grader v1.0 deployed 2026-02-22. Validation window in progress.
**Primary Blocker:** Tim's grader validation report is overdue. Nothing downstream can be trusted until it's in.
**Next Human Decision Required:** Todd go/no-go after Tim delivers report.

---

## OPEN LOOPS

| # | What | Who | Due | Status |
|---|------|-----|-----|--------|
| OL-2 | Grader validation — 10 conversations, 3 manually scored, delta ≤ 0.5 | Tim | 2026-02-28 | 🔴 Overdue |
| OL-4 | Version Governance Matrix updated for Schema Contract 3 | Mike | 2026-03-07 | 🟡 Open |
| OL-7 | Airtable + n8n build | Freelancer (Upwork) | 2026-03-14 | 🟡 Pending hire |
| OL-8 | Claude project instructions updated (new system prompt) | Todd | 2026-03-01 | 🟡 Pending |
| OL-9 | New project knowledge files added | Todd | 2026-03-01 | 🟡 Pending |
| OL-10 | Tim added to Claude project | Todd | 2026-03-01 | 🟡 Confirm before sending README |

---

## ACTIVE CONFLICTS

| Conflict | Files | Blocking? | Owner | Due |
|----------|-------|-----------|-------|-----|
| Version Governance Matrix references Contract 2; production is on Contract 3 | Version_Governance_Matrix vs. canonical_schema.md r06 | No | Mike | 2026-03-07 |

**Resolved Conflicts:**
- 2026-02-28: BB overlay files referenced Schema Contract 2 in headers — resolved when Todd confirmed Contract 3 fields already live in BB production. Documentation-only gap.
- 2026-02-28: Duplicate conflicts registers (two versions) — resolved by consolidating into single file.

**Conflict Rules:**
- 🔴 Active/Blocking: Two docs give contradictory instructions affecting production → work stops, Todd resolves immediately
- 🟡 Open/Non-blocking: Docs out of sync but no production harm → resolve within 7 days
- Flag when: two files contradict on same topic, a production change makes a doc inaccurate, schema version changes but companion docs still reference old version

---

## BUILD STATE

**Focus:** Grader v1.0 validation (VAI + CAI)
**Done:** Schema Contract 3 live in BB production. BB overlay files corrected.
**Blocked on:** Tim's validation report (OL-2)
**Next build action after unblock:** Airtable + n8n infrastructure (freelancer)

---

## GOVERNANCE STATE

Stable. Two items in flight — matrix update (Mike, non-blocking) and infrastructure build (freelancer). No Tier 0/1 conflicts active.

---

## OPERATORS

**Barley Bus**
- Status: Live in production
- Schema: Contract 3 (r06) — confirmed live 2026-02-28
- Grader: Deployed 2026-02-22 — validation in progress
- QA Scores: Provisional until OL-2 closes
- Open Items: None operator-specific beyond grader validation

*(Add new `## Operator: [Name]` sections here as new operators go live)*

---

## DECISIONS LOG

| Decision | Authority | Date |
|----------|-----------|------|
| Airtable confirmed as data layer | Todd | 2026-02-28 |
| n8n built as reusable operator template — operator name as variable | Todd | 2026-02-28 |
| Mike focused on GHL-specific work — data infrastructure hired out | Todd | 2026-02-28 |
| Freelancer hired via Upwork for Airtable + n8n QA data flow | Todd | 2026-02-28 |
| BB confirmed as Operator #1 | Todd | 2026-02-28 |
| BB Schema Contract 3 migration confirmed complete in production | Todd | 2026-02-28 |

---

## ISSUES LOG

*Recurring issues only — 2+ occurrences to enter. Single incidents stay in the weekly review entry.*
*An issue cannot be marked Resolved without: (1) documented verified root cause AND (2) confirmed no recurrence for 14 consecutive days.*

### Active Issues

| Date | Issue ID | Description | Category | Severity | Frequency | Root Cause | Fix Attempted | Owner | Status |
|------|----------|-------------|----------|----------|-----------|------------|--------------|-------|--------|
| — | — | No active issues logged | — | — | — | — | — | — | — |

### Resolved Issues

| Date | Issue ID | Description | Category | Fix | Resolved | Notes |
|------|----------|-------------|----------|-----|----------|-------|
| — | — | No resolved issues logged yet | — | — | — | — |

### Issue ID Format
`TOUROPS-[OPERATOR]-[NUMBER]`
Examples: `TOUROPS-BB-001`, `TOUROPS-GLOBAL-001`

### Issue Categories

| Category | Description |
|----------|-------------|
| Context Awareness | Asked for info caller already provided |
| Data Collection | Missed required info before sending link |
| Boundary Enforcement | Failed to handle out-of-scope request correctly |
| KB Usage | Didn't query KB / gave wrong factual answer |
| Conversation Flow | Too long, rambling, awkward pacing |
| Escalation Logic | Didn't escalate when trigger condition was met |
| Field Stamping | Disposition fields missing or incorrect after call |
| Grader | Grader failed to fire or scored inaccurately |
| Persona | Agent name, tone, or intro incorrect or hardcoded — OP_Profile.md mismatch |
| Technical | System error, failed SMS, workflow malfunction |

### Recurring Issue Policy

| Occurrence | Required Action |
|------------|----------------|
| 2nd occurrence (same issue type) | Log in this file. Flag in next weekly review. |
| 3rd occurrence in 30 days | Architecture review. Escalate to Todd + BUILD. |
| Critical issue (any count) | Escalate to Todd same day. |

### Monthly Metrics Targets

| Metric | Target |
|--------|--------|
| Open critical issues | 0 |
| Avg time to resolution (critical) | < 48 hours |
| Avg time to resolution (important) | < 1 week |
| Repeat failure rate | 0 |
| Issues per deployment | Trending down |
| Persona issues (OP_Profile.md mismatches) | 0 |

---

## HOW TO USE THIS FILE

**Session start:** Read this file. Note the current stage, open loops, and active conflicts before doing anything.
**Session end:** Update open loops (close what's done), add new decisions, note any new conflicts.
**New operator goes live:** Add a new `## Operator: [Name]` section.
**Closing a loop:** Remove from Open Loops, note resolution in Decisions Log.

**This file does NOT replace:** Schema contracts, platform rules, prompt files, regression suites. Those stay as standalone files. This file is only for what's actively moving.
