from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Core shared tools
from .clarify.tool import ask_user

# DealHunter tools
from .query_platform_price.tool import query_platform_price
from .compare_multi_platform_prices.tool import compare_multi_platform_prices
from .search_product_catalog.tool import search_product_catalog
from .lookup_user_profile.tool import lookup_user_profile
from .format_price_comparison.tool import format_price_comparison
from .platform_policy.tool import search_platform_policy
from .set_price_alert.tool import set_price_alert
from .search_external_market_price.tool import search_external_market_price
from .detect_fake_discount_and_history.tool import detect_fake_discount_and_history

# Retained IT Helpdesk tools for reference/backward compatibility
from .check_service_status.tool import check_service_status
from .create_ticket.tool import create_ticket
from .format_incident_report.tool import format_incident_report
from .inspect_device.tool import inspect_device
from .lookup_user.tool import lookup_user
from .policy.tool import search_company_policy
from .search_kb.tool import search_kb
from .search_device_info.tool import search_device_info


TOOL_FUNCTIONS = {
    # DealHunter tools (Primary Domain)
    "clarify": ask_user,
    "query_platform_price": query_platform_price,
    "compare_multi_platform_prices": compare_multi_platform_prices,
    "search_product_catalog": search_product_catalog,
    "lookup_user_profile": lookup_user_profile,
    "format_price_comparison": format_price_comparison,
    "platform_policy": search_platform_policy,
    "set_price_alert": set_price_alert,
    "search_external_market_price": search_external_market_price,
    "detect_fake_discount_and_history": detect_fake_discount_and_history,

    # Reference IT Helpdesk tools
    "search_kb": search_kb,
    "search_device_info": search_device_info,
    "check_service_status": check_service_status,
    "inspect_device": inspect_device,
    "lookup_user": lookup_user,
    "format_incident_report": format_incident_report,
    "policy": search_company_policy,
    "create_ticket": create_ticket,
}


def load_tool_declarations(path: Path) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["tools"]


def to_openai_tools(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "type": "function",
        "function": {
            "name": item["name"],
            "description": item.get("description", ""),
            "parameters": item.get("parameters", {"type": "object", "properties": {}}),
        },
    } for item in declarations]
