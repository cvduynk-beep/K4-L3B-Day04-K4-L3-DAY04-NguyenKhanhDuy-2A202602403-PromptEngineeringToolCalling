from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

from tools._shared import ROOT, err


ALERT_DIR = ROOT / "alerts"
SENSITIVE_DATA_PATTERN = re.compile(
    r"\b(?:password|passwd|token|api[ _-]?key|mfa|otp|cvv|credit[ _-]?card|stk|atm)(?:\s*[:=]\s*|\s+(?:is|la|là)\s+)\S+",
    re.IGNORECASE,
)


def set_price_alert(
    product_name: str = "",
    target_price: int = 0,
    variant: str = "",
    user_id: str = "",
    confirmed: bool = False,
) -> dict[str, Any]:
    """Tạo thông báo theo dõi giá khi sản phẩm giảm xuống dưới ngưỡng mong muốn. Bắt buộc có xác nhận rõ ràng."""
    normalized_product = (product_name or "").strip()
    if not normalized_product:
        return {"tool": "set_price_alert", "error": "missing_product_name"}

    if not isinstance(target_price, (int, float)) or target_price <= 0:
        return {"tool": "set_price_alert", "error": "invalid_target_price", "message": "Target price must be a positive integer."}

    target_price_int = int(target_price)

    # Check for credentials or sensitive payment details
    check_str = f"{normalized_product} {variant} {user_id}"
    if SENSITIVE_DATA_PATTERN.search(check_str):
        return {
            "tool": "set_price_alert",
            "error": "restricted_sensitive_data",
            "message": "Không được đưa thông tin thanh toán, thẻ tín dụng, CVV hoặc mật khẩu vào yêu cầu đặt thông báo giá.",
        }

    if confirmed is not True:
        return {
            "tool": "set_price_alert",
            "status": "needs_confirmation",
            "message": f"Bạn có chắc chắn muốn đặt thông báo khi '{normalized_product}' ({variant or 'bản chuẩn'}) giảm xuống dưới {target_price_int:,} VNĐ không? Vui lòng xác nhận.",
        }

    try:
        now = datetime.now(timezone.utc)
        seed = f"{now.isoformat()}|{normalized_product}|{target_price_int}|{variant}|{user_id}"
        alert_id = "ALERT-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()

        payload = {
            "alert_id": alert_id,
            "product_name": normalized_product,
            "target_price": target_price_int,
            "variant": variant or "Standard",
            "user_id": user_id or "ANONYMOUS",
            "created_at": now.isoformat(),
            "status": "active",
        }

        ALERT_DIR.mkdir(parents=True, exist_ok=True)
        path = ALERT_DIR / f"{alert_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "tool": "set_price_alert",
            "status": "created",
            "alert_id": alert_id,
            "target_price": target_price_int,
            "path": str(path),
        }
    except Exception as exc:
        return err("set_price_alert", exc)
