from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err, terms


PRODUCTS_FILE = ROOT / "deal_data" / "products.json"


def search_product_catalog(
    query: str = "",
    category: str = "all",
    top_k: int = 3,
) -> dict[str, Any]:
    """Tìm kiếm thông số kỹ thuật, model chuẩn và danh mục trong catalog sản phẩm chính thức."""
    try:
        data = json.loads(PRODUCTS_FILE.read_text(encoding="utf-8"))
        category_key = (category or "all").strip().lower()
        query_terms = terms(query)

        scored: list[tuple[int, dict[str, Any]]] = []
        for prod in data["products"]:
            if category_key not in {"all", ""} and prod["category"].lower() != category_key:
                continue

            text_blob = f"{prod['name']} {prod['brand']} {prod['specs']} {' '.join(prod.get('variants', []))}"
            prod_terms = terms(text_blob)
            overlap = len(query_terms & prod_terms) if query_terms else 1
            if overlap > 0 or not query_terms:
                scored.append((overlap, prod))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored[:max(1, min(top_k, 5))]]

        return {
            "tool": "search_product_catalog",
            "query": query,
            "category": category_key,
            "total_matches": len(results),
            "products": results,
        }
    except Exception as exc:
        return err("search_product_catalog", exc)
