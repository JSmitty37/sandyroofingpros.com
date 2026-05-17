// Smith Asset Group — Agent Configuration
// All constants from smith_asset_group_agent_handoff.docx

export const DB = {
  LIVE_LEADS:   "8bc8b705-8629-4b17-ac80-f84adce107a8",
  PARTNER_DIR:  "24f3a86e-c101-4d49-8a2a-d062d9d6a19b",
  AD_METRICS:   "47d3c105-4ffa-4a9e-8455-66a4c1c3c355",
  FINANCES:     "8458dc3f-6b78-4f3c-9b42-b5dd143ecdfa",
};

export const PAGE = {
  COMMAND_CENTER: "34ad9bd2-b6bd-81aa-b10b-c2e7124cb3c7",
  WEEK1_DASH:     "34ad9bd2-b6bd-8109-8360-da0717763fe5",
  EXPANSION:      "34ad9bd2-b6bd-8112-bd00-db8aaba68295",
};

// Live Leads select options
export const LEAD_STATUS        = ["🆕 New", "📞 Called", "🤝 Free Trial", "✅ Closed", "❌ Not Qualified"];
export const LEAD_GRADE         = ["A Hot", "B Warm", "C Cool", "D Cold"];
export const SERVICE_OPTIONS    = ["Emergency Roof Leak Repair", "Storm Damage Roof Repair", "Roof Inspection", "Other / Not Sure"];
export const EST_JOB_VALUE      = ["Under $1K", "$1K–$3K", "$3K–$8K", "$8K–$15K", "$15K+"];
export const TERRITORY_OPTIONS  = ["In Target Zone", "Edge Zone", "Outside Zone", "Unknown"];
export const REC_ACTION_OPTIONS = ["Call Immediately", "Schedule Follow-up", "Monitor", "Do Not Contact"];

// Partner Directory select options
export const PARTNER_STATUS = ["Not Contacted", "Called", "Interested", "Committed", "Declined", "Client"];

// Territory ZIP codes
export const IN_TARGET_ZIPS = new Set(["84070","84094","84093","84092","84095","84096","84047","84121"]);
export const EDGE_ZIPS      = new Set(["84084","84088","84065","84020"]);

// CPL kill-rule thresholds (USD)
export const CPL_SCALE_THRESHOLD = 25;
export const CPL_OK_THRESHOLD    = 50;
export const KILL_SPEND_NO_LEADS = 100;

// Agent model
export const AGENT_MODEL   = "claude-sonnet-4-6";
export const MAX_TOKENS    = 4096;

// Contractor outreach priority list
export const CONTRACTORS = [
  { priority: 1,  business: "Utah Roofing Pros",     owner: "John Panos",       phone: "(801) 688-3853", email: "john@utahroofingpros.com", tier: "TOP" },
  { priority: 2,  business: "AMCO American Roofing",  owner: "Brent Yorgason",   phone: "(801) 269-1276", email: "brent@amcoroof.com",       tier: "TOP" },
  { priority: 3,  business: "Alta Roofing",           owner: "Bennett Sorensen", phone: "(385) 450-7663", email: null,                       tier: "TOP" },
  { priority: 4,  business: "Shingle Pro Roofing",    owner: "Jason Harenberg",  phone: "(801) 567-9093", email: null,                       tier: "MED" },
  { priority: 5,  business: "Vertex Roofing",         owner: "Devin Parker",     phone: "(801) 639-0477", email: null,                       tier: "MED" },
  { priority: 6,  business: "Bighorn Roofing",        owner: "Family-owned",     phone: "(801) 305-4851", email: null,                       tier: "MED" },
  { priority: 7,  business: "Canyon Roofing",         owner: "Verify on call",   phone: "(801) 835-1070", email: null,                       tier: "MED" },
  { priority: 8,  business: "Salty Roofer",           owner: "Verify on call",   phone: "(385) 433-6650", email: null,                       tier: "MED" },
  { priority: 9,  business: "Hometown Roofing",       owner: "Verify on call",   phone: "(801) 969-1307", email: null,                       tier: "MED" },
  { priority: 10, business: "Bartlett Roofing",       owner: "Doug Bartlett",    phone: "(801) 509-6464", email: null,                       tier: "LOW" },
];
