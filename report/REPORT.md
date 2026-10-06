# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Chưa cung cấp | Chưa cung cấp | Hoàn thiện harness, thiết kế thí nghiệm, phân tích và báo cáo |

- Mô hình, nhiệt độ, `recursion_limit`: chưa cấu hình model; dự kiến `LAB_TEMPERATURE=0`, `recursion_limit=60` theo cấu hình mặc định của lab.
- Deep Agents: `0.7.21`; hệ điều hành Windows; chạy trực tiếp bằng Python 3.12 từ runtime cục bộ.
- Số lần chạy tác vụ đã dùng / ngân sách: 0 lượt gọi model; 29/29 test offline đạt.
- Commit của tag `freeze`: chưa tạo; chỉ tạo sau khi curator sinh skill và trước các lượt chạy chính thức.

## 2. Giả thuyết (commit trước tag `freeze`)

- H1 (subagents so với baseline): `subagents` có thể tăng độ tin cậy ở tác vụ nhiều bước nhờ tách vai trò khảo sát, thực hiện và rà soát, nhưng điểm đánh giá trung bình được dự đoán chỉ ngang hoặc nhỉnh hơn `baseline`, trong khi token cao hơn rõ rệt vì mỗi lần giao việc phát sinh thêm lượt gọi mô hình.
- H2 (skills-auto so với baseline): `skills-auto` được dự đoán cải thiện các check quy ước tương tự lỗi đã thấy ở tập học khi agent thực sự đọc skill; mức cải thiện check kỹ thuật có thể nhỏ và lợi ích trên quy ước mới của tập đánh giá không chắc chắn vì skill tự sinh dễ quá khớp. Căn cứ là lưu ý trong tài liệu lab: skill do mô hình tự sinh trung bình không bảo đảm có lợi và lợi ích trên tập học có thể không chuyển sang tác vụ mới.
- H3 (tác vụ học so với tác vụ đánh giá): mức tăng của `skills-auto` so với `baseline` được dự đoán lớn hơn trên tác vụ học so với tác vụ đánh giá, vì curator chỉ nhận phản hồi từ tập học và bị chặn hoàn toàn khỏi định danh/dữ liệu đánh giá; chênh lệch này, nếu xuất hiện, là dấu hiệu quá khớp chứ không phải bằng chứng rò rỉ.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định nhận các công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, công cụ shell `execute`, và công cụ giao việc `task`. `execute` là công cụ chạy lệnh.
2. `task` mô tả `general-purpose` là subagent dùng cho nghiên cứu câu hỏi phức tạp, tìm tệp/nội dung và tác vụ nhiều bước, có cùng tập công cụ với tác tử chính. Mỗi lần gọi là một phiên độc lập: subagent chỉ thấy prompt giao việc và trả về một báo cáo cuối, nên tác tử chính phải truyền đủ ngữ cảnh.
3. Chỉ dẫn hành vi tiêu biểu của `task`: dùng một message có nhiều tool call khi các việc độc lập để chạy song song. Chỉ dẫn của `execute`: dùng đường dẫn tuyệt đối, tránh `cd`, và ưu tiên công cụ `grep`/`glob`/`read_file` thay cho lệnh tìm kiếm trong shell.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Chưa có dữ liệu vì model/API chưa được cấu hình. Bảng này sẽ chỉ được điền từ các check thất bại của ba lượt `baseline` trên tác vụ học.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| Chờ kết quả thực nghiệm | Chờ kết quả thực nghiệm | Chờ phân loại | Không suy diễn dữ liệu trước khi chạy |

Nhận xét sẽ dựa trên `run.json`, `trace.md` và kết quả `scripts/check_breakdown.py`, không dựa trên workspace gốc.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` đọc và thu thập bằng chứng nhưng không sửa; `implementer` thực hiện thay đổi có phạm vi và kiểm thử; `reviewer` kiểm tra độc lập yêu cầu, edge case và đầu ra nhưng không sửa. Ba vai trò tách khám phá, hành động và kiểm chứng để giảm xung đột trách nhiệm.
- `subagent_calls` ở từng tác vụ: chờ kết quả thực nghiệm.
- Chất lượng thông tin trong lời giao việc: sẽ đối chiếu trực tiếp tool call `task` và báo cáo trả về trong `trace.md`.
- Ảnh hưởng đến token và thời gian: sẽ so sánh trung bình với `baseline` sau khi đủ sáu lượt mỗi điều kiện.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: chưa chạy vì chưa có kết quả `baseline` của tác vụ học.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| Chờ curator sinh tự động | Chờ đánh giá | Chờ đánh giá | Chờ kết quả thực nghiệm |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Chưa tạo bảng chính thức vì chưa có kết quả model. `report/table.md` sẽ được sinh bằng `python -m lab.compare` sau khi đủ 18 lượt chạy hợp lệ.

## 8. Phân tích

Phần này sẽ được điền sau khi có số liệu. Phân tích sẽ: (1) tách learning/evaluation; (2) tách check kỹ thuật và `rule_`; (3) đối chiếu `skills_read` với trace; (4) so sánh token và điểm/token; (5) kiểm tra rò rỉ/quá khớp; và (6) ước lượng nhiễu bằng hai lượt learning dùng cùng bộ skill.

## 9. Hạn chế và tính hợp lệ

1. Chỉ có ba họ tác vụ và một tác vụ cho mỗi vai trò trong mỗi họ; một trường hợp bất thường có thể dịch chuyển trung bình lớn, nên kết luận chỉ áp dụng cho phạm vi benchmark này.
2. Thiết kế chính chạy mỗi cấu hình một lần trong khi đầu ra mô hình vẫn có nhiễu dù nhiệt độ bằng 0; khác biệt nhỏ có thể là dao động chạy, vì vậy phải đối chiếu lượt learning trước/sau freeze và không diễn giải quá mức.
3. Các tác vụ và quy ước ẩn do cùng một nhóm thiết kế; cấu trúc lỗi có thể thuận lợi bất thường cho curator, làm giảm tính khái quát sang dự án thực tế.
4. Chỉ một model được đánh giá; kết luận về subagent và skill phụ thuộc năng lực dùng công cụ, tuân thủ prompt và context window của model đó.
5. Trace chỉ lưu luồng chính, không lưu thao tác nội bộ của subagent; giải thích cơ chế đa tác tử vì vậy dựa trên lời giao việc và báo cáo cuối, không quan sát được toàn bộ quá trình.

## 10. Kết luận

Chưa kết luận trước khi hoàn tất các lượt chạy chính thức. Kết luận cuối sẽ chỉ nêu các khác biệt được bảng điểm, token, check breakdown và trace cùng hỗ trợ.

## Phụ lục

- Lệnh đã chạy: `pip install -e .`; `python scripts/tour.py`; `python -m pytest -q` (29 passed); `python scripts/check_breakdown.py`.
- Thử thách mở rộng: chưa thực hiện; chỉ cân nhắc sau khi hoàn tất toàn bộ hạng mục chính.
- Ghi chú: không tạo skill thủ công, không tạo kết quả giả và chưa đọc dữ liệu đánh giá để phục vụ curator.
