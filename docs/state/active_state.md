# TourOps_Active_State.md

**Replaces:** TO_Build_Current_State.md, TO_Gov_Current_State.md, BB_Current_State.md
**Rule:** Upload this at the start of every session. Update it before you close. One file, one source of truth.
**Last Updated:** 2026-03-03
**Updated By:** Todd Abrams [SYSTEM_OWNER]

---

## WHERE WE ARE (Read First)

**Stage:** V6.0 GHL build active in BB production. Steps 1–5 of 9 complete. After-call workflow (step 6) in progress. Schema Contract 4 live. Google Sheets integration mapped.
**Primary Blocker:** Complete V6.0 GHL build (steps 6–9). Then wire Grader → Google Sheets and run end-to-end test.
**Next Human Decision Required:** Confirm `vai_outcome` values align with Sheets summary formulas (OL-16). Then complete remaining build steps and test one full call through the pipeline.

---

## OPEN LOOPS (The Only List That Matters)

| # | What | Who | Due | Status |
|---|------|-----|-----|--------|
| OL-2 | Grader validation — 10 conversations, 3 manually scored, delta ≤ 0.5 | Tim | 2026-02-28 | 🔴 Overdue |
| OL-4 | Version Governance Matrix updated for Schema Contract 4 | Mike | 2026-03-07 | 🟡 Open |
| OL-7 | Airtable + n8n build | Freelancer (Upwork) | 2026-03-14 | 🟡 Pending hire |
| OL-8 | Claude project instructions updated (new system prompt) | Todd | 2026-03-01 | 🟡 Pending |
| OL-9 | New project knowledge files added | Todd | 2026-03-01 | 🟡 Pending |
| OL-10 | Tim added to Claude project | Todd | 2026-03-01 | 🟡 Confirm before sending README |
| OL-11 | Wire Grader → Google Sheets row action | Todd | 2026-03-07 | 🟡 Mapping complete — GHL wiring is Step 9 of V6.0 build |
| OL-12 | Grader prompt update to write `tourops_score_notes` | Mike | 2026-03-07 | 🟡 Field created — grader prompt update is Step 7 of V6.0 build |
| OL-13 | Test calendar booking flow end-to-end (one call) | Todd | 2026-03-07 | 🔄 In progress — calendar exists, V6.0 prompt active, build steps 6–9 remaining |
| OL-14 | Update VAI + CAI prompts with calendar offer logic | Mike | 2026-03-10 | 🔄 In progress — V6.0 prompt pasted (step 5 done), CAI modules pending (step 8) |
| OL-15 | Confirm `vai_outcome` values currently written by disposition workflow | Todd/Mike | 2026-03-05 | 🟢 Confirmed — disposition workflow uses `tourops_disposition_blob_text` branching. Values: LinkSent, CalendarBooked, Escalated, Answered, Abandoned, Voicemail, Spam + V6.0 pending: ConsultationBooked, TaskCreated |
| OL-16 | Update BB_Daily_Call_Log spreadsheet with actual `vai_outcome` enum values | Todd | After OL-15 | 🟡 Unblocked — update Sheets summary formulas with confirmed values above |
| OL-17 | Set `tourops_aov` and `tourops_conversion_rate` custom values in BB GHL account | Todd | 2026-03-07 | 🟡 Open — onboarding questions defined, values TBD for BB |
| OL-18 | Build Tour Ops Command Center dashboard in BB (3 signals + Proof of Work section) | Todd | 2026-03-07 | 🔄 In progress — widgets added, Proof of Work pending |
| OL-19 | Build nightly Proof of Work calculation workflow (writes `tourops_daily_est_revenue`) | Todd/Mike | 2026-03-14 | 🟡 Open — schema defined, workflow not yet built |

---

## ACTIVE CONFLICTS

| Conflict | Files | Blocking? | Owner | Due |
|----------|-------|-----------|-------|-----|
| Version Governance Matrix references Contract 2/3, production is on Contract 4 | Version_Governance_Matrix vs. canonical_schema.md r07 | No | Mike | 2026-03-07 |

---

## BUILD STATE

**Focus:** V6.0 GHL build in BB production (BB-first approach — intentional)
**Done:** Schema Contract 4 live. Calendar created. callback_scheduling_link set. ConsultationBooked SMS template. Book Appointment action. V6.0 prompt pasted.
**In Progress:** After-call workflow — adding ConsultationBooked and TaskCreated branches (step 6)
**Blocked on:** Steps 7–9 (Grader prompt, Conv AI modules, end-to-end test)

**V6.0 GHL Build — BB Production (9-Step Sequence):**

| Step | Item | Status |
|------|------|--------|
| 1 | Consultation calendar created (Tim's calendar, 8AM–5PM, 15-min slots) | ✅ Done |
| 2 | `callback_scheduling_link` custom value set in BB production | ✅ Done |
| 3 | `OPERATOR__BarleyBus__ConsultationBooked` SMS template configured | ✅ Done |
| 4 | Book Appointment action configured (3 days / 3 slots / 1hr buffer) | ✅ Done |
| 5 | V6.0 prompt + personality module pasted into Voice AI | ✅ Done |
| 6 | After-call Disposition workflow — add ConsultationBooked + TaskCreated branches | 🔄 In progress |
| 7 | Grader prompt update — add `tourops_score_notes` write + new outcome scoring | ⬜ Pending |
| 8 | Conv AI modules update — READY, DISC, RES_CHG, REF_CAN, CORP | ⬜ Pending |
| 9 | End-to-end test (5 scenarios: small booking, 10+ consultation, refund, reservation change, safety escalation) | ⬜ Pending |

**Next build action:** Complete step 6 (after-call workflow), then step 7 (grader prompt).

---

## GOVERNANCE STATE

**Schema Contract 4 approved and documented.** Changes:
- `CalendarBooked` added to `tourops_outcome` enum
- `tourops_score_notes` field added (grader reasoning)
- `callback_scheduling_link` custom value added (calendar booking link)
- Deflection Rate KPI added

Updated docs: canonical_schema.md (r07), barley_bus.md, conversation_design.md (r11)

**Schema Contract 5 (pending):** `ConsultationBooked` and `TaskCreated` outcome values are in active use in BB production disposition workflow. Formal change control after BB proof of concept.

---

## OPERATOR: BARLEY BUS (BB)

**Status:** Live in production
**Schema:** Contract 4 (r07) — CalendarBooked enum, tourops_score_notes, callback_scheduling_link created in GHL 2026-03-03
**Calendar:** ✅ Created in GHL (single combined callback/consultation calendar — Tim)
**V6.0 Build:** Steps 1–5 complete, step 6 in progress
**Grader:** Deployed 2026-02-22 — validation in progress. Score notes field ready, grader prompt needs update (step 7).
**Google Sheets:** BB_Daily_Call_Log created with Raw + Daily Summary tabs. Column mapping documented in barley_bus.md. Waiting on Grader workflow wiring (step 9, OL-11).
**QA Scores:** Provisional until OL-2 closes

---

## DECISIONS LOG

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
| V6.0 GHL build order: build in BB production first, test in BB, then replicate to sandbox (intentional non-standard order) | [SYSTEM_OWNER] | 2026-03-03 |
| V6.0 ConsultationBooked + TaskCreated outcome values added to disposition workflow — pending Schema Contract 5 formal change control | [SYSTEM_OWNER] | 2026-03-03 |
| GHL Sales Pipeline: 4 stages — New Lead, Quoted, Booked, Lost (sales-intent only — no vendor/support/FAQ contacts) | [SYSTEM_OWNER] | 2026-03-04 |
| Dashboard architecture: Tour Ops Command Center — 3 signals (Urgent Issues, Today's Callbacks, Leads This Week) + Proof of Work section | [SYSTEM_OWNER] | 2026-03-04 |
| AOV and conversion rate stored as per-operator custom values (`tourops_aov`, `tourops_conversion_rate`) — set at onboarding, default conversion rate 0.25 | [SYSTEM_OWNER] | 2026-03-04 |
| Proof of Work estimated revenue calculation: daily inquiries × `tourops_conversion_rate` × `tourops_aov` — written nightly to `tourops_daily_est_revenue` | [SYSTEM_OWNER] | 2026-03-04 |

---

## HOW TO USE THIS FILE

**Session start:** Upload this file. I read it. We work.
**Session end:** Tell me what changed. I update the artifact. You copy it, save it, replace the old one.
**Adding a new operator:** Add a new `## OPERATOR: [NAME]` section.
**Closing a loop:** Move it out of Open Loops, note resolution in Decisions Log.

---

## WHAT THIS FILE DOES NOT REPLACE

Schema contracts, platform rules, prompt files, regression suites — those stay as standalone files in project knowledge. They don't change often. This file is only for what's actively moving.
