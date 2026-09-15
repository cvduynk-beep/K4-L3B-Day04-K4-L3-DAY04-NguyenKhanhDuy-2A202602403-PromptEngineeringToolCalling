from __future__ import annotations

import os
import re
from typing import Any

from tools._shared import err


SENSITIVE_IDENTIFIER_PATTERN = re.compile(
    r"\b(?:USER-\d+|ALERT-\d+|09\d{8}|08\d{8}|03\d{8}|05\d{8})\b",
    re.IGNORECASE,
)


def search_external_market_price(
    manufacturer: str = "",
    model: str = "",
    query_type: str = "price",
    max_results: int = 3,
) -> dict[str, Any]:
    """Tìm thông tin giá tham chiếu quốc tế/chính hãng trên web. Chỉ truyền hãng và model công khai."""
    mfg_clean = (manufacturer or "").strip()
    model_clean = (model or "").strip()

    if not mfg_clean or not model_clean:
        return {
            "tool": "search_external_market_price",
            "error": "missing_parameters",
            "message": "Cần cung cấp đầy đủ hãng sản xuất (manufacturer) và tên model (model).",
        }

    combined = f"{mfg_clean} {model_clean}"
    if SENSITIVE_IDENTIFIER_PATTERN.search(combined):
        return {
            "tool": "search_external_market_price",
            "error": "restricted_identifier",
            "message": "Không được gửi mã người dùng, số điện thoại hoặc định danh nội bộ lên công cụ tìm kiếm web.",
        }

    # If Tavily API key is provided, execute external search; otherwise return deterministic reference
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if api_key:
        try:
            import requests
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": f"{mfg_clean} {model_clean} official price specs Vietnam",
                    "max_results": max_results,
                },
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "tool": "search_external_market_price",
                    "manufacturer": mfg_clean,
                    "model": model_clean,
                    "source": "tavily_live",
                    "results": data.get("results", []),
                }
        except Exception:
            pass

    # Deterministic mock response for consistent evaluation
    return {
        "tool": "search_external_market_price",
        "manufacturer": mfg_clean,
        "model": model_clean,
        "query_type": query_type,
        "source": "mock_market_feed",
        "reference_info": {
            "global_msrp_usd": 999 if "iphone" in model_clean.lower() else 1099 if "macbook" in model_clean.lower() else 399,
            "vietnam_suggested_retail_price": "28.990.000 VNĐ" if "iphone" in model_clean.lower() else "27.990.000 VNĐ" if "macbook" in model_clean.lower() else "8.490.000 VNĐ",
            "official_warranty": "12 tháng tại các trung tâm bảo hành ủy quyền",
        },
    }
