from __future__ import annotations

from typing import Any

from tools._shared import err


def format_price_comparison(
    findings: list[dict[str, Any]],
    template: str = "brief",
    comparison_title: str = "Bảng So Sánh Giá",
) -> dict[str, Any]:
    """Trình bày các mức giá và ưu đãi đã thu thập thành bảng so sánh hoàn chỉnh."""
    try:
        normalized_template = (template or "brief").strip().lower()
        if normalized_template not in {"brief", "detailed", "ranking"}:
            normalized_template = "brief"

        lines = [f"# {comparison_title}", f"Mẫu hiển thị: {normalized_template}", ""]

        if normalized_template == "ranking":
            lines.append("## Xếp hạng giá từ thấp đến cao:")
            for idx, item in enumerate(findings, 1):
                platform = item.get("platform", "N/A")
                price = item.get("price") or item.get("final_effective_price") or item.get("detail", "N/A")
                seller = item.get("seller") or item.get("seller_name", "")
                seller_str = f" ({seller})" if seller else ""
                lines.append(f"{idx}. {platform.upper()}{seller_str}: {price:,} VNĐ" if isinstance(price, (int, float)) else f"{idx}. {platform.upper()}: {price}")

        elif normalized_template == "detailed":
            lines.append("## Chi tiết giá & ưu đãi trên các nền tảng:")
            for item in findings:
                platform = item.get("platform", "N/A")
                lines.append(f"- Sàn: {platform.upper()}")
                lines.append(f"  • Người bán: {item.get('seller_name', item.get('seller', 'Chính hãng'))}")
                lines.append(f"  • Giá niêm yết: {item.get('listed_price', 'N/A')}")
                lines.append(f"  • Giảm giá voucher: {item.get('voucher_discount', 0)}")
                lines.append(f"  • Phí vận chuyển: {item.get('shipping_fee', 0)}")
                lines.append(f"  • Giá thanh toán cuối: {item.get('final_effective_price', item.get('price', 'N/A'))}")
                lines.append(f"  • Tình trạng kho: {item.get('stock_status', 'Còn hàng')}")
        else:
            lines.append("## Tóm tắt deal tốt nhất:")
            for item in findings:
                label = item.get("label", item.get("platform", "Nguồn"))
                detail = item.get("detail", item.get("final_effective_price", item.get("price", "")))
                status = item.get("status", "")
                status_str = f" [{status}]" if status else ""
                lines.append(f"- {label}: {detail}{status_str}")

        report_text = "\n".join(lines)
        return {
            "tool": "format_price_comparison",
            "template": normalized_template,
            "comparison_title": comparison_title,
            "items_count": len(findings),
            "formatted_report": report_text,
        }
    except Exception as exc:
        return err("format_price_comparison", exc)
