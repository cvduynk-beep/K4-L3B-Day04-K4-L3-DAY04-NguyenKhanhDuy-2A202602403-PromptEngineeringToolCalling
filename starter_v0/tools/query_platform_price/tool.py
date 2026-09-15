from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err


PRICES_FILE = ROOT / "deal_data" / "prices.json"


def query_platform_price(
    platform: str = "",
    product_name: str = "",
    variant: str = "",
) -> dict[str, Any]:
    """Tra cứu giá niêm yết và giá khuyến mãi của một sản phẩm trên sàn TMĐT cụ thể."""
    try:
        data = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
        platform_key = (platform or "").strip().lower()
        query_name = (product_name or "").strip().lower()
        variant_key = (variant or "").strip().lower()

        matches: list[dict[str, Any]] = []
        for item in data["prices"]:
            if item["platform"].lower() != platform_key:
                continue
            name_match = not query_name or (query_name in item["product_name"].lower() or query_name in item["product_id"].lower())
            variant_match = not variant_key or (variant_key in item["variant"].lower())
            if name_match and variant_match:
                matches.append(item)

        if matches:
            return {
                "tool": "query_platform_price",
                "platform": platform_key,
                "product_name": product_name,
                "variant": variant,
                "matches": matches,
                "count": len(matches),
            }

        return {
            "tool": "query_platform_price",
            "platform": platform_key,
            "product_name": product_name,
            "variant": variant,
            "error": "not_found",
            "message": f"Không tìm thấy sản phẩm {product_name} trên sàn {platform_key}",
            "available_platforms": ["shopee", "tiki", "lazada", "cellphones"],
        }
    except Exception as exc:
        return err("query_platform_price", exc)
