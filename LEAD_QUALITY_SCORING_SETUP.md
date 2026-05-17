# Lead Quality Scoring Engine — Make.com Setup Guide

**Scenario:** 4885026 — Sandy Roofing — Form → Notion + Email Alert  
**What we're adding:** An AI scoring step between JSON parse and Notion that grades every lead automatically before it hits the database.

---

## Overview of the New Flow

```
[1] Webhook → [4] Parse JSON → [5] OpenAI Score → [6] Parse Score JSON → [2] Notion (with grades) → [3] Gmail (enriched alert)
```

After this setup, every lead in Notion will have:
- **Lead Grade** (A/B/C/D)
- **Urgency Score** (1–5)
- **Est. Job Value** range
- **Territory Status** (In Target Zone / Edge Zone / Outside Zone / Unknown)
- **Recommended Action** (Call Immediately / Schedule Follow-up / Monitor / Do Not Contact)
- **Contractor Note** (one sentence for Noah)
- **Red Flags** (if any)

---

## Prerequisites

You need an **OpenAI API key**. Get one at https://platform.openai.com/api-keys  
Cost: ~$0.001 per lead scored (negligible). Fund with $5–10 to start.

> **Alternative:** If you prefer not to use OpenAI, use the Anthropic API instead. The HTTP module config is at the bottom of this guide.

---

## Step 1 — Add the OpenAI Module (Module 5)

1. Open scenario **4885026** in Make.com
2. Click the **+** button on the connection line between **Module 4 (Parse JSON)** and **Module 2 (Notion)**
3. Search for **OpenAI** → select **"Create a Chat Completion"**
4. Connect your OpenAI account (paste your API key when prompted)

**Module 5 Settings:**

| Field | Value |
|-------|-------|
| Model | `gpt-4o-mini` |
| Max Tokens | `500` |
| Temperature | `0` |
| Response Format | `JSON Object` |

**Messages — add 2 messages:**

**Message 1 — Role: System**
Paste this entire block as the system message:

```
You are the Lead Quality & Qualification Engine for Sandy Roofing Pros, a roofing lead generation business serving the Salt Lake City metro area. Score every incoming form lead and return ONLY valid JSON.

TARGET ZIP CODES:
- In Target Zone: 84070, 84094, 84093, 84092, 84095, 84096, 84047, 84121
- Edge Zone (serve if pipeline is slow): 84084, 84088, 84065, 84020
- All others: Outside Zone
- Blank or missing zip: Unknown

GRADING RULES:
- Grade A (Hot): Urgency 4-5 + in target zone + clear specific service + valid phone
- Grade B (Warm): Urgency 3-4 + likely in/near zone + clear intent + valid contact
- Grade C (Cool): Urgency 2-3 + vague message OR edge zone OR unverified contact
- Grade D (Cold): Spam indicators, outside zone, no phone, test submissions, fake info

URGENCY SCORING (1-5):
5 → "emergency", "active leak", "ceiling caving", "flooding", "need today", "urgent"
4 → "hail damage", "storm damage", "missing shingles", "insurance claim", "need ASAP"
3 → "getting estimates", "planning to replace", "free inspection", "sometime this year"
2 → "curious", "just looking", "no rush", "maybe next year"
1 → Blank message, one-word replies, test submissions, spam

EST. JOB VALUE:
- Emergency leak repair: Under $1K or $1K - $3K
- Storm/hail damage: $3K - $8K or $8K - $15K
- Full roof replacement: $8K - $15K or $15K+
- Insurance claim: $8K - $15K
- Free inspection: Under $1K (but flag as upsell opportunity)
- Other/vague: $1K - $3K

RED FLAGS — check for these:
- Fake phone: all same digits (5555555555), 000-000-0000, 1234567890, fewer than 10 digits
- Fake name: "test", "asdf", "qwerty", single letter
- Fake email: contains "test@", "fake@", "spam@"
- Blank or lorem ipsum message
- Service = "Other" with no explanation
- ZIP is outside Utah

ALWAYS respond with ONLY this JSON structure, nothing else:
{
  "grade": "A" or "B" or "C" or "D",
  "urgency_score": 1 to 5 (integer),
  "est_job_value": "Under $1K" or "$1K - $3K" or "$3K - $8K" or "$8K - $15K" or "$15K+",
  "territory_status": "In Target Zone" or "Edge Zone" or "Outside Zone" or "Unknown",
  "recommended_action": "Call Immediately" or "Schedule Follow-up" or "Monitor" or "Do Not Contact",
  "contractor_note": "One sentence max. Direct and actionable for the contractor.",
  "red_flags": "None" or comma-separated list of specific red flags found
}
```

**Message 2 — Role: User**
Build this dynamically using the variable pills from Module 4:

```
Score this roofing lead:

Name: [4.name]
Phone: [4.phone]
Email: [4.email]
Zip Code: [4.zipcode]
Service Requested: [4.service]
Message: [4.message]
```

*(Replace `[4.x]` with actual variable pills from the picker — click the field, then select from Module 4)*

---

## Step 2 — Add the JSON Parse Module (Module 6)

The OpenAI response comes back as a string. We need to parse it into individual fields.

1. Click **+** after Module 5
2. Search for **JSON** → select **"Parse JSON"**

**Module 6 Settings:**

| Field | Value |
|-------|-------|
| JSON string | `[5.choices[].message.content]` (pill from Module 5) |
| Data structure | Create new → name it **"Lead Score Response"** |

**Data Structure fields for "Lead Score Response":**

| Name | Type |
|------|------|
| grade | Text |
| urgency_score | Number |
| est_job_value | Text |
| territory_status | Text |
| recommended_action | Text |
| contractor_note | Text |
| red_flags | Text |

Click **Save** after creating the data structure.

---

## Step 3 — Update Module 2 (Notion) Field Mappings

Open the Notion module. Add these new field mappings using pills from **Module 6**:

| Notion Field | Make Variable |
|-------------|---------------|
| Lead Grade | `[6.grade]` → map to the correct option: "A - Hot 🔥", "B - Warm ✅", "C - Cool 👀", "D - Cold ❌" |
| Urgency Score | `[6.urgency_score]` |
| Est. Job Value | `[6.est_job_value]` |
| Territory Status | `[6.territory_status]` → map to: "✅ In Target Zone", "⚠️ Edge Zone", "❌ Outside Zone", "❓ Unknown" |
| Recommended Action | `[6.recommended_action]` → map to: "📞 Call Immediately", "📅 Schedule Follow-up", "👀 Monitor", "🚫 Do Not Contact" |
| Contractor Note | `[6.contractor_note]` |
| Red Flags | `[6.red_flags]` |

> **Note on Select fields:** For Grade, Territory Status, and Recommended Action, you may need to use a Text Aggregator or IF function to convert the AI's plain text output to the Notion option name with emoji. See the "Option Mapping" section below.

### Option Mapping (for Select fields)

Because Notion select options include emojis but the AI returns plain text, use Make's **"if"** function in the field mapping:

**For Lead Grade:**
```
{{if(6.grade = "A"; "A - Hot 🔥"; if(6.grade = "B"; "B - Warm ✅"; if(6.grade = "C"; "C - Cool 👀"; "D - Cold ❌")))}}
```

**For Territory Status:**
```
{{if(6.territory_status = "In Target Zone"; "✅ In Target Zone"; if(6.territory_status = "Edge Zone"; "⚠️ Edge Zone"; if(6.territory_status = "Outside Zone"; "❌ Outside Zone"; "❓ Unknown")))}}
```

**For Recommended Action:**
```
{{if(6.recommended_action = "Call Immediately"; "📞 Call Immediately"; if(6.recommended_action = "Schedule Follow-up"; "📅 Schedule Follow-up"; if(6.recommended_action = "Monitor"; "👀 Monitor"; "🚫 Do Not Contact")))}}
```

---

## Step 4 — Update Module 3 (Gmail) Email Alert

Make the alert email more useful by including the score. Update the email body to include:

```
🏠 NEW ROOFING LEAD — GRADE [6.grade] | URGENCY [6.urgency_score]/5

Name: [4.name]
Phone: [4.phone]
Email: [4.email]
Zip Code: [4.zipcode]
Service: [4.service]

📋 AI ASSESSMENT:
Grade: [6.grade]
Job Value Est.: [6.est_job_value]
Territory: [6.territory_status]
Action: [6.recommended_action]

💬 Contractor Note: [6.contractor_note]

⚠️ Red Flags: [6.red_flags]

📝 Their Message:
[4.message]
```

---

## Step 5 — Test the Scenario

1. Submit a test lead on the website with:
   - Name: Test Lead
   - Phone: 801-555-1234
   - Email: test@test.com
   - Zip: 84070
   - Service: Emergency Leak Repair
   - Message: I have an active roof leak causing water damage

2. Watch the scenario run in Make.com (click "Run once" first)
3. Verify Module 5 returns a JSON response
4. Verify Module 6 parses it correctly
5. Verify Notion entry has all score fields populated
6. Verify Gmail alert includes the grade

Expected result for this test lead: **Grade A, Urgency 5, In Target Zone, Call Immediately**

---

## Alternative: Using Anthropic API (HTTP Module)

If you want to use Claude instead of OpenAI:

**Module 5 — HTTP Make a Request:**

| Field | Value |
|-------|-------|
| URL | `https://api.anthropic.com/v1/messages` |
| Method | POST |
| Headers | `x-api-key: YOUR_ANTHROPIC_API_KEY` and `anthropic-version: 2023-06-01` and `content-type: application/json` |

**Body (JSON):**
```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 500,
  "system": "[PASTE THE SYSTEM PROMPT FROM STEP 1 ABOVE]",
  "messages": [
    {
      "role": "user",
      "content": "Score this roofing lead:\n\nName: {{4.name}}\nPhone: {{4.phone}}\nEmail: {{4.email}}\nZip Code: {{4.zipcode}}\nService: {{4.service}}\nMessage: {{4.message}}"
    }
  ]
}
```

**Module 6 JSON parse path:** Use `[5.content[].text]` instead of `[5.choices[].message.content]`

Get your Anthropic API key at: https://console.anthropic.com/settings/keys

---

## Module Order After Setup

| # | Module | Function |
|---|--------|----------|
| 1 | Webhooks | Receives form POST |
| 4 | Parse JSON | Extracts lead fields |
| **5** | **OpenAI** | **Scores the lead with AI** |
| **6** | **Parse JSON** | **Extracts score fields** |
| 2 | Notion | Creates enriched lead record |
| 3 | Gmail | Sends enriched alert |

---

*Setup estimated time: 30–45 minutes. Once live, every lead scores itself in <2 seconds at ~$0.001/lead.*
