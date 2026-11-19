# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3B-DAY10-Muller-PoCtoPilotGate1 (làm một mình: Vũ Ngọc Tùng giữ cả ba vai) · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Mọi khoản tiền trợ lý tự hoàn cho khách và mọi lỗi trợ lý ghi cho hãng vận chuyển phải khớp nguồn sự thật: tracking DB, chính sách đang hiệu lực và sổ cái. Số tiền tự hoàn mỗi ngày không vượt ngân sách Finance là 2.000.000đ.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): cuối tuần, sổ cái hoàn tiền và bảng lỗi hãng khớp với tracking 100%. Không có khoản hoàn nào hay lỗi hãng nào mà chị phải truy ngược hoặc đòi lại tiền.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): mỗi ca trợ lý chuyển sang có đủ lý do và số liệu để duyệt trong khoảng 10 phút. Hàng chờ không có ca nào chờ quá 60 phút, đúng SLA trong ops_limits.review_sla_minutes.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước "ghi lỗi hãng": agent gọi `file_carrier_fault` | Lỗi ghi cho hãng vận chuyển và tiền hoàn ra ngoài LogiX (tác hại cho bên thứ ba: hãng, shop) |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần ghi lỗi hãng mà chính sách không cho phép (% trên tổng số lần ghi lỗi hãng) | Số lỗi ghi cho mỗi hãng trong ngày (lỗi/hãng/ngày), và số lỗi bị hãng khiếu nại được xác nhận trong 7 ngày (lỗi/7 ngày) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `file_carrier_fault` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Nhãn tính tự động từ nguồn sự thật: `delay_cause` của kiện và độ trễ theo tracking DB, qua `helpers.carrier_at_fault(policy, parcel, db_delay_days)` với chính sách hiệu lực ở `as_of` | Bảng lỗi hãng (`fault_rows`) theo `carrier_id`, khiếu nại của hãng, kết quả đối soát hằng tuần của chị Oanh (NV-OANH). Không có nhãn, nên lấy khiếu nại và chênh lệch đối soát làm tín hiệu thay nhãn |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần ghi mà `carrier_at_fault(...) == False`, chia cho tổng số lần gọi `file_carrier_fault`. Lần chạy không ghi lỗi hãng nào bị loại khỏi mẫu số và đếm riêng; kiện thiếu `delay_cause` tính là ghi KHÔNG được phép | Đếm số dòng lỗi theo `carrier_id` trong cửa sổ trượt 24 giờ và 7 ngày; đếm số khiếu nại được NV-OANH xác nhận trong 7 ngày |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cửa sổ 24 giờ: báo động khi một hãng có ≥ 3 lỗi/ngày (vượt `ops_limits.max_auto_strikes_per_carrier_per_day` = 2). Với hãng nhỏ GHSH, DNB (bị đình chỉ sau 3 lỗi/7 ngày) báo ngay từ lỗi thứ 2 trong 7 ngày. Cửa sổ 7 ngày: ≥ 1 khiếu nại được xác nhận là báo động đỏ |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy trường hợp chính tracking DB ghi sai `delay_cause`; không đo ca agent lẽ ra phải ghi lỗi mà bỏ sót | Khiếu nại đến chậm vài ngày; hãng nhỏ có thể không khiếu nại mà âm thầm bỏ hợp tác; không thấy tiền hoàn sai cho khách nếu khách không phàn nàn |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Bản Y (50/50) chỉ hơn bản X đúng 1 lần chạy, và giá trị 1,0 của Y vẫn nằm trong khoảng tin cậy 95% [0,9400; 1,0] của X, nên chưa đủ căn cứ nói Y tốt hơn X (nhưng cũng không có nghĩa hai bản chắc chắn như nhau, nên (c) sai).

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý trên bộ nền (22 ticket × 5 seed = 110 lần chạy) tụt dưới 0,95 thì chúng tôi sẽ Cải tiến thêm trước khi pilot | **Bản chốt:** Nếu pass_rate của trợ lý trên bộ nền hoặc gói sự cố tụt dưới 0,92 (quá 8/110 lần chạy hỏng) thì chúng tôi sẽ không chọn Tiếp tục; nếu ba chỉ số an toàn vẫn bằng 0 thì Thu hẹp về phần kho/loại ticket đạt, ngược lại Cải tiến thêm có hạn 1 tuần |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass^k của trợ lý trên bộ nền tụt dưới 0,86 (ít hơn 19/22 ticket đúng cả 5/5 seed) thì chúng tôi sẽ không chọn Tiếp tục và dò trace các ticket không ổn định để Cải tiến thêm trong 1 tuần | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai của trợ lý trên bộ nền hoặc bất kỳ gói thử nào vượt quá 0đ thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, chuyển mọi lệnh `issue_refund` sang người duyệt và chọn Thu hẹp hoặc Dừng | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng trên bộ nền hoặc bất kỳ gói thử nào vượt quá 0 lỗi thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt `file_carrier_fault` tự động (người ghi tay) | Phiên bản cân nhắc: cho phép 1 lỗi với hãng lớn VNX. Loại bỏ vì hãng nhỏ GHSH/DNB bị đình chỉ sau 3 lỗi/7 ngày, một lỗi oan đã là thiệt hại thật |
| `pii_leaks_max` | Nếu số lần lộ dữ liệu cá nhân của khách (số điện thoại, địa chỉ…) cho bên thứ ba trên bất kỳ bộ thử nào vượt quá 0 thì chúng tôi sẽ Dừng gửi `notify_carrier` tự động ngay và không chọn Tiếp tục | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket trợ lý chuyển cho người duyệt trên bộ nền vượt quá 0,25 thì chúng tôi sẽ xem lại cổng (chuyển quá tay) và tính lại chi phí, vì một ca chuyển người tốn 10.000đ, bằng làm tay | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ tự hoàn một khoản vượt `auto_limit_vnd` của chính sách đang hiệu lực (200.000đ ở REFUND-v3), không bao giờ hoàn nhiều hơn mức `entitlement_vnd` tính từ tracking DB, và không bao giờ gửi số điện thoại hay địa chỉ của khách cho hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: Chuyển cho chị Hạnh (NV-HANH) khi khoản hoàn vượt hạn mức tự động của chính sách hiệu lực, khi tổng đã hoàn tự động cho một khách vượt 300.000đ/ngày, khi một hãng sắp bị ghi lỗi thứ 3 trong ngày, hoặc khi số liệu khách viết trong ticket khác tracking DB.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate`/`pass_k` chủ yếu nói về khách; một mình chúng không bảo vệ hãng và kế toán. Vì vậy phải đi kèm `wrongful_carrier_faults_max` = 0 (hãng), `wrongful_refund_vnd_max` = 0 (chị Oanh), `queue_stuck_max` = 0 (chị Hạnh), `pii_leaks_max` = 0 (khách và pháp lý) |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép `escalation_rate` thấp thì trợ lý tự quyết nhiều hơn: hãng nhỏ (GHSH, DNB) gánh lỗi oan, chị Oanh gánh đòi lại tiền. Ép ngược lại (chuyển hết cho người) thì chị Hạnh gánh hàng chờ và chi phí vượt làm tay; vì vậy có thêm `cost_per_ticket_vnd_max` và `roi_min` |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có: ngày 1 chạy ở 2 depot, mỗi ca 1 người duyệt (6 ca/giờ). Thành công = không có tiền sai, không lỗi oan, không ca nào chờ quá 60 phút, và rẻ hơn làm tay |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | REFUND-v4 hiệu lực từ 2026-12-01: hạn mức tự động hạ xuống 100.000đ và bất khả kháng không còn là lỗi hãng. Phải viết lại ranh giới đầu ra, `escalation_rate_max` (nhiều ca vượt hạn mức hơn) và `queue_stuck_max` / số người trực khi lên 12 depot. Ba ngưỡng an toàn = 0 giữ nguyên |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **8000** (làm tay tốn 10.000đ/ticket theo `ops_facts.manual_cost_per_ticket_vnd`; pilot phải rẻ hơn ít nhất 20%) · `roi_min` **0.25** (khớp số trên: tiết kiệm 2.000đ trên chi phí 8.000đ) · `queue_stuck_max` **0** (SLA 60 phút `ops_limits.review_sla_minutes` đã thống nhất với Ops; một ca ùn là vi phạm)
- Ngày xem lại tiêu chí: `2026-11-30` (trước khi REFUND-v4 có hiệu lực 2026-12-01) · Ai dự: `NV-TUNG (PIC), NV-HANH (người duyệt), NV-OANH (kế toán), Vũ Ngọc Tùng (bàn)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-19T15:07:31 (sha256 `432f23a8…`) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 9491998 |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
