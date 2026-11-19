# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Muller
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Muller-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S1

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Vũ Ngọc Tùng | 2A202604106 | Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý | X |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VuNgocTung-2A202604106

### Phần việc phụ trách

Làm một mình, giữ cả ba vai (Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý): toàn bộ câu 1.1–1.6, 2.1–2.10, 3.0–3.7 và quyết định v1, v2; Phiếu A (A1–A5), Phiếu B (B0–B8), Phiếu C (C0–C12, phần riêng S1: C1 + C3.5); các file `config/acceptance_criteria.json`, `lab10/guards.py`, `lab10/monitors.py`, `config/operating_gates.json`, `submission/submission.json`.

### Đóng góp cụ thể

- Viết và ký Bản tiêu chí trước lần chạy đầu tiên (5 ngưỡng bắt buộc, `escalation_rate_max`, `business_ops`, `stop_condition`, 4 dòng `decision_rule`).
- Đo mốc base, dò `T-002@55`; bản đồ dữ liệu, HAZOP, checklist 9 nhóm, pre-mortem bốn lăng kính.
- Cổng vòng 1 trong `guards.py`: tiền hoàn ≤ quyền lợi theo tracking, phê duyệt hợp lệ, chống hoàn trùng, ghi lỗi hãng theo tracking, lọc dữ liệu gửi hãng, ghim chính sách theo ngày hiệu lực; điền `operating_gates.json`; runbook 1–3, giờ cao điểm; quyết định v1 Thu hẹp.
- Thẻ S1: phân tích 4 nhánh (số khách khai, `delivered_date` trống, trần lỗi/hãng/ngày, khách khai ít hơn); sửa vòng 2 (`_tracking_gap`, trần `carrier_strike_cap`, `_gate_reply`); 2 monitor mới (`max_faults_per_carrier_day`, `model_override_rate`); runbook 4–5, risk register; quyết định v2 Tiếp tục.
- Dùng AI (Claude Code) để: đọc và giải thích code của lab, gợi ý cách viết cổng và monitor, chạy lệnh eval/trace/grade, soạn nháp câu trả lời trong ba phiếu. Mọi ngưỡng, con số trong config và hai quyết định do tôi soát lại và chịu trách nhiệm giải thích lúc demo.

### Bằng chứng

- Commit: `9491998` (ký tiêu chí, 2026-11-19T15:07:31, hash `432f23a8`), `a4865e7` (chốt vòng 1 `3ccb1074`, quyết định v1), `f5e05be` (nhận thẻ S1), commit bài nộp cuối.
- Lần chạy: base `R-base-before-20261119-153601-bde05c`, prepared `R-base-prepared-20261119-154548-e78167`, S1 grade `R-S1-grade-20261119-163303-e46e1d` (PASS-VISIBLE), bộ nền sau sửa `R-base-after-20261119-162855-e46e1d`.
- Phiếu B mục B8 (v1), Phiếu C mục C7–C12 (sửa và v2).

### Exit ticket

- Học được: ngưỡng phải viết và ký trước khi xem số; một sự cố có nhiều nhánh ở nhiều tầng (đầu vào, dữ liệu, quyền hạn), sửa một nhánh (vòng 1 chặn số khách khai) chỉ giảm một nửa lỗi oan.
- Còn chưa chắc: cổng có giữ được trên bài kiểm tra ẩn không (đơn, cách viết khác), và cửa sổ 3 lỗi/7 ngày của hãng nhỏ, thứ cổng theo ngày chưa nhìn thấy.
