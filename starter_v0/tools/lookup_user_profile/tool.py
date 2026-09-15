from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err


USERS_FILE = ROOT / "deal_data" / "users.json"


def lookup_user_profile(user_id: str = "") -> dict[str, Any]:
    """Tra cứu hồ sơ khách hàng, hạng thành viên, quyền lợi freeship và các voucher đã lưu."""
    try:
        data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        user_key = (user_id or "").strip().upper()

        for user in data["users"]:
            if user["user_id"].upper() == user_key:
                return {
                    "tool": "lookup_user_profile",
                    "user_id": user_key,
                    "profile": user,
                }

        return {
            "tool": "lookup_user_profile",
            "user_id": user_key,
            "error": "not_found",
            "message": f"Không tìm thấy người dùng có mã {user_key}",
            "available_users": [u["user_id"] for u in data["users"]],
        }
    except Exception as exc:
        return err("lookup_user_profile", exc)
