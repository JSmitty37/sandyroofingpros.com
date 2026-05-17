// Smith Asset Group — Notion Tool Implementations
// All Notion calls use the REST API via fetch.

import { DB, IN_TARGET_ZIPS, EDGE_ZIPS, CPL_SCALE_THRESHOLD, CPL_OK_THRESHOLD, KILL_SPEND_NO_LEADS } from "./config.js";

const NOTION_VERSION = "2022-06-28";

function headers() {
  const key = process.env.NOTION_API_KEY;
  if (!key) throw new Error("NOTION_API_KEY is not set.");
  return {
    "Authorization": `Bearer ${key}`,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
  };
}

async function notionGet(path) {
  const res = await fetch(`https://api.notion.com/v1${path}`, { headers: headers() });
  if (!res.ok) throw new Error(`Notion GET ${path} → ${res.status}: ${await res.text()}`);
  return res.json();
}

async function notionPost(path, body) {
  const res = await fetch(`https://api.notion.com/v1${path}`, {
    method: "POST", headers: headers(), body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Notion POST ${path} → ${res.status}: ${await res.text()}`);
  return res.json();
}

async function notionPatch(path, body) {
  const res = await fetch(`https://api.notion.com/v1${path}`, {
    method: "PATCH", headers: headers(), body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Notion PATCH ${path} → ${res.status}: ${await res.text()}`);
  return res.json();
}

// ─── Property builders ────────────────────────────────────────────────────────
const titleProp    = v => ({ title: [{ text: { content: v } }] });
const richTextProp = v => ({ rich_text: [{ text: { content: String(v) } }] });
const selectProp   = v => ({ select: { name: v } });
const numberProp   = v => ({ number: Number(v) });
const phoneProp    = v => ({ phone_number: String(v) });
const emailProp    = v => ({ email: String(v) });
const dateProp     = v => ({ date: { start: v } });
const checkboxProp = v => ({ checkbox: Boolean(v) });

// ─── Property reader ──────────────────────────────────────────────────────────
function readProp(page, name) {
  const prop = page?.properties?.[name];
  if (!prop) return null;
  const t = prop.type;
  if (t === "title")       return prop.title?.[0]?.plain_text ?? null;
  if (t === "rich_text")   return prop.rich_text?.[0]?.plain_text ?? null;
  if (t === "select")      return prop.select?.name ?? null;
  if (t === "number")      return prop.number;
  if (t === "phone_number") return prop.phone_number;
  if (t === "email")       return prop.email;
  if (t === "checkbox")    return prop.checkbox;
  if (t === "date")        return prop.date?.start ?? null;
  if (t === "url")         return prop.url;
  return null;
}

function flattenPage(page) {
  const out = { id: page.id, url: page.url };
  for (const name of Object.keys(page.properties ?? {})) {
    out[name] = readProp(page, name);
  }
  return out;
}

// ─── Live Leads ───────────────────────────────────────────────────────────────
export async function getNewLeads() {
  const result = await notionPost(`/databases/${DB.LIVE_LEADS}/query`, {
    filter: { property: "Status", select: { equals: "🆕 New" } },
    sorts:  [{ timestamp: "created_time", direction: "descending" }],
  });
  return result.results.map(flattenPage);
}

export async function getAllLeads(limit = 50) {
  const result = await notionPost(`/databases/${DB.LIVE_LEADS}/query`, {
    sorts: [{ timestamp: "created_time", direction: "descending" }],
    page_size: Math.min(limit, 100),
  });
  return result.results.map(flattenPage);
}

export async function getLead(pageId) {
  return flattenPage(await notionGet(`/pages/${pageId}`));
}

export async function updateLead(pageId, updates) {
  const propMap = {};
  const FIELD_MAP = {
    name: ["Name", "title"], phone: ["Phone", "phone"],
    message: ["Message", "rich_text"], zip_code: ["Zip Code", "rich_text"],
    contractor_note: ["Contractor Note", "rich_text"], red_flags: ["Red Flags", "rich_text"],
    source: ["Source", "select"], status: ["Status", "select"],
    service: ["Service", "select"], lead_grade: ["Lead Grade", "select"],
    est_job_value: ["Est. Job Value", "select"],
    territory_status: ["Territory Status", "select"],
    recommended_action: ["Recommended Action", "select"],
    urgency_score: ["Urgency Score", "number"],
  };
  for (const [key, value] of Object.entries(updates)) {
    const mapping = FIELD_MAP[key];
    if (!mapping) continue;
    const [displayName, type] = mapping;
    if (type === "title")      propMap[displayName] = titleProp(value);
    else if (type === "phone") propMap[displayName] = phoneProp(value);
    else if (type === "rich_text") propMap[displayName] = richTextProp(value);
    else if (type === "select")    propMap[displayName] = selectProp(value);
    else if (type === "number")    propMap[displayName] = numberProp(value);
  }
  return flattenPage(await notionPatch(`/pages/${pageId}`, { properties: propMap }));
}

export async function routeLeadToPartner(leadPageId, contractorName, note = "") {
  const noteText = `Routed to ${contractorName}.${note ? " " + note : ""}`;
  return updateLead(leadPageId, { status: "Contacted Partner", contractor_note: noteText });
}

// ─── Partner Directory ────────────────────────────────────────────────────────
export async function getPartners(assignedOnly = false) {
  const body = { sorts: [{ property: "Priority", direction: "ascending" }] };
  if (assignedOnly) body.filter = { property: "Assigned Partner", checkbox: { equals: true } };
  const result = await notionPost(`/databases/${DB.PARTNER_DIR}/query`, body);
  return result.results.map(flattenPage);
}

export async function updatePartner(pageId, updates) {
  const propMap = {};
  const FIELD_MAP = {
    name: ["Name", "title"], owner_name: ["Owner Name", "rich_text"],
    notes: ["Notes", "rich_text"], status: ["Status", "select"],
    priority: ["Priority", "select"], source: ["Source", "select"],
    phone: ["Phone", "phone"], email: ["Email", "email"],
    assigned_partner: ["Assigned Partner", "checkbox"],
    last_contacted: ["Last Contacted", "date"],
  };
  for (const [key, value] of Object.entries(updates)) {
    const mapping = FIELD_MAP[key];
    if (!mapping) continue;
    const [displayName, type] = mapping;
    if (type === "title")     propMap[displayName] = titleProp(value);
    else if (type === "rich_text") propMap[displayName] = richTextProp(value);
    else if (type === "select")    propMap[displayName] = selectProp(value);
    else if (type === "phone")     propMap[displayName] = phoneProp(value);
    else if (type === "email")     propMap[displayName] = emailProp(value);
    else if (type === "checkbox")  propMap[displayName] = checkboxProp(value);
    else if (type === "date")      propMap[displayName] = dateProp(value);
  }
  return flattenPage(await notionPatch(`/pages/${pageId}`, { properties: propMap }));
}

// ─── Ad Metrics ───────────────────────────────────────────────────────────────
export async function getAdMetrics(days = 7) {
  // Fetch all rows and filter in JS — avoids Notion date-filter type mismatches
  const result = await notionPost(`/databases/${DB.AD_METRICS}/query`, {
    sorts: [{ timestamp: "created_time", direction: "descending" }],
    page_size: 100,
  });
  const cutoff = new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
  const rows = result.results.map(flattenPage);
  // Filter by the Date property value if present, otherwise return all
  return rows.filter(r => {
    const d = r["Date"];
    return d ? d >= cutoff : true;
  });
}

export async function logAdMetric({ date, platform, campaign, spend, impressions, clicks, conversions, avg_cpc, notes = "" }) {
  const ctr = impressions ? Math.round((clicks / impressions) * 10000) / 100 : 0;
  const cpl = conversions ? Math.round((spend / conversions) * 100) / 100 : 0;
  const page = await notionPost("/pages", {
    parent: { database_id: DB.AD_METRICS },
    properties: {
      "Date":        dateProp(date),
      "Platform":    selectProp(platform),
      "Campaign":    richTextProp(campaign),
      "Spend":       numberProp(spend),
      "Impressions": numberProp(impressions),
      "Clicks":      numberProp(clicks),
      "CTR":         numberProp(ctr),
      "Conversions": numberProp(conversions),
      "CPL":         numberProp(cpl),
      "Avg CPC":     numberProp(avg_cpc),
      "Notes":       richTextProp(notes),
    },
  });
  return flattenPage(page);
}

export function evaluateCpl(spend, conversions) {
  if (conversions === 0) {
    const action = spend >= KILL_SPEND_NO_LEADS
      ? `KILL — $${spend.toFixed(2)} spend with zero leads. Test new copy or image.`
      : `WATCH — $${spend.toFixed(2)} spent, no conversions yet. Kill threshold: $${KILL_SPEND_NO_LEADS}.`;
    return { spend, conversions, cpl: null, action };
  }
  const cpl = Math.round((spend / conversions) * 100) / 100;
  let action;
  if (cpl < CPL_SCALE_THRESHOLD)
    action = `SCALE — CPL $${cpl} is excellent. Hold or increase to $25/day.`;
  else if (cpl <= CPL_OK_THRESHOLD)
    action = `ACCEPTABLE — CPL $${cpl} is industry-average. Test new creative variation.`;
  else
    action = `KILL — CPL $${cpl} exceeds $50 threshold. Kill ad set and test new copy.`;
  return { spend, conversions, cpl, action };
}

// ─── Finances ─────────────────────────────────────────────────────────────────
export async function getFinances(category = null) {
  const body = { sorts: [{ property: "Date", direction: "descending" }] };
  if (category) body.filter = { property: "Category", select: { equals: category } };
  const result = await notionPost(`/databases/${DB.FINANCES}/query`, body);
  return result.results.map(flattenPage);
}

export async function logFinance({ title, date, category, amount, platform = "", notes = "" }) {
  const page = await notionPost("/pages", {
    parent: { database_id: DB.FINANCES },
    properties: {
      "Transaction Title": titleProp(title),
      "Date":              dateProp(date),
      "Category":          selectProp(category),
      "Amount":            numberProp(amount),
      "Platform":          richTextProp(platform),
      "Notes":             richTextProp(notes),
    },
  });
  return flattenPage(page);
}

export async function getPlSummary() {
  const rows = await getFinances();
  const revenue  = rows.reduce((s, r) => s + (r.Amount > 0 ? r.Amount : 0), 0);
  const expenses = rows.reduce((s, r) => s + (r.Amount < 0 ? r.Amount : 0), 0);
  return {
    revenue:  Math.round(revenue  * 100) / 100,
    expenses: Math.round(expenses * 100) / 100,
    net:      Math.round((revenue + expenses) * 100) / 100,
    rows:     rows.length,
  };
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
export async function getDashboardSummary() {
  const [newLeads, partners, metrics7d, pl] = await Promise.all([
    getNewLeads(),
    getPartners(),
    getAdMetrics(7),
    getPlSummary(),
  ]);
  const assigned = partners.filter(p => p["Assigned Partner"]);
  const clients  = partners.filter(p => p["Status"] === "Client");
  const recentSpend = metrics7d.reduce((s, r) => s + (r["Spend"] || 0), 0);
  const recentLeads = metrics7d.reduce((s, r) => s + (r["Conversions"] || 0), 0);
  return {
    new_leads_pending_routing: newLeads.length,
    new_lead_details: newLeads.slice(0, 5),
    total_partners_researched: partners.length,
    assigned_partners: assigned.length,
    clients_on_retainer: clients.length,
    ad_spend_last_7d: Math.round(recentSpend * 100) / 100,
    ad_leads_last_7d: recentLeads,
    pl_summary: pl,
    week1_checklist: {
      market_selected: true,
      domain_registered: true,
      site_live: true,
      contractor_list_built: true,
      noah_outreach_started: true,
      make_pipeline_live: true,
      google_ads_live: true,
      advertiser_verification: "PENDING",
      first_committed_partner: clients.length > 0,
      first_lead_delivered: recentLeads > 0,
      first_retainer_closed: clients.length > 0,
    },
  };
}

export function classifyZip(zipCode) {
  const z = String(zipCode).trim();
  if (IN_TARGET_ZIPS.has(z)) return "In Target Zone";
  if (EDGE_ZIPS.has(z))      return "Edge Zone";
  if (z.startsWith("84") || z.startsWith("83")) return "Edge Zone";
  return "Outside Zone";
}

// ─── Tool definitions for Anthropic tool_use ─────────────────────────────────
export const TOOL_DEFINITIONS = [
  {
    name: "get_dashboard_summary",
    description: "Return a live snapshot: unrouted leads, partner counts, 7-day ad spend, and P&L. Use this first when asked 'what's the status'.",
    input_schema: { type: "object", properties: {}, required: [] },
  },
  {
    name: "get_new_leads",
    description: "Return all leads in '🖕 New' status that haven't been routed to a contractor yet.",
    input_schema: { type: "object", properties: {}, required: [] },
  },
  {
    name: "get_all_leads",
    description: "Return the most recent leads from the Live Leads DB regardless of status.",
    input_schema: {
      type: "object",
      properties: { limit: { type: "integer", description: "Max rows to return (default 50, max 100)", default: 50 } },
      required: [],
    },
  },
  {
    name: "get_lead",
    description: "Return full details for a single lead by Notion page ID.",
    input_schema: {
      type: "object",
      properties: { page_id: { type: "string" } },
      required: ["page_id"],
    },
  },
  {
    name: "update_lead",
    description: "Update one or more fields on a lead. Common uses: mark as contacted, add contractor note, update grade.",
    input_schema: {
      type: "object",
      properties: {
        page_id: { type: "string" },
        updates: { type: "object", description: "Snake_case field names: status, lead_grade, contractor_note, territory_status, recommended_action, urgency_score, etc." },
      },
      required: ["page_id", "updates"],
    },
  },
  {
    name: "route_lead_to_partner",
    description: "Route a lead to a named contractor: sets Status → 'Contacted Partner' and writes routing note.",
    input_schema: {
      type: "object",
      properties: {
        lead_page_id:    { type: "string" },
        contractor_name: { type: "string" },
        note:            { type: "string", default: "" },
      },
      required: ["lead_page_id", "contractor_name"],
    },
  },
  {
    name: "get_partners",
    description: "Return all contractor partners from the Partner Directory.",
    input_schema: {
      type: "object",
      properties: { assigned_only: { type: "boolean", default: false } },
      required: [],
    },
  },
  {
    name: "update_partner",
    description: "Update one or more fields on a contractor partner record.",
    input_schema: {
      type: "object",
      properties: {
        page_id: { type: "string" },
        updates: { type: "object", description: "Snake_case keys: status, notes, assigned_partner, last_contacted, etc." },
      },
      required: ["page_id", "updates"],
    },
  },
  {
    name: "get_ad_metrics",
    description: "Return ad performance rows from the last N days.",
    input_schema: {
      type: "object",
      properties: { days: { type: "integer", default: 7 } },
      required: [],
    },
  },
  {
    name: "log_ad_metric",
    description: "Manually log a daily ad performance row to the Ad Metrics DB.",
    input_schema: {
      type: "object",
      properties: {
        date:        { type: "string", description: "YYYY-MM-DD" },
        platform:    { type: "string", description: "Google Ads | Meta | CallRail" },
        campaign:    { type: "string" },
        spend:       { type: "number" },
        impressions: { type: "integer" },
        clicks:      { type: "integer" },
        conversions: { type: "integer" },
        avg_cpc:     { type: "number" },
        notes:       { type: "string", default: "" },
      },
      required: ["date", "platform", "campaign", "spend", "impressions", "clicks", "conversions", "avg_cpc"],
    },
  },
  {
    name: "evaluate_cpl",
    description: "Apply CPL kill rules and return the recommended action (scale / hold / kill).",
    input_schema: {
      type: "object",
      properties: {
        spend:       { type: "number" },
        conversions: { type: "integer" },
      },
      required: ["spend", "conversions"],
    },
  },
  {
    name: "get_pl_summary",
    description: "Return total revenue, expenses, and net P&L from the Finances DB.",
    input_schema: { type: "object", properties: {}, required: [] },
  },
  {
    name: "log_finance",
    description: "Create a new transaction row in the Finances & P&L DB.",
    input_schema: {
      type: "object",
      properties: {
        title:    { type: "string" },
        date:     { type: "string", description: "YYYY-MM-DD" },
        category: { type: "string", description: "Ad Spend | Tool/Software | Domain | Legal | Revenue | Misc" },
        amount:   { type: "number", description: "Positive = revenue, negative = expense" },
        platform: { type: "string", default: "" },
        notes:    { type: "string", default: "" },
      },
      required: ["title", "date", "category", "amount"],
    },
  },
  {
    name: "classify_zip",
    description: "Return the territory classification for a ZIP code (In Target Zone / Edge Zone / Outside Zone).",
    input_schema: {
      type: "object",
      properties: { zip_code: { type: "string" } },
      required: ["zip_code"],
    },
  },
];

// ─── Tool dispatcher ──────────────────────────────────────────────────────────
export async function dispatch(toolName, input) {
  switch (toolName) {
    case "get_dashboard_summary": return getDashboardSummary();
    case "get_new_leads":         return getNewLeads();
    case "get_all_leads":         return getAllLeads(input.limit ?? 50);
    case "get_lead":              return getLead(input.page_id);
    case "update_lead":           return updateLead(input.page_id, input.updates);
    case "route_lead_to_partner": return routeLeadToPartner(input.lead_page_id, input.contractor_name, input.note ?? "");
    case "get_partners":          return getPartners(input.assigned_only ?? false);
    case "update_partner":        return updatePartner(input.page_id, input.updates);
    case "get_ad_metrics":        return getAdMetrics(input.days ?? 7);
    case "log_ad_metric":         return logAdMetric(input);
    case "evaluate_cpl":          return evaluateCpl(input.spend, input.conversions);
    case "get_pl_summary":        return getPlSummary();
    case "log_finance":           return logFinance(input);
    case "classify_zip":          return classifyZip(input.zip_code);
    default: throw new Error(`Unknown tool: ${toolName}`);
  }
}
