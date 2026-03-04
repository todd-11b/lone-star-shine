# TourOps_Active_State.md

**Replaces:** TO_Build_Current_State.md, TO_Gov_Current_State.md, BB_Current_State.md
**Rule:** Upload this at the start of every session. Update it before you close. One file, one source of truth.
**Last Updated:** 2026-03-03
**Updated By:** Todd Abrams [SYSTEM_OWNER]

---

## WHERE WE ARE (Read First)

**Stage:** Schema Contract 4 deployed. Three-tier escalation model documented. Google Sheets integration mapped. Calendar created in GHL.
**Primary Blocker:** Wire Grader workflow → Google Sheets. Test calendar booking flow end-to-end.
**Next Human Decision Required:** Confirm `vai_outcome` values so spreadsheet summary tab can match. Then test one call through the full pipeline.

---

## OPEN LOOPS (The Only List That Matters)

| # | What | Who | Due | Status |
|---|------|-----|-----|--------|
| OL-2 | Grader validation — 10 conversations, 3 manually scored, delta ≤ 0.5 | Tim | 2026-02-28 | 🔴 Overdue |
| OL-4 | Version Governance Matrix updated for Schema Contract 4 | Mike | 2026-03-07 | 🟡 Open (was Contract 3, now needs Contract 4) |
| OL-7 | Airtable + n8n build | Freelancer (Upwork) | 2026-03-14 | 🟡 Pending hire |
| OL-8 | Claude project instructions updated (new system prompt) | Todd | 2026-03-01 | 🟡 Pending |
| OL-9 | New project knowledge files added | Todd | 2026-03-01 | 🟡 Pending |
| OL-10 | Tim added to Claude project | Todd | 2026-03-01 | 🟡 Confirm before sending README |
| OL-11 | Wire Grader → Google Sheets row action | Todd | 2026-03-07 | 🟡 New — mapping complete, needs GHL wiring |
| OL-12 | Grader prompt update to write `tourops_score_notes` | Mike | 2026-03-07 | 🟡 New — field created, grader needs prompt tweak |
| OL-13 | Test calendar booking flow end-to-end (one call) | Todd | 2026-03-07 | 🟡 New — calendar exists, needs prompt + workflow update |
| OL-14 | Update VAI + CAI prompts with calendar offer logic | Mike | 2026-03-10 | 🟡 New — conversation_design_standard r10 defines the pattern |
| OL-15 | Confirm `vai_outcome` values currently written by disposition workflow | Todd/Mike | 2026-03-05 | 🟡 New — needed to align spreadsheet summary formulas |
| OL-16 | Update BB_Daily_Call_Log spreadsheet with actual `vai_outcome` enum values | Todd | After OL-15 | 🟡 Blocked on OL-15 |

---

## ACTIVE CONFLICTS

| Conflict | Files | Blocking? | Owner | Due |
|----------|-------|-----------|-------|-----|
| Version Governance Matrix references Contract 2/3, production is on Contract 4 | Version_Governance_Matrix vs. Schema_v2_0 r07 | No | Mike | 2026-03-07 |

---

## BUILD STATE

**Focus:** Three-tier escalation model + Google Sheets daily call log
**Done:** Schema Contract 4 live (CalendarBooked enum + tourops_score_notes field + callback_scheduling_link custom value). Calendar created in GHL. Conversation Design Standard r10 written. BB_Profile updated.
**Blocked on:** Grader → Sheets wiring (OL-11), Grader prompt tweak for score_notes (OL-12), VAI/CAI prompt updates with calendar logic (OL-14)
**Next build action after unblock:** Test one call through full pipeline — call → grader → Sheets row → verify summary tab

---

## GOVERNANCE STATE

**Schema Contract 4 approved and documented.** Changes:
- `CalendarBooked` added to `tourops_outcome` enum
- `tourops_score_notes` field added (grader reasoning)
- `callback_scheduling_link` custom value added (calendar booking link)
- Deflection Rate KPI added

Updated docs: canonical_schema.md (r07), bb_ai_system.md, bb_profile.md, conversation_design_standard.md (r10)

---

## OPERATOR: BARLEY BUS (BB)

**Status:** Live in production
**Schema:** Contract 4 (r07) — CalendarBooked enum, tourops_score_notes, callback_scheduling_link created in GHL 2026-03-03
**Calendar:** Created in GHL (single combined callback/consultation calendar)
**Grader:** Deployed 2026-02-22 — validation in progress. Score notes field ready, grader prompt needs update.
**Google Sheets:** BB_Daily_Call_Log created with Raw + Daily Summary tabs. Column mapping documented in bb_ai_system.md. Waiting on Grader workflow wiring.
**QA Scores:** Provisional until OL-2 closes
**Open Items:** Grader → Sheets wiring, prompt updates for calendar offer logic, end-to-end test

---

## DECISIONS LOG (This Session)

| Decision | Authority | Date |
|----------|-----------|------|
| Three-tier escalation model approved (Tier 1: AI resolves, Tier 2: Calendar booking, Tier 3: Human escalation) | [SYSTEM_OWNER] | 2026-03-03 |
| Combined callback + consultation into single GHL calendar | [SYSTEM_OWNER] | 2026-03-03 |
| `CalendarBooked` added to `tourops_outcome` — Schema Contract 4 | [SYSTEM_OWNER] | 2026-03-03 |
| `tourops_score_notes` field created in GHL | [SYSTEM_OWNER] | 2026-03-03 |
| `callback_scheduling_link` custom value created in GHL | [SYSTEM_OWNER] | 2026-03-03 |
| Google Sheets row appended from Grader workflow (not Disposition) — Grader fires last, all fields populated | [SYSTEM_OWNER] | 2026-03-03 |
| BB_Daily_Call_Log column mapping finalized (11 columns: Date, Time, Contact Name, Phone, Intent Bucket, Outcome, Work State, Score, Score Notes, Next Action, Summary) | [SYSTEM_OWNER] | 2026-03-03 |
| Deflection Rate KPI added — (CalendarBooked) / (CalendarBooked + Escalated) | [SYSTEM_OWNER] | 2026-03-03 |
| "Scheduling calls" removed from BB out-of-scope — calendar booking is now an AI capability | [SYSTEM_OWNER] | 2026-03-03 |

---

## HOW TO USE THIS FILE

**Session start:** Upload this file. I read it. We work.
**Session end:** Tell me what changed. I update the artifact. You copy it, save it, replace the old one.
**Adding a new operator:** Add a new `## OPERATOR: [NAME]` section.
**Closing a loop:** Move it out of Open Loops, note resolution in Decisions Log.

---

## WHAT THIS FILE DOES NOT REPLACE

Schema contracts, platform rules, prompt files, regression suites — those stay as standalone files in project knowledge. They don't change often. This file is only for what's actively moving.
