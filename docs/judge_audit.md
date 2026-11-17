# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | ĐẠT (κ=0.757≥0.6, P=0.857≥0.8, R=0.800≥0.7) | DÙNG (giám sát giọng điệu) |
| helpful | 100 | 0.375 | 1.000 | 0.300 | KHÔNG ĐẠT (κ=0.375 < 0.6, Recall=0.300 < 0.7) | LOẠI (không dùng làm gate) |

## ≥5 case audit thủ công (trích từ audit tone)
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú & Đề xuất sửa Rubric |
|---|---|---|---|---|---|
| 1 | `H-008` | PASS | FAIL | Người đúng | Câu trả lời *"Em đã hoàn tiền cho anh rồi nha, anh check giúp em"* xưng hô suồng sã ("anh - em", "nha"), không đạt chuẩn CSKH doanh nghiệp. Cần bổ sung rubric: bắt buộc xưng hô "LogiX - anh/chị", cấm từ thân mật không trang trọng. |
| 2 | `H-017` | PASS | FAIL | Người đúng | Dùng *"bạn ơi... rồi nha"*, thiếu tính chuyên nghiệp. Judge bị đánh lừa bởi từ "Dạ" ở đầu câu mà bỏ qua ngữ khí cợt nhả phía sau. |
| 3 | `H-029` | PASS | FAIL | Người đúng | *"Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm."* Giọng điệu cộc lốc, gạt phăng khách hàng. Judge không phân biệt được sự lịch sự giả tạo với thái độ phục vụ chuẩn mực. |
| 4 | `H-042` | FAIL | PASS | Người đúng | *"Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ."* Câu trả lời chuẩn mực, nêu rõ thời gian dự kiến nhưng Judge bắt lỗi nhầm (False Positive) do câu văn ngắn gọn. |
| 5 | `H-051` | FAIL | PASS | Người đúng | *"Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ."* Judge phạt vì dùng từ tiếng Anh "refund", trong khi thực tế ngành e-commerce/fintech chấp nhận từ mượn này. |

## Kết luận
- **Tiêu chí bị loại:** `helpful` bị loại hoàn toàn khỏi release gate vì:
  + Ma trận nhầm lẫn: `tp=9, fp=0, fn=21, tn=70`.
  + Tỉ lệ bỏ lọt lỗi cực cao: `fn=21` trên tổng số 30 ca lỗi (Recall chỉ đạt 30.0%, Kappa đạt 0.375 thảm hại).
  + Judge bị đánh lừa bởi các mẫu câu xin lỗi sáo rỗng (*"Dạ, LogiX thành thật xin lỗi anh/chị vì sự bất tiện này..."*) mà không kiểm tra xem câu trả lời có giải quyết được thắc mắc hay cung cấp hướng dẫn tiếp theo cho khách hàng hay không. Tỉ lệ lỗi thực tế (sau hiệu chỉnh Rogan-Gladen) là 30.0% nhưng judge chỉ thấy 9.0%.
- **Rủi ro còn lại:** Cả hai judge đều được replay trên tập CSV công khai tĩnh; cần định kỳ lấy mẫu trace sản xuất và gán nhãn người (blind human review) để đánh giá held-out định kỳ.
