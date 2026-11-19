"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _attempted_faults(t):
    """Số lệnh ghi lỗi hãng trợ lý ĐỊNH ghi trong trial (đã ghi, hoặc bị cổng chặn), theo hãng."""
    out = {}
    for e in t.get("events") or []:
        if e.get("type") == "tool" and e.get("tool") == "file_carrier_fault":
            out[e.get("carrier_id")] = out.get(e.get("carrier_id"), 0) + 1
        elif e.get("type") == "guard" and e.get("kind") == "carrier_strike_cap":
            out[e.get("carrier_id")] = out.get(e.get("carrier_id"), 0) + 1
    return out


def max_faults_per_carrier_day(trials):
    """Thẻ S1 · lỗi hãng dồn trong một ngày. Số lệnh ghi lỗi lớn nhất mà MỘT hãng phải nhận trong MỘT ngày vận hành
    (cùng seed, cùng day), kể cả lệnh bị cổng trần giữ lại. So với trần 2 (ops_limits) và ngưỡng ngưng tuyến 3/7 ngày."""
    per = {}
    for t in trials:
        for carrier, n in _attempted_faults(t).items():
            key = (t.get("seed"), t.get("day"), carrier)
            per[key] = per.get(key, 0) + n
    return max(per.values(), default=0)


def model_override_rate(trials):
    """Tỉ lệ trial mà model lấy số ngày khách khai đè lên số của tracking DB (sự kiện model_override)."""
    hit = sum(any(e.get("type") == "model_override" for e in (t.get("events") or [])) for t in trials)
    return round(hit / max(1, len(trials)), 4)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "max_faults_per_carrier_day": max_faults_per_carrier_day,   # thẻ S1: lỗi dồn về một hãng trong một ngày
    "model_override_rate": model_override_rate,                 # số khách khai đè lên tracking
}
STARTER_MONITORS = ("escalation_rate",)
