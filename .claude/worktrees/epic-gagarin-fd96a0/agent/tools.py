"""
Smith Asset Group — Notion Tool Implementations

All Notion calls use the REST API directly (no SDK dependency).
Requires: NOTION_API_KEY in environment.
"""

import os
import json
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional

import config

NOTION_VERSION = "2022-06-28"


def _headers() -> dict:
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        raise EnvironmentError("NOTION_API_KEY is not set in environment.")
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _notion_get(path: str) -> dict:
    r = requests.get(f"https://api.notion.com/v1{path}", headers=_headers())
    r.raise_for_status()
    return r.json()


def _notion_post(path: str, body: dict) -> dict:
    r = requests.post(f"https://api.notion.com/v1{path}", headers=_headers(), json=body)
    r.raise_for_status()
    return r.json()


def _notion_patch(path: str, body: dict) -> dict:
    r = requests.patch(f"https://api.notion.com/v1{path}", headers=_headers(), json=body)
    r.raise_for_status()
    return r.json()


# ─── Property builders ───────────────────────────────────────────────────────

def _title(value: str) -> dict:
    return {"title": [{"text": {"content": value}}]}

def _rich_text(value: str) -> dict:
    return {"rich_text": [{"text": {"content": value}}]}

def _select(value: str) -> dict:
    return {"select": {"name": value}}

def _number(value: float) -> dict:
    return {"number": value}

def _phone(value: str) -> dict:
    return {"phone_number": value}

def _email_prop(value: str) -> dict:
    return {"email": value}

def _date_prop(value: str) -> dict:
    return {"date": {"start": value}}

def _checkbox(value: bool) -> dict:
    return {"checkbox": value}


# ─── Property readers ────────────────────────────────────────────────────────

def _read_prop(page: dict, name: str) -> str | int | float | bool | None:
    props = page.get("properties", {})
    prop = props.get(name)
    if not prop:
        return None
    t = prop["type"]
    if t == "title":
        parts = prop["title"]
        return parts[0]["plain_text"] if parts else None
    if t == "rich_text":
        parts = prop["rich_text"]
        return parts[0]["plain_text"] if parts else None
    if t == "select":
        s = prop["select"]
        return s["name"] if s else None
    if t == "number":
        return prop["number"]
    if t == "phone_number":
        return prop["phone_number"]
    if t == "email":
        return prop["email"]
    if t == "checkbox":
        return prop["checkbox"]
    if t == "date":
        d = prop["date"]
        return d["start"] if d else None
    if t == "url":
        return prop["url"]
    return None


def _flatten_page(page: dict) -> dict:
    """Return a plain dict of a Notion page's property values."""
    return {
        "id": page["id"],
        "url": page.get("url"),
        **{name: _read_prop(page, name) for name in page.get("properties", {})},
    }


# ─── Live Leads ──────────────────────────────────────────────────────────────

def get_new_leads() -> list[dict]:
    """Return all leads with Status = '🖕 New'."""
    body = {
        "filter": {
            "property": "Status",
            "select": {"equals": "🖕 New"},
        },
        "sorts": [{"timestamp": "created_time", "direction": "descending"}],
    }
    result = _notion_post(f"/databases/{config.DB_LIVE_LEADS}/query", body)
    return [_flatten_page(p) for p in result.get("results", [])]


def get_all_leads(limit: int = 50) -> list[dict]:
    """Return the most recent leads regardless of status."""
    body = {
        "sorts": [{"timestamp": "created_time", "direction": "descending"}],
        "page_size": min(limit, 100),
    }
    result = _notion_post(f"/databases/{config.DB_LIVE_LEADS}/query", body)
    return [_flatten_page(p) for p in result.get("results", [])]


def get_lead(page_id: str) -> dict:
    """Return a single lead by Notion page ID."""
    page = _notion_get(f"/pages/{page_id}")
    return _flatten_page(page)


def update_lead(page_id: str, updates: dict) -> dict:
    """
    Update any subset of lead fields.
    `updates` keys match config.LEAD_PROPS keys (snake_case names).
    Example: update_lead(id, {"status": "Contacted Partner", "contractor_note": "Sent to John Panos"})
    """
    prop_map = {}
    for key, value in updates.items():
        display = config.LEAD_PROPS.get(key)
        if not display:
            continue
        if key == "name":
            prop_map[display] = _title(value)
        elif key in ("message", "zip_code", "contractor_note", "red_flags"):
            prop_map[display] = _rich_text(str(value))
        elif key in ("source", "status", "service", "lead_grade",
                     "est_job_value", "territory_status", "recommended_action"):
            prop_map[display] = _select(str(value))
        elif key == "urgency_score":
            prop_map[display] = _number(int(value))
        elif key == "phone":
            prop_map[display] = _phone(str(value))

    page = _notion_patch(f"/pages/{page_id}", {"properties": prop_map})
    return _flatten_page(page)


def route_lead_to_partner(lead_page_id: str, contractor_name: str, note: str = "") -> dict:
    """
    Mark lead as 'Contacted Partner' and log which contractor received it.
    Returns the updated lead page.
    """
    note_text = f"Routed to {contractor_name}." + (f" {note}" if note else "")
    return update_lead(lead_page_id, {
        "status": "Contacted Partner",
        "contractor_note": note_text,
    })


# ─── Partner Directory ───────────────────────────────────────────────────────

def get_partners(assigned_only: bool = False) -> list[dict]:
    """Return all partners, optionally filtering to only assigned ones."""
    body: dict = {"sorts": [{"property": "Priority", "direction": "ascending"}]}
    if assigned_only:
        body["filter"] = {
            "property": "Assigned Partner",
            "checkbox": {"equals": True},
        }
    result = _notion_post(f"/databases/{config.DB_PARTNER_DIR}/query", body)
    return [_flatten_page(p) for p in result.get("results", [])]


def get_partner(page_id: str) -> dict:
    return _flatten_page(_notion_get(f"/pages/{page_id}"))


def get_partner_by_name(name: str) -> Optional[dict]:
    """Case-insensitive search for a partner by business name."""
    partners = get_partners()
    name_lower = name.lower()
    for p in partners:
        pname = p.get("Name") or ""
        if name_lower in pname.lower():
            return p
    return None


def update_partner(page_id: str, updates: dict) -> dict:
    """
    Update any subset of partner fields.
    `updates` keys match config.PARTNER_PROPS keys (snake_case).
    """
    prop_map = {}
    for key, value in updates.items():
        display = config.PARTNER_PROPS.get(key)
        if not display:
            continue
        if key == "name":
            prop_map[display] = _title(value)
        elif key in ("owner_name", "notes"):
            prop_map[display] = _rich_text(str(value))
        elif key in ("status", "priority", "source"):
            prop_map[display] = _select(str(value))
        elif key == "phone":
            prop_map[display] = _phone(str(value))
        elif key == "email":
            prop_map[display] = _email_prop(str(value))
        elif key == "assigned_partner":
            prop_map[display] = _checkbox(bool(value))
        elif key == "last_contacted":
            prop_map[display] = _date_prop(str(value))
        elif key == "lead_source_url":
            prop_map[display] = {"url": str(value)}

    page = _notion_patch(f"/pages/{page_id}", {"properties": prop_map})
    return _flatten_page(page)


def mark_partner_as_client(page_id: str) -> dict:
    """Set partner status to Client (retainer closed)."""
    return update_partner(page_id, {"status": "Client"})


def mark_partner_committed(page_id: str) -> dict:
    return update_partner(page_id, {"status": "Committed"})


# ─── Ad Metrics ──────────────────────────────────────────────────────────────

def get_ad_metrics(days: int = 7) -> list[dict]:
    """Return ad metric rows from the last N days."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    body = {
        "filter": {
            "property": "Date",
            "date": {"on_or_after": cutoff},
        },
        "sorts": [{"property": "Date", "direction": "descending"}],
    }
    result = _notion_post(f"/databases/{config.DB_AD_METRICS}/query", body)
    return [_flatten_page(p) for p in result.get("results", [])]


def log_ad_metric(
    date: str,
    platform: str,
    campaign: str,
    spend: float,
    impressions: int,
    clicks: int,
    conversions: int,
    avg_cpc: float,
    notes: str = "",
) -> dict:
    """
    Create a new row in the Ad Metrics DB.
    `date` format: YYYY-MM-DD
    `platform`: one of 'Google Ads' | 'Meta' | 'CallRail'
    """
    ctr = round(clicks / impressions * 100, 2) if impressions else 0
    cpl = round(spend / conversions, 2) if conversions else 0
    props = {
        "Date":        _date_prop(date),
        "Platform":    _select(platform),
        "Campaign":    _rich_text(campaign),
        "Spend":       _number(spend),
        "Impressions": _number(impressions),
        "Clicks":      _number(clicks),
        "CTR":         _number(ctr),
        "Conversions": _number(conversions),
        "CPL":         _number(cpl),
        "Avg CPC":     _number(avg_cpc),
        "Notes":       _rich_text(notes),
    }
    page = _notion_post("/pages", {
        "parent": {"database_id": config.DB_AD_METRICS},
        "properties": props,
    })
    return _flatten_page(page)


def evaluate_cpl(spend: float, conversions: int) -> dict:
    """Return kill-rule evaluation based on CPL thresholds."""
    if conversions == 0:
        cpl = None
        if spend >= config.KILL_SPEND_NO_LEADS:
            action = "KILL — $100+ spend with zero leads. Test new copy or image."
        else:
            action = f"WATCH — ${spend:.2f} spent, no conversions yet. Kill at $100."
    else:
        cpl = round(spend / conversions, 2)
        if cpl < config.CPL_HOLD_THRESHOLD:
            action = f"SCALE — CPL ${cpl:.2f} is excellent. Hold or increase to $25/day."
        elif cpl <= config.CPL_OK_THRESHOLD:
            action = f"ACCEPTABLE — CPL ${cpl:.2f} is industry-average. Test new creative variation."
        else:
            action = f"KILL — CPL ${cpl:.2f} exceeds $50 threshold. Kill ad set."
    return {"spend": spend, "conversions": conversions, "cpl": cpl, "action": action}


# ─── Finances ────────────────────────────────────────────────────────────────

def get_finances(category: Optional[str] = None) -> list[dict]:
    """Return finance rows, optionally filtered by category."""
    body: dict = {"sorts": [{"property": "Date", "direction": "descending"}]}
    if category:
        body["filter"] = {
            "property": "Category",
            "select": {"equals": category},
        }
    result = _notion_post(f"/databases/{config.DB_FINANCES}/query", body)
    return [_flatten_page(p) for p in result.get("results", [])]


def log_finance(
    title: str,
    date: str,
    category: str,
    amount: float,
    platform: str = "",
    notes: str = "",
) -> dict:
    """
    Create a new P&L row.
    `amount`: positive = revenue, negative = expense.
    `category`: see config.FINANCE_CATEGORIES
    """
    props = {
        "Transaction Title": _title(title),
        "Date":              _date_prop(date),
        "Category":          _select(category),
        "Amount":            _number(amount),
        "Platform":          _rich_text(platform),
        "Notes":             _rich_text(notes),
    }
    page = _notion_post("/pages", {
        "parent": {"database_id": config.DB_FINANCES},
        "properties": props,
    })
    return _flatten_page(page)


def get_pl_summary() -> dict:
    """Return total revenue, total expenses, and net P&L."""
    rows = get_finances()
    revenue  = sum(r.get("Amount") or 0 for r in rows if (r.get("Amount") or 0) > 0)
    expenses = sum(r.get("Amount") or 0 for r in rows if (r.get("Amount") or 0) < 0)
    return {
        "revenue":  round(revenue, 2),
        "expenses": round(expenses, 2),
        "net":      round(revenue + expenses, 2),
        "rows":     len(rows),
    }


# ─── Dashboard / status ──────────────────────────────────────────────────────

def get_dashboard_summary() -> dict:
    """Return a high-level snapshot of business state for the agent."""
    new_leads   = get_new_leads()
    partners    = get_partners()
    assigned    = [p for p in partners if p.get("Assigned Partner")]
    clients     = [p for p in partners if p.get("Status") == "Client"]
    metrics_7d  = get_ad_metrics(days=7)
    pl          = get_pl_summary()

    recent_spend = sum(r.get("Spend") or 0 for r in metrics_7d)
    recent_leads = sum(int(r.get("Conversions") or 0) for r in metrics_7d)

    return {
        "new_leads_pending_routing": len(new_leads),
        "new_lead_details": new_leads[:5],
        "total_partners_researched": len(partners),
        "assigned_partners": len(assigned),
        "clients_on_retainer": len(clients),
        "ad_spend_last_7d": round(recent_spend, 2),
        "ad_leads_last_7d": recent_leads,
        "pl_summary": pl,
        "week1_checklist": {
            "market_selected": True,
            "domain_registered": True,
            "site_live": True,
            "contractor_list_built": True,
            "noah_outreach_started": True,
            "make_pipeline_live": True,
            "google_ads_live": True,
            "advertiser_verification": "PENDING",
            "first_committed_partner": len(clients) > 0,
            "first_lead_delivered": recent_leads > 0,
            "first_retainer_closed": len(clients) > 0,
        },
    }


def classify_zip(zip_code: str) -> str:
    """Return territory classification for a 5-digit zip."""
    z = str(zip_code).strip()
    if z in config.IN_TARGET_ZIPS:
        return "In Target Zone"
    if z in config.EDGE_ZIPS:
        return "Edge Zone"
    if z.startswith("84") or z.startswith("83"):
        return "Edge Zone"
    return "Outside Zone"


# ─── Tool definitions for Anthropic tool_use ─────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "get_dashboard_summary",
        "description": (
            "Return a high-level snapshot of the Smith Asset Group business: "
            "unrouted leads, partner counts, 7-day ad spend, and P&L summary. "
            "Use this first when the user asks 'what's the status' or 'what's happening.'"
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_new_leads",
        "description": "Return all leads currently in 'New' status that haven't been routed to a contractor yet.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_all_leads",
        "description": "Return the most recent leads from the Live Leads DB regardless of status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max rows to return (default 50, max 100)", "default": 50}
            },
            "required": [],
        },
    },
    {
        "name": "get_lead",
        "description": "Return full details for a single lead by its Notion page ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "string", "description": "Notion page ID of the lead"}
            },
            "required": ["page_id"],
        },
    },
    {
        "name": "update_lead",
        "description": (
            "Update one or more fields on a lead. Common uses: mark as contacted, "
            "add a contractor note, or update territory/grade after manual review."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "string"},
                "updates": {
                    "type": "object",
                    "description": (
                        "Key-value pairs using snake_case field names from config.LEAD_PROPS. "
                        "E.g. {\"status\": \"Contacted Partner\", \"contractor_note\": \"Sent to John Panos\"}"
                    ),
                },
            },
            "required": ["page_id", "updates"],
        },
    },
    {
        "name": "route_lead_to_partner",
        "description": (
            "Route a lead to a named contractor: sets Status → 'Contacted Partner' "
            "and writes a routing note. Use after confirming which contractor should receive the lead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_page_id":    {"type": "string"},
                "contractor_name": {"type": "string", "description": "Business name of the contractor"},
                "note":            {"type": "string", "description": "Optional extra note", "default": ""},
            },
            "required": ["lead_page_id", "contractor_name"],
        },
    },
    {
        "name": "get_partners",
        "description": "Return all contractor partners from the Partner Directory. Set assigned_only=true to see only active routing partners.",
        "input_schema": {
            "type": "object",
            "properties": {
                "assigned_only": {"type": "boolean", "default": False}
            },
            "required": [],
        },
    },
    {
        "name": "update_partner",
        "description": "Update one or more fields on a contractor partner record.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "string"},
                "updates": {
                    "type": "object",
                    "description": "Key-value pairs using snake_case field names from config.PARTNER_PROPS.",
                },
            },
            "required": ["page_id", "updates"],
        },
    },
    {
        "name": "get_ad_metrics",
        "description": "Return ad performance rows from the last N days.",
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Number of days to look back (default 7)", "default": 7}
            },
            "required": [],
        },
    },
    {
        "name": "log_ad_metric",
        "description": "Manually log a daily ad performance row to the Ad Metrics DB.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date":        {"type": "string", "description": "YYYY-MM-DD"},
                "platform":    {"type": "string", "description": "Google Ads | Meta | CallRail"},
                "campaign":    {"type": "string"},
                "spend":       {"type": "number", "description": "USD"},
                "impressions": {"type": "integer"},
                "clicks":      {"type": "integer"},
                "conversions": {"type": "integer"},
                "avg_cpc":     {"type": "number"},
                "notes":       {"type": "string", "default": ""},
            },
            "required": ["date", "platform", "campaign", "spend", "impressions", "clicks", "conversions", "avg_cpc"],
        },
    },
    {
        "name": "evaluate_cpl",
        "description": "Apply the Smith Asset Group CPL kill rules and return the recommended action.",
        "input_schema": {
            "type": "object",
            "properties": {
                "spend":       {"type": "number", "description": "Total ad spend in USD"},
                "conversions": {"type": "integer", "description": "Number of leads generated"},
            },
            "required": ["spend", "conversions"],
        },
    },
    {
        "name": "get_pl_summary",
        "description": "Return total revenue, expenses, and net P&L from the Finances DB.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "log_finance",
        "description": "Create a new transaction row in the Finances & P&L DB.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title":    {"type": "string"},
                "date":     {"type": "string", "description": "YYYY-MM-DD"},
                "category": {"type": "string", "description": "Ad Spend | Tool/Software | Domain | Legal | Revenue | Misc"},
                "amount":   {"type": "number", "description": "Positive = revenue, negative = expense"},
                "platform": {"type": "string", "default": ""},
                "notes":    {"type": "string", "default": ""},
            },
            "required": ["title", "date", "category", "amount"],
        },
    },
    {
        "name": "classify_zip",
        "description": "Return the territory classification (In Target Zone / Edge Zone / Outside Zone) for a ZIP code.",
        "input_schema": {
            "type": "object",
            "properties": {
                "zip_code": {"type": "string"}
            },
            "required": ["zip_code"],
        },
    },
]


# ─── Tool dispatcher ─────────────────────────────────────────────────────────

def dispatch(tool_name: str, tool_input: dict):
    """Call the correct Python function for a given tool name + input dict."""
    if tool_name == "get_dashboard_summary":
        return get_dashboard_summary()
    if tool_name == "get_new_leads":
        return get_new_leads()
    if tool_name == "get_all_leads":
        return get_all_leads(tool_input.get("limit", 50))
    if tool_name == "get_lead":
        return get_lead(tool_input["page_id"])
    if tool_name == "update_lead":
        return update_lead(tool_input["page_id"], tool_input["updates"])
    if tool_name == "route_lead_to_partner":
        return route_lead_to_partner(
            tool_input["lead_page_id"],
            tool_input["contractor_name"],
            tool_input.get("note", ""),
        )
    if tool_name == "get_partners":
        return get_partners(tool_input.get("assigned_only", False))
    if tool_name == "update_partner":
        return update_partner(tool_input["page_id"], tool_input["updates"])
    if tool_name == "get_ad_metrics":
        return get_ad_metrics(tool_input.get("days", 7))
    if tool_name == "log_ad_metric":
        return log_ad_metric(**tool_input)
    if tool_name == "evaluate_cpl":
        return evaluate_cpl(tool_input["spend"], tool_input["conversions"])
    if tool_name == "get_pl_summary":
        return get_pl_summary()
    if tool_name == "log_finance":
        return log_finance(**tool_input)
    if tool_name == "classify_zip":
        return classify_zip(tool_input["zip_code"])
    raise ValueError(f"Unknown tool: {tool_name}")
