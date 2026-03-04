# TourOps — Operations Manual

**Last Updated:** 2026-02-26
**Owner:** Mike
**Primary KPI:** Voice AI Conversation Quality Score ≥ 4.0 average
**SOP Drift Rule:** Any SOP not reviewed in 90 days must be audited before use.
**Ownership Rule:** Every recurring task has a named owner. No shared ownership without a primary.
**Consolidated from:** TO_Run_Operations_Manual.md, TO_Run_Training_Guide.md, TO_Run_Weekly_Review.md, TO_Run_Performance_Dashboard.md

---

## System Overview

TourOps Voice AI RUN manages the daily and weekly quality operations for the Primary Voice Agent and all operator AI deployments. Primary responsibilities: QA scoring, issue tracking, escalation handling, operator support, and weekly review reporting.

---

## Role Responsibilities

| Role | Responsibilities | Tools | Primary Owner |
|------|-----------------|-------|---------------|
| QA Manager | Weekly review, scoring, issues log, weekly review | GHL, Google Sheets, Claude AI Command Center | Mike |
| QA Support & Communications | Primary owner of all communications — grader validation, customer callbacks, escalation handling, all outbound/inbound communications with operators and customers. Tim's primary function is Barley Bus GM operations; QA Support duties scoped to available capacity. | GHL, Google Sheets, Quality Rubric | Tim |
| System Owner | Approve prompt changes, P0/P0b escalations, schema decisions | GHL, all files | Todd |

---

## Core SOPs

### SOP 1 — Daily Escalation Review

**Trigger:** 9:00 AM every business day | **Owner:** Mike | **KPI:** Escalation Rate, Customer Experience

1. Open GHL → filter contacts by `tourops_work_state = HUMAN_ACTIVE` (authoritative)
2. Secondary visual check: `Human handover` tag (visibility aid only — not authoritative)
3. Count open escalations. Identify any past SLA.
4. Prioritize by category: Safety (P0) > DayOf > Human Request > Standard
5. Handle all overdue items first. Assign to appropriate handler.
6. For P0/P0b: Notify Todd immediately via GHL internal chat
7. Log any new patterns (same question 3+ times = KB gap)

**Done when:** All HUMAN_ACTIVE contacts have an open task. All P0/P0b escalated to Todd. No contacts past SLA without a logged reason.

---

### SOP 2 — Weekly QA Review

**Trigger:** Every Wednesday by 12:00 PM | **Owner:** Mike | **KPI:** Quality Score

1. Pull all conversations from prior 7 days (GHL + Google Sheets)
2. Pull grader scores from `tourops_last_score` field on reviewed contacts
3. For any conversation scoring < 3.0 OR flagged Critical: pull full transcript and manually score using `operations/quality.md`
4. Manually spot-check 3 additional random conversations (grader validation)
5. Calculate weekly averages: Overall score, category breakdowns, pass rate, critical failure count
6. Update Performance Dashboard section in this file with weekly metrics
7. Identify top 3 friction points. Determine root cause.
8. Log any recurring issues (2nd occurrence) in `state/active_state.md`
9. Complete Weekly Review entry. Flag escalations to Todd if needed.

**Done when:** Weekly Review entry completed and dated. Any 🔴 metrics escalated to Todd via GHL.

---

### SOP 3 — Customer Callback (Escalation Resolution)

**Trigger:** Escalation task assigned in GHL | **Owner:** Tim (primary) | **KPI:** Escalation Rate, Customer Experience

1. Open GHL task. Read full conversation transcript before calling.
2. Identify: What did the AI fail to resolve? What does the customer need?
3. Call customer back. Use appropriate script from `operations/escalation_playbook.md`.
4. Resolve issue or route to Todd (P0/P0b).
5. Complete GHL task.
6. System auto-resets `tourops_work_state = AI_ACTIVE` upon task completion. Verify reset occurred.
7. If resolution reveals KB gap or recurring pattern, log in `state/active_state.md`

**Done when:** Task completed. Customer issue resolved or routed. work_state confirmed back to AI_ACTIVE.

---

### SOP 4 — New Operator QA Onboarding

**Trigger:** BUILD confirms 19/19 regression pass | **Owner:** Mike | **KPI:** Quality Score (new operator)

1. Receive confirmation from BUILD: "Operator [Name] deployed. 19/19 pass."
2. Confirm operator OP_Profile.md is on file and Agent_Name is active in deployed prompt
3. Add operator to weekly QA rotation in Google Sheets
4. Monitor first 10 live customer conversations manually (grader + manual spot check)
5. Report to Todd after conversations 5 and 10: "Operator [Name] QA update — score X.X, issues: [list]"
6. Begin standard weekly QA cadence for operator

**Done when:** First 10 conversations reviewed. Todd notified. Operator in standard QA rotation. OP_Profile.md confirmed active.

---

### SOP 5 — Prompt Change QA Monitoring

**Trigger:** BUILD deploys prompt change to production | **Owner:** Mike | **KPI:** Quality Score

1. Receive deployment notification from BUILD via GHL internal chat
2. Flag new prompt version in Google Sheets tracker (deployment date + version)
3. Confirm OP_Profile.md persona still active in new prompt (agent name not hardcoded)
4. Score first 5 live conversations post-deployment manually, regardless of grader
5. Compare pre/post scores. Flag any delta > 0.5 drop for immediate review.
6. Report to Todd at 24h and 48h post-deploy
7. If score drops below 3.5 within first 3 days → escalate to Todd immediately for rollback decision

**Done when:** 48h report sent to Todd. No rollback required OR rollback executed and confirmed. OP_Profile.md persona confirmed active.

---

## Task Schedule

| Task | Owner | Frequency | Time |
|------|-------|-----------|------|
| Daily escalation review | Mike | Daily 9:00 AM | 15 min |
| Grader score spot check (3 random calls) | Tim | Daily | 20 min |
| Customer callbacks (open tasks) | Tim (primary) / Mike | As needed | Varies |
| Weekly QA review | Mike | Wednesday by noon | 45 min |
| Performance Dashboard update | Mike | Wednesday | 15 min |
| Weekly Review completion | Mike | Wednesday | 20 min |
| Issues log review | Mike | Wednesday | 10 min |
| Grader validation vs. manual score | Tim | Weekly | 30 min |
| OP_Profile.md audit (confirm persona active per operator) | Mike | Monthly | 15 min |
| SOP audit (90-day drift check) | Mike | Monthly | 30 min |

---

## Weekly Review Template

*Complete every Wednesday by noon. Append each entry below previous.*

---

### Week of [DATE]

**Completed by:** Mike | **Time:** [When completed]

**KPI Summary**

| Metric | This Week | Last Week | Target | Status |
|--------|-----------|-----------|--------|--------|
| Avg Quality Score | — | — | ≥ 4.0 | 🟢🟡🔴 |
| Pass Rate (≥ 4.0) | — | — | ≥ 80% | 🟢🟡🔴 |
| Critical Failures | — | — | 0 | 🟢🟡🔴 |
| Escalation Rate | — | — | < 20% | 🟢🟡🔴 |
| Grader Coverage | — | — | 100% | 🟢🟡🔴 |

**Overall Status:** 🟢 On track / 🟡 Watch / 🔴 Escalate to Todd now

**Escalation Required?** YES / NO — If YES: [What issue, to whom, sent when]

**Top 3 Friction Points**
1. [Friction point] — KPI affected: [KPI] — Recommendation: [action]
2. [Friction point] — KPI affected: [KPI] — Recommendation: [action]
3. [Friction point] — KPI affected: [KPI] — Recommendation: [action]

**Active Improvement Initiatives** (max 3)

| Initiative | Owner | Status | Due |
|-----------|-------|--------|-----|
| 1. | | | |
| 2. | | | |
| 3. | | | |

**New Issues for Issues Log:** [Any issue appearing 2nd time — or "None"]

**Grader Validation:** Tim manually scored [X] conversations. Average delta vs. grader: [X.X] pts. Status: 🟢🟡🔴

**Persona Compliance:** OP_Profile.md confirmed active for [X] operator(s). Hardcoding detected: YES / NO.

**Capacity:** Available next week: [%] | Utilization: [%] | Constraint: Yes/No

**Recommendations to TO_Lead:**
1. [Recommendation] — KPI impact: [impact] — Urgency: High/Med/Low

---

**First Entry — Week of 2026-02-24**

*Note: First week of grader-assisted QA. Grader deployed 2026-02-22. Scores this week establish the baseline. Tim validating grader accuracy — results due 2026-02-28.*

Overall Status: 🟡 Watch — Grader in validation, no confirmed baseline yet.

Recommendations:
1. Hold off on scoring targets until grader validation complete — Urgency: High
2. Confirm BB OP_Profile.md creation on track (due 2026-03-03) — Urgency: Med

---

## Performance Dashboard

*Updated every Wednesday before Weekly Review is completed.*

**Leading Indicator Rule:** 2+ leading indicators 🟡 in the same week → pre-escalation review required even if lagging KPIs are 🟢.

### Week of: [DATE]

**Primary KPI**

| Metric | This Week | Last Week | % Change | Target | Status |
|--------|-----------|-----------|----------|--------|--------|
| Avg Quality Score (all operators) | — | — | — | ≥ 4.0 | 🟢🟡🔴 |

**Lagging KPIs**

| Metric | This Week | Last Week | Threshold | Status |
|--------|-----------|-----------|-----------|--------|
| Pass Rate (score ≥ 4.0) | — | — | ≥ 80% | 🟢🟡🔴 |
| Critical Failures | — | — | 0 | 🟢🟡🔴 |
| Escalation Rate | — | — | < 20% | 🟢🟡🔴 |
| Grader Coverage | — | — | 100% | 🟢🟡🔴 |
| Open Critical Issues | — | — | 0 | 🟢🟡🔴 |

**Leading Indicators (Early Warning)**

| Indicator | This Week | Last Week | Threshold | Status |
|-----------|-----------|-----------|-----------|--------|
| Avg Context Awareness score | — | — | ≥ 4.0 | 🟢🟡🔴 |
| Avg Escalation Logic score | — | — | ≥ 4.0 | 🟢🟡🔴 |
| Avg KB Usage score | — | — | ≥ 4.0 | 🟢🟡🔴 |
| Grader accuracy delta (manual vs. auto) | — | — | ≤ 0.5 | 🟢🟡🔴 |
| Stuck-state contacts (HUMAN_ACTIVE, no task) | — | — | 0 | 🟢🟡🔴 |
| Disposition field miss rate | — | — | 0% | 🟢🟡🔴 |
| Operators with OP_Profile.md confirmed active | — | — | 100% | 🟢🟡🔴 |

**Category Breakdown**

| Category | Avg This Week | Avg Last Week | Trend | Status |
|----------|--------------|--------------|-------|--------|
| 1. Context Awareness | — | — | ↑↓→ | 🟢🟡🔴 |
| 2. Data Collection | — | — | ↑↓→ | 🟢🟡🔴 |
| 3. Boundary Enforcement | — | — | ↑↓→ | 🟢🟡🔴 |
| 4. KB Usage | — | — | ↑↓→ | 🟢🟡🔴 |
| 5. Conversation Flow | — | — | ↑↓→ | 🟢🟡🔴 |
| 6. Escalation Logic | — | — | ↑↓→ | 🟢🟡🔴 |

**Per-Operator Breakdown**

| Operator | Conversations | Avg Score | Pass Rate | Critical Failures | OP_Profile.md Active | Status |
|----------|--------------|-----------|-----------|-------------------|----------------------|--------|
| Barley Bus | — | — | — | — | Pending (due 2026-03-03) | 🟢🟡🔴 |

**4-Week Trend**

| Week | Avg Score | Pass Rate | Critical Failures | Overall Status |
|------|-----------|-----------|-------------------|----------------|
| [Week -3] | — | — | — | 🟢🟡🔴 |
| [Week -2] | — | — | — | 🟢🟡🔴 |
| [Week -1] | — | — | — | 🟢🟡🔴 |
| This Week | — | — | — | 🟢🟡🔴 |

**Overall Status:** 🟢 On track / 🟡 Watch / 🔴 Escalate to Todd now

---

## New Team Member Training

*Use this to onboard anyone new to TourOps RUN operations. Complete enough that Todd is not needed.*

### Step 1 — System Orientation (Day 1, ~2 hours)

1. Read `system/canonical_schema.md` — understand all canonical fields, especially `tourops_work_state`, `tourops_intent_bucket`, `tourops_outcome`. Pay attention to allowed enum values — case-sensitive. *(45 min)*
2. Read `operators/barley_bus.md` — understand what Hope is allowed to do and what triggers escalation. *(30 min)*
3. Read `operations/escalation_playbook.md` — understand the full escalation lifecycle. *(20 min)*
4. Read `operations/quality.md` — memorize the 6 categories and critical failure triggers. *(20 min)*

**Checkpoint — can you answer these without looking?**
- What field controls AI suppression? (`tourops_work_state`)
- What are the 7 intent buckets?
- What triggers an auto-score of 1 in Escalation Logic?
- What does an operator do when they receive a GHL task?

### Step 2 — QA Scoring Practice (Day 2, ~2 hours)

1. Pull 5 historical conversation transcripts from GHL (ask Mike for access to BB test calls)
2. Score each using `operations/quality.md` — all 6 categories
3. Compare your scores to Mike's scores for the same calls
4. Discuss any deltas > 0.5 with Mike
5. Repeat with 5 more calls until your average delta is ≤ 0.3

**Pass Criteria:** ≤ 0.3 average delta from Mike's scores across 10 calls.

### Step 3 — GHL Navigation (Day 2–3, ~1 hour)

1. Log into GHL. Locate Barley Bus sub-account.
2. Filter contacts by `tourops_work_state = HUMAN_ACTIVE`. Understand what you're seeing.
3. Open a contact. Find: `tourops_intent_bucket`, `tourops_outcome`, `tourops_last_score`.
4. Open a completed GHL task. Understand the title format: `TOUROPS — {Intent} — {Summary}`.
5. Practice completing a test task (Mike will set one up). Verify `work_state` resets to `AI_ACTIVE` after.

### Step 4 — Escalation Handling Shadow (Day 3–5, ~3 days)

1. Shadow Mike on 5 escalation callbacks (listen only)
2. Review transcript before each call, score the AI conversation, then observe the human resolution
3. Handle 3 callbacks with Mike on the line (Human Request / Standard tier only — not P0/P0b)
4. Handle 5 callbacks independently with Mike reviewing after

**Pass Criteria:** Mike signs off: "Ready to handle Human Request and Standard escalations independently."

### Step 5 — Weekly QA Review Shadow (First Wednesday)

1. Shadow Mike through one full Wednesday QA review
2. Run the following week's QA review independently with Mike reviewing output
3. Mike compares your Weekly Review to what he would have written — flag deltas

**Pass Criteria:** Mike signs off: "Weekly review output meets standard."

### Required Knowledge Before Operating Independently

- [ ] All 6 QA categories and critical failure triggers (memorized)
- [ ] All 7 intent buckets and their corresponding script plays
- [ ] Escalation priority ladder and SLAs
- [ ] How to filter GHL by `tourops_work_state`
- [ ] How to complete a GHL task and verify work_state reset
- [ ] What NOT to say on P0/P0b calls (no fault admission, no policy discussion)
- [ ] When to escalate to Todd vs. handle independently
- [ ] What OP_Profile.md is and why agent persona lives there (not in Platform prompts)

### What You Should Never Do

- Complete a GHL task before the customer issue is actually resolved
- Handle P0 or P0b without notifying Todd first
- Score a conversation without reading/listening to the full transcript
- Log something in the issues log on the first occurrence — wait for recurrence
- Tell a customer you'll have someone call them by a specific time (no SLA promises)
- Modify any canonical fields (`tourops_*`) manually — let the system handle it
- Reference an agent by name in customer communications unless the operator's OP_Profile.md has confirmed the agent name for that deployment
