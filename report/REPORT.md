# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Chưa cung cấp | Chưa cung cấp | Hoàn thiện harness, thiết kế và chạy thí nghiệm, phân tích kết quả |

- Mô hình chính thức: `deepseek:deepseek-reasoner`; `LAB_TEMPERATURE=0`. `recursion_limit=60`, riêng các lượt dữ liệu phải chạy lại sau lỗi đệ quy dùng 80 (`skills-auto/data-learn`, `subagents/data-eval`, `skills-auto/data-eval`). Các `run.json` chính thức đều không còn `error`.
- Deep Agents `0.7.21`, Python 3.12, Windows, chạy trực tiếp. Backend dùng môi trường tối thiểu, tắt pytest plugin tự nạp và chỉ chuyển các biến hệ thống Windows không chứa bí mật.
- Khoảng 30 lượt tác vụ đã thử: 18 lượt chính thức, 3 lượt `skills-auto` trước freeze giữ ở `results/skills-auto-dev/`, và 9 lượt chẩn đoán/chạy lại/bị ngắt. Các lượt DeepSeek Chat bị vòng lặp đã bị ghi đè; toàn bộ số liệu chính thức dùng DeepSeek Reasoner.
- Commit `hypotheses`: `0516fe7`; commit và tag `freeze`: `8fe9ad6`.
- Kiểm tra cuối: 29/29 test offline đạt; `verify_freeze.py` kiểm tra 6 lượt skill và báo `OK`.

## 2. Giả thuyết (đã commit trước tag `freeze`)

- H1 (subagents so với baseline): `subagents` có thể tăng độ tin cậy ở tác vụ nhiều bước nhờ tách vai trò khảo sát, thực hiện và rà soát, nhưng điểm đánh giá trung bình được dự đoán chỉ ngang hoặc nhỉnh hơn `baseline`, trong khi token cao hơn rõ rệt vì mỗi lần giao việc phát sinh thêm lượt gọi mô hình.
- H2 (skills-auto so với baseline): `skills-auto` được dự đoán cải thiện các check quy ước tương tự lỗi đã thấy ở tập học khi agent thực sự đọc skill; mức cải thiện check kỹ thuật có thể nhỏ và lợi ích trên quy ước mới của tập đánh giá không chắc chắn vì skill tự sinh dễ quá khớp. Căn cứ trong tài liệu lab: SkillsBench báo skill do người biên soạn tăng trung bình khoảng 16 điểm phần trăm nhưng skill tự sinh trung bình không bảo đảm có lợi; SkillEvolBench ghi nhận lợi ích tập học thường không chuyển sang tác vụ mới.
- H3 (tác vụ học so với tác vụ đánh giá): mức tăng của `skills-auto` so với `baseline` được dự đoán lớn hơn trên tác vụ học so với tác vụ đánh giá, vì curator chỉ nhận phản hồi từ tập học và bị chặn khỏi dữ liệu đánh giá; chênh lệch này, nếu có, là dấu hiệu quá khớp chứ không phải bằng chứng rò rỉ.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định nhận các công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, công cụ shell `execute`, và công cụ giao việc `task`. `execute` là công cụ chạy lệnh.
2. `task` mô tả `general-purpose` là subagent dùng cho nghiên cứu câu hỏi phức tạp, tìm tệp/nội dung và tác vụ nhiều bước, có cùng tập công cụ với tác tử chính. Mỗi lần gọi là một phiên độc lập: subagent chỉ thấy prompt giao việc và trả về một báo cáo cuối, nên tác tử chính phải truyền đủ ngữ cảnh.
3. Chỉ dẫn tiêu biểu của `task`: dùng một message có nhiều tool call khi các việc độc lập để chạy song song. Chỉ dẫn của `execute`: dùng đường dẫn ổn định và ưu tiên `grep`/`glob`/`read_file` thay cho lệnh tìm kiếm trong shell.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Ba tác vụ học baseline đạt 17/18 check kỹ thuật nhưng 0/9 check quy ước. Vì vậy bằng chứng phủ định cho nhóm A–D là mạnh: agent xử lý đúng gần như toàn bộ logic kỹ thuật; nhóm E chiếm 9/10 lỗi. Ngoại lệ kỹ thuật duy nhất là agent đã sửa tệp test hiện có.

| Tác vụ | Check thất bại | Nhóm | Bằng chứng từ `detail` |
|---|---|---|---|
| code-learn | `tests_not_modified` | A – bỏ qua đặc tả | “the original files in tests/ must not be modified” |
| code-learn | `rule_type_hints` | E – quy ước | “every public function ... has type annotations...” |
| code-learn | `rule_regression_tests` | E – quy ước | “add tests/test_regressions.py ... at least 3” |
| code-learn | `rule_changelog` | E – quy ước | yêu cầu ít nhất 3 bullet theo mẫu `fix(<function name>)` |
| data-learn | `rule_money_in_cents` | E – quy ước | tiền trong `answer.json` phải là integer cents |
| data-learn | `rule_meta_block` | E – quy ước | yêu cầu object `meta` với `source`, `rows_in`, `rows_used` |
| data-learn | `rule_clean_csv` | E – quy ước | yêu cầu `clean.csv` với schema và chuẩn hóa cụ thể |
| logs-learn | `rule_service_names` | E – quy ước | service phải lower-case và đổi `-` thành `_` |
| logs-learn | `rule_sorted_errors` | E – quy ước | `errors` phải sort theo service rồi timestamp |
| logs-learn | `rule_schema_header` | E – quy ước | yêu cầu `schema_version=2`, `generated_by=log-triage` |

Nhóm E chiếm đa số tuyệt đối. Skill có thể mã hóa quy trình rà soát deliverable và các quy ước đã nhận phản hồi, nhưng không thể biết chính xác một quy ước hoàn toàn mới nếu đề bài không nêu.

## 5. Điều kiện `subagents` (Phần 2.3)

- Đã định nghĩa `explorer` (đọc và báo bằng chứng, không sửa), `implementer` (sửa có phạm vi và kiểm thử), `reviewer` (kiểm tra độc lập, không sửa).
- Số `subagent_calls`: `code-learn=0`, `data-learn=1`, `logs-learn=0`, `code-eval=2`, `data-eval=0`, `logs-eval=1`.
- `data-learn` giao cho subagent mặc định toàn bộ schema, quy tắc ngày/múi giờ, dữ liệu thiếu và năm giá trị cần kiểm tra; thông tin đủ và kết quả được đối chiếu. `code-eval` gọi song song `implementer` và `explorer` với đường dẫn, giới hạn sửa và đặc tả hàm khá đầy đủ, nhưng explorer kết luận “Everything passes” và implementer không bao phủ các quy ước ẩn; điểm còn giảm từ 7/11 xuống 6/11. `logs-eval` truyền đầy đủ định dạng log/output cho subagent mặc định nhưng vẫn không biết bốn quy ước mới.
- Trung bình toàn bộ: baseline 100,261 token và 33.2 giây/lượt; subagents 262,602 token và 74.9 giây/lượt, khoảng 2.62 lần token và 2.26 lần thời gian. Điểm evaluation giảm 0.60 xuống 0.57, nên đa tác tử không đáng chi phí trong thí nghiệm này.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy đúng một lần, sinh ba skill; không skill nào bị xóa hoặc sửa tay. Cả ba qua `validate_skill` và không chứa marker của tập đánh giá.

| Skill | Tổng quát | Đúng/sai | Độ dài, `description`, mức dùng |
|---|---|---|---|
| `code-fix-deliverables` | Tổng quát cho tác vụ sửa package có ràng buộc repo | Đúng; checklist type hint, regression test, changelog và kiểm thử khớp feedback học. Quy tắc changelog vẫn chưa được agent áp dụng đúng. | 11 dòng; description nêu rõ khi có repo-wide constraints. Được đọc trong 6/6 lượt cùng hai skill khác. |
| `output-spec-compliance` | Tổng quát cho output schema, unit, naming, ordering và file phụ | Đúng, ngắn và mệnh lệnh; không chứa tên task/input hay đáp án. Nó không thể cung cấp tên/value của quy ước ẩn mới. | 13 dòng; description rộng và kích hoạt đúng cho data/log/code. Được đọc 6/6 lượt. |
| `verify-artifacts-and-environment` | Tổng quát cho mọi tác vụ chạy script hoặc ghi file | Đúng; nhấn mạnh interpreter, đường dẫn, đọc lại artifact và validation sau cleanup. Một số bước trùng hành vi baseline nên lợi ích điểm không rõ. | 11 dòng; description rộng. Được đọc 6/6 lượt. |

Ở lượt trước freeze, điểm learning là 8/10, 5/8, 6/9. Sau freeze, cùng bộ skill vẫn đạt đúng ba điểm đó; agent luôn đọc cả ba skill vì `SKILLS_NOTE` yêu cầu đọc skill có description phù hợp.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 6/10 | 8/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 6/9 |
| code-eval | 7/11 | 6/11 | 8/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.63 | 0.63 | 0.70 |
| **Mean score - evaluation tasks** | 0.60 | 0.57 | 0.63 |
| **Mean tokens per run** | 100,261 | 262,602 | 164,388 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

Phân rã check:

| Điều kiện | Vai trò | Kỹ thuật | Quy ước | Token TB | Đọc skill |
|---|---|---:|---:|---:|---:|
| baseline | eval | 17/18 | 1/12 | 116,470 | 0/3 |
| baseline | learn | 17/18 | 0/9 | 84,053 | 0/3 |
| subagents | eval | 17/18 | 0/12 | 302,867 | 0/3 |
| subagents | learn | 17/18 | 0/9 | 222,338 | 0/3 |
| skills-auto | eval | 17/18 | 2/12 | 178,999 | 3/3 |
| skills-auto | learn | 17/18 | 2/9 | 149,777 | 3/3 |

Không lượt chính thức nào có `error` hoặc `skills_modified=true`. Các lỗi recursion trong giai đoạn chẩn đoán đã được chạy lại và ghi đè; kết quả trước-freeze được giữ ở thư mục backup không được `lab.compare` đọc.

## 8. Phân tích

1. Trên learning, `skills-auto` tăng mean score từ 0.63 lên 0.70; `subagents` giữ 0.63. Trên evaluation, `skills-auto` tăng 0.60 lên 0.63 còn `subagents` giảm xuống 0.57. H3 chỉ được hỗ trợ một phần: mức tăng learning (+0.07) lớn hơn evaluation (+0.03), nhưng skill vẫn chuyển giao được một phần sang code-eval.
2. Cả ba điều kiện cùng đạt 17/18 check kỹ thuật ở cả hai vai trò. Skill nâng check quy ước từ 0/9 lên 2/9 trên learning và từ 1/12 lên 2/12 trên evaluation. Hai lợi ích learning nằm ở `rule_type_hints` và `rule_regression_tests`; trên code-eval skill giúp `rule_regression_tests` nhưng quy ước mới `rule_version_bump` vẫn thất bại. Các quy ước mới không có nội dung cụ thể trong skill nên agent không thể suy ra chính xác.
3. Trace `skills-auto/code-learn` đọc `code-fix-deliverables` trước, sau đó rà public functions và tạo regression tests, khiến hai check tương ứng chuyển từ fail sang pass. Ngược lại, ở data/log agent đã đọc `output-spec-compliance` nhưng chỉ tạo các key/file được đề công khai yêu cầu; trace `data-learn` ghi rõ không invent convention khi không có tài liệu, nên `meta`, cents và `clean.csv` vẫn fail.
4. Mean token lần lượt là 100,261; 262,602; 164,388. Dùng trung bình hai role để chuẩn hóa, điểm trung bình trên 100k token xấp xỉ 0.61 (baseline), 0.23 (subagents), 0.40 (skills-auto). Baseline hiệu quả token cao nhất; skills-auto đổi 64% chi phí tăng thêm lấy khoảng +0.05 điểm chung, còn subagents vừa tốn hơn vừa kém điểm.
5. Không có dấu hiệu rò rỉ evaluation: curator chỉ đọc `role=learn`, validator chặn marker eval, ba skill không có task id/tên input/đáp án, và skill đã commit/tag trước lượt eval. Có dấu hiệu quá khớp nhẹ: skill tăng hai check quy ước code đã thấy nhưng không giải quyết quy ước mới của data/log hoặc version bump.
6. Cùng bộ skill trước và sau freeze cho điểm learning giống hệt: 8/10, 5/8, 6/9; chênh lệch mean score bằng 0.00. Token trung bình thay đổi từ 203,048 xuống 149,777 (giảm khoảng 26%), cho thấy đường đi/cost vẫn nhiễu mạnh dù điểm ổn định; chênh lệch điểm nhỏ chỉ nên xem là bằng chứng yếu với một lượt chạy.

## 9. Hạn chế và tính hợp lệ

1. Chỉ có ba họ tác vụ và một tác vụ cho mỗi vai trò; một check có thể dịch chuyển trung bình nhiều, nên kết luận chỉ áp dụng cho benchmark này.
2. Mỗi cấu hình chính thức chỉ có một lượt. Dù nhiệt độ 0, token trước/sau freeze lệch 26%, cho thấy model và tool path vẫn có nhiễu; chênh lệch 0.03 ở evaluation chưa đủ để kết luận mạnh.
3. Các quy ước ẩn do cùng benchmark thiết kế và có dạng lặp lại; điều này có thể thuận lợi cho curator hơn dự án thật, trong khi quy ước mới lại làm transfer trông kém hơn.
4. Chỉ DeepSeek Reasoner được dùng cho số liệu chính thức; kết luận phụ thuộc năng lực tool calling và xu hướng dùng subagent của model này.
5. `trace.md` chỉ lưu luồng chính; thao tác nội bộ của subagent không quan sát được, nên phân tích delegation chỉ dựa vào prompt và báo cáo cuối.
6. `LocalShellBackend` trên Windows không cô lập shell ở mức hệ điều hành. Prompt ranh giới được thêm sau khi model chẩn đoán từng dò ngoài workspace; dù không thấy khóa API trong artifacts và kết quả chính thức tuân thủ đường dẫn, đây vẫn là đe dọa tới tính an toàn và khả năng tái lập. WSL/Docker là cấu hình phù hợp hơn.
7. Một số lượt data dùng recursion limit 80 thay vì 60 sau khi lượt 60 chạm giới hạn; điều này giúp có bản ghi hợp lệ nhưng làm ngân sách bước không hoàn toàn đồng nhất giữa mọi ô.

## 10. Kết luận

Trong benchmark này, skill tự sinh tăng điểm trung bình nhưng không tăng hiệu quả trên mỗi token so với baseline. Lợi ích chuyển giao chỉ thấy rõ ở họ code và gắn với quy ước đã xuất hiện trong feedback học. Subagent không cải thiện điểm và tốn khoảng 2.62 lần token baseline. Không có bằng chứng rò rỉ evaluation, nhưng có dấu hiệu quá khớp theo loại quy ước. Bước tiếp theo nên lặp mỗi cấu hình ít nhất ba lần trong Docker/WSL và thử skill ngắn hơn, chọn lọc theo family.

## Phụ lục

- Trình tự chính: cài dependency; chạy `scripts/tour.py`; hoàn thiện harness và `pytest`; chạy baseline/subagents learning; `python -m lab.curator`; chạy skill learning và sao lưu; commit hypotheses/freeze và tag; chạy evaluation; chạy lại `skills-auto`; sinh `report/table.md`; chạy breakdown và verify.
- Lệnh kiểm tra cuối: `python -m pytest -q`; `python -m lab.compare`; `python scripts/check_breakdown.py`; trên Windows dùng `PYTHONUTF8=1 python scripts/verify_freeze.py` để tránh lỗi giải mã output Git tiếng Việt.
- Thử thách mở rộng: chưa thực hiện vì ưu tiên đủ artifacts chính thức và hạn chế thêm chi phí API.
- An toàn: `.env` bị Git bỏ qua; quét artifacts không tìm thấy mẫu khóa `sk-...`; agent shell không kế thừa biến môi trường chứa API key.
