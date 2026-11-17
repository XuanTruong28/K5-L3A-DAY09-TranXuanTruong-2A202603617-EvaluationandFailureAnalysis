# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID: `R-seeded_regression-C-002-11` |
| Triệu chứng | `lab8.metrics.trial_pass` báo FAIL (status resolved != denied); reply thông báo "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202" trong khi label mong đợi là denied và refund=0 |
| Bước sai đầu tiên | Event 3, kind: `model_override`, payload: `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 (`handoff`) khởi tạo đúng contract, Event 2 (`investigator: lookup_order`) trả về dữ liệu đơn hàng chính xác từ DB với số ngày trễ thực tế `delay_days=2` (chưa đủ điều kiện hoàn). Tuy nhiên ngay bước 3, agent tự ý dùng `model_override` đè giá trị `delay_days` thành 5 theo lời ticket người dùng |
| Failure mode | FM-03 (`ticket_trust`) |
| Đối chứng | Cùng claim@seed trên shape `fixed`: sau Event 2 investigator thì Event 3 là `quote` trả về `amount_vnd: 0, reason: no_entitlement`, hoàn toàn không có `model_override`, kết quả denied chuẩn xác |
| Regression test | `test_public_single_run_cases[swarm-C-002-11]` trong `test_public_matrix.py` hoặc assertion kiểm tra không có event `model_override` trong trace; test fail trên `seeded_regression` và pass trên `fixed` |
| Chưa chắc chắn | Trace không lưu lại chuỗi suy luận nội tâm (internal reasoning) của MockLLM tại thời điểm quyết định tin ticket hơn DB |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
