# TourOps — Build Backlog & Product Gap Tracker

**Last Updated:** 2026-03-02
**Owner:** Todd Abrams
**KPI Linkage Rule:** Every P1 item must state the KPI it impacts. No KPI = P3 or removed.
**WIP Rule:** No more than 3 active P1 items at once.
**Hygiene Rule:** Items in Planned >90 days without progress → moved to P3 or removed at monthly health check.
**Gap Rule:** If a feature is not ✅ Live, it cannot be sold as included. No exceptions.
**Consolidated from:** TO_Build_Backlog.md, TO_Product_Gap_Tracker.md

---

# Part 1 — Build Backlog

## Active P1 Count: 0/3

## P1 — Critical Priority

| Feature | Problem Solved | KPI Impact | Owner | Status | Target |
|---------|---------------|------------|-------|--------|--------|
| Barley Bus → Schema Contract 3 Migration | BB running legacy prompt (pre-Schema v2). Grader fields, narrative memory, and work_state controls not aligned with current contract. Creates schema drift risk as new operators onboard on Contract 3. | Voice AI Quality Score | Todd | Planned | 2026-03-03 |

## P2 — Important

| Feature | Problem Solved | KPI Impact | Owner | Status | Target |
|---------|---------------|------------|-------|--------|--------|
| Automated Regression Harness (Conv AI API) | Manual SMS/WebChat regression testing takes ~3 hours. Automation cuts to ~20 min. | Quality Score | Mike | Planned | Q3 2026 |
| Founder Cohort Operator #1 Deployment | First non-BB operator. Validates multi-operator model end-to-end. Data infrastructure inherited from reusable n8n template — per-operator setup under 20 minutes. | Call-to-Book Rate | Todd | Planned | Q2 2026 |
| Conversation AI Module Expansion — CORP | Corporate/B2B intent currently routes to escalation. Dedicated CORP module handles W-9, invoice, and group inquiry flows before handoff. | Escalation Rate | Mike | Planned | Q3 2026 |
| OP_Profile.md for all active operators | BB and live operators need persona overlay files created and confirmed. Agent_Name injected correctly, not hardcoded. | Deployment Consistency | Mike | In Progress | 2026-03-03 |

## P3 — Backlog / Future

| Feature | Problem Solved | KPI Impact | Owner | Status | Target |
|---------|---------------|------------|-------|--------|--------|
| Real-time availability check via webhook | Voice AI cannot confirm tour availability. Requires external API integration. | Call-to-Book Rate | Todd | Planned | FLAG NEEDED |
| Operator-level QA dashboard (Sheets → GHL) | QA scores tracked in Google Sheets. GHL-native view reduces ops friction. | Quality Score | Mike | Planned | Q4 2026 |
| Schema Contract 4 planning | Contract 4 may add multi-location, multi-tour-type, or revenue attribution fields. | TBD | Todd | Planned | Q4 2026 |
| Voice AI → Conversation AI handoff flow | Caller converts to SMS mid-conversation — no warm handoff between channels. | SMS Engagement Rate | Mike | Planned | Q3 2026 |

## Completed

| Feature | Completed | KPI Impact | Result |
|---------|-----------|------------|--------|
| n8n Reusable Template — GHL → Airtable | 2026-02-28 | Deployment Velocity | Per-operator data infra setup under 20 minutes. Operator name as variable. |
| Platform name-agnostic refactor (OP_Profile.md) | 2026-02-26 | Deployment Consistency | Agent persona removed from all Platform files. OP_Profile.md template created. |
| Schema Contract 3 — QA Grader Fields | 2026-02-22 | Quality Score | tourops_last_score, tourops_last_review_date, tourops_issue_count added |
| Narrative Memory Fields | 2026-02-17 | Quality Score / Context Awareness | Cross-channel memory enabled |
| GHL Auto-Summaries Integration | 2026-02-17 | Context Awareness | Conversation AI session summaries to contact notes |
| VAI Grader Workflow v1.0 | 2026-02-22 | Quality Score | Automated per-call scoring deployed |
| CAI Grader Workflow v1.0 | 2026-02-22 | Quality Score | Automated per-session scoring deployed |
| Voice Master Snapshot v1.2 | 2026-02-17 | Deployment Speed | Authoritative build guide supersedes v1.1 |
| Prompt Compiler v1.1 | 2026-02-17 | Deployment Consistency | Operator-specific prompt generation standardized |
| Voice AI Regression Test Suite v1.0 | 2026-02-14 | Quality Score | 19 RACE-format tests, 19/19 required to deploy |
| Canonical Schema Contract 2 | 2026-02-14 | All KPIs | work_state as authoritative control, lifecycle-aware model |

## FLAGS NEEDED — Blocked on Todd

| Item | What's Needed | Flagged |
|------|--------------|---------|
| Real-time availability API | Which booking system? What endpoint? Rate limits? | 2026-02-24 |
| Schema Contract 4 scope | What business problem does it solve? What KPI? | 2026-02-24 |

---

# Part 2 — Product Gap Tracker

What's promised at each pricing tier vs. what's actually built. Filter to ✅ Live only when writing sales materials.

## Readiness Summary

| Tier | Promised | Live | Partial | Not Started | Readiness |
|------|----------|------|---------|-------------|-----------|
| Tier 1 — Launch ($297) | 22 | 13 | 2 | 7 | 🟡 ~59% |
| Tier 2 — Growth ($497) | 18 | 1 | 3 | 14 | 🔴 ~11% |
| Tier 3 — Scale ($897) | 14 | 0 | 2 | 12 | 🔴 ~7% |

## Tier 1 — Launch ($297/mo)

### AI Communication Engine
| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 1.1 | Voice AI answering and qualifying inbound calls | ✅ Live | Hope V5.0, 8-intent routing, 6 KBs | Live |
| 1.2 | Conversation AI handling SMS, chat, web 24/7 | ✅ Live | Router + 8-module architecture | Live |
| 1.3 | AI configured with operator-specific tour info | ✅ Live | 6 KBs for BB. Prompt Compiler v1.1 ready. | Live |
| 1.4 | Missed-call textback | ✅ Live | GHL native | Live |

### Unified Operations
| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 1.5 | Unified inbox (calls, SMS, email, web chat, social DMs) | ✅ Live | GHL native | Live |
| 1.6 | Tour-operator CRM with pipeline stages | ✅ Live | GHL native, customizable per operator | Live |
| 1.7 | 72-hour follow-up enforcement | 🔴 Not Started | Pipeline stages exist but no time-based enforcement workflow | Q2 2026 |
| 1.8 | AI-to-human handoff via GHL | ✅ Live | Task Completed workflow + work_state control active | Live |
| 1.9 | Pre-built inquiry and feedback forms | 🟡 Partial | GHL forms exist. No standardized TourOps templates. | Q2 2026 |
| 1.10 | Basic private/group inquiry visibility | 🟡 Partial | Pipeline stage exists. CORP module routes to escalation only. | Q3 2026 |

### Operator Scorecard
| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 1.11 | Weekly scorecard email (Monday 8am) | 🔴 Not Started | v0 = Mike sends manually from GHL + Sheets | v0: now. v1: Q2 2026 |
| 1.12 | Inquiry coverage % | 🔴 Not Started | No metric calculation built | Q2 2026 |
| 1.13 | After-hours coverage | 🔴 Not Started | No time-of-day classification | Q2 2026 |
| 1.14 | Conversations & actions (booking links sent, consultations) | 🟡 Partial | GHL tracks counts. Booking links not tracked discretely. | Q2 2026 |
| 1.15 | Estimated Revenue Protected calculation | 🔴 Not Started | Formula defined. Needs operator inputs + workflow. | Q2 2026 |
| 1.16 | Staff hours absorbed | 🔴 Not Started | Blocked by scorecard infrastructure | Blocked by 1.11 |
| 1.17 | Investment vs. impact ratio | 🔴 Not Started | Dependent on Revenue Protected calc | Blocked by 1.15 |
| 1.18 | "Top 3 Conversations You Would Have Missed" | 🔴 Not Started | Requires after-hours classification + snippet extraction | Blocked by 1.13 |

### Messaging & Compliance
| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 1.19 | Reactive-only messaging enforcement | ✅ Live | GHL sub-account settings. Config during onboarding. | Live |
| 1.20 | Usage caps (300 voice min, 500 SMS, 2,500 contacts) | ✅ Live | GHL native | Live |
| 1.21 | Overage alerting | ✅ Live | GHL native | Live |
| 1.22 | Compliance defaults (STOP/HELP, opt-out, consent) | ✅ Live | GHL native defaults. A2P registration documented. | Live |

## Tier 2 — Growth ($497/mo)

*Everything in Tier 1, plus:*

| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 2.1 | Booking events feed into CRM | 🔴 Not Started | No webhook/API with FareHarbor, Peek, or Xola | FLAG NEEDED |
| 2.2 | Events trigger automations | 🔴 Not Started | Blocked by 2.1 | Blocked by 2.1 |
| 2.3 | Source attribution (OTA vs. direct vs. referral) | 🔴 Not Started | Requires booking integration | Blocked by 2.1 |
| 2.4 | Post-tour review requests | 🔴 Not Started | No review automation built | Q4 2026 |
| 2.5 | Negative feedback interception | 🔴 Not Started | Blocked by 2.4 | Blocked by 2.4 |
| 2.6 | Reputation dashboard | 🔴 Not Started | Blocked by 2.4 | 2027 |
| 2.7 | Upsell automation | 🔴 Not Started | Requires booking integration | Blocked by 2.1 |
| 2.8 | Reactivation campaigns | 🔴 Not Started | Requires booking data + proactive messaging | Blocked by 2.1 |
| 2.9 | Referral program | 🔴 Not Started | No referral infrastructure | 2027 |
| 2.10 | Abandoned inquiry recovery sequences | 🔴 Not Started | Can be built on GHL without booking integration | Q3 2026 |
| 2.11 | Dedicated group intake form | 🟡 Partial | GHL forms exist. No standardized template. | Q2 2026 |
| 2.12 | Group follow-up sequences with SLA enforcement | 🔴 Not Started | Same gap as 1.7 for group pipeline | Q3 2026 |
| 2.13 | CORP module | 🔴 Not Started | Currently routes to escalation. Dedicated module planned. | Q3 2026 |
| 2.14 | GHL payment/invoice links for deposits | 🟡 Partial | GHL native. Not configured for TourOps. | Q2 2026 |
| 2.15 | Lead form integration | ✅ Live | GHL native. Opt-in language needs standardization. | Live |
| 2.16 | Full Value Dashboard | 🔴 Not Started | Requires booking integration | Blocked by 2.1 |
| 2.17 | Proactive messaging | 🟡 Partial | GHL handles caps. Compliance review workflow not built. | Q3 2026 |
| 2.18 | Monthly detailed impact report | 🔴 Not Started | Requires scorecard + booking data | Blocked by 1.11 + 2.1 |

## Tier 3 — Scale ($897/mo)

*Everything in Tier 2, plus:*

| # | Feature | Status | Notes | Target |
|---|---------|--------|-------|--------|
| 3.1 | Bidirectional booking system sync | 🔴 Not Started | Major engineering effort | 2027 |
| 3.2 | Corporate proposal and contract templates | 🔴 Not Started | No automation | 2027 |
| 3.3 | Automated corporate follow-up cadences | 🔴 Not Started | Blocked by 2.13 | 2027 |
| 3.4 | Group-specific pricing and deposit workflows | 🔴 Not Started | Blocked by 2.14 | 2027 |
| 3.5 | Multi-location management | 🔴 Not Started | Schema Contract 4 may include multi-location fields | 2027 |
| 3.6 | Full GHL workflow builder access for operators | 🔴 Not Started | Governance question unresolved | 2027 |
| 3.7 | Call intelligence (transcription, categorization) | 🔴 Not Started | Voice AI transcripts exist. No analytics layer. | 2027 |
| 3.8 | Network benchmarking (cross-operator) | 🔴 Not Started | Requires multiple operators generating data | 2027+ |
| 3.9 | Guide coordination workflows | 🔴 Not Started | Scoped as beta. Not on roadmap. | 2027 |
| 3.10 | Dedicated success manager + QBRs | 🔴 Not Started | Hiring decision | When revenue supports |
| 3.11 | Priority support (under 4 hours) | 🔴 Not Started | Hiring decision | When revenue supports |
| 3.12 | White-label branded communications | 🟡 Partial | GHL supports it. Not configured for TourOps. | Q4 2026 |
| 3.13 | Custom API access | 🔴 Not Started | No API layer built | 2027+ |
| 3.14 | High-volume messaging (10K SMS, 3K voice) | 🟡 Partial | GHL native. Abuse monitoring not built. | Q4 2026 |

## Critical Path — What to Build First

| Priority | Feature(s) | Why First | Effort | Target |
|----------|-----------|-----------|--------|--------|
| **P0** | Operator Scorecard v0 (1.11–1.18) | Retention engine. Without it, operators can't see value. v0 = Mike sends manually Monday from GHL + Sheets. | v0: Low. v1: Med-High. | v0: now. v1: Q2 2026 |
| **P1** | 72-hour follow-up enforcement (1.7) | Conversion engine. Differentiates TourOps from "just an AI answering service." | Medium | This week |
| **P2** | Standardized onboarding templates (1.9, 2.11) | Speed to deploy new operators. Founding cohort depends on this. | Low-Med | This week |
| **P3** | Booking system integration one-way (2.1) | Unlocks entire Tier 2. Single biggest feature dependency. | High | Q3–Q4 2026 |
| **P4** | Review automation (2.4) | Strongest natural upsell trigger Tier 1 → Tier 2. | Medium | Q4 2026 |

## Dependencies Map

```
Scorecard (1.11) ──► Revenue Protected (1.15) ──► Investment vs. Impact (1.17)
       ├──► Staff Hours (1.16)
       ├──► After-Hours Classification (1.13) ──► Top 3 Missed (1.18)
       └──► Upgrade Triggers

Booking Integration (2.1) ──► Source Attribution (2.3)
       ├──► Event Automations (2.2) ──► Upsell (2.7) + Reactivation (2.8)
       ├──► Full Value Dashboard (2.16)
       └──► Bidirectional Sync (3.1)

CORP Module (2.13) ──► Corporate Follow-Up (3.3)
       └──► Group Pricing Workflows (3.4)
```
