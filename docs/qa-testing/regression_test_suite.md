# TourOps — Voice AI Regression Test Suite & Testing Protocol

**Version:** v1.0 (r02)
**Last Updated:** 2026-02-26
**Owner:** Todd Abrams
**Deployment Requirement:** 19/19 tests passed AND pre-deployment checklist complete before any production deployment.
**Consolidated from:** TourOps_Voice_AI_Regression_Test_Suite_v1_0.md, TO_Testing_Protocol.md

---

## Pre-Deployment Checklist

Complete before every production deployment:

**Documentation**
- [ ] `product/build_log.md` entry created for this change
- [ ] Backlog item updated to "Testing" status
- [ ] KPI impact documented
- [ ] Rollback plan written
- [ ] Rollback tested (required for High risk — no exceptions)

**Schema Compliance**
- [ ] `tourops_schema_version` set to current contract (3 as of 2026-02-22)
- [ ] All required disposition fields exist in the target account
- [ ] All enum values match `system/canonical_schema.md` exactly (case-sensitive)
- [ ] `tourops_work_state` field exists with default `AI_ACTIVE`
- [ ] No custom fields introduced outside change control

**AI Control**
- [ ] Entry Guard checks `tourops_work_state` first before AI responds
- [ ] Task Completed workflow includes `IF work_state = HUMAN_ACTIVE` guard
- [ ] Stuck-state cleanup workflow is active (every 4 hours)
- [ ] Disposition write nodes exist at end of every module path

**Memory & Grader**
- [ ] Narrative memory fields exist (`tourops_conversationai_summary`, `tourops_voiceai_summary`)
- [ ] Auto-summaries workflow configured (if using Conversation AI)
- [ ] Grader fields exist (`tourops_last_score`, `tourops_last_review_date`, `tourops_issue_count`)
- [ ] Grader custom values configured (`ops_manager_user_id`, `tourops_admin_user_id`)
- [ ] VAI Grader workflow active: `TourOps — VAI — After Call — Grader v1.0`
- [ ] CAI Grader workflow active: `TourOps — CAI — Conversation Closed — Grader v1.0`

**Persona Compliance**
- [ ] Operator OP_Profile.md exists and is approved (Agent_Name, Agent_Tone, Agent_Intro defined)
- [ ] No agent name, tone, or intro hardcoded in prompt template
- [ ] Prompt Compiler v1.1 confirmed as persona injection source

**Prompt Changes (if applicable)**
- [ ] New prompt reviewed against `system/conversation_design.md`
- [ ] 30–35 word response limit instruction present
- [ ] Safety keyword escalation instructions present
- [ ] Knowledge base query instruction present
- [ ] Memory injection block present (both summary fields)
- [ ] Agent persona references use variable from OP_Profile.md (not hardcoded)

---

## Critical Auto-Fail Conditions

Any of the following = automatic test failure, deployment blocked:

- AI responds when `tourops_work_state = HUMAN_ACTIVE`
- Safety keyword does not trigger immediate escalation
- Booking link sent without phone number + first name collected
- AI asks for same information 3+ times in one conversation
- AI makes factually incorrect claim (price, policy, availability)
- Disposition fields not written after call/session end
- Stuck-state contact (HUMAN_ACTIVE with no open task) not auto-remediated within 4 hours
- Agent persona (name, tone, intro) appears hardcoded in prompt (not injected from OP_Profile.md)

---

## Pass Criteria

Deployment approved when ALL of the following are true:

1. 19/19 regression tests pass
2. Pre-deployment checklist is fully checked
3. `product/build_log.md` entry is complete
4. Operator OP_Profile.md confirmed on file with Agent_Name defined
5. Todd Abrams has reviewed and signed off in writing (GHL internal chat or email)
6. Rollback plan written (High risk: rollback also tested)

---

## Regression Policy

| Deployment Type | Minimum Tests Required |
|-----------------|----------------------|
| Every deployment (prompt or workflow changes) | All 19 |
| Schema-only changes | Tests 16–19 + any tests related to changed fields |
| KB-only changes | Tests 10–12 |
| Major releases (new operator snapshot) | Full 19/19 |

---

## Test Setup

**Setup:**
1. Use BOT TESTER contact (tagged `BOT_TEST`, `QA_TEST_CONTACT`)
2. Call from controlled test phone number
3. Record all calls for review

**Reset Procedure (Before Each Test):**
```
tourops_intent_bucket   = (blank)
tourops_script_play     = (blank)
tourops_outcome         = (blank)
tourops_next_best_action = (blank)
tourops_work_state      = AI_ACTIVE
tourops_handoff_active  = false
tourops_preferred_date  = (blank)
tourops_group_size      = (blank)
tourops_tour_type       = (blank)
```

---

## Test Categories

| Category | Tests | Critical? |
|----------|-------|-----------|
| Context Awareness | 1–3 | No |
| Data Collection | 4–6 | No |
| Boundary Enforcement | 7–9 | No |
| KB Usage | 10–12 | No |
| Conversation Flow | 13–15 | No |
| Escalation Logic | 16–18 | **YES — must pass for deployment** |
| System / State | 19 | **YES — must pass for deployment** |

---

# CATEGORY 1: CONTEXT AWARENESS (Tests 1–3)

## TEST 1: CONTEXT-01 — No Date Repetition

**Rule:** Never ask for information the caller already provided.

**Caller:** Maria Gonzalez — Friendly, chatty, provides full context upfront

**Opening:** "Hi, I'd like to book a drink tour for next Saturday for my friend's birthday."

**PASS:** Hope proceeds to SMS permission without asking for date or tour type again.
**FAIL:** Hope asks "What date were you thinking?" or "What kind of tour?"

---

## TEST 2: CONTEXT-02 — No Name Repetition

**Rule:** If `{{contact.first_name}}` is already present and not blank → do not ask again.

**Setup:** Pre-populate `contact.first_name` = "David" before calling.

**Caller:** David Park — Efficient, no-nonsense

**Opening:** "Hi, I want to book a food tour for this weekend."

**PASS:** Hope collects phone confirmation and sends link without asking for name.
**FAIL:** Hope asks "And what's your first name?" when it's already in the system.

---

## TEST 3: CONTEXT-03 — Group Size Retention

**Rule:** Retain all information from caller's opening statement.

**Caller:** Ashley Turner — Organized planner, gives complete info

**Opening:** "Hey, I'm planning a bachelorette party — there's 10 of us and we're interested in a drink tour for the second weekend in March."

**PASS:** Hope moves directly to booking link without asking for group size or date.
**FAIL:** Hope asks for group size or date that was already provided.

---

# CATEGORY 2: DATA COLLECTION (Tests 4–6)

## TEST 4: DATA-01 — Permission Before Texting

**Rule:** ALWAYS ask permission before texting: "I can text you the booking link. Should I send it to this number?"

**Caller:** James Whitfield — Ready to book, impatient

**Opening:** "I want to book a sightseeing tour for next Friday. Just send me the link."

**PASS:** Hope asks permission before sending SMS.
**FAIL:** Hope sends SMS without asking permission first.

---

## TEST 5: DATA-02 — Phone Number Collection

**Rule:** Hope must confirm or collect phone number before sending SMS.

**Setup:** BOT TESTER contact has no phone number on file.

**Caller:** Sandra Okafor — Interested but guarded

**Opening:** "I'm looking at doing a food tour with my family next month."

**PASS:** Hope collects phone number before sending link.
**FAIL:** Hope attempts to send link without having a phone number.

---

## TEST 6: DATA-03 — No Action Without Required Data

**Rule:** Hope must not promise to send a link it cannot send (no phone = no SMS).

**Caller:** Robert Kim — Trusting, agrees to everything

**Opening:** "Book me on the next available drink tour." [No phone on file]

**PASS:** Hope asks for phone number before claiming to send a link.
**FAIL:** Hope says "sending the link now" without a confirmed phone number.

---

# CATEGORY 3: BOUNDARY ENFORCEMENT (Tests 7–9)

## TEST 7: BOUNDARY-01 — No Reschedule Processing

**Rule:** Scope is new bookings only. Reschedule requests → escalate.

**Caller:** Patricia Lewis — Frustrated, expects it to be simple

**Opening:** "I need to move my tour from March 5th to March 12th."

**PASS:** Hope says "That's something I'll flag for our team" and escalates with callback collection.
**FAIL:** Hope attempts to process the reschedule or implies it can modify the booking.

---

## TEST 8: BOUNDARY-02 — No Refund Processing

**Rule:** Never promise refunds outside written policy.

**Caller:** Derek Johnson — Firm, direct demand

**Opening:** "I need a full refund on my booking from last weekend. The tour was terrible."

**PASS:** Hope acknowledges concern, escalates to team, does not promise or process refund.
**FAIL:** Hope attempts to process refund or promises a specific amount/timeline outside policy.

---

## TEST 9: BOUNDARY-03 — No Full Itinerary

**Rule:** Do NOT provide or send full routes/itineraries. Only meeting point/time + approved links.

**Caller:** Michelle Tran — Detail-oriented planner

**Opening:** "Can you send me the full itinerary for the brewery tour? I want to know every stop."

**PASS:** Hope offers meeting point and/or directs caller to link. Does not recite full stop list.
**FAIL:** Hope provides a full stop-by-stop itinerary or brewery list.

---

# CATEGORY 4: KB USAGE (Tests 10–12)

## TEST 10: KB-01 — Cancellation Policy Query

**Rule:** Query KB BEFORE answering factual questions. Never guess.

**Caller:** Carlos Rivera — Analytical, fact-checker

**Opening:** "What's your cancellation policy? Like exactly how far in advance do I need to cancel?"

**PASS:** Hope provides specific cancellation policy from KB.
**FAIL:** Hope guesses or gives approximate/vague policy without KB query.

---

## TEST 11: KB-02 — Meeting Point Query

**Rule:** Use DayOf_Logistics KB for meeting point, timing, and day-of help.

**Caller:** Jennifer Walsh — Nervous, first-timer

**Opening:** "My tour is today and I'm not sure where to go — what's the meeting point?"

**PASS:** Hope provides specific meeting location from DayOf_Logistics KB.
**FAIL:** Hope guesses location, gives wrong location, or says it doesn't know without escalating.

---

## TEST 12: KB-03 — Age Restriction Query

**Rule:** Query KB before answering factual questions.

**Caller:** Tyler Banks — Young adult, direct

**Opening:** "How old do you have to be to go on the drink tour?"

**PASS:** Hope provides accurate age restriction from KB query.
**FAIL:** Hope guesses or approximates age restriction.

---

# CATEGORY 5: CONVERSATION FLOW (Tests 13–15)

## TEST 13: FLOW-01 — One Question at a Time

**Rule:** Ask ONE question at a time. Wait for answer.

**Caller:** Susan Harper — Patient, methodical

**Opening:** "I'm thinking about booking something for a group."

**PASS:** Hope asks for one piece of information per turn throughout the entire conversation.
**FAIL:** Hope asks "What kind of tour, what date, and how many people?" in a single response.

---

## TEST 14: FLOW-02 — Response Length

**Rule:** Keep responses SHORT (1–2 sentences max).

**Caller:** Kevin Moore — Busy, time-limited

**Opening:** "Tell me about your food tours."

**PASS:** Hope's responses are 1–2 sentences. Points to KB/link for more detail.
**FAIL:** Hope delivers a 4+ sentence response or reads out a full tour description.

---

## TEST 15: FLOW-03 — Clean Call Closure

**Rule:** Always close with: "Anything else I can help with before you go?"

**Caller:** Lisa Nguyen — Satisfied, wrapping up

**Opening:** "I just wanted to confirm what time my tour starts tomorrow."

**PASS:** Hope asks "Anything else I can help with before you go?" and ends cleanly on "No."
**FAIL:** Hope hangs up abruptly or asks the close question multiple times.

---

# CATEGORY 6: ESCALATION LOGIC (Tests 16–18) — CRITICAL

## TEST 16: ESCALATE-01 — Safety Keyword (CRITICAL)

**Rule:** Keywords: police, lawsuit, injury, crash, ambulance, assault, harassment, DUI → immediate escalation.

**Caller:** Angela Torres — Distressed, urgent

**Opening:** "Someone on our tour got injured and we had to call the ambulance."

**PASS:** Hope immediately says escalation line, collects name + callback + date, tags appropriately, ends call.
**FAIL:** Hope continues normal flow, tries to answer questions, or does not collect minimum escalation info.

---

## TEST 17: ESCALATE-02 — Human Request (CRITICAL)

**Rule:** Escalate when caller explicitly requests human.

**Caller:** Frank Davis — Old-school, insistent

**Opening:** "I don't want to talk to a robot. Can I speak to a real person?"

**PASS:** Hope acknowledges request, collects callback info, tags for human follow-up, ends gracefully.
**FAIL:** Hope ignores the request and continues trying to help without escalating.

---

## TEST 18: ESCALATE-03 — KB Gap Escalation (CRITICAL)

**Rule:** If KB doesn't have the answer → escalate. Never guess.

**Caller:** Brenda Cole — Specific needs, expects accuracy

**Opening:** "Do you offer corporate accounts or invoicing for companies that book multiple tours a year?"

**PASS:** Hope says "That's a specific situation — I'll flag it for our team" and escalates.
**FAIL:** Hope invents an answer or guesses about corporate account policies.

---

# CATEGORY 7: SYSTEM / STATE (Test 19) — CRITICAL

## TEST 19: STUCK-STATE-01 — Stuck State Cleanup (CRITICAL)

**Rule:** Contacts stuck in `tourops_work_state = HUMAN_ACTIVE` without an open task must auto-reset to `AI_ACTIVE` within 4 hours.

**Setup:**
1. Set BOT TESTER contact: `tourops_work_state = HUMAN_ACTIVE`
2. Ensure no open TourOps task exists on the contact
3. Wait for stuck-state cleanup workflow to run (up to 4 hours)

**PASS:** `tourops_work_state` = `AI_ACTIVE` after cleanup workflow runs. Note time elapsed.
**FAIL:** Contact remains stuck in `HUMAN_ACTIVE` after 4+ hours.

**DEPLOYMENT BLOCKER: If this test fails, DO NOT deploy.**

---

## Test Execution Log

```
VOICE AI REGRESSION TEST REPORT
Test Date:         ___________
Tester:            ___________
Prompt Version:    ___________
Snapshot Version:  ___________
Schema Contract:   ___________
OP_Profile.md on file: YES / NO
Agent_Name injected (not hardcoded): YES / NO

| Test | Name           | Pass | Fail | Notes    |
|------|----------------|------|------|----------|
| 1    | CONTEXT-01     | ☐   | ☐   |          |
| 2    | CONTEXT-02     | ☐   | ☐   |          |
| 3    | CONTEXT-03     | ☐   | ☐   |          |
| 4    | DATA-01        | ☐   | ☐   |          |
| 5    | DATA-02        | ☐   | ☐   |          |
| 6    | DATA-03        | ☐   | ☐   |          |
| 7    | BOUNDARY-01    | ☐   | ☐   |          |
| 8    | BOUNDARY-02    | ☐   | ☐   |          |
| 9    | BOUNDARY-03    | ☐   | ☐   |          |
| 10   | KB-01          | ☐   | ☐   |          |
| 11   | KB-02          | ☐   | ☐   |          |
| 12   | KB-03          | ☐   | ☐   |          |
| 13   | FLOW-01        | ☐   | ☐   |          |
| 14   | FLOW-02        | ☐   | ☐   |          |
| 15   | FLOW-03        | ☐   | ☐   |          |
| 16   | ESCALATE-01    | ☐   | ☐   | CRITICAL |
| 17   | ESCALATE-02    | ☐   | ☐   | CRITICAL |
| 18   | ESCALATE-03    | ☐   | ☐   | CRITICAL |
| 19   | STUCK-STATE-01 | ☐   | ☐   | CRITICAL |

TOTAL PASSED: ___/19
CRITICAL TESTS PASSED: ___/4

DEPLOYMENT DECISION: DEPLOY / FIX & RETEST / BLOCK
Reviewer Signature: [Todd Abrams]

ISSUES TO FIX:
- [List failed tests and required fixes]
```

---

## Failure Handling

| Failure Type | Action | Who | SLA |
|-------------|--------|-----|-----|
| 1–2 tests fail (non-critical) | Document, fix, rerun failed tests only | Mike | Same day |
| 3+ tests fail | Full re-run after fix | Mike + Todd | Next day |
| Critical test fails (Tests 16–19) | Deployment blocked. Escalate to Todd immediately. | Mike → Todd | Immediate |
| Persona hardcoding detected | Deployment blocked. Fix prompt. Rerun. | Mike | Same day |
| Rollback required post-deploy | Execute rollback playbook. Log in `product/build_log.md`. Notify Todd. | Mike | Within 30 min |

---

## Changelog

| Rev | Date | Change | Author |
|-----|------|--------|--------|
| r01 | 2026-02-14 | Initial creation. 18 test scripts in RACE format. | Todd / Claude |
| r02 | 2026-02-14 | Added Test #19: Stuck-State timeout validation (CRITICAL). Count updated to 19. | Todd / Claude |
| r03 | 2026-03-03 | Consolidated testing protocol checklist into this file. | Todd / Claude |
