# SLC Metro Roofing — Project Handoff
**Date:** May 4, 2026  
**Status:** Ads LIVE ✅ — Pipeline LIVE ✅ — SEO Overhaul COMMITTED (needs push) ✅ — **NOW: Push SEO changes + Land first contractor**

---

## Session Wins (What Just Got Done)

### ✅ SEO Overhaul — Committed, Needs One Push to Go Live
Full SEO implementation completed on local `main` branch (commit `66e48b8`). Parented cleanly on latest origin. **Jackson needs to run `git push origin main` from the project folder to deploy.**

Changes made across 13 files:
- **Schema:** `LocalBusiness` → `RoofingContractor` across the entire site
- **Sitemap:** Expanded from 1 URL (homepage only) to all 9 pages — Google can now properly discover and crawl the full site
- **OG tags:** `og:image`, `og:image:width/height`, `og:image:alt`, `twitter:image` added sitewide; twitter card upgraded to `summary_large_image`
- **All title tags** converted to keyword-first format (biggest quick-win for CTR):
  - Homepage: `"Emergency Roof Repair Sandy, UT | Sandy Roofing Pros"`
  - Services: `"Roof Repair Services Sandy, UT | Emergency, Storm & Inspection | Sandy Roofing Pros"`
  - FAQ: `"Roofing FAQ — Sandy, UT | Roof Repair Questions Answered | Sandy Roofing Pros"`
  - Insurance Claims: `"Roof Insurance Claims Utah | Storm Damage Help | Sandy Roofing Pros"`
  - Service Area: `"Roof Repair Near Me — Sandy, Draper, South Jordan & SLC, UT | Sandy Roofing Pros"`
  - Contact: `"Contact Sandy Roofing Pros | Free Roof Estimate — Sandy, UT"`
- **Header nav:** Added Insurance Claims, FAQ, Blog links (Google crawls pages it can find via nav)
- **Footer:** Added "Resources" column with FAQ, Insurance Claims Guide, Storm Damage Guide
- **Blog post:** `Article` + `BreadcrumbList` JSON-LD schema added
- **Area pages (Draper, South Jordan):** `Service` + `BreadcrumbList` JSON-LD schema added, `&amp;` encoding bug fixed in titles
- **areaServed:** Enriched with Wikipedia `sameAs` links for all 7 cities

### ✅ Previously Completed (Prior Sessions)
- Multi-territory city/service field added to lead form
- Make.com webhook URL fixed and verified live
- Week 1 Dashboard and Notion Command Center updated for multi-territory model
- Meta Ads billing restored — campaign active at $21/day (corrected from $15/day)
- PageSpeed: 653ms load, 85ms DOMContentLoaded, 0 CLS
- Mobile QA: viewport correct, form accessible, sticky header working
- Ad metrics logged to Notion with launch context

---

## Immediate Action Items — Do These First

### 🔴 #1 — Push SEO Changes (2 minutes)
Open a terminal in your project folder and run:
```
git push origin main
```
Note: If you have VS Code or another git client open, close it first or it may hold a file lock. The push itself is unaffected by the index.lock file — only git add/commit need that cleared.

### 🔴 #2 — Submit Sitemap to Google Search Console (5 minutes)
After the push deploys:
1. Go to https://search.google.com/search-console
2. Select `sandyroofingpros.com`
3. Left sidebar → Sitemaps
4. Submit: `https://sandyroofingpros.com/sitemap.xml`

This is what actually triggers Google to crawl all 9 pages immediately. Without this, you wait weeks.

### 🔴 #3 — Create OG Social Card Image (10 minutes, use Canva)
The site now has `og:image` meta tags pointing to `/public/images/og-default.jpg`. That image doesn't exist yet. Without it, Facebook/LinkedIn/iMessage shares show no image (big trust signal missed).
- Create a 1200×630px image in Canva
- Something clean: logo + tagline + phone number or "Emergency Roof Repair — Sandy, Utah"
- Save as `og-default.jpg` and drop it in `public/images/` in your repo
- Commit and push

### 🟡 #4 — CallRail Decision (Before May 7)
Your CallRail free trial ends ~May 7. Decide before then:
- **Keep it ($45/mo):** Add a credit card to your CallRail account. Worth it if you're tracking which ads drive calls.
- **Cancel:** Redirect the CallRail number to just your cell. You lose call attribution but save the money.
- **Before canceling:** Make sure your site phone `(801) 514-7004` routes correctly if you remove CallRail.

### 🟡 #5 — Meta Campaign Lead Form Check
Still unresolved from last session: **are your ads using a native Facebook Instant Form or sending people to the website?**
- In Ads Manager → Campaigns → click your ad → look at the "Destination" field
- If it says "Instant Form" → leads go to Facebook, NOT your Notion pipeline. You'd need to integrate Meta Lead Ads → Make → Notion separately
- If it says "Website" → you're good, leads hit sandyroofingpros.com and flow through normally

---

## Full Infrastructure Status

| Component | Status | Notes |
|-----------|--------|-------|
| Live site | ✅ | https://sandyroofingpros.com |
| GitHub repo | ✅ | https://github.com/JSmitty37/sandyroofingpros.com |
| Make pipeline | ✅ Active | Form → Notion + Gmail alert |
| Notion Live Leads | ✅ | https://www.notion.so/8bc8b70586294b17ac80f84adce107a8?v=387766cb80574532a623319f31667019 |
| Formspree backup | ✅ | Form ID: mvzdjovl |
| Meta Ads | ✅ Active | act=1712322076878327, $21/day, Salt Lake County ages 30–65 |
| Site phone | ✅ | (801) 514-7004 via CallRail (trial ends ~May 7) |
| SEO changes | ⚠️ Committed locally | Run `git push origin main` to deploy |
| OG image | ❌ Missing | Create 1200×630px at `/public/images/og-default.jpg` |
| Meta Pixel | ❌ Not installed | Sarah's task — Meta optimizing on clicks, not leads until done |
| CallRail | ⚠️ Trial ending | Decide keep/cancel before May 7 |

---

## 10-Step Playbook — Current Status

| Step | Owner | Status |
|------|-------|--------|
| 1. Market Selection | Jackson | ✅ Done |
| 2. Demand Validation | Jackson | ✅ Done |
| 3. Website Built | Sarah | ✅ Done |
| 4. Build BO List (10 contractors) | Noah | ✅ Done |
| 5. Outreach — get BO committed | Noah | 🔴 **IN PROGRESS — highest priority** |
| 6. Launch Meta Ads ($21/day) | Jackson | ✅ Done |
| 7. Evaluate Ads (~$100 spend) | Jackson | ⏳ ~May 8-10 window |
| 8. Handle Leads → send to BO | Jackson | Ready — waiting on Step 5 |
| 9. Free Trial (monitor BO response) | Noah | Not started |
| 10. Close BO (monthly retainer) | Noah | Not started |

---

## Contractor Outreach (Noah) — Status

**Goal:** 1 committed contractor by end of week. One is enough to start.

**What "committed" means:**
- Verbal yes to receive leads
- Name, business name, callback phone confirmed
- Agreed to respond within 1 hour
- Info logged in Notion "Assigned Partner" field

**Outreach priority order:**
1. Contractors already paying Angi/HomeAdvisor — they're in lead-buying mode, easiest pitch
2. Contractors with weak websites or few reviews — most to gain
3. Skip: top 3-star Google Maps results — already winning organically, harder to close

**Call script (opening):**
> "Hey, is this [Name]? My name is Noah — I help run a local roofing lead site here in Sandy. Do you have like 60 seconds?"
>
> "We just launched sandyroofingpros.com and we're starting to get homeowners reaching out for estimates. We're looking to work with one or two local contractors on a trial basis — completely free leads to start, no commitment. Would that be something you'd be open to?"

---

## When the First Lead Comes In

1. Jackson gets Gmail alert to jacksonrsmith@gmail.com
2. Open Notion Live Leads DB — row has: name, phone, service needed, city
3. Text/call committed contractor immediately with name + phone + what they need
4. Log in Notion: Status → "Contacted Partner", note which contractor received it
5. Follow up with homeowner within 24 hrs to confirm they were contacted

**Do not let a lead sit.** Speed-to-contact is the entire value prop to the contractor.

---

## Ad Evaluation Window (~May 8-10, after ~$100 spend)

- **CPL < $25** → Campaign working, hold or scale to $25/day
- **CPL $25–$50** → Acceptable for home services, test a new creative variation
- **CPL > $50 or 0 leads** → Kill ad set, test new copy or image
- **Check:** Is delivery showing "Active"? If still "Processing" after 48hrs, Meta may have flagged the creative

---

## SEO — What's Next After the Push

The overhaul covers the foundational layer. These are the next-tier SEO plays:

1. **Add city pages for Murray, West Jordan, Midvale, Salt Lake City** — you have content for these cities in service-area.astro already. Each city page = a new ranking opportunity for "[city] roof repair"
2. **Google Business Profile** — create one at business.google.com for Sandy Roofing Pros. This is the single highest-leverage local SEO move. Once you have a GBP URL, add it to the `sameAs` array in BaseLayout.astro schema.
3. **Add 1-2 more blog posts** — target queries like "how long does roof repair take Utah", "cost of roof repair Salt Lake County". The FAQ and existing blog post give you a great base.
4. **Internal links** — link from FAQ answers to the relevant service pages. Currently the FAQ page is a dead end.

---

## Team Roles — Right Now

| Person | Priority Task |
|--------|--------------|
| **Jackson** | Push SEO changes → submit sitemap → decide on CallRail → check Meta ad destination type |
| **Noah** | Contractor outreach calls — 1 committed BO by end of week |
| **Sarah** | Meta Pixel install (`src/layouts/BaseLayout.astro` + Lead event on form submit success) |

---

## What to Tell Claude in the Next Chat

Paste this to start fast:

> "I'm running a roofing lead gen business in Sandy, UT at sandyroofingpros.com. Ads are live on Meta at $21/day. The lead pipeline is fully operational (form → Make → Notion + Gmail). I just pushed a full SEO overhaul and submitted the sitemap to Google Search Console. My contractor partner (Noah) is working on landing our first committed BO. Help me with [choose below]."

**Options:**
1. "My Meta ad has been running for X days and spent ~$100 — here's my data. Help me evaluate and decide what to do next."
2. "A lead just came in — help me handle it and route it to the contractor."
3. "Help me build the next 4 city landing pages (Murray, West Jordan, Midvale, Salt Lake City) for SEO."
4. "Help me set up a Google Business Profile for Sandy Roofing Pros."
5. "Help me write 2 more blog posts targeting local roof repair keywords."
6. "The Meta Pixel still isn't installed — help me get Sarah up to speed on what needs to happen."
