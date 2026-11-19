"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

# Cổng vòng 1 của bàn Muller. Mọi kiểm tra chỉ dựa vào NGUỒN SỰ THẬT (tracking DB, chính sách theo ngày hiệu lực,
# bảng phê duyệt, sổ cái, bảng lỗi hãng); không bao giờ tin con số khách tự gõ, không xử lý riêng theo mã ticket.
#   Cổng 1 (B6 kỹ thuật, B2 lỗi 1)  issue_refund: tiền ≤ quyền lợi tính từ DB; phê duyệt phải hợp lệ; không hoàn trùng;
#                                    không ghi khi model lỗi (fail_open) hoặc khi làm theo câu lệnh trong chữ khách.
#   Cổng 2 (B6 pháp lý, B4 WRONG/INCOMPLETE) file_carrier_fault: chỉ ghi khi tracking xác nhận lỗi hãng, đúng kiện,
#                                    đúng số ngày; notify_carrier chỉ gửi các trường chính sách cho phép.
#   Cổng 3 (B6 kinh doanh)          trần tiền hoàn tự động mỗi ngày: config business.daily_refund_cap_vnd (tools.py áp dụng).
#   pre_guard (B4 INVALID)          ghim phiên bản chính sách theo NGÀY HIỆU LỰC, không theo cờ index_active.


def _policy(ctx):
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """Sự thật về đơn của ticket này: (order, parcel, db_delay, policy). None nếu thiếu."""
    order = ctx.tools.lookup_order(order_id)
    policy = _policy(ctx)
    if order is None or policy is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), policy


def _seen(ctx, kind):
    return any(e.get("type") == kind for e in ctx.events)


def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có chính sách hoàn tiền hiệu lực cho ngày hôm nay")
    ctx.log("policy_pinned", policy_id=pol["policy_id"], as_of=ctx.as_of)
    return Verdict.allow(policy_id=pol["policy_id"])


def _gate_refund(ctx, action):
    # model không chạy được mà vẫn "hoàn cho vui lòng khách" -> người xử lý
    if action.get("basis") == "fail_open":
        return Verdict.escalate("kiểm tra chính sách bằng model lỗi (fail_open): chuyển người duyệt")
    # chữ khách / ghi chú đơn chứa câu lệnh mà trợ lý đã làm theo -> không ghi gì, chuyển người
    if _seen(ctx, "directive_obeyed"):
        return Verdict.escalate("ticket chứa câu lệnh cho hệ thống: chuyển người duyệt")
    if action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate(f"bên trả tiền {action.get('payer')} không theo chính sách: chuyển người duyệt")

    # không hoàn trùng: đơn đã có dòng hoàn trong sổ cái (ghi lại lần 2, hoặc cờ đối soát đêm chưa cập nhật)
    if ctx.tools.ledger_rows(order_id=action.get("order_id")):
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái: không hoàn lần nữa")

    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.escalate("thiếu dữ liệu đơn / tracking / chính sách: chuyển người duyệt")
    order, parcel, delay, policy = f
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    amount = action.get("amount_vnd", 0)

    # phê duyệt phải đúng ticket, đúng đơn, còn hiệu lực, đủ hạn mức
    appr_id = action.get("approval_id")
    if appr_id:
        a = next(iter(ctx.tools.lookup_approvals(approval_id=appr_id)), None)
        ok = (a is not None and a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
              and a.get("ticket_id") == ctx.ticket.get("ticket_id") and a.get("order_id") == order["order_id"]
              and a.get("max_vnd", 0) >= min(amount, entitled))
        if not ok:
            return Verdict.escalate(f"phê duyệt {appr_id} không hợp lệ cho ticket này: chuyển người duyệt")
    elif min(amount, entitled) > policy["auto_limit_vnd"]:
        return Verdict.escalate("vượt hạn mức tự động của chính sách hiệu lực, chưa có phê duyệt")

    # tiền không vượt quyền lợi tính từ tracking DB (không dùng số ngày khách tự khai)
    if amount > entitled:
        ctx.log("refund_vs_db", asked=amount, entitled=entitled, db_delay_days=delay)
        if entitled <= 0:
            return Verdict.deny(f"theo tracking đơn trễ {delay} ngày, chưa đủ điều kiện hoàn")
        return Verdict.modify(f"hạ số tiền về quyền lợi theo tracking ({entitled}đ)", amount_vnd=entitled)
    return Verdict.allow()


def _gate_fault(ctx, action):
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.deny("thiếu dữ liệu để ghi lỗi hãng")
    order, parcel, delay, policy = f
    if not parcel.get("delay_cause") or not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny(f"tracking không xác nhận lỗi hãng (trễ {delay} ngày, nguyên nhân "
                            f"{parcel.get('delay_cause')}): không ghi lỗi")
    fix = {k: parcel.get(k) for k in ("parcel_id", "carrier_id", "driver_id")}
    fix["delay_days"] = delay
    if any(action.get(k) != v for k, v in fix.items()):
        return Verdict.modify("ghi lỗi đúng kiện, đúng hãng, đúng số ngày theo tracking", **fix)
    return Verdict.allow()


def _gate_notify(ctx, action):
    pol = _policy(ctx)
    allowed = set((pol or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "district", "delay_days"])
    payload = dict(action.get("payload") or {})
    clean = {k: v for k, v in payload.items() if k in allowed}
    faults = [r for r in ctx.tools.fault_rows(ticket_id=action.get("ticket_id"))
              if r.get("parcel_id") == clean.get("parcel_id")]
    if faults:
        clean["delay_days"] = faults[-1].get("delay_days")
    if clean != payload:
        return Verdict.modify("chỉ gửi hãng các trường chính sách cho phép (không gửi chữ khách, liên hệ người nhận)",
                              payload=clean)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()
