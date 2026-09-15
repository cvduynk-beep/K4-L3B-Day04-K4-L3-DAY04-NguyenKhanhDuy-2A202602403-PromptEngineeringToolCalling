from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err


HISTORY_FILE = ROOT / "deal_data" / "price_history.json"


def detect_fake_discount_and_history(
    product_name: str = "",
    current_price: int = 0,
    platform: str = "",
) -> dict[str, Any]:
    """Phát hiện giảm giá ảo và phân tích biến động giá lịch sử 90 ngày của sản phẩm (BONUS TOOL)."""
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        query = (product_name or "").strip().lower()

        matched_history = None
        for item in data["products_history"]:
            if query in item["product_name"].lower() or query in item["product_id"].lower():
                matched_history = item
                break

        if not matched_history:
            return {
                "tool": "detect_fake_discount_and_history",
                "product_name": product_name,
                "current_price": current_price,
                "status": "no_history_record",
                "recommendation": "UNKNOWN",
                "analysis": f"Chưa có dữ liệu biến động giá 90 ngày cho sản phẩm '{product_name}'.",
            }

        all_time_low = matched_history["all_time_low"]
        avg_price = matched_history["average_90d"]

        # Evaluate current price against historical metrics
        if current_price and current_price <= all_time_low:
            recommendation = "REAL_DEAL"
            verdict = "Giá chạm đáy lịch sử! Đây là cơ hội mua tốt nhất trong 90 ngày qua."
        elif matched_history.get("recent_price_inflated"):
            recommendation = "FAKE_DISCOUNT"
            verdict = "CẢNH BÁO GIẢM GIÁ ẢO: Shop đã nâng giá niêm yết lên cao rồi mới tạo giảm giá. Giá thực tế không rẻ hơn ngày thường."
        elif current_price and current_price < avg_price:
            recommendation = "GOOD_PRICE"
            verdict = f"Giá hiện tại ({current_price:,}đ) thấp hơn mức trung bình 90 ngày ({avg_price:,}đ)."
        else:
            recommendation = matched_history.get("recommendation", "NORMAL_PRICE")
            verdict = matched_history.get("analysis", "Mức giá ở mức bình thường của thị trường.")

        return {
            "tool": "detect_fake_discount_and_history",
            "product_name": matched_history["product_name"],
            "current_price": current_price,
            "platform": platform or "multi_platform",
            "all_time_low": all_time_low,
            "all_time_high": matched_history["all_time_high"],
            "average_90d": avg_price,
            "recommendation": recommendation,
            "verdict": verdict,
        }
    except Exception as exc:
        return err("detect_fake_discount_and_history", exc)
