# Smith Asset Group — Project Handoff
**Date:** May 12, 2026
**Project:** Sandy Roofing Pros — SLC Metro Digital Real Estate Pilot
**Handoff from:** Claude (Cowork) session covering ~3 weeks of build work
**Purpose:** Give a new Claude session everything it needs to continue without asking clarifying questions

---

## WHO WE ARE

**Smith Asset Group** is a digital real estate / lead generation business. The model: build hyper-local service websites, generate homeowner leads via Google Ads and SEO, deliver those leads to local contractors on a free trial, then close them on a $1K/month exclusive territory retainer.

**The Pilot:** Roofing leads in Sandy, Utah (SLC metro). First market. 4-week sprint.

**Team:**
- **Jackson** (you) — Strategy, Google Ads, Stripe, CRM/Notion, lead handling, overall operations
- **Sarah** — Website tech: Astro build, GitHub deploy, pixel install, QA
- **Noah** — Sales: contractor research, outreach calls, free trial delivery, closing

**The 10-Step Playbook:**
1. Market Selection ✅
2. Demand Validation ✅
3. Website Build ✅
4. Build BO List (10 contractors) ✅
5. Outreach — get BO committed 🔴 IN PROGRESS (Noah)
6. Launch Ads ⚠️ PARTIAL (Google Ads live but blocked on advertiser verification)
7. Evaluate Ads (~$100 spend) ⏳ PENDING
8. Handle Leads ⏳ READY — waiting on first lead from ads
9. Free Trial ❌ NOT STARTED
10. Close BO on Retainer ❌ NOT STARTED

**Critical path right now:** Noah lands one committed contractor → Google Ads verification clears → ads run → first lead → deliver to contractor → close on retainer.

---

## LIVE INFRASTRUCTURE

### Website
- **URL:** https://sandyroofingpros.com
- **Framework:** Astro (static site)
- **Hosting:** GitHub Pages (free)
- **Repo:** https://github.com/JSmitty37/sandyroofingpros.com (public)
- **Local path:** `C:\Users\jacks\OneDrive\Documents\Claude\Projects\Project Launch- SLC Metro Roofing (1)\`
- **Pages live (14):**
  - `/` — Homepage (has lead form)
  - `/services`, `/service-area`, `/contact`, `/faq`, `/insurance-claims`
  - `/areas/draper`, `/areas/south-jordan`, `/areas/murray`, `/areas/midvale`, `/areas/west-jordan`, `/areas/salt-lake-city`
  - `/blog/roof-repair-cost-utah`, `/blog/how-to-spot-storm-damage`
- **Phone on site:** (801) 514-7004 (CallRail — status unknown, see Open Issues)
- **Brand:** Navy + white, clean/professional, local trust
- **Schema:** RoofingContractor JSON-LD in BaseLayout.astro, Article + BreadcrumbList on blog pages
- **GSC:** Connected ✅, sitemap submitted ✅
- **Google site verification token:** BN57UIDtesbzlqyobU6Uq9o5PECz1ZjLu79a2T_N8KI
- **Google Ads tag:** AW-18149105122 (gtag.js in BaseLayout.astro)
- **Conversion label:** Y9Y7CMiv6qkcEOK7lc5D
- **Meta Pixel:** 1498618978558062 (installed, campaign paused)

### Lead Form
- **Component:** `src/components/LeadForm.astro`
- **Fields:** name (text, required), phone (tel, required), email (email, optional), zipcode (text, required, pattern [0-9]{5}), service (select, required: Emergency Roof Leak Repair | Storm Damage Roof Repair | Roof Inspection | Other / Not Sure), message (textarea, optional)
- **On submit:** Promise.all fires both:
  1. Formspree POST → https://formspree.io/f/mvzdjovl (backup)
  2. Make.com webhook POST → https://hook.us2.make.com/0hvtk7eovyrsp97idje1zuil4rd3bgvo (primary pipeline)
- **On success:** Fires `fbq('track', 'Lead')` and `gtag('event','conversion',{'send_to':'AW-18149105122/Y9Y7CMiv6qkcEOK7lc5D'})`

### Make.com Pipeline (LIVE ✅)
- **Org ID:** 2214094 (us2 region)
- **Scenario:** 4885026 — "Sandy Roofing — Form → Notion + Email Alert"
- **Status:** Active, runs every 15 minutes
- **Flow:**
  ```
  Module 1: Webhooks (receives form POST as {{1.value}})
       ↓
  Filter: "Skip empty payloads" — {{1.value}} Exists (added 2026-05-12, fixes auto-deactivation bug)
       ↓
  Module 4: Parse JSON → {{4.name}}, {{4.phone}}, {{4.email}}, {{4.zipcode}}, {{4.service}}, {{4.message}}
       ↓
  Module 5: HTTP POST → https://api.anthropic.com/v1/messages
             Model: claude-haiku-4-5-20251001, max_tokens: 400
             Connection: "Anthropic Claude" (API Key Auth, x-api-key header)
             Additional header: anthropic-version: 2023-06-01
             Response path: {{5.data.content[1].text}} (JSON string)
       ↓
  Module 2: Notion — Create a Data Source Item (14 fields, DB: 8bc8b705-8629-4b17-ac80-f84adce107a8)
       ↓
  Module 3: Gmail — Send alert to jacksonrsmith@gmail.com
  ```
- **⚠️ CRITICAL:** Do NOT open and save the Notion module panel in Make.com UI. It will strip 3 fields (Contractor Note, Red Flags, Urgency Score) that aren't in Make's schema cache. Edit Notion module via blueprint import only.

### Notion Command Center (LIVE ✅)
- **URL:** https://www.notion.so/34ad9bd2b6bd81aab10bc2e7124cb3c7
- **Databases & IDs:**

| Database | Page/DB ID | Collection ID |
|---|---|---|
| Week 1 Dashboard (page) | 34ad9bd2-b6bd-8109-8360-da0717763fe5 | — |
| Live Leads DB | 8bc8b705-8629-4b17-ac80-f84adce107a8 | c5b21c2d-6b81-4002-828b-c36f6e079b68 |
| Partner Directory DB | 24f3a86e-c101-4d49-8a2a-d062d9d6a19b | d75e12d8-edf0-4ecf-bebd-012321bd31d6 |
| Ad Metrics DB | 47d3c105-4ffa-4a9e-8455-66a4c1c3c355 | e9f67945-aefb-45c4-bd56-07a0ce809808 |
| Finances & P&L DB | 8458dc3f-6b78-4f3c-9b42-b5dd143ecdfa | 2c20968b-ff84-4af6-af7b-4adad58db0e4 |
| Expansion Pipeline (page) | 34ad9bd2-b6bd-8112-bd00-db8aaba68295 | — |

- **Live Leads DB properties (14 fields):**

| Property | Notion Short ID | Type | Values |
|---|---|---|---|
| Name | title | Title | Lead full name |
| Phone | L_Je | Phone | |
| Message | uuvI | Rich Text | |
| Source | Qm}q | Select | Form Submission |
| Status | S<If | Select | 🆕 New |
| Service | ^XX^ | Select | Emergency Roof Leak Repair, Storm Damage Roof Repair, Roof Inspection, Other / Not Sure |
| Zip Code | i@:j | Rich Text | |
| Lead Grade | b;hi | Select | A Hot, B Warm, C Cool, D Cold |
| Est. Job Value | szBn | Select | Under $1K, $1K–$3K, $3K–$8K, $8K–$15K, $15K+ |
| Territory Status | Ntk[ | Select | In Target Zone, Edge Zone, Outside Zone, Unknown |
| Recommended Action | w~>x | Select | Call Immediately, Schedule Follow-up, Monitor, Do Not Contact |
| Contractor Note | Y?~f | Rich Text | AI 1-sentence note |
| Red Flags | Hd}c | Rich Text | |
| Urgency Score | j}t` | Number | 1–5 |

- **Notion update protocol:** Claude should update the Command Center autonomously as work progresses. Jackson does not want to manage Notion himself.

### Google Ads
- **Conversion ID:** AW-18149105122
- **Conversion Label:** Y9Y7CMiv6qkcEOK7lc5D
- **Account status:** ⚠️ Advertiser verification PENDING (requires LLC + D&B DUNS)
- **Campaign:** Roofing — Sandy UT
- **Budget:** $30/day
- **Bid strategy:** Maximize Clicks (must switch to Target CPA after 30+ conversions)
- **Location:** Sandy, UT 15-mile radius (fixed from US-wide — this was the root cause of spam leads)
- **Active ad group:** General Roofing (1 RSA with 10 headlines, 4 descriptions)
- **Blocked ad groups:** Emergency, Insurance/Storm (drafted, cannot launch until verification clears)
- **Extensions:** Call (801) 514-7004, 4 sitelinks, callouts, structured snippets
- **Keywords:** All converted to phrase match. ~18 active keywords across emergency, general, insurance/storm intent.
- **Conversion tracking:** Installed via gtag in BaseLayout.astro ✅

### Connected Services

| Service | ID / Account | Status |
|---|---|---|
| Google Workspace | @sandyroofingpros.com (jackson@, sarah@, noah@) | Live ✅ |
| GitHub | JSmitty37 | Live ✅ |
| Make.com | Org 2214094 | Live ✅ |
| Anthropic API | Connected in Make.com as "Anthropic Claude" (sk-ant-...) | Live ✅ |
| Notion | Command Center workspace | Live ✅ |
| Google Search Console | sandyroofingpros.com verified | Live ✅ |
| Formspree | mvzdjovl | Live ✅ |
| Google Ads | AW-18149105122 | Live, verification pending ⚠️ |
| Meta Ads | act=1712322076878327 | Paused ⏸️ |
| Meta Pixel | 1498618978558062 | Installed, campaign paused |
| CallRail | (801) 514-7004 | Trial ended May 7 — status UNKNOWN ⚠️ |
| Stripe | Account created | ID verification incomplete ❌ |
| Google Analytics 4 | — | Not installed ❌ |
| Google Business Profile | — | Not created ❌ |

---

## WHAT WAS BUILT IN THESE SESSIONS

### Site & SEO
- Full 14-page Astro site built and deployed to GitHub Pages
- Full SEO overhaul: RoofingContractor schema, sitemap (all pages), OG tags, keyword-first title tags, internal nav links, area city pages (Murray, Midvale, West Jordan, SLC), blog posts
- Trust signals added to homepage (stats bar, badge, review placeholders)
- OG social card image deployed
- GSC verified and sitemap submitted

### Make.com Pipeline
- Scenario 4885026 built: Webhooks → JSON Parse → Claude AI scoring (HTTP) → Notion → Gmail
- AI lead scoring module added using claude-haiku-4-5-20251001 via Anthropic API
- 14-field Notion mapper implemented via blueprint import (including 3 AI score fields Make.com UI can't see)
- Empty payload filter added (2026-05-12) — fixes the auto-deactivation bug from polling empty webhook queue
- Scenario reactivated and confirmed live

### Google Ads
- Full account audit completed (report in project folder)
- Location targeting fixed (US → Sandy UT 15-mile radius)
- RSA expanded to 10 headlines, 4 descriptions, display paths
- All extensions added (call, 4 sitelinks, callouts, structured snippets)
- Keywords converted to phrase match, dead terms paused
- Emergency and Insurance/Storm ad groups drafted (blocked on advertiser verification)

### Documents Created (in project folder)
- `smith_asset_group_agent_handoff.docx` — full technical AI agent handoff (9 sections, exact IDs and logic)
- `Sandy_Roofing_Google_Ads_Audit.docx` — complete Google Ads audit report
- `contractor_agreement.docx` — contractor service agreement template
- `claude_lead_scoring_setup.docx` — Make.com setup guide for Claude AI scoring
- `LEAD_QUALITY_SCORING_SETUP.md` — full scoring system docs
- `lead_scoring_prompt.txt` — exact system prompt used in Make.com HTTP module
- `Digital RealEstate SOPs/` — full SOP library (9 documents)

---

## OPEN ISSUES & BLOCKERS

### 🔴 Jackson Must Do (Blocking Revenue)
1. **Google Ads advertiser verification** — Requires LLC formation + D&B DUNS number. Until this clears, Emergency and Insurance/Storm ad groups cannot go live. This is the #1 ads blocker.
2. **CallRail decision** — Trial ended ~May 7. Phone (801) 514-7004 is on the site everywhere. If the trial lapsed, all inbound calls are dead. Check callrail.com immediately and confirm or replace the number.
3. **Stripe ID verification** — Account created but incomplete. Cannot receive retainer payment even if Noah closes first contractor. Complete this before Noah's first close call.

### 🟡 Noah Must Do (Blocking Revenue)
4. **Land first committed contractor** — Noah is in active outreach (Step 5). He does NOT call until Jackson texts: **"Pipeline is live. First lead is in the sheet. Go."**
   - Call priority: John Panos (Utah Roofing Pros) (801) 688-3853 → Brent Yorgason (AMCO) (801) 269-1276 → Bennett Sorensen (Alta Roofing) (385) 450-7663

### 🟡 Technical Open Loops
5. **Notion select option naming mismatch** — AI returns plain text (e.g. "A Hot") but Notion options may have emoji prefixes (e.g. "A - Hot 🔥"). Check the Live Leads DB. If mismatched, either rename Notion options to plain text OR add if() mapping in Make.com mapper.
6. **Google Analytics 4 not installed** — Required for Smart Bidding once 30+ conversions accumulate. Install GA4, link to Google Ads.
7. **Google Business Profile not created** — Single highest-leverage remaining SEO move. Creates Map Pack eligibility. Create at business.google.com.
8. **Make.com automations not yet built:**
   - Lead → Noah SMS (Grade A/B trigger)
   - Lead → Contractor SMS (auto-route without Jackson middleman)
   - Daily Google Ads stats → Notion Ad Metrics DB
   - 24hr homeowner follow-up SMS
   - Contractor response tracking

---

## CURRENT MANUAL PROCESSES (what still requires human hands)
- Jackson reads Gmail alert → manually texts Noah with lead details
- Noah manually contacts assigned contractor
- Jackson manually updates Notion Status after routing a lead
- Jackson manually pulls Google Ads stats and logs to Notion
- Jackson manually follows up with homeowner 24hrs after lead
- Noah manually tracks contractor response time and close rate (not logged in Notion)
- Jackson manually creates Stripe invoice when Noah closes a contractor

---

## BUSINESS LOGIC

### CPL Kill Rules
- CPL < $25 → Hold or scale to $25/day
- CPL $25–$50 → Acceptable, test new creative
- CPL > $50 or 0 leads after $100 spend → Kill ad set, test new copy

### Lead Scoring (Claude AI via Make.com)
**Grades:** A Hot | B Warm | C Cool | D Cold
**Urgency:** 1–5 (5 = active leak right now, 1 = vague/no info)
**Target ZIPs:** 84070, 84094, 84093, 84092, 84095, 84096, 84047, 84121
**Edge ZIPs:** 84084, 84088, 84065, 84020
**Recommended Action:** Call Immediately (A/high-B) | Schedule Follow-up (B/strong-C) | Monitor (C) | Do Not Contact (D)

### Contractor Retainer Model
- Free trial: 2–3 leads delivered, no money
- Close trigger: Contractor closes 1 job OR gives 2+ estimates
- Retainer price: $1,000/month, exclusive territory
- Contract: `contractor_agreement.docx` in project folder

### AI Agent Decision (from last session)
Decided to build **one unified orchestrator agent** (not separate agents per domain) because the pipeline is too tightly coupled at this stage. Recommended approach:
- Use Claude Console Workbench to design system prompt and tool definitions
- Execute via Make.com HTTP modules (extending existing Scenario 4885026 pattern)
- Use Claude Code if Make.com hits its limits

Full technical spec is in `smith_asset_group_agent_handoff.docx`.

---

## HOW TO CONTINUE

**To pick up ads work:**
> "I'm running a roofing lead gen pilot in Sandy, UT at sandyroofingpros.com. Google Ads account ID AW-18149105122. Advertiser verification is pending (blocked on LLC + DUNS). The Emergency and Insurance/Storm ad groups are drafted but can't go live until verification clears. Help me with [your task]."

**To pick up Noah's outreach:**
> "I'm running a lead gen pilot at sandyroofingpros.com. My sales guy Noah is doing contractor outreach. First priority is John Panos at Utah Roofing Pros (801) 688-3853. Help me with [script / objection handling / follow-up]."

**To build the AI agent:**
> "I'm building an AI orchestrator agent for a roofing lead gen business. The full technical spec is in smith_asset_group_agent_handoff.docx. The agent runs via Anthropic API + Make.com. Help me build [specific automation]."

**To work on the website:**
> "I have an Astro site at sandyroofingpros.com hosted on GitHub Pages (repo: JSmitty37/sandyroofingpros.com). The site is in my project folder. Help me with [your task]."

**To update Notion:**
> Claude should update the Notion Command Center autonomously. Jackson does not want to manage Notion manually. Always update relevant DB rows when tasks are completed or status changes.

---

## FILES IN PROJECT FOLDER
`C:\Users\jacks\OneDrive\Documents\Claude\Projects\Project Launch- SLC Metro Roofing (1)\`

```
smith_asset_group_agent_handoff.docx  ← AI agent technical build spec (9 sections)
Sandy_Roofing_Google_Ads_Audit.docx   ← Full Google Ads audit
contractor_agreement.docx             ← Contractor service agreement template
claude_lead_scoring_setup.docx        ← Make.com AI scoring setup guide
LEAD_QUALITY_SCORING_SETUP.md         ← Lead scoring system documentation
lead_scoring_prompt.txt               ← Exact Claude system prompt used in Make.com
HANDOFF_NEW_CHAT.md                   ← This file
Digital RealEstate SOPs/              ← 9 SOP documents (market selection through deployment)
src/                                  ← Astro site source code
dist/                                 ← Built site (don't edit directly)
```

---

*Last updated: 2026-05-12 by Claude (Cowork session)*
*Continued from: ~3 weeks of build sessions covering full site, Make.com pipeline, Google Ads, SEO, Notion, and AI lead scoring*
