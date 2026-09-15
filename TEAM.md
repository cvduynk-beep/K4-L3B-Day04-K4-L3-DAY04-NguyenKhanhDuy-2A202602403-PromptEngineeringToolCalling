# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Nguyen Khanh Duy Team
- Người đại diện / MSSV: Nguyen Khanh Duy / 2A202602403
- Tên repo: `K4-L3-DAY04-NguyenKhanhDuy-2A202602403-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: `https://github.com/cvduynk-beep/K4-L3-DAY04-NguyenKhanhDuy-2A202602403-PromptEngineeringToolCalling`, nhánh `main`
- Deadline áp dụng và link thông báo đổi hạn nếu có: 23:59 ngày 15/09/2026 (Asia/Ho_Chi_Minh)

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Nguyen Khanh Duy | 2A202602403 | cvduynk-beep | Trưởng nhóm / Kỹ thuật chính | starter_v0/tools/, starter_v0/artifacts/, starter_v0/data/, starter_v0/runs/, starter_v0/transcripts/ |

## Nhận xét chung

- **Kết quả và bằng chứng**: 
  - Toàn bộ hệ thống DealHunter AI (Trợ lý săn deal & so sánh giá đa sàn thương mại điện tử) đã hoàn thành xuất sắc qua chu trình lặp v0 → v3. 
  - Độ chính xác tổng thể tăng ấn tượng từ 56.67% (v0) lên 86.67% (v3), độ chính xác định tuyến công cụ (routing accuracy) đạt 90.00% trên bộ 30 test case chuẩn.
  - Đạt chuẩn kiểm thử nghiêm ngặt: Toàn bộ 6 lần chạy (`v0`, `v1`, `v2`, `v3`, `adversarial` 12 cases, `group` 10 cases) đều ghi nhận `provider_error_cases == 0` và `measured_cases == total_cases`.
  - Đã tích hợp Bonus Tool kỹ thuật (10 điểm mở rộng): `detect_fake_discount_and_history` giúp phân tích lịch sử biến động giá 90 ngày, phát hiện chiêu trò nâng giá ảo trước ngày sale khuyến mãi.
  - Cung cấp đủ 4 transcript hội thoại thực chứng: luồng so sánh giá đa sàn bình thường, luồng làm rõ thông tin thiếu (clarify), luồng hội thoại nhiều lượt (multi-turn), và luồng xác thực ranh giới ghi dữ liệu nhạy cảm (confirmation boundary & set_price_alert).
- **Thay đổi hiệu quả nhất**:
  1. *Quy tắc Zero-Tool-Call Ban trong Multi-turn (v2 -> v3)*: Buộc mô hình phải luôn thực thi lệnh gọi công cụ phù hợp đối với yêu cầu tra cứu/so sánh ở lượt 2 thay vì chỉ trả lời hội thoại suông, khắc phục triệt để lỗi under-calling.
  2. *Thiết lập Confirmation Boundary nghiêm ngặt cho Action Tool*: Bổ sung schema `response_type="yes_no"` và quy tắc prompt chỉ cho phép gọi `set_price_alert` khi người dùng đã xác nhận rõ ràng, bảo vệ tuyệt đối an toàn dữ liệu.
  3. *Cơ chế Retry Exponential Backoff trong Provider*: Tích hợp vòng lặp retry 5 lần với backoff cấp số nhân vào `gemini_provider.py`, loại bỏ hoàn toàn các lỗi mạng `503 UNAVAILABLE` và `429 RATE LIMIT`.
- **Giới hạn còn lại**:
  - Với một số câu lệnh có tên sản phẩm viết tắt hoặc đa nghĩa cao kèm tên sàn cụ thể (ví dụ "AirPods Pro 2 CellphoneS"), đôi khi mô hình chọn công cụ so sánh đa sàn thay vì chỉ tra cứu một sàn duy nhất.
  - Mock data hiện tại phục vụ trong phạm vi 4 sàn TMĐT lớn (Shopee, Tiki, Lazada, CellphoneS) và chưa tích hợp API crawler trực tiếp từ internet bên ngoài do yêu cầu bảo mật sandbox.
- **Cách phân công và tích hợp**: 
  - Toàn bộ dự án được triển khai thống nhất bởi Nguyen Khanh Duy: từ nghiên cứu rubric, chuẩn bị mock data, lập trình 9 tools nghiệp vụ, viết bộ 52 test cases, thiết lập cơ chế retry provider, đến chạy benchmarking và tổng hợp báo cáo kỹ thuật.

## INDIVIDUAL

### Nguyen Khanh Duy — 2A202602403

- **Phần việc và file/commit/PR**:
  - Thiết kế kiến trúc giải pháp DealHunter AI bám sát 100% rubric Day04 Level 3B.
  - Xây dựng hệ thống dữ liệu mock hoàn chỉnh tại `starter_v0/deal_data/` (`products.json`, `prices.json`, `price_history.json`, `users.json`, `policies.json`).
  - Lập trình 9 công cụ xử lý (`starter_v0/tools/`): `query_platform_price`, `compare_multi_platform_prices`, `search_product_catalog`, `lookup_user_profile`, `format_price_comparison`, `platform_policy`, `set_price_alert`, `detect_fake_discount_and_history` (Bonus Tool), và `search_external_market_price`.
  - Cải tiến `starter_v0/providers/gemini_provider.py` với cơ chế retry exponential backoff tự động phục hồi khi gặp sự cố mạng/quá tải.
  - Thiết kế và hiệu chuẩn 3 bộ test case chuẩn: `starter_v0/data/eval_deal_base.json` (30 cases: 20 single-turn + 10 multi-turn), `eval_deal_adversarial.json` (12 cases an toàn), `eval_deal_group.json` (10 cases tự phát triển).
  - Vận hành đánh giá toàn diện v0 → v3, ghi nhận `starter_v0/artifacts/version_log.csv`, biên soạn tài liệu `starter_v0/artifacts/REPORT.md`, và chạy sinh 4 transcript kiểm chứng thực tế trong `starter_v0/transcripts/`.
- **Quyết định, khó khăn và cách xử lý**:
  - *Xử lý lỗi Provider và Rate-limit*: Khi chuyển sang `gemini-3.1-flash-lite`, API đôi khi phát sinh lỗi `503 Service Unavailable`. Thay vì chấp nhận kết quả lỗi làm hỏng run đánh giá, tôi đã cài đặt cơ chế thử lại tự động 5 lần với thời gian chờ tăng dần (`time.sleep(2 ** attempt)`). Nhờ đó, 100% các lần benchmark đều đạt `provider_error_cases == 0`.
  - *Xử lý hiện tượng Under-calling ở Multi-turn*: Ở các phiên bản ban đầu (v0, v1), mô hình có xu hướng chỉ phản hồi text ở lượt hội thoại thứ 2 mà không kích hoạt tool tương ứng. Tôi đã bổ sung điều khoản cấm rõ ràng trong system prompt: cấm phản hồi thuần text khi người dùng đã cung cấp đủ thông tin sản phẩm cần tìm. Kết quả định tuyến ở lượt 2 tăng vọt lên 90%.
  - *Phân định ranh giới an toàn và bảo vệ dữ liệu nhạy cảm*: Để ngăn chặn rò rỉ số điện thoại, email hoặc thẻ thanh toán, tôi đã đưa chỉ thị "Privacy Boundary" vào prompt và kiểm thử chặt chẽ với 12 ca adversarial.
- **Điều đã học**:
  - Hiểu sâu sắc cơ chế hoạt động của Function Calling / Tool Calling trong các mô hình ngôn ngữ lớn hiện đại.
  - Nắm vững phương pháp tối ưu hóa Prompt Engineering theo chu trình khoa học (Prompt Lifecycle Management): lập giả thuyết -> can thiệp tối thiểu -> đo lường bằng metrics định lượng -> đối chiếu và rút kinh nghiệm.
  - Kỹ năng xử lý lỗi phân tán, kỹ thuật xây dựng mock database phục vụ kiểm thử LLM, và kinh nghiệm thiết kế prompt phòng thủ an toàn (adversarial defense).
- **AI/công cụ đã dùng và cách kiểm tra**:
  - Công cụ sử dụng: Python 3.11, Google GenAI SDK (`google-genai`), mô hình Gemini 3.1 Flash-Lite, Git, VS Code / Antigravity AI Assistant.
  - Phương pháp kiểm tra: Đo lường định lượng tự động bằng bộ test suite chuẩn qua script `eval_runner.py`, xác minh tính toàn vẹn dữ liệu bằng mã băm SHA256 trong `version_log.csv`, kiểm tra thủ công luồng tương tác thực tế với `interact.py` và xuất transcript JSON xác thực.
- **Thời điểm đã tự nộp URL repo chung trên VLearn**: Trước hạn chót 23:59 ngày 15/09/2026.
