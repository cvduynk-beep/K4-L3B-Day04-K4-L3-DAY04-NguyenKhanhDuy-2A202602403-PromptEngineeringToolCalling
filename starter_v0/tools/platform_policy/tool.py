from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err, terms


POLICIES_FILE = ROOT / "deal_data" / "policies.json"


def search_platform_policy(
    query: str = "",
    policy_area: str = "all",
    top_k: int = 3,
) -> dict[str, Any]:
    """Tìm kiếm chính sách bảo hành, cam kết giá rẻ và đổi trả của các sàn thương mại điện tử."""
    try:
        data = json.loads(POLICIES_FILE.read_text(encoding="utf-8"))
        area_key = (policy_area or "all").strip().lower()
        query_terms = terms(query)

        scored: list[tuple[int, dict[str, Any]]] = []
        for policy in data["policies"]:
            if area_key not in {"all", ""} and policy["policy_area"].lower() != area_key:
                continue

            text_blob = f"{policy['title']} {policy['content']} {policy['conditions']}"
            pol_terms = terms(text_blob)
            overlap = len(query_terms & pol_terms) if query_terms else 1
            if overlap > 0 or not query_terms:
                scored.append((overlap, policy))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored[:max(1, min(top_k, 5))]]

        return {
            "tool": "platform_policy",
            "query": query,
            "policy_area": area_key,
            "total_matches": len(results),
            "policies": results,
        }
    except Exception as exc:
        return err("platform_policy", exc)
