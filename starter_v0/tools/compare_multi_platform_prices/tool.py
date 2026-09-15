from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err


PRICES_FILE = ROOT / "deal_data" / "prices.json"


def compare_multi_platform_prices(
    product_name: str = "",
    variant: str = "",
    platforms: list[str] | None = None,
) -> dict[str, Any]:
    """Quét và so sánh giá giữa nhiều sàn (Shopee, Tiki, Lazada, CellphoneS) để tìm mức giá rẻ nhất."""
    try:
        data = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
        query_name = (product_name or "").strip().lower()
        variant_key = (variant or "").strip().lower()
        target_platforms = [p.strip().lower() for p in platforms] if platforms else ["shopee", "tiki", "lazada", "cellphones"]

        matches: list[dict[str, Any]] = []
        for item in data["prices"]:
            if item["platform"].lower() not in target_platforms:
                continue
            name_match = not query_name or (query_name in item["product_name"].lower() or query_name in item["product_id"].lower())
            variant_match = not variant_key or (variant_key in item["variant"].lower())
            if name_match and variant_match:
                matches.append(item)

        if not matches:
            return {
                "tool": "compare_multi_platform_prices",
                "product_name": product_name,
                "variant": variant,
                "error": "no_offers_found",
                "message": f"Không tìm thấy ưu đãi nào cho {product_name} trên các sàn được chọn.",
            }

        # Sort by final effective price ascending (lowest first)
        matches.sort(key=lambda x: x.get("final_effective_price", x.get("discount_price", 999999999)))
        best_deal = matches[0]

        return {
            "tool": "compare_multi_platform_prices",
            "product_name": product_name,
            "variant": variant,
            "offers_compared": len(matches),
            "best_deal": {
                "platform": best_deal["platform"],
                "seller": best_deal["seller_name"],
                "final_price": best_deal["final_effective_price"],
                "original_discount_price": best_deal["discount_price"],
                "voucher_discount": best_deal["voucher_discount"],
                "shipping_fee": best_deal["shipping_fee"],
            },
            "all_ranked_offers": matches,
        }
    except Exception as exc:
        return err("compare_multi_platform_prices", exc)
