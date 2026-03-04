# TO_Run_Escalation_Playbook.md

**Last Updated:** 2026-02-26
**Owner:** Mike
**Source:** TourOps_Escalation_Playbook_v2.md (r02) — canonical escalation rules. This file translates those rules into RUN-level operational playbooks.

---

## Escalation Priority Ladder

| Priority | Trigger | Response Time | Handler |
|----------|---------|--------------|---------|
| **P0 — Safety/Emergency** | Injury, crash, accident, ambulance, 911, police (active), assault, harassment (active), emergency, threat | 15 min max | Mike → Todd immediately |
| **P0b — Legal** | Attorney, lawsuit, claim | 30 min max | Mike → Todd immediately |
| **DayOf — Ops Urgent** | Tour is today, bus isn't here, running late, dispatch required | 5 min max | Mike / Tim |
| **Human Request / Fallback** | Caller asked for human, AI hit 3-exchange confidence limit | 30 min | Mike / Tim |
| **Standard** | Corporate lead, refund/cancel edge case, out-of-scope beyond KB | Same business day | Mike / Tim |

**Priority Rule:** Safety > DayOf > Human Request > Standard. If multiple escalations exist for one contact, highest priority wins. Only one escalation tier active at a time (Single Active Escalation Rule).

---

## Escalation Triggers (From AI System)

The following are non-negotiable escalation triggers. If the Primary Voice Agent fails to escalate any of these, it is a Critical Failure (auto-score 1).

**Immediate (P0):** Police, lawsuit, injury, crash, ambulance, assault, harassment, DUI, emergency, threat
**Immediate (P0b):** Attorney, lawsuit, claim
**DayOf:** Any urgency marker + unresolved by KB ("bus isn't here," "running late," "tour is in 20 min")
**Human Request:** Explicit "let me talk to someone" / "I need a human"
**Confidence Fallback:** 3 exchanges on voice without confident classification

---

## SLA Monitoring Loops (Automated — GHL Workflows)

For P0, P0b, and DayOf, GHL automatically re-notifies handlers if task is not completed:

| Category | First Re-notify | Owner/Manager Escalation | Repeat |
|----------|----------------|--------------------------|--------|
| P0 Safety | 10 min | 20 min | Every 15 min |
| P0b Legal | 20 min | 40 min | Every 20 min |
| DayOf | 5 min | 15 min | Every 10 min |

Loop stops when `tourops_work_state` changes to `AI_ACTIVE` (task completed). Standard escalations have no monitoring loop — handled via daily 9 AM review.

---

## Operator Actions by Category

### P0 — Safety/Emergency

1. Read full transcript immediately
2. If injury/police/legal → **notify Todd immediately** (do not wait to investigate)
3. Call customer from personal phone (not system number)
4. Resolve or coordinate with emergency services
5. Complete GHL task

**Script:** *"Hi [Name], this is [Staff] from [Company]. I saw your message about [incident]. I want to make sure you're okay and understand what happened."*

**NEVER:** Admit fault, discuss policy in detail, give legal opinions.

---

### P0b — Legal

1. Read transcript
2. Notify Todd immediately — do NOT handle without Todd awareness
3. Gather facts only (what happened, when, who)
4. Do not offer resolution without Todd approval
5. Complete task after Todd directs

**Script:** *"Hi [Name], this is [Staff] from [Company]. I understand you have a concern about [topic]. I want to make sure this gets to the right person — can you walk me through what happened?"*

---

### DayOf — Operational Urgency

1. Read transcript — identify the operational issue (bus location, meeting point, late arrival)
2. Contact dispatch, driver, or venue immediately
3. Call or text customer with resolution within 5 minutes
4. Complete task

**Script:** *"Hi [Name], this is [Staff] from [Company]. I got your message about [issue]. Let me get this sorted out right now."*

---

### Human Request / Confidence Fallback

1. Read transcript — understand what the AI couldn't resolve
2. Call or text customer to complete what the AI started
3. If booking: confirm details and send booking link manually if needed
4. Complete task

**Script:** *"Hi [Name], this is [Staff] from [Company]. Our assistant flagged that you needed some help — I'm here to take care of that for you."*

---

### Standard (Corporate / Refund / Edge Case)

Standard escalations now arrive in two forms — check the contact before calling:

**Pre-Scheduled (AwaitScheduledCall):** Customer already picked a time via scheduling link. Check the calendar for the scheduled slot. Show up prepared with the transcript context.

**ASAP (AwaitHumanFollowUp):** Customer declined scheduling. Respond same business day.

1. Read transcript — know the issue before you reach out
2. If scheduled → show up at the booked time ready to resolve
3. If ASAP → call or text customer same business day
4. Handle per policy or route to Todd for policy exception
5. Complete task

---

## Task Closure — Operator Rules

**Operators do one thing: complete the GHL task.**

The system handles all of the following automatically upon task completion:
- `tourops_work_state` → `AI_ACTIVE`
- `tourops_handoff_active` → `false`
- `tourops_outcome` → `Resolved`
- `tourops_next_best_action` → `NoFurtherAction`
- `Human handover` tag removed

**Verify after task completion:** Check that `tourops_work_state` has reset to `AI_ACTIVE`. If it hasn't within 2 minutes, notify Mike.

---

## Escalation Levels (RUN → LEAD)

### Level 1 — Internal RUN Escalation

**Who:** Mike → Tim or Todd (GHL internal chat)
**When:** P0/P0b triggers, critical failure on live call, quality score 🔴, 2+ leading indicators 🟡 same week
**Response:** Immediate (P0/P0b) or same day (quality)

### Level 2 — LEAD Escalation

**Who:** Mike → Todd (GHL internal chat + follow-up)
**When:** Quality KPI 🔴 for 2+ consecutive weeks, 3+ occurrences of same issue, recurring critical failures, grader accuracy breakdown
**Response:** Next business day minimum — Todd sets strategic direction

---

## Daily Escalation Review Checklist (9:00 AM)

- [ ] Filter GHL by `tourops_work_state = HUMAN_ACTIVE`
- [ ] Identify any contacts past SLA
- [ ] Prioritize by category (Safety > DayOf > Human Request > Standard)
- [ ] Handle all overdue items first
- [ ] Assign any unassigned tasks to Mike or Tim
- [ ] Log any recurring patterns (3+ same trigger = KB gap — flag in Issues_Log)

---

## SLA Table

| Issue Type | Response Time | Resolution Time |
|-----------|--------------|-----------------|
| P0 Safety | Immediate | 15 min |
| P0b Legal | Immediate | 30 min |
| DayOf | 5 min | Resolved before tour time |
| Human Request | 30 min | Same business day |
| Standard — Scheduled | Show up at booked time | At booked appointment |
| Standard — ASAP | Same business day | 2 business days |
| QA Critical Failure (live call) | 1 hour | Fix/rollback same day |
