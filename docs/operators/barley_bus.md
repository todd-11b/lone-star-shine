# Barley Bus — Operator Reference

**Operator:** Barley Bus
**System Owner:** Todd Abrams
**Last Updated:** 2026-03-03
**Consolidated from:** BB_Profile.md, BB_AI_System.md, BB_Current_State.md

---

## Part 1 — Operator Profile

### Overview

| Field | Value |
|-------|-------|
| Business Name | Barley Bus |
| Location | Kansas City, Missouri |
| Industry | Tour & Transportation |
| Main Line | 816-323-3889 |
| AI Agent Name | Hope |
| Agent Persona | Friendly, confident, concise. Warm but not overly casual. No emojis. No long intros. Keeps it moving. |

### Mission & Scope

**Hope's Primary Functions (in order):**
1. Classify caller intent within the first ~10 seconds
2. Answer using the Knowledge Base as the single source of truth
3. Send the correct CaptainBook booking link via SMS (SMS-first)
4. Offer calendar booking for non-emergency callbacks and consultations (Tier 2)
5. Escalate to human follow-up only for safety, legal, or active emergencies (Tier 3)

**In Scope:**
- New booking inquiries
- Tour information questions
- Day-of logistics (meeting points, timing, running late)
- Policy questions (cancellation, refunds, weather, age restrictions)
- Private tour / group event inquiries
- Scheduling callbacks and consultations via calendar link
- Escalation for safety, legal, active emergencies

**Out of Scope (escalate immediately):**
- Processing refunds
- Modifying existing bookings
- Providing or emailing full itineraries
- Quoting custom private tour prices
- Anything not in the Knowledge Base

### Persona Guidelines

**Voice:**
- Confident, warm, efficient
- Sounds like a knowledgeable local who's done this many times
- Matches caller energy: slow down if upset, keep pace if excited

**Language Rules:**
- 1–2 sentences max per response (voice)
- Ask ONE question at a time
- Never mention: tags, routing, KB, internal systems, "transfer," "handoff"
- Never send full itineraries — only meeting point/time and booking links
- Never glamorize intoxication
- Never invent URLs — only use KB booking links or the calendar link

**Calendar Language:**
- When offering a callback or consultation: "I can have someone from our team reach out — would you like me to send you a link to pick a time?"
- Do NOT say "appointment" for tours — say "booking link" or "reserve link"
- Calendar link is for callbacks and consultations only, not for tour bookings

### Tour Categories

| Category | Description | Booking Link Variable |
|----------|-------------|----------------------|
| CAT_1 | Drink Tours (brewery, wine, distillery) | `{{custom_value.booking_url_cat_1}}` |
| CAT_2 | Food Tours (tacos, BBQ, culinary) | `{{custom_value.booking_url_cat_2}}` |
| CAT_3 | Sightseeing Tours (city, landmarks, history) | `{{custom_value.booking_url_cat_3}}` |
| PRIVATE | Private events (bachelorette, corporate, custom groups) | `{{custom_value.booking_url_private}}` |
| BUS_RENTAL | Transportation only (no guided tour) | `{{custom_value.booking_url_bus_rental}}` |
| GENERAL | Unknown / browsing | `{{custom_value.booking_url_general}}` |
| CALLBACK | Callback / consultation scheduling | `{{custom_value.callback_scheduling_link}}` |

### Knowledge Bases

| KB Name | Purpose | Query When |
|---------|---------|------------|
| DayOf_Logistics | Meeting points, timing, late arrival, parking | Tour is today; caller running late; can't find meeting point |
| Policies | Cancellation, refunds, weather, age restrictions | Cancellation, refund, reschedule, weather concern, age restriction question |
| Escalation_Safety | Safety incidents, disputes, de-escalation scripts | Safety keyword detected, complaint, dispute, legal mention |
| Private_Tours_Sales | Private tour packages, group events, pricing guidance | Private tour, group event, bachelorette, corporate, bus rental |
| Tour_Descriptions | Tour details, inclusions, highlights | "What tours do you have?", "What's included?", "Tell me about..." |
| Booking_Links | Authoritative URLs by category | Ready to send a booking link — ALWAYS check before sending |

### Escalation Model (Three-Tier)

#### Tier 1 — AI Resolves
AI answers from KB, sends booking link, or provides information. No human involvement.

#### Tier 2 — AI Schedules (Calendar Booking)
For non-emergency situations that would otherwise escalate. AI offers to send a calendar link so the customer can pick a time for a callback or consultation.

| Trigger | Action |
|---------|--------|
| Corporate / private event inquiry | Offer consultation: "Would you like me to send a link to pick a time to chat with our team?" |
| Reservation change request | Offer callback: "I can have someone reach out — want me to send a link to pick a time?" |
| Refund processing needed | Provide policy from KB, offer callback for processing |
| Caller requests human (non-emergency) | Offer callback: "I can have someone call you back — would you like to pick a time?" |
| Confidence fallback (AI unsure) | Offer callback before creating a task |

**Disposition:** `tourops_outcome = CalendarBooked`, `tourops_work_state = AI_ACTIVE` (no human handoff)

#### Tier 3 — True Escalation (Human Handoff)
Only for safety, legal, and active emergencies. Creates a task, sets `tourops_work_state = HUMAN_ACTIVE`.

| Trigger | Priority | Action |
|---------|----------|--------|
| Safety keywords (police, lawsuit, injury, crash, ambulance, assault, harassment, DUI) | P0 — CRITICAL | Immediate escalation, collect name/number/date, tag: human handover + support-urgent, end call |
| Legal keywords (attorney, lawyer, sue, BBB, ADA) | P0b — CRITICAL | Immediate escalation, collect details neutrally, end call |
| Active DayOf emergency (bus not at location, safety issue in progress) | P1 — URGENT | Immediate escalation to dispatch |

**Disposition:** `tourops_outcome = Escalated`, `tourops_work_state = HUMAN_ACTIVE`

### Team & Contacts

| Role | Use When | GHL Variable |
|------|----------|-------------|
| Owner / Manager (Todd Abrams) | Safety, legal, policy exceptions, refund overrides, prompt changes | `{{custom_value.OWNER_NAME}}` |
| Daily QA Reviewer (Mike) | Customer callbacks, quality issues, escalation follow-up | Internal |
| Dispatch / Driver | Day-of routing, bus location, pickup issues | `{{custom_value.DISPATCH_CONTACT}}` |

**Communication Protocol:** GHL Internal Chat

### Non-Negotiables

- If `{{contact.first_name}}` is already present → do NOT ask again, do NOT overwrite
- ALWAYS get permission before texting ("Should I send it to this number?")
- NEVER promise refunds outside written policy
- NEVER provide or send full routes/itineraries — only meeting point/time and approved links
- NEVER invent booking links — only use URLs from Booking_Links KB or `{{custom_value.callback_scheduling_link}}`
- NEVER say "appointment" for tours
- NEVER bypass Tier 3 for P0/P0b — safety and legal always get immediate human escalation
- NEVER send calendar link for P0/P0b situations

---

## Part 2 — AI System Configuration

**Platform Version:** TourOps Schema Contract 4
**Schema Contract:** 4 (Doc Revision r07, 2026-03-03)

### Voice AI

| Field | Value |
|-------|-------|
| File | `prompts/vai_production_prompt.md` |
| Agent Name | Hope |
| Platform | GoHighLevel Voice AI Agent |
| Status | V6.0 active in BB production — pending 23/23 regression tests + Todd Abrams sign-off before full deploy |
| Last Changed | 2026-03-03 |
| Turn limit for confidence fallback | 3 exchanges before escalation fires |

**Voice AI Actions (V6.0):**

| Action Name | Type | Trigger | Notes |
|-------------|------|---------|-------|
| Send Booking Link — CAT_1 (Drink) | SMS | PATH D1: drink tour, under 10 | No change from V5 |
| Send Booking Link — CAT_2 (Food) | SMS | PATH D1: food tour, under 10 | No change from V5 |
| Send Booking Link — CAT_3 (Sightseeing) | SMS | PATH D1: sightseeing, under 10 | No change from V5 |
| Send Booking Link — PRIVATE | SMS | PATH D1: private inquiry under 10 | No change from V5 |
| Send Booking Link — BUS_RENTAL | SMS | PATH E: transportation only | No change from V5 |
| Send Booking Link — GENERAL | SMS | Fallback / unknown tour type | No change from V5 |
| `OPERATOR__BarleyBus__ConsultationBooked` | SMS | PATH E/G: email-fallback when caller declines to give email | **NEW — V6.0.** Sends `{{custom_value.callback_scheduling_link}}`. Before delivery: "Sending that over now." After delivery: "Did that come through? Sometimes it takes a second or two." |
| Book Appointment | Appointment | PATH E: 10+ private tour. PATH G: Human request / confidence fallback | **NEW — V6.0.** Calendar: Barley Bus Consultation (Tim). Offering days: 3. Slots/day: 3. Buffer: 1 hour. Before: "Let me get that set up for you." After: "You're all set — you'll get a confirmation to that email." |

### Conversation AI

| Field | Value |
|-------|-------|
| Bot Name | TourOps — Barley Bus — Master Router |
| Platform | GoHighLevel Conversation AI Flow Builder |
| Channels | SMS, WebChat |
| Status | DRAFT — Pending System Owner Approval |
| Turn limit for confidence fallback | 4 exchanges before escalation fires |
| Auto-Summaries | Enabled. Inactivity: 30 min. Minimum messages: 5. |

### GHL Bot Settings

| Setting | Value |
|---------|-------|
| Status | Auto Pilot |
| Max Messages | 100 |
| Tone (Bot Goals) | Friendly + Confident |
| Stop Bot toggle | OFF |
| Human Handover toggle | OFF |
| Auto Followup toggle | OFF |
| Allow Bot to Cancel Appointment | OFF |
| Allow Bot to Reschedule Appointment | OFF |
| GHL Snapshot ID | ⚠️ To be recorded by Technical Lead after Golden Snapshot is created |

> **Why all toggles OFF:** Escalation is handled via `tourops_work_state` inside modules. Bot Goals action toggles bypass the escalation logic and must remain OFF.

### Custom Fields in Use

**Core Interaction Fields:**
- `tourops_intent_bucket`, `tourops_intent_detail`, `tourops_script_play`
- `tourops_outcome`, `tourops_next_best_action`, `tourops_last_sms_template`

**Lifecycle & System Control Fields:**
- `tourops_lifecycle_stage`, `tourops_work_state`, `tourops_handoff_active`
- `tourops_last_interaction_at`, `tourops_primary_channel`

**Customer Data Fields:**
- `tourops_preferred_date`, `tourops_group_size`, `tourops_tour_type`
- `tourops_booking_status`, `tourops_open_loop`

**Narrative Memory Fields (Contract 3):**
- `tourops_conversationai_summary`, `tourops_voiceai_summary`

**QA Grader Fields (Contract 3+):**
- `tourops_last_score`, `tourops_last_review_date`, `tourops_issue_count`
- `tourops_score_notes` *(Contract 4 — grader writes one-line reasoning)*

**Calendar Scheduling (Contract 4):**
- `callback_scheduling_link` *(Custom Value — GHL calendar booking URL)*
- `{{custom_value.callback_scheduling_link}}` = `https://links.opsaiworks.com/widget/booking/TKYfczjDev5Is1yOu9Vx`
- ✅ Set in BB production (2026-03-03). Set in sandbox before sandbox deploy.

**Helper Fields (Non-Contract):**
- `tourops_disposition_blob_text` — Raw AI classification output used for workflow branching
- `tourops_escalation_priority` — Escalation priority flag
- `tourops_handoff_task_open` — Tracks open handoff task state

**Voice AI Native Fields (used in workflow mapping):**
- `vai_outcome` *(Voice AI outcome — maps to Google Sheets column F)*
- `vai_nextaction` *(Voice AI next action — maps to Sheets column J)*
- `cai_nextaction` *(Conv AI next action)*

**Barley Bus Operator-Specific Fields (Voice AI — captured silently when offered):**
- `CALL_DateRequested`, `CALL_GroupSize`, `VAI_Occasion`, `CALL_PickupArea`

### Google Sheets Integration (Contract 4)

**Sheet:** BB_Daily_Call_Log
**Tabs:** Raw (one row per call), Daily Summary (auto-aggregating formulas)
**Workflow:** Append row as last action in `TourOps — VAI — After Call — Grader v1.0`

**Column Mapping (Voice AI):**

| Column | Header | GHL Merge Field |
|--------|--------|----------------|
| A | Date | `{{contact.tourops_last_interaction_at}}` (format YYYY-MM-DD) |
| B | Time | `{{contact.tourops_last_interaction_at}}` (time portion) |
| C | Contact Name | `{{contact.name}}` |
| D | Phone | `{{contact.phone}}` |
| E | Intent Bucket | `{{contact.tourops_intent_bucket}}` |
| F | Outcome | `{{contact.vai_outcome}}` |
| G | Work State | `{{contact.tourops_work_state}}` |
| H | Score | `{{contact.tourops_last_score}}` |
| I | Score Notes | `{{contact.tourops_score_notes}}` |
| J | Next Action | `{{contact.vai_nextaction}}` |
| K | Summary | `{{contact.tourops_voiceai_summary}}` |

> **Note:** Date column must land as YYYY-MM-DD text for Daily Summary COUNTIFS to match TODAY(). If GHL sends full datetime, add a formatter step before the Sheets action.

### Intent Routing

| AI Splitter Internal Label | Canonical `tourops_intent_bucket` Value |
|----------------------------|-----------------------------------------|
| `DAYOF` | `DayOf` |
| `READY` | `ReadyToBook` |
| `RES_CHG` | `ReservationChange` |
| `DISC` | `Discovery` |
| `REF_CAN` | `RefundCancel` |
| `CORP` | `Corporate` |
| `PART` | `PartnerVendor` |
| `OTHER` / No Condition Met | `Other` |

> Do not change the AI Splitter routing labels. Canonical enum values written to GHL fields must match Schema Contract 4 exactly.

### Known Prompt Overrides

**Quote Lead Intercept (Added 2026-02-20):**
Conversation AI includes a pre-splitter if/else branch that intercepts contacts tagged `tourops_quote_lead` before they reach the Master AI Splitter. These contacts route directly to the `DISC — Quote Lead` module. This exists because quote leads have already selected a tour package option via drip SMS survey — the splitter misclassifies single-digit replies.

No other prompt overrides are active as of 2026-03-03.

### Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| GoHighLevel Voice AI Agent | Platform | Active account required |
| GoHighLevel Conversation AI Flow Builder | Platform | SMS + WebChat channels enabled |
| GoHighLevel Auto-Summaries | Platform | Required for `tourops_conversationai_summary`; shipped GHL Feb 10, 2026 |
| GoHighLevel Calendar | Platform | Required for callback/consultation scheduling (Contract 4) |
| Knowledge Base (6 KBs) | Content | Must be populated and current before go-live |
| SMS Templates | Content | Must exist with `OPERATOR__BarleyBus__` prefix |
| `tourops_schema_version = 4` field | Configuration | Must be set on account before deployment |
| Stuck-State Cleanup Workflow | Automation | Must be active every 4 hours |
| Google Sheets (BB_Daily_Call_Log) | Integration | Grader workflow appends row after each scored call |
| `callback_scheduling_link` custom value | Configuration | Must contain working GHL calendar URL |
| `tourops_quote_lead` tag | GHL Tag | Required for Quote Lead intercept to function |

---

## Part 3 — Current State

### Live Production Status

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Voice AI Prompt | Hope V6.0 | 🔄 Active in BB — pending 23/23 + sign-off | V5.0 was previous live version |
| Schema Contract | 4 (r07) | ✅ LIVE | Confirmed in production 2026-03-03 |
| Conversation AI | 8-module system | ✅ LIVE | Router + Module architecture, memory injection implemented |
| Auto-Summaries | Active | ✅ LIVE | Field: `tourops_conversationai_summary`. Inactivity: 30min, Min: 5 messages |
| Grader Workflows | VAI + CAI | ✅ LIVE | Schema Contract 4 grader fields active |
| Google Sheets | BB_Daily_Call_Log | 🔄 Wiring in progress | Column mapping finalized, Grader → Sheets action pending (OL-11) |
| GHL Account | Barley Bus Production | ✅ LIVE | LC Phone, Voice AI, Conversation AI |

### Environment Status

| Environment | Status | Notes |
|-------------|--------|-------|
| Production | ✅ Live | V6.0 build active in BB. Build-in-BB-first approach (intentional). |
| Golden | ✅ Active | Source of truth snapshot for current production build |
| Sandbox | ✅ Active | V6.0 changes will be replicated here after BB proof of concept |

### Active Workflows

| Workflow | Purpose | Status |
|----------|---------|--------|
| TourOps — VAI — After Call — Disposition | Post-call classification + field stamping | ✅ Active — V6.0 branches added (ConsultationBooked, TaskCreated) |
| TourOps — VAI — After Call — Grader v1.0 | Post-call scoring + Sheets append | ✅ Active — Sheets wiring pending (OL-11) |
| TourOps — CAI — Conversation Closed — Grader v1.0 | Conversation scoring | ✅ Active |
| TourOps — Auto-Summaries | CAI summary → Notes append | ✅ Active |
| TourOps — Task Completed Guard | Handoff resolution + work_state reset | ✅ Active |
| TourOps — Stuck State Cleanup | Resets stuck HUMAN_ACTIVE contacts | ✅ Active (every 4 hours) |

### Quality Targets

| Metric | Target |
|--------|--------|
| Average Score | ≥ 4.0/5 |
| Pass Rate (≥4.0) | ≥ 80% |
| Critical Failures | 0 |

### Pending / Roadmap

| Item | Priority | Target |
|------|----------|--------|
| Hope V6.0 — Complete GHL build steps 5-9 | REQUIRED | Active build |
| Hope V6.0 — Run 23/23 regression tests | REQUIRED | Before V6.0 sign-off |
| Hope V6.0 — Todd Abrams written sign-off | REQUIRED | Before V6.0 full deploy |
| Wire Grader → Google Sheets row action | HIGH | 2026-03-07 |
| Grader prompt update for `tourops_score_notes` | HIGH | 2026-03-07 |
| Conv AI modules update (READY, DISC, RES_CHG, REF_CAN, CORP) | HIGH | After Voice AI build complete |
| Schema Contract 5 — ConsultationBooked + TaskCreated | MEDIUM | After BB proof of concept |

### Known GHL Platform Constraints

| Constraint | Impact | Workaround |
|-----------|--------|------------|
| Task Completed trigger can't filter by task title | Could reset AI suppression for unrelated tasks | `tourops_work_state = HUMAN_ACTIVE` guard on Task Completed workflow |
| 3 Custom Triggers per Conversation AI bot | Limits distinct automations per flow | Reserve for high-value dispositions (booking, escalation, corporate) |
| Transfer Bot loses all context | Customer must repeat info | Transfer Bot permanently banned; all intents handled in single-bot Router+Module |
| RAG retrieval ~3 chunks max | KB answers may miss detail if KB is large | Keep KB chunks focused and concise |
| Voice AI cannot write fields directly from prompt | Disposition requires workflow action | Use "After The Call" workflow for all field stamps |

### Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-03 | Hope V6.0 active in BB production. V6.0 GHL build in progress (steps 1-4 complete). After-call Disposition workflow updated with ConsultationBooked and TaskCreated branches. | Todd Abrams |
| 2026-03-03 | Schema Contract 4 (r07) live. CalendarBooked enum, tourops_score_notes, callback_scheduling_link created in GHL. Google Sheets column mapping finalized. | Todd Abrams |
| 2026-02-28 | Schema Contract 3 (r06) confirmed live in BB production. | Todd Abrams |
| 2026-02-28 | Document consolidated from BB_Profile, BB_AI_System, BB_Current_State | Todd Abrams |
| 2026-02-22 | Schema Contract 3 approved and active | Todd Abrams |
| 2026-02-17 | Auto-Summaries implemented. Cross-channel memory active. | Todd Abrams |
| 2026-02-14 | Schema Contract 2 architecture documented. Conversation AI 8-module system live. | Todd Abrams |
| 2024-12-29 | Hope V5.0 deployed to production | Todd Abrams |

---

### Change Control

| Change Type | Approval Required | Process |
|-------------|------------------|---------|
| Prompt changes | Todd Abrams | Draft → test → approve → deploy → log in Prompt_Changelog |
| KB content updates | Todd Abrams | Update KB → verify in sandbox → deploy |
| Schema changes | Todd Abrams | Full change control process (see canonical_schema.md) |
| Escalation rule changes | Todd Abrams | Review + regression test before deploy |
| Calendar configuration | Todd Abrams | Update calendar settings → test booking flow → deploy |

*Update this file after every deployment, prompt change, or schema migration.*
