"""
Smith Asset Group — AI Agent Configuration
All constants derived from smith_asset_group_agent_handoff.docx
"""

# ─── Notion Database IDs ─────────────────────────────────────────────────────

DB_LIVE_LEADS     = "8bc8b705-8629-4b17-ac80-f84adce107a8"
DB_PARTNER_DIR    = "24f3a86e-c101-4d49-8a2a-d062d9d6a19b"
DB_AD_METRICS     = "47d3c105-4ffa-4a9e-8455-66a4c1c3c355"
DB_FINANCES       = "8458dc3f-6b78-4f3c-9b42-b5dd143ecdfa"

PAGE_COMMAND_CENTER = "34ad9bd2-b6bd-81aa-b10b-c2e7124cb3c7"
PAGE_WEEK1_DASH     = "34ad9bd2-b6bd-8109-8360-da0717763fe5"
PAGE_EXPANSION      = "34ad9bd2-b6bd-8112-bd00-db8aaba68295"

# ─── Live Leads DB — Property Names (Notion display names) ───────────────────

LEAD_PROPS = {
    "name":               "Name",           # Title
    "phone":              "Phone",
    "message":            "Message",        # Rich Text
    "source":             "Source",         # Select
    "status":             "Status",         # Select
    "service":            "Service",        # Select
    "zip_code":           "Zip Code",       # Rich Text
    "lead_grade":         "Lead Grade",     # Select
    "est_job_value":      "Est. Job Value", # Select
    "territory_status":   "Territory Status", # Select
    "recommended_action": "Recommended Action", # Select
    "contractor_note":    "Contractor Note", # Rich Text
    "red_flags":          "Red Flags",      # Rich Text
    "urgency_score":      "Urgency Score",  # Number
}

LEAD_STATUS_OPTIONS = [
    "🖕 New",
    "Contacted Partner",
    "Estimate Scheduled",
    "Job Closed",
    "Dead",
]

LEAD_GRADE_OPTIONS   = ["A Hot", "B Warm", "C Cool", "D Cold"]
SERVICE_OPTIONS      = [
    "Emergency Roof Leak Repair",
    "Storm Damage Roof Repair",
    "Roof Inspection",
    "Other / Not Sure",
]
EST_JOB_VALUE_OPTIONS = ["Under $1K", "$1K–$3K", "$3K–$8K", "$8K–$15K", "$15K+"]
TERRITORY_OPTIONS     = ["In Target Zone", "Edge Zone", "Outside Zone", "Unknown"]
REC_ACTION_OPTIONS    = ["Call Immediately", "Schedule Follow-up", "Monitor", "Do Not Contact"]

# ─── Partner Directory — Property Names ──────────────────────────────────────

PARTNER_PROPS = {
    "name":             "Name",
    "owner_name":       "Owner Name",
    "phone":            "Phone",
    "email":            "Email",
    "status":           "Status",
    "priority":         "Priority",
    "source":           "Source",
    "assigned_partner": "Assigned Partner",
    "lead_source_url":  "Lead Source URL",
    "notes":            "Notes",
    "last_contacted":   "Last Contacted",
}

PARTNER_STATUS_OPTIONS = [
    "Not Contacted", "Called", "Interested", "Committed", "Declined", "Client"
]

# ─── Ad Metrics — Property Names ─────────────────────────────────────────────

AD_METRIC_PROPS = {
    "date":        "Date",
    "platform":    "Platform",
    "campaign":    "Campaign",
    "spend":       "Spend",
    "impressions": "Impressions",
    "clicks":      "Clicks",
    "ctr":         "CTR",
    "conversions": "Conversions",
    "cpl":         "CPL",
    "avg_cpc":     "Avg CPC",
    "notes":       "Notes",
}

# ─── Finances — Property Names ────────────────────────────────────────────────

FINANCE_PROPS = {
    "title":    "Transaction Title",
    "date":     "Date",
    "category": "Category",
    "amount":   "Amount",
    "platform": "Platform",
    "notes":    "Notes",
}

FINANCE_CATEGORIES = ["Ad Spend", "Tool/Software", "Domain", "Legal", "Revenue", "Misc"]

# ─── Business Logic ───────────────────────────────────────────────────────────

IN_TARGET_ZIPS = {
    "84070", "84094", "84093", "84092", "84095",
    "84096", "84047", "84121",
}
EDGE_ZIPS = {"84084", "84088", "84065", "84020"}

CPL_HOLD_THRESHOLD  = 25   # CPL < $25 → hold or scale
CPL_OK_THRESHOLD    = 50   # CPL $25–$50 → acceptable, test new creative
CPL_KILL_THRESHOLD  = 50   # CPL > $50 → kill ad set
KILL_SPEND_NO_LEADS = 100  # $100 spend with 0 conversions → kill

GRADE_RULES = {
    "A": "Active emergency (water in now, storm just hit, urgent language) + homeowner in service territory + high job value likely + valid phone",
    "B": "Clear damage described + planning soon + good SLC County location + valid contact",
    "C": "Vague description ('just getting quotes') OR no urgency OR unclear location OR low expected value",
    "D": "Likely spam OR fake phone OR outside service area OR extremely vague",
}

URGENCY_SCORE_RULES = {
    5: "Leaking NOW — 'coming in', 'tonight', 'flooding', 'right now'",
    4: "Recent storm damage (1–7 days), visible shingle loss, wants someone this week",
    3: "Known issue, flexible timeline, wants estimate",
    2: "Planning ahead, no current problem, thinking about replacement",
    1: "Extremely vague — just a name/phone with no job context",
}

# ─── Team contacts ────────────────────────────────────────────────────────────

TEAM = {
    "jackson": {
        "name": "Jackson Smith",
        "email": "jacksonrsmith@gmail.com",
        "role": "Strategy & Operations",
    },
    "noah": {
        "name": "Noah",
        "role": "Sales & Client Acquisition",
        "trigger": "Pipeline is live. First lead is in the sheet. Go.",
    },
    "sarah": {
        "name": "Sarah",
        "role": "Website Technology",
    },
}

# ─── Contractor outreach priority list ───────────────────────────────────────

CONTRACTOR_OUTREACH = [
    {"priority": 1, "business": "Utah Roofing Pros",      "owner": "John Panos",         "phone": "(801) 688-3853", "email": "john@utahroofingpros.com", "notes": "Active on Angi — buying leads"},
    {"priority": 2, "business": "AMCO American Roofing",  "owner": "Brent Yorgason",     "phone": "(801) 269-1276", "email": "brent@amcoroof.com",        "notes": "Referral-heavy, responsive"},
    {"priority": 3, "business": "Alta Roofing",           "owner": "Bennett Sorensen",   "phone": "(385) 450-7663", "email": None,                        "notes": "Active local presence"},
    {"priority": 4, "business": "Shingle Pro Roofing",    "owner": "Jason Harenberg",    "phone": "(801) 567-9093", "email": None,                        "notes": "550+ reviews, may be self-sufficient"},
    {"priority": 5, "business": "Vertex Roofing",         "owner": "Devin Parker",       "phone": "(801) 639-0477", "email": None,                        "notes": "Strong web presence"},
    {"priority": 6, "business": "Bighorn Roofing",        "owner": "Family-owned",       "phone": "(801) 305-4851", "email": None,                        "notes": "Thin online footprint"},
    {"priority": 7, "business": "Canyon Roofing",         "owner": "Verify on call",     "phone": "(801) 835-1070", "email": None,                        "notes": None},
    {"priority": 8, "business": "Salty Roofer",           "owner": "Verify on call",     "phone": "(385) 433-6650", "email": None,                        "notes": None},
    {"priority": 9, "business": "Hometown Roofing",       "owner": "Verify on call",     "phone": "(801) 969-1307", "email": None,                        "notes": None},
    {"priority":10, "business": "Bartlett Roofing",       "owner": "Doug Bartlett",      "phone": "(801) 509-6464", "email": None,                        "notes": "Boise franchise — not ideal"},
]

# ─── Make.com / endpoints ────────────────────────────────────────────────────

MAKE_WEBHOOK_URL  = "https://hook.us2.make.com/0hvtk7eovyrsp97idje1zuil4rd3bgvo"
FORMSPREE_URL     = "https://formspree.io/f/mvzdjovl"
MAKE_SCENARIO_ID  = "4885026"
MAKE_ORG_ID       = "2214094"

# ─── AI model for this agent ─────────────────────────────────────────────────

AGENT_MODEL = "claude-sonnet-4-6"   # orchestrator
SCORING_MODEL = "claude-haiku-4-5-20251001"  # used by Make.com for lead scoring
MAX_TOKENS = 4096
