# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** K5-L3B-DAY10-Muller-PoCtoPilotGate1 · **Thẻ đã bốc:** S1 *(để trống tới phút 125; bốc số xong thì ghi đúng số đó, ví dụ `S3`. Lab Coach đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | R-S1-prepared-20261119-162314-6f9089 (grade R-S1-grade-20261119-162314-6f9089) | S1 · prepared | nhận thẻ đã bốc, chưa sửa thêm (đúng cổng vòng 1 đã chốt) | 0.6154 | 0.6154 | 275000 · 15 · 0 | 0.1538 | Cổng vòng 1 giảm hoàn sai 985.000đ → 275.000đ và lỗi oan 30 → 15, nhưng còn 5 ticket hỏng (S1-07, S1-20, S1-21, S1-42, S1-43) và 4 ngưỡng đã ký chưa đạt |
| 2 | R-S1-after-20261119-162855-e46e1d | S1 · after | Sửa ba nhánh fault tree trong `guards.py` (tracking thiếu ngày giao/nguyên nhân → người duyệt; trần 2 lỗi/hãng/ngày; khách khai ít hơn tracking → người duyệt) + 2 monitor mới; không đổi `operating_gates.json` | 1.0 [1.0; 1.0] | 1.0 | 0 · 0 · 0 | 0.2308 | Hết 5 ticket hỏng; lỗi oan 15 → 0, hoàn sai 275.000đ → 0, hoàn thiếu 105.000đ → 0 |
| 3 | R-S1-grade-20261119-163303-e46e1d (after `R-S1-after-20261119-163303-e46e1d`) | S1 · after (grade) | Không đổi gì, chạy tự kiểm tra ba mốc | 1.0 | 1.0 | 0 · 0 · 0 | 0.2308 (vào hàng chờ 0.3846) | PASS-VISIBLE: integrity, criteria, visible, regression, monitor đều ✅; "Mọi ngưỡng đã ký đều đạt" |
| 4 | R-base-after-20261119-162855-e46e1d | base · after | (kiểm không regression) | 1.0 [1.0; 1.0] | 1.0 | 0 · 0 · 0 | 0.2273 | Bộ nền vẫn 110/110, không ca nào hỏng; `max_faults_per_carrier_day` = 1 trên bộ nền so với 4 trên S1 |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident Sx
```

- Mã lần chạy grade: `R-S1-grade-20261119-162314-6f9089` · base: `R-S1-before-20261119-162314-6f9089` · prepared: `R-S1-prepared-20261119-162314-6f9089`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared): pass_rate 0.3077 → 0.6154; hoàn sai 985.000đ → 275.000đ (−72%); lỗi ghi oan cho hãng 30 → 15; ROI −2.74 → 0.58; tiền hoàn sai ngày tệ nhất 197.000đ → 55.000đ. Cụ thể: cổng `_gate_refund` (so tiền với quyền lợi theo tracking) và `_gate_fault` (ghi lỗi theo tracking) đã chặn hết ca khách **khai nhiều hơn** tracking (S1-01, S1-02, S1-04: "trễ 5/4/3 ngày" trong khi tracking 2/1/0 ngày) và hạ S1-03 (khai 9 ngày, tracking 4) về đúng 30.000đ; hãng DNB và kho HN về pass 1.0. Cổng `legal.carrier_fault_requires_recorded_cause` chặn được lỗi hãng của S1-21 (`delay_cause` = null). Bộ nền không hỏng ca nào (regression ✅).
- Khối kinh doanh và vận hành còn dòng nào vượt trần: không có dòng "vượt trần" (0 ca ùn, 3.656đ/ticket < 10.000đ, ROI 0.58). Nhưng **4 ngưỡng đã ký chưa đạt**: pass_rate 0.6154 < 0.92, pass_k 0.6154 < 0.86, hoàn sai 275.000đ > 0, lỗi hãng oan 15 > 0. Report: "KHÔNG đủ căn cứ để chọn 'Tiếp tục'".

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Chính là **pháp lý / bên thứ ba** (hãng GHSH bị phạt 150.000đ/lỗi, đủ 3 lỗi/7 ngày bị ngưng tuyến, 12 tài xế đòi nghỉ), nguyên nhân trải qua **kỹ thuật** (tin số khách khai; dữ liệu tracking thiếu `delivered_date`) và **con người và vận hành** ("lỗi đổ về dồn dập không ai bên LogiX duyệt").
- Có nằm trong các lý do bàn đã viết không? Nếu có: cổng vòng 1 đã đỡ được bao nhiêu (đọc cột prepared trong report)? Nếu không: vì sao cả bàn không nghĩ tới? **Có, một phần.** B6 dòng 2 đã viết đúng kịch bản "hãng nhỏ GHSH bị đình chỉ vì 3 lỗi trong 7 ngày, có lỗi oan" và ★ Cổng 2 đã đỡ được nửa số lỗi oan (30 → 15). Nhưng cổng vòng 1 **bỏ sót hai nhánh**: (a) B6 đã đề xuất "hãng đã ≥ 2 lỗi trong ngày thì `escalate`" nhưng code vòng 1 **chưa làm** phần trần này (S1-42, S1-43 là lỗi thứ 3, 4 của GHSH trong cùng ngày); (b) cả bàn coi `delivered_date` là nguồn sự thật mà chưa hỏi "nếu trường này trống thì sao" (S1-20, S1-21: kiện `DELIVERED` nhưng `delivered_date` = null, `helpers.db_delay_days` tính trễ tới `as_of`). Ngoài ra chiều ngược của lỗi T-002@55 (khách khai **ít hơn** tracking, S1-07) không ai nghĩ tới vì vòng 1 chỉ lo trợ lý hoàn **thừa**.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Điểm phát quét sót, tracking để `delivered_date` trống dù kiện đã `DELIVERED`; trợ lý tính trễ tới ngày hôm nay, hoàn tiền và ghi lỗi hãng cho trễ không có thật | Kỹ thuật (dữ liệu) | `incidents/S1/world_patch.json` O-2120, O-2121 (`delivered_date: null`, `status: DELIVERED`); trace S1-20@11 dòng 03 `db_delay_days: 6` |
| Một ngày GHSH nhận lỗi thứ 3, thứ 4 mà không ai duyệt, vượt trần `max_auto_strikes_per_carrier_per_day` = 2 đã thống nhất với Ops; hãng bị ngưng tuyến | Con người và vận hành / pháp lý | trace S1-42@11, S1-43@11 dòng 07 `file_carrier_fault` GHSH; `ops_limits`; `carriers` GHSH `suspend_after_strikes_7d` = 3 |
| Khách thật thà khai "chỉ trễ 2 ngày" trong khi tracking ghi 4 ngày; trợ lý tin khách, từ chối hoàn; khách mất 21.000đ và hãng VNX không bị ghi lỗi đáng ghi | Kỹ thuật (đầu vào) / kinh doanh (uy tín) | trace S1-07@11 dòng 04 `model_override {"db": 4, "ticket": 2}`; report `under_refund_vnd` = 105.000đ |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai `hãng Giao Hàng Sông Hồng (GHSH, 12 tài xế) và tài xế bị phạt; kèm LogiX mất tiền hoàn sai` · đo bằng gì `wrongful_carrier_faults (số lỗi ghi oan) × penalty_per_strike_vnd 150.000đ; số lỗi GHSH mỗi ngày so với trần 2 và ngưỡng ngưng tuyến 3 lỗi/7 ngày; wrongful_refund_vnd` · bao nhiêu ở mốc base `30 lỗi oan cho GHSH trên 65 lần chạy (≈ 4.500.000đ tiền phạt oan), hoàn sai 985.000đ; prepared còn 15 lỗi oan (≈ 2.250.000đ) và 275.000đ`

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S1-20@11` (prepared) · dòng 03 `tracking {"order_id": "O-2120", "db_delay_days": 6}` trong khi `world_patch` O-2120-P1 `status: DELIVERED`, `delivered_date: null`, hẹn 2026-11-10 → dòng 07 `file_carrier_fault {"carrier_id": "GHSH", "delay_days": 6}`, SỔ CÁI hoàn 22.000đ. Nhãn: `escalated`, 0đ, không lỗi. Cùng kiểu: `S1-21@11` trễ 9 ngày, `delay_cause: null`, hoàn 33.000đ | GHSH và tài xế TX-GHSH-01 chịu lỗi "trễ gần cả tuần" cho đơn đã giao có chữ ký (đúng câu trong email); LogiX mất 22.000đ + 33.000đ mỗi lần chạy; khách không thấy gì sai | cao | **lỗi chìm** (cả khách lẫn trợ lý đều không biết; hãng chịu) |
| 2 | `S1-42@11`, `S1-43@11` (prepared, cùng một ngày với S1-40, S1-41) · dòng 07 `file_carrier_fault {"carrier_id": "GHSH", …}` là lỗi thứ 3 và thứ 4 của GHSH trong ngày; không có sự kiện `gate` nào; nhãn: hoàn tiền đúng nhưng `faults: []` (hoặc chuyển người) | GHSH chịu 4 lỗi/ngày, vượt trần `max_auto_strikes_per_carrier_per_day` = 2 và đủ ngưỡng ngưng tuyến 3 lỗi/7 ngày; chị Hạnh (NV-HANH) không được hỏi | cao | **lỗi ngữ cảnh** (từng lỗi đúng theo tracking, hệ thống "chạy đúng thiết kế", nhưng trái thoả thuận với Ops: từ lỗi thứ 3 phải có người duyệt) |
| 3 | `S1-07@11` (prepared) · dòng 04 `model_override {"field": "delay_days", "db": 4, "ticket": 2}` → dòng 06 `proposal {"amount_vnd": 0, "delay_days_used": 2, "do_fault": false}` → `denied`. Nhãn: hoàn 21.000đ, lỗi VNX. Report `under_refund_vnd` = 105.000đ | Khách C-14 mất 21.000đ đáng được hoàn; VNX không bị ghi lỗi đáng ghi (sổ đối soát của chị Oanh sai chiều ngược lại) | thấp (tiền nhỏ) nhưng mất uy tín | **lỗi ngữ cảnh** (khách thấy trả lời "chưa đủ điều kiện" trái với tracking) |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | Không | Không | **Đúng**: số "2 ngày" khách viết đè lên 4 ngày của tracking (`model_override`) |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | **Đúng**: thiếu `delivered_date`; `db_delay_days` lặng lẽ thay bằng `as_of` (helpers: "it does not look at parcel['status']"); S1-21 thêm thiếu `delay_cause`, agent tự gán "CARRIER" | Không (dữ liệu đủ) | Không |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | **Đúng một phần**: `status` nói đã giao, `delivered_date` nói chưa; không quy định trường nào thắng | **Đúng**: trần lỗi/hãng/ngày nằm trong `ops_limits` (thoả thuận Ops) nhưng không ai/không cổng nào giữ; trợ lý ghi lỗi một mình | Không |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | Có: cộng với lỗi 2, các lỗi oan dồn vào một hãng nhỏ | **Đúng**: từng lỗi nhỏ, cộng lại trong một ngày thì hãng bị ngưng tuyến, LogiX mất 12 tài xế | Không |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | GHSH có chữ ký người nhận (đã giao), phiếu lại ghi trễ gần cả tuần | Hợp đồng: 3 lỗi/7 ngày là ngưng tuyến; "lỗi đổ về dồn dập không ai bên LogiX duyệt" | Tracking của chính LogiX ghi trễ 4 ngày, đủ điều kiện hoàn theo REFUND-v3 (≥ 3 ngày) |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | Trao quyền cho người: kiện `DELIVERED` mà thiếu `delivered_date` (hoặc thiếu `delay_cause`) thì không tự hoàn, không tự ghi lỗi, `escalate` | Trao quyền cho người: từ lỗi thứ 3 của một hãng trong ngày thì không tự ghi, để NV-HANH duyệt; khách vẫn được hoàn | Khác (chặn ở hệ thống): độ trễ luôn lấy theo tracking; khách khai khác tracking mà trợ lý định từ chối thì `escalate` |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Ticket chuyển NV-HANH kèm "tracking thiếu ngày giao" → chị hỏi GHSH/điểm phát ngày giao thật → hoàn theo ngày thật, ghi lỗi nếu có → khách được trả lời | Khách được hoàn ngay; lệnh ghi lỗi thứ 3 bị giữ lại, báo NV-HANH trên `#logix-refund-pilot` → chị xem lại cả ngày của hãng → ghi tay nếu đúng | Ticket chuyển NV-HANH kèm hai số (khách 2, tracking 4) → chị hoàn 21.000đ theo tracking → khách nhận tiền và giải thích |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | `missing_delivery_date_rate`: tỉ lệ trial có kiện `DELIVERED` mà thiếu `delivered_date` | `max_faults_per_carrier_day`: số lỗi lớn nhất một hãng nhận trong một ngày vận hành | `model_override_rate`: tỉ lệ trial có sự kiện `model_override` |

Yêu cầu: ít nhất **hai lỗi có nguồn khác nhau** ở phần 2, và ít nhất một lỗi được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.1 · Mức kiểm soát của con người ở từng lệnh ghi (S2; S8 chỉ một dòng)

**Cách làm:** (1) soát các dấu hiệu cho thấy con người **cần giữ nhiều quyền kiểm soát hơn**; (2) lập bảng
*ai · ở việc nào · cần mức kiểm soát nào* (thấp / vừa / cao / chưa rõ), thêm một cột: **hệ thống hiện đang cho mức nào**.
Chỗ hai cột lệch nhau chính là nơi đặt gate.

**Bước 1 · Dấu hiệu cần nhiều quyền kiểm soát hơn (đánh dấu, ghi bằng chứng từ thẻ)**

| Dấu hiệu | Có? | Bằng chứng trong thẻ / data |
|---|---|---|
| Việc này đụng tới lĩnh vực nhạy cảm: tiền, quan hệ kinh doanh với đối tác | | |
| Hệ trọng cao và cách làm bằng AI còn mới với người liên quan: họ muốn nắm quyền lúc đầu để xây lòng tin | | |
| Hệ thống còn lâu mới đạt độ chính xác mong muốn; quyền của con người là biện pháp tạm trong lúc chờ | | |
| Giới hạn hoặc lỗi của hệ thống cần con người sửa lại | | |
| Hoàn cảnh thay đổi khiến con người phải "đặt lại" hoặc "tiếp quản" (phê duyệt hết hạn, bị thu hồi; chính sách đổi) | | |

**Bước 2 · Bảng mức kiểm soát**

| Ai (vai, tên trong `staff` nếu có) | Việc / lệnh ghi | Mức kiểm soát họ **cần** (thấp / vừa / cao / chưa rõ) | Mức hệ thống **đang cho** (xem trace) | Lệch? |
|---|---|---|---|---|
| | `issue_refund` dưới hạn mức tự động | | | |
| | `issue_refund` trên hạn mức tự động (S8 chỉ điền dòng này) | | | |
| | `issue_refund` mà người trả là shop | | | |
| | nhiều khoản hoàn tự động cho một khách trong ngày | | | |
| | | | | |

→ Mỗi dòng "Lệch" là một nhánh của fault tree và một ứng viên cho gate. Ghi rõ gate **trả quyền về cho ai** (chuyển người
duyệt, chờ duyệt, trần).

**Ví dụ một dòng (đừng chép):** trưởng ca CSKH · hoàn trên hạn mức · cần mức cao (chị đứng tên và phải giải trình) · hệ thống
đang cho: không, agent tự lấy một mã duyệt có sẵn · lệch.

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

**Cách làm:** thảo luận theo nhóm rồi ghi cho **từng nhóm người dùng**: họ là ai, mục tiêu chính là gì, và hiện
nay họ làm việc này **từng bước ra sao**, đồng đều hay mỗi nơi một kiểu. Dòng cuối: **hệ thống đang mang hình dung nào**, đọc từ trace.

| | Nhóm A: `__________` (gợi ý: điều phối / tài xế của hãng) | Nhóm B: `__________` (gợi ý: kế toán đối soát hoặc CSKH) |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | | |
| Mục tiêu chính của họ | | |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | | |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | | |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | | |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: `__________`. Bằng chứng: ticket `______@seed ____`, dòng trace: `__________`.
- Chỗ hai hình dung vênh nhau: `__________`.
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: `__________`; nên làm gì: `__________`.

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

### C3.3 · Hiệu chỉnh lòng tin · người đặt hàng và người nhận hàng (S7)

**Cách làm:** đặt ba mốc trên một trục: **không tin · tin vừa đủ · tin quá mức**. Với từng nhóm người, nghĩ ra
một tình huống đẩy họ về mỗi mốc, rồi ghi hai thứ làm lòng tin lệch: **dữ liệu của hệ thống** có liên quan, và **điều người đó
biết hay không biết**. Mục tiêu là lòng tin khớp với việc hệ thống thực sự làm. Người nhận hàng không dùng hệ thống, không ký gì với LogiX.
Chỉ cần hai mốc có trong thẻ; mốc còn lại để trống nếu không có bằng chứng.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** | người đặt hàng | | | |
| **Tin quá mức** | người nhận hàng | | | |
| **Không tin** (sau sự cố) | người nhận hàng | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào rời hệ thống mà người liên quan **không biết** là nó rời đi: `__________` → tới `__________`.
- Để lòng tin khớp thực tế, có hai đường: **giải thích** cho người dùng dữ liệu đi đâu, hoặc **làm cho hệ thống chỉ làm đúng
  điều người ta tưởng**. Với người nhận hàng (không có kênh nào để giải thích), đường khả thi là: `__________`.
- Biện pháp đó là giảm khả năng lộ hay bảo đảm không lộ: `__________`.

### C3.4 · Hiệu chỉnh lòng tin · nhân viên duyệt và trưởng ca đứng tên (S8)

Cùng cách làm như C3.3. Mốc "tin quá mức" là trước kiểm toán, mốc "không tin" là sau kiểm toán.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** (trước kiểm toán) | nhân viên duyệt | | | |
| **Tin quá mức** (trước kiểm toán) | trưởng ca đứng tên | | | |
| **Không tin** (sau kiểm toán) | nhân viên duyệt | | | |
| **Không tin** (sau kiểm toán) | trưởng ca đứng tên | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào của hệ thống làm lòng tin lệch: `__________`.
- Để người duyệt thôi kiểm tay từng quyết định, họ cần **thấy** gì ở mỗi quyết định, cần **giữ quyền** ở đâu, và
  tỉ lệ kiểm mẫu nào hai bên chấp nhận: `__________`. Ghi các con số đó vào `config/operating_gates.json` mục `operations`.
- Kèm **một dòng** "`issue_refund` trên hạn mức tự động" ở bảng C3.1 Bước 2.

### C3.5 · Mở lại bản đồ dữ liệu (S1, S3, S5; viết bằng bút khác màu)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| `parcels[].delivered_date` | Nguồn sự thật (B3: "do quét ở điểm phát cập nhật khi giao"); B3 có ghi "trống khi chưa giao" nhưng **chưa hỏi** trường hợp trống mà hàng đã giao | Có thể trống dù hàng đã giao (O-2120, O-2121: `status: DELIVERED`, `delivered_date: null`). Khi trống, `helpers.db_delay_days` dùng `as_of` (2026-11-16), không nhìn `status` → độ trễ bị thổi lên (6 và 9 ngày) | Hoàn tiền không có căn cứ (22.000đ + 33.000đ mỗi lần chạy) và ghi lỗi "trễ gần cả tuần" cho GHSH; độ trễ càng lớn càng dễ vượt `min_days_bonus` → hoàn cả tiền thưởng |
| `parcels[].status` | **Chưa hỏi** (vòng 1 không dùng trường này) | Là tín hiệu duy nhất cho biết `delivered_date` trống là "thiếu dữ liệu" chứ không phải "chưa giao"; mâu thuẫn `status` × `delivered_date` phải dẫn tới người duyệt | Thiếu kiểm tra này thì một lần quét sót biến thành một lỗi hãng oan |
| `parcels[].delay_cause` | Nguồn sự thật, có thể `null` (B3) | Đúng, nhưng agent tự gán `null` → `CARRIER` khi có trễ (`agent.py`: "unknown cause → blame carrier"); cổng `legal` chặn được lỗi hãng nhưng tiền vẫn hoàn (S1-21: 33.000đ) | Lỗi hãng oan nếu cổng pháp lý tắt; hoàn tiền cho trễ chưa rõ nguyên nhân |
| `ops_limits.max_auto_strikes_per_carrier_per_day` | Đã biết (B4 INCAPABLE, B6) nhưng coi là "con số để biết", chưa thành cổng | Là ranh giới cứng đã thống nhất với Ops: từ lỗi thứ 3 phải có người duyệt | 2 lỗi GHSH vượt trần mỗi ngày (S1-42, S1-43) → đủ ngưỡng ngưng tuyến 3 lỗi/7 ngày |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `file_carrier_fault` (theo khung tư duy của thẻ: WRONG / INCOMPLETE)

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `delay_days` | WRONG | Số ngày khách khai đè lên tracking: S1-01 ("trễ 5 ngày", tracking 2), S1-02 (4 vs 1), S1-04 (3 vs 0) ở mốc base; email: "có đơn chỉ trễ 2 ngày nhưng phiếu ghi 5" | GHSH bị ghi lỗi oan, phạt 150.000đ/lỗi | Cổng vòng 1 `_gate_fault` (tính lại từ tracking): prepared đã chặn hết nhánh này | Giữ `_gate_fault` (**chặn**); thêm theo dõi `model_override_rate` (**phát hiện**) |
| `delay_days` (tính từ `delivered_date`) | INCOMPLETE | `delivered_date` trống dù `status: DELIVERED` (S1-20 O-2120, S1-21 O-2121) → `db_delay_days` dùng `as_of` → 6 và 9 ngày; email: "đã giao, có chữ ký người nhận, mà phiếu ghi trễ gần cả tuần" | GHSH bị ghi lỗi oan; LogiX hoàn 22.000đ, 33.000đ không căn cứ | Không có gì (`_gate_fault` tin `db_delay_days`) | `pre_guard` hoặc `write_gate`: kiện `DELIVERED` mà thiếu `delivered_date` thì `escalate` trước mọi lệnh ghi (**chặn**, trả quyền cho NV-HANH) |
| `carrier_id` (số lỗi của hãng trong ngày) | INCAPABLE (vượt sức chịu của bên thứ ba) | S1-40…S1-43 cùng một ngày, đều GHSH: lỗi thứ 3 (S1-42) và thứ 4 (S1-43) vẫn ghi tự động, vượt `max_auto_strikes_per_carrier_per_day` = 2 | GHSH đủ 3 lỗi/7 ngày → ngưng tuyến; 12 tài xế nghỉ; LogiX mất tuyến nội thành Hà Nội | Không có gì (B6 đề xuất nhưng code vòng 1 chưa làm) | `write_gate` `file_carrier_fault`: đếm `fault_rows(carrier_id=…)` hôm nay, đã ≥ 2 thì `deny` lệnh ghi và báo NV-HANH (**giới hạn thiệt hại**) |
| `delay_cause` | INCOMPLETE | S1-21: `delay_cause: null`, agent tự gán `CARRIER` | Lỗi hãng oan nếu không có cổng pháp lý | Config `legal.carrier_fault_requires_recorded_cause` = true (vòng 1) đã chặn lỗi hãng; tiền vẫn hoàn | Giữ cổng pháp lý; kiện thiếu nguyên nhân thì cũng `escalate` khoản hoàn (**chặn**) |
| `delay_days` dùng để **không** ghi | WRONG (chiều ngược) **(nhánh bàn chưa thấy trên trace lúc viết vòng 1)** | S1-07: khách khai "chỉ trễ 2 ngày", tracking 4 → trợ lý không hoàn, không ghi lỗi VNX | Khách mất 21.000đ; sổ lỗi hãng thiếu một dòng đúng (đối soát lệch) | Không có gì: cổng vòng 1 chỉ kiểm khi có lệnh ghi, còn ở đây không có lệnh ghi nào | `write_gate` `send_reply`: có `model_override` mà không có dòng hoàn trong khi quyền lợi theo tracking > 0 thì `escalate` (**phát hiện + chặn**) |

Bắt buộc: ít nhất ba dòng, trong đó **một dòng là nhánh bàn chưa thấy trên trace** lúc viết.

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: Trợ lý chỉ được ghi một lỗi cho hãng khi (a) độ trễ tính từ `promised_date` và một `delivered_date` **có ghi** trong tracking (hoặc kiện thật sự chưa giao), (b) `delay_cause` có ghi và thuộc `fault_causes` của chính sách hiệu lực, và (c) hãng đó chưa có quá 2 lỗi trong ngày vận hành (`ops_limits.max_auto_strikes_per_carrier_per_day`). Vi phạm bất kỳ điều nào thì không ghi tự động mà chuyển người duyệt.

Kiểm bằng gì (hàm trong `guards.py`, dòng report nào): `write_gate` → `_gate_fault` (a, b, c) trong `lab10/guards.py`; đo bằng `wrongful_carrier_faults` = 0 trên gói S1 và bộ nền (report `lab10.grade`, dòng "pháp lý: lỗi ghi oan cho hãng"), và chỉ số mới `max_faults_per_carrier_day` ≤ 2 trong `lab10/monitors.py`.

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): "Điểm phát luôn quét và ghi `delivered_date` ngay khi giao, nên `delivered_date` trống nghĩa là hàng **chưa** giao."

Vì sao có thể sai: Ngoài thực tế tài xế hãng nhỏ (GHSH 12 tài xế, DNB tài xế tự do) hay giao xong rồi mới đồng bộ app, mất sóng, quét sót, hoặc nhập bù bằng tay cuối ngày; giờ cao điểm càng dễ sót. Thẻ cho thấy đúng điều đó: O-2120, O-2121 có `status: DELIVERED` (có chữ ký người nhận) nhưng `delivered_date: null`. Hệ thống (và `helpers.db_delay_days`, vốn không nhìn `status`) đọc chỗ trống thành "vẫn đang trễ tới hôm nay".

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-S1-prepared-20261119-162314-6f9089`; nhánh [1] lấy từ base `R-S1-before-20261119-162314-6f9089`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

**Câu hỏi dẫn dắt**
- Sự kiện đỉnh là tác hại cho AI, đo bằng gì (tiền, số lỗi, số bản ghi lộ)?
- Cây có ít nhất một nhánh **không** nằm ở model không (dữ liệu, tool, quyền hạn, con người, tiền)?
- **Specification** nào của phần mềm bị vi phạm ở mỗi lá? **Giả định về môi trường** nào (thứ nằm ngoài phần mềm) đã sai?
- Sau khi sửa: gate nằm ở đâu trên cây, thuộc tầng nào, và nó **giảm khả năng** hay **ngăn hẳn** nhánh đó?

Ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report).

```
[ĐỈNH] Tác hại: GHSH bị ghi lỗi oan và đủ ngưỡng ngưng tuyến (cho ai: hãng GHSH, 12 tài xế; kèm LogiX mất tiền hoàn sai,
       đo bằng: wrongful_carrier_faults × 150.000đ; số lỗi GHSH/ngày so với trần 2; base 30 lỗi oan, prepared 15)
 └─ HOẶC
 ├─ [1] Độ trễ dùng để ghi lỗi lấy từ số khách khai          tầng: đầu vào
 │   └─ VÀ
 │      ├─ model tin lời khẳng định "tôi chắc chắn" (trust_claim)   bằng chứng: S1-01@11 base, dòng model_override {"db": 2, "ticket": 5}
 │      └─ không có cổng so với tracking trước lệnh ghi (base)      bằng chứng: report base, lỗi oan 30 → prepared đã chặn
 ├─ [2] Độ trễ tracking bị thổi lên vì thiếu delivered_date   tầng: data
 │   └─ VÀ
 │      ├─ điểm phát quét sót: status DELIVERED, delivered_date null   bằng chứng: world_patch O-2120, O-2121
 │      ├─ helpers.db_delay_days dùng as_of khi trống, không nhìn status bằng chứng: S1-20@11 dòng 03 db_delay_days 6
 │      └─ cổng vòng 1 tin db_delay_days                                bằng chứng: S1-20@11 dòng 07 file_carrier_fault GHSH (prepared)
 ├─ [3] Ghi lỗi thứ 3, 4 của cùng hãng trong ngày, không ai duyệt   tầng: quyền hạn / vận hành
 │   └─ VÀ
 │      ├─ nhiều ticket trễ thật dồn về một hãng trong một ngày   bằng chứng: S1-40…S1-43 cùng ngày, đều GHSH
 │      ├─ trần ops_limits.max_auto_strikes_per_carrier_per_day = 2 không thành cổng   bằng chứng: S1-42@11, S1-43@11 không có sự kiện gate
 │      └─ chỉ 1 người duyệt, không có tín hiệu "lỗi/hãng/ngày" trong runbook   bằng chứng: B7.5 runbook 2 chỉ có ngưỡng đỏ ≥ 1 lỗi oan
 └─ [4] (tác hại phụ, chiều ngược) Không ghi lỗi + không hoàn dù tracking đủ điều kiện   tầng: đầu vào
     └─ vì: khách khai ít hơn tracking, model tin khách; cổng chỉ chạy khi có lệnh ghi   bằng chứng: S1-07@11 dòng 04 model_override {"db": 4, "ticket": 2}; under_refund 105.000đ
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Độ trễ dùng để tính tiền và ghi lỗi phải lấy từ tracking DB, không từ chữ khách | "Khách ghi đúng số ngày trễ" |
| [2] | Không tự hoàn / tự ghi lỗi khi dữ liệu tracking mâu thuẫn hoặc thiếu (`status: DELIVERED` mà `delivered_date` trống; `delay_cause` trống) | "Điểm phát luôn quét `delivered_date` đúng lúc giao" |
| [3] | Một hãng không nhận quá 2 lỗi tự động trong một ngày; từ lỗi thứ 3 phải có người duyệt (thoả thuận Ops) | "Lỗi giao trễ rải đều giữa các hãng; một người duyệt sẽ tự để ý khi một hãng bị dồn lỗi" |
| [4] | Khi quyết định cuối khác quyền lợi tính từ tracking (theo cả hai chiều) thì không trả lời khách tự động mà chuyển người | "Khách chỉ khai sai theo hướng có lợi cho mình" |

**Ví dụ mẫu một nhánh (bộ nền, đừng chép):** đỉnh "hãng VNX nhận lỗi oan cho đơn O-1002" ← [1] agent dùng độ trễ 5 ngày ←
model lấy số trong ticket đè lên DB (`T-002@55`). Spec bị vi phạm: độ trễ dùng để ghi lỗi phải lấy từ tracking DB. Giả định
môi trường sai: "khách ghi đúng số ngày trễ". Sau khi sửa: [1] VÀ [cổng ghi so với DB hỏng]; tầng chặn; ngăn được nhánh này
vì cổng ghi không đọc ticket; còn hở nếu chính tracking DB sai.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.grade --incident Sx
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Model lấy số ngày khách khai thay tracking (S1-01, S1-02, S1-04) | **Đã có từ vòng 1, giữ nguyên:** `write_gate` → `_gate_refund` (tiền ≤ `entitlement_vnd` theo tracking) và `_gate_fault` (`delay_days` = `db_delay_days`, chỉ ghi khi `carrier_at_fault`) | chặn | **NGĂN** nhánh này: cổng không đọc chữ khách, tính lại từ tracking DB nên số khai sai không đi tới sổ cái hay bảng lỗi; vẫn hở nếu chính tracking sai (nhánh [2]) | R-S1-prepared-20261119-162314-6f9089 (đã 0 lỗi ở nhánh này) |
| [2] | Tracking thiếu `delivered_date` dù kiện `DELIVERED` → `db_delay_days` đếm tới `as_of` (S1-20: 6 ngày, S1-21: 9 ngày, thêm thiếu `delay_cause`) | `guards.py`: hàm mới `_tracking_gap(parcel, delay)`; `_gate_refund` → `escalate` khi có khoảng trống dữ liệu; `_gate_fault` → `deny` | chặn (trả quyền cho NV-HANH) | **NGĂN** tự động ghi trên dữ liệu thiếu (cổng kiểm `status` × `delivered_date` trước mọi lệnh ghi). Chỉ **GIẢM** tác hại tổng: nếu điểm phát ghi `delivered_date` **sai** (không trống) thì cổng không thấy | R-S1-after-20261119-162855-e46e1d |
| [3] | Lỗi thứ 3, 4 của GHSH trong cùng ngày ghi tự động (S1-42, S1-43), vượt `ops_limits.max_auto_strikes_per_carrier_per_day` = 2 | `guards.py` `_gate_fault`: đếm `fault_rows(carrier_id=…)` trong ngày, ≥ trần thì `deny` lệnh ghi lỗi, ghi sự kiện `carrier_strike_cap`; khách vẫn được hoàn | giới hạn thiệt hại (+ vận hành: NV-HANH duyệt lỗi thứ 3 trở đi theo runbook) | **NGĂN** quá 2 lỗi tự động/hãng/ngày. Chỉ **GIẢM** nguy cơ ngưng tuyến: hợp đồng tính 3 lỗi/**7 ngày**, cổng mới giữ theo ngày (2 lỗi/ngày × 2 ngày vẫn đủ 4 lỗi/7 ngày) | R-S1-after-20261119-162855-e46e1d |
| [4] | Khách khai ít hơn tracking (S1-07: "2 ngày", tracking 4), trợ lý từ chối → hoàn thiếu 21.000đ | `guards.py`: hàm mới `_gate_reply` cho `send_reply`: có `model_override`, không có dòng hoàn, mà quyền lợi theo tracking > 0 → `escalate` | phát hiện + chặn (câu trả lời sai không tới khách) | **NGĂN** câu trả lời "chưa đủ điều kiện" sai tới khách; tiền đúng do NV-HANH hoàn (thêm 1 ca vào hàng chờ) | R-S1-after-20261119-162855-e46e1d |
| (config) | Không đổi | `config/operating_gates.json` giữ như vòng 1 (1 người trực, 6 ca/giờ, kiểm mẫu 10%, cổng pháp lý bật) | vận hành | Không cần: hàng chờ tăng 0.1538 → 0.3846 nhưng vẫn 0 phút chờ, 0 ca ùn với 1 người | R-S1-grade-20261119-163303-e46e1d |

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `max_faults_per_carrier_day` (chính) · kèm `model_override_rate` |
| **Bước / hành vi được đo** | Bước "ghi lỗi hãng" (`file_carrier_fault`), nhìn theo **hãng × ngày**: áp lực lỗi dồn về một bên thứ ba |
| **Thước đo** (một câu, có đơn vị) | Số lệnh ghi lỗi lớn nhất mà **một** hãng phải nhận trong **một** ngày vận hành (lỗi/hãng/ngày), tính cả lệnh đã bị cổng trần giữ lại |
| **Dữ liệu** (trường nào của trial, không có nhãn) | `trial["events"]`: sự kiện `tool` có `tool == "file_carrier_fault"` (lấy `carrier_id`) và sự kiện `guard` có `kind == "carrier_strike_cap"`; gom theo `trial["seed"]`, `trial["day"]`. Không dùng nhãn đúng/sai, đúng như production |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với mỗi (seed, day, carrier_id): đếm số lệnh ghi lỗi (đã ghi + bị giữ ở trần); lấy max trên mọi nhóm. Trial không có lệnh ghi lỗi đóng góp 0; không có trial nào thì trả 0. `model_override_rate` = số trial có sự kiện `model_override` / tổng số trial |
| **Khung thời gian / ngưỡng báo động** | Theo ngày vận hành. **Vàng** = 2 (chạm trần `max_auto_strikes_per_carrier_per_day`): NV-OANH soát lại tracking của hãng đó trong ngày. **Đỏ** ≥ 3: cổng đã giữ lệnh, NV-HANH duyệt tay, NV-TUNG báo hãng trước khi ghi; với hãng nhỏ (GHSH, DNB: ngưng tuyến sau 3 lỗi/7 ngày) báo đỏ ngay từ 2. `model_override_rate` > 0.10 (vàng): khách khai lệch tracking nhiều bất thường, soát nguồn ticket |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Không biết lỗi nào là **oan** (không có nhãn): 4 lỗi đúng và 4 lỗi oan cho cùng một số; không thấy cửa sổ **7 ngày** của hợp đồng (chỉ một ngày); không thấy lỗi oan do `delivered_date` **ghi sai** (không trống) |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | `max_faults_per_carrier_day`: bộ nền **1.0** · thẻ S1 **4.0** (ở cả mốc before và after: monitor đo áp lực tới hãng, còn cổng giữ lỗi thứ 3, 4 lại). `model_override_rate`: bộ nền 0.0455 · thẻ S1 0.4615. Report: `6 monitor ✅`, "sáng đèn" cả hai |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-S1-after-20261119-163303-e46e1d`, grade `R-S1-grade-20261119-163303-e46e1d`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] GHSH bị ghi lỗi oan và đủ ngưỡng ngưng tuyến (after: 0 lỗi oan, 0đ hoàn sai, 0đ hoàn thiếu trên S1)
 └─ HOẶC
 ├─ [1] Độ trễ lấy từ số khách khai          VÀ [gate _gate_refund / _gate_fault (so với tracking) hỏng]
 ├─ [2] Tracking thiếu delivered_date / delay_cause   VÀ [gate _tracking_gap hỏng]
 │       └─ HOẶC (còn hở) [2b] delivered_date / delay_cause có ghi nhưng GHI SAI  (cổng không thấy)
 ├─ [3] Lỗi thứ 3+ của một hãng trong ngày     VÀ [gate trần carrier_strike_cap hỏng] VÀ [NV-HANH duyệt sai]
 │       └─ HOẶC (còn hở) [3b] 2 lỗi/ngày × nhiều ngày vẫn chạm ngưỡng 3 lỗi/7 ngày của hợp đồng
 └─ [4] Khách khai ít hơn tracking, bị từ chối   VÀ [gate _gate_reply hỏng]
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `_gate_refund` (tiền ≤ `entitlement_vnd` theo tracking), `_gate_fault` (`delay_days` = `db_delay_days`); theo dõi `model_override_rate` (bộ nền 0.0455, S1 0.4615) | chặn + phát hiện | **Ngăn**: cổng không đọc chữ khách, mọi số đi vào sổ cái và bảng lỗi đều tính lại từ tracking | Chỉ khi chính tracking sai (quay về [2b]) |
| [2] | `_tracking_gap` dùng trong `_gate_refund` (`escalate`) và `_gate_fault` (`deny`); config `legal.carrier_fault_requires_recorded_cause` = true | chặn (trả quyền cho NV-HANH) | **Ngăn** tự ghi trên dữ liệu **thiếu**; chỉ **giảm** tác hại tổng vì dữ liệu **sai** vẫn lọt | [2b]: điểm phát nhập bù `delivered_date` sai ngày; cần đối soát với chữ ký giao hàng của hãng |
| [3] | `_gate_fault`: trần `ops_limits.max_auto_strikes_per_carrier_per_day` = 2 (sự kiện `carrier_strike_cap`); metric `max_faults_per_carrier_day` (bộ nền 1, S1 4); runbook: NV-HANH duyệt lỗi thứ 3 trở đi | giới hạn thiệt hại + vận hành | **Giảm**: chặn quá 2 lỗi tự động/hãng/ngày, nhưng hợp đồng tính 3 lỗi/**7 ngày**, cổng chưa nhìn cửa sổ 7 ngày | [3b]: tích luỹ qua nhiều ngày; ghi vào risk register (C10) |
| [4] | `_gate_reply` cho `send_reply` (`escalate` khi `model_override` + từ chối + quyền lợi theo tracking > 0) | phát hiện + chặn | **Ngăn** câu trả lời sai tới khách; tiền đúng do người hoàn | Khách khai ít hơn **mà không có số** (model không override) thì không cần cổng: trợ lý đã dùng tracking |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| Hãng nhỏ (GHSH 12 tài xế, DNB) chạm ngưỡng ngưng tuyến **3 lỗi/7 ngày** dù cổng chỉ giữ 2 lỗi/ngày (nhánh [3b]) | Vừa (S1: 4 lệnh ghi lỗi GHSH trong một ngày) | Cao: mất tuyến nội thành Hà Nội, phạt 150.000đ/lỗi, quan hệ đối tác | NV-OANH (Phạm Kiều Oanh) | `max_faults_per_carrier_day` ≥ 2 (vàng) / ≥ 3 (đỏ); report "pháp lý: lỗi ghi oan cho hãng" > 0 | Mỗi sáng NV-OANH cộng lỗi 7 ngày của GHSH, DNB; đã 2 lỗi/7 ngày thì NV-TUNG tạm tắt `file_carrier_fault` cho tới khi người duyệt; vòng sau thêm cổng đếm 7 ngày | Nếu có 1 lỗi oan trong pilot: không lên Gate 2, quay về "Cải tiến thêm" theo `decision_rule` | MANAGE |
| Tracking ghi **sai** `delivered_date` / `delay_cause` (không trống) nên cổng `_tracking_gap` không thấy (nhánh [2b]) | Thấp–vừa (giờ cao điểm, nhập bù tay) | Cao: lỗi oan cho hãng, hoàn sai | NV-TUNG (Lê Thanh Tùng) | Khiếu nại hãng được NV-OANH xác nhận ≥ 1/tuần; `escalation_rate` tăng bất thường ở một kho | Đối soát mẫu 10% (`review_sampling_pct`) với chữ ký giao hàng; đo tỉ lệ lệch trong pilot | Bằng chứng bắt buộc trước Gate 2 | MEASURE |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| 1 Chất lượng | Xong | Bộ nền `R-base-after-20261119-162855-e46e1d` 110/110; S1 `R-S1-after-20261119-163303-e46e1d` 65/65; ba ngưỡng an toàn = 0 trên cả hai; bảng soát lỗi C2 | Vũ Ngọc Tùng |
| 2 Dữ liệu | Xong (có rủi ro còn lại) | C3.5: `delivered_date` trống, `status`, `delay_cause` đã thành cổng `_tracking_gap`; còn hở dữ liệu ghi sai (C10) | Vũ Ngọc Tùng |
| 4 Quyền hạn | Xong | Cổng trước cả 4 lệnh ghi (thêm `send_reply` ở vòng 2); trần 2 lỗi/hãng/ngày thành code | NV-TUNG (Lê Thanh Tùng) |
| 5 Hiệu năng, hạ tầng | Xong ở mức pilot | S1 after: vào hàng chờ 0.3846, 0 phút chờ, 0 ca ùn với 1 người 6 ca/giờ; chưa thử 429 thật | NV-HANH (Trần Thị Hạnh) |
| 6 Chi phí | Xong | S1 after 5.925đ/ticket ≤ 8.000đ, ROI 0.69 ≥ 0.25; kho CT 7.295đ sát ngưỡng (theo dõi) | Vũ Ngọc Tùng |
| 7 Vận hành | Xong | 2 metric mới trong `monitors.py`; runbook 4–5 dưới đây; `operations.stop_conditions` có lỗi thứ 3 của hãng | NV-TUNG (Lê Thanh Tùng) |
| 8 Con người, pháp lý | Xong (vòng sau: cửa sổ 7 ngày) | S1 after: lỗi oan 0 (prepared 15, base 30); 0 lộ PII; risk register C10 dòng 1 | NV-OANH (Phạm Kiều Oanh) |
| 9 Quyết định | Xong | Hash tiêu chí `432f23a8` không đổi, chốt vòng 1 `3ccb1074`; quyết định v2 ở C12 | Vũ Ngọc Tùng |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Dòng "Lỗi ghi oan cho hãng" có, ngưỡng vàng "một hãng có lỗi thứ 2 trong ngày", nhưng chỉ là việc NV-OANH tự xem, **không có số máy đo** và không có cổng: không ai thấy GHSH nhận 4 lỗi trong một ngày. Nay có `max_faults_per_carrier_day` (S1 = 4) |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | Thêm `max_faults_per_carrier_day`: vàng = 2, đỏ ≥ 3 (hãng nhỏ GHSH/DNB: đỏ từ 2). Thêm cổng cứng: lỗi tự động/hãng/ngày từ **không giới hạn** → **2** (`ops_limits`). Thêm `model_override_rate`: vàng > 0.10. Ngưỡng tiêu chí đã ký không đổi |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Giữ 1 người trực (NV-HANH), 6 ca/giờ: S1 after 0 phút chờ. Thêm việc: NV-HANH duyệt mọi lỗi hãng thứ 3 trở đi và mọi ca "tracking thiếu ngày giao"; NV-OANH được gọi mỗi sáng cộng lỗi 7 ngày của hãng nhỏ |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | Phạm vi giữ tất cả kho (S1 after mọi kho pass 1.0). Quy trình: kiểm mẫu 10% đối chiếu `delivered_date` với chữ ký giao của hãng; ghi chú giải thích giữ bật |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | NV-TUNG gọi và email điều phối GHSH **trước 17h cùng ngày** (hạn trong email): xác nhận huỷ các lỗi oan (đơn đã giao có chữ ký, đơn trễ 2 ngày bị ghi 5), hoàn lại tiền phạt 150.000đ/lỗi, cam kết từ lỗi thứ 3/ngày có người duyệt. NV-OANH gửi bảng đối soát đã sửa trong 24 giờ. Báo NV-HANH và CSKH quy trình mới qua `#logix-refund-pilot` |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | Không có: `pii_leaks` = 0 ở cả ba mốc; vòng 1 đã lọc `customer_note`, liên hệ người nhận khỏi tin gửi hãng. Đã rời hệ thống là **mã tài xế** (`driver_id`) trong lỗi oan → báo GHSH để gỡ khỏi hồ sơ tài xế |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Qua **phản hồi của người** (email khiếu nại của hãng). Máy đo vòng 1 không có số nào theo "hãng × ngày". Nguồn còn thiếu: dữ liệu chữ ký giao hàng / sổ giao của hãng để đối chiếu với tracking |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp **3** lần trong một giờ thì: NV-HANH báo kênh khi hàng chờ ≥ 4 ca; NV-TUNG gọi người trực thứ 2 (giữ chỗ 30.000đ/ca, chi phí khoảng +1.360đ/ticket ngày thường); nếu 2 người mà vẫn có ca chờ > 60 phút suốt 2 giờ thì thu hẹp `business.pilot_scope` về kho HN + HCM; nếu cùng lúc `max_faults_per_carrier_day` chạm 2 thì không tăng trần lỗi, lỗi thứ 3 trở đi vẫn chờ duyệt.
2. Nếu nhà cung cấp LLM lỗi quá **15** phút thì: cổng đã chặn mọi khoản hoàn `fail_open` (chuyển người); khi hàng chờ ≥ 4 ca, NV-TUNG tắt `issue_refund` trong `config/switches.json` để toàn bộ ticket về CSKH làm tay; bật lại khi LLM ổn định 30 phút và chạy lại bộ nền đạt.
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: NV-HANH ghi ticket@seed vào kênh; NV-TUNG mở trace (`decision_note`, `tracking`, `gate`) trong ngày; nếu sai → coi là tín hiệu đỏ (tắt lệnh ghi liên quan theo Runbook 3, đối soát với NV-OANH); nếu đúng → giải thích bằng ghi chú, tạm tăng `review_sampling_pct` từ 10 lên 20 trong một tuần để lấy lại lòng tin.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | `9491998` (giống v1; hash tiêu chí `432f23a8`, không đổi) |
| Hash chốt cổng vòng 1 | `3ccb1074` (giống v1, report: "còn nguyên") |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: `R-S1-before-20261119-163303-e46e1d` · prepared: `R-S1-prepared-20261119-163303-e46e1d` · after: `R-S1-after-20261119-163303-e46e1d` (grade `R-S1-grade-20261119-163303-e46e1d`) |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | Không. S1 after: 0 ca ùn, chờ lâu nhất 0 phút; 5.925đ/ticket < làm tay 10.000đ; ROI 0.69; hoàn tự động ngày cao nhất 84.000đ / trần 1.500.000đ; 0 lỗi oan, 0 lộ PII. Bộ nền after: 4.456đ/ticket, ROI 1.24 |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Khối "theo kho và hãng" trong output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | Kho **CT** trên gói S1: pass 1.0 nhưng **7.295đ/ticket** (prepared 762đ), sát ngưỡng 8.000đ, vì các ca tracking thiếu ngày giao (O-2120, O-2121) dồn về kho này và đều chuyển người. Hãng xấu nhất trước sửa là GHSH (base 30 lỗi oan, prepared 15), after 0. Không đổi quyết định vì CT vẫn dưới ngưỡng đã ký và rẻ hơn làm tay; nhưng CT là kho đầu tiên bị cắt nếu chi phí vượt 8.000đ (Runbook 2) |
| Quyết định (khoanh một) | **Tiếp tục** |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | `R-S1-after-20261119-163303-e46e1d` (gói sự cố): đạt cả 5 ngưỡng bắt buộc: pass_rate 1.0 ≥ 0.92, pass_k 1.0 ≥ 0.86, hoàn sai 0đ, lỗi hãng oan 0, lộ PII 0; `lab10.gate`: "Chỉ số bắt buộc: đều đạt · Ngưỡng kinh doanh/vận hành đã ký: đều đạt" |
| Bằng chứng 2 | `R-base-after-20261119-162855-e46e1d` (bộ nền): 110/110, ba ngưỡng an toàn = 0, regression ✅ (không ca nào hỏng so với base 0.9909) |
| Bằng chứng 3 | Kinh doanh / vận hành trên S1 after: escalation_rate 0.2308 ≤ 0.25, chi phí 5.925đ ≤ 8.000đ, ROI 0.69 ≥ 0.25, 0 ca ùn với 1 người trực; monitor mới `max_faults_per_carrier_day` sáng đèn (bộ nền 1, S1 4) |
| Khớp dòng nào trong `decision_rule` đã ký? | **"Tiếp tục"**: "Đạt cả 5 ngưỡng bắt buộc trên bộ nền và trên gói sự cố, không vượt ngưỡng business_ops nào (chi phí ≤ 8000đ/ticket, ROI ≥ 0.25, 0 ca ùn) và report không còn dòng vượt trần." Cả bốn điều kiện đều có số ở ba dòng bằng chứng trên |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | (không chọn) Pilot giữ cả 4 kho, 100%, 1 người trực (NV-HANH) |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | (không chọn) Nhánh còn hở [3b] cửa sổ 7 ngày và [2b] dữ liệu ghi sai được theo dõi bằng risk register C10, không chặn quyết định |
| Nếu Dừng: bài học ghi lại | (không chọn) |
| Ngày quyết định lại (trừ khi Dừng) | **2026-11-30**, trước khi REFUND-v4 có hiệu lực (2026-12-01); hoặc sớm hơn ngay khi có 1 tín hiệu đỏ theo `stop_condition` đã ký |
| PIC ký | NV-TUNG (Lê Thanh Tùng), soạn bởi Vũ Ngọc Tùng-2A202604106 |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: **Đổi** từ Thu hẹp (v1) sang Tiếp tục. v1 chọn Thu hẹp chỉ vì dòng "Tiếp tục" đã ký đòi đạt **cả trên gói sự cố**, mà lúc đó chưa có. Nay gói S1 after có pass_rate 1.0, lỗi oan 0 (từ 15 ở prepared), hoàn sai 0 (từ 275.000đ), hoàn thiếu 0 (từ 105.000đ), mà bộ nền vẫn 110/110: đủ điều kiện "Tiếp tục" đã ký.
- Report tự kiểm tra: mã lần chạy `R-S1-grade-20261119-163303-e46e1d` · ô nào còn đỏ (nguyên nhân × tầng): không còn ô đỏ; `PASS-VISIBLE` (1 integrity, 2 criteria, 3 visible, 5 regression, 6 monitor đều ✅; 4 hidden do team chấm chạy).
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: Đỡ được nhánh [1] (khách khai nhiều hơn tracking: S1-01, 02, 04 về đúng; S1-03 hạ về 30.000đ) và lỗi hãng của S1-21 (cổng pháp lý `delay_cause`): lỗi oan 30 → 15, hoàn sai 985.000đ → 275.000đ, ROI −2.74 → 0.58. Bỏ sót: [2] `delivered_date` trống (S1-20, 21), [3] trần lỗi/hãng/ngày (S1-42, 43; pre-mortem đã nêu nhưng chưa code), [4] khách khai ít hơn (S1-07).
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: Report ghi **"Mọi ngưỡng đã ký đều đạt. Được phép cân nhắc 'Tiếp tục'"**; quyết định Tiếp tục khớp.
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: Chưa đo **cửa sổ 7 ngày** (hợp đồng GHSH: 3 lỗi/7 ngày) và **tracking ghi sai** (không trống). Vì vậy Tiếp tục kèm điều kiện: NV-OANH cộng lỗi 7 ngày mỗi sáng, có 1 lỗi oan trong pilot là quay về "Cải tiến thêm"; bài kiểm tra ẩn (đơn, khách, cách viết khác) cũng chưa chạy trên máy bàn.

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: Đội giả định khi điểm phát đã ghi `delivered_date` và `delay_cause` thì hai trường đó đúng; thẻ S1 cho thấy chúng có thể trống dù hàng đã giao (O-2120, O-2121), và ngoài thực tế còn có thể bị nhập bù sai ngày, khi đó cổng vẫn tin tracking.
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: Cổng NGĂN được lỗi oan do số khách khai và do tracking thiếu dữ liệu (tính lại mọi số từ tracking, dữ liệu thiếu thì chuyển người; S1 lỗi oan 15 → 0), nhưng chỉ GIẢM nguy cơ hãng nhỏ bị ngưng tuyến vì trần 2 lỗi/hãng/ngày chưa nhìn cửa sổ 3 lỗi/7 ngày của hợp đồng và không thấy tracking ghi sai.
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: Đo tỉ lệ kiện DELIVERED thiếu hoặc sai `delivered_date` so với chữ ký giao của hãng, số lỗi mỗi hãng trong 7 ngày (`max_faults_per_carrier_day` cộng dồn) cùng số khiếu nại hãng được xác nhận, và thời gian chờ thật của NV-HANH khi tỉ lệ chuyển người lên khoảng 38% như trên gói S1.
