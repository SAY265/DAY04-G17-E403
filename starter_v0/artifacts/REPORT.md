# Day 04 Lab v2 Report — Research Agent

## Team
- **Team**: Research Agent Team G17
- **Provider/model**: OpenRouter (`openai/gpt-4o-mini`)

### 👥 Phân công Vai trò & Nhiệm vụ Thành viên (Role Division):

| Thành viên | Vai trò | Nhiệm vụ chính |
|---|---|---|
| **Giáp Quốc Anh** | **Lead & Agent System Architecture** | Tối ưu hóa `system_prompt.md`, quản lý vòng lặp phiên bản `v0-v3`, phát triển ứng dụng Web Streamlit UI (`app.py`), cấu hình `tools.yaml`. |
| **Chu Tuấn Việt** | **Custom Tool Developer** | Thiết kế và phát triển Custom Tool `calculator` (`TOOL.md`, `calculator.py`, `tool.py`), đăng ký tool vào hệ thống và viết test script độc lập. |
| **Hà Xuân Sơn** | **Eval & Benchmark Specialist** | Thiết kế bộ đề kiểm thử nhóm 10 cases (`data/eval_group.json`), thực thi `run_eval.py`, thu thập metrics và phân tích lỗi (Failure Analysis). |
| **Vũ Quốc Anh** | **Safety & Guardrail Specialist** | Thiết lập ranh giới xác nhận an toàn (Confirmation Boundary cho `send`), kiểm thử ranh giới `clarify` và soạn thảo tài liệu báo cáo `REPORT.md`. |

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent là trợ lý trí tuệ nhân tạo chuyên sâu về tra cứu, tìm kiếm tin tức trên Web và mạng xã hội X (Twitter), đọc nội dung bài viết từ URL, tính toán biểu thức toán học và xin ý kiến xác nhận từ người dùng trước khi thực hiện các hành động nhạy cảm.

**Link dùng thử:**
- **Public URL (Trực tiếp 100% không cần mật khẩu)**: `https://13af26d5c77764f4-14-238-145-226.serveousercontent.com`
- **Local URL**: `http://localhost:8501` (Giao diện Streamlit tương tác trực quan)

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận yes/no trước hành động nhạy cảm | Không |
| `timeline` | Lấy danh sách các bài đăng mới nhất từ tài khoản X/Twitter theo screenname | Không |
| `social_search` | Tìm kiếm bài đăng trên mạng xã hội X/Twitter theo từ khóa | Không |
| `lookup` | Tra cứu thông tin, bài báo, tin tức trên Internet qua API Tavily | Không |
| `fetch` | Tải và đọc nội dung văn bản Markdown từ một địa chỉ URL | Không |
| `format` | Trình bày và tổng hợp dữ liệu thô thành bản tin/digest hoàn chỉnh | Không |
| `send` | Gửi bản tin hoặc thông báo lên kênh Telegram bên ngoài | Không |
| `policy` | Tra cứu tài liệu chính sách và quy định nội bộ công ty | Không |
| `papers` | Tìm kiếm bài báo khoa học trên thư viện arXiv | Không |
| `paper_text` | Trích xuất nội dung văn bản chi tiết của bài báo arXiv | Không |
| `calculator` | Thực hiện tính toán an toàn các biểu thức toán học (cộng, trừ, nhân, chia, lũy thừa, sqrt, sin/cos) | **Có (Custom Tool)** |

## A3. Câu hỏi mẫu để thử

1. **Tìm kiếm tin tức AI mới nhất**: `"Tin tức AI hôm nay có gì nổi bật?"`
2. **Hỏi thông tin bị thiếu (Missing Info)**: `"Tóm tắt 5 tweet mới nhất giúp mình"` *(Agent sẽ hỏi lại tên tài khoản)*
3. **Ranh giới an toàn (Safety Boundary)**: `"Đăng bản tin này lên Telegram giúp mình"` *(Agent sẽ xin xác nhận yes/no trước)*
4. **Tính toán biểu thức toán học (Custom Tool)**: `"Tính giúp mình 25 * 4 + sqrt(144)"`
5. **Đọc và tóm tắt bài viết từ URL**: `"Tóm tắt bài này giúp mình: https://openai.com/index/gpt-5"`

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| 1. Hỏi bài đăng Twitter khi chưa đưa handle | `v0`: Đoán mò `sama` ➔ Gọi `timeline`<br>`v3`: Gọi `clarify` hỏi lại username | ở `v0`, Agent tự ý đoán mò tài khoản Sam Altman. Lên `v3`, Agent biết dừng lại gọi `clarify` hỏi lại rõ ràng. | `runs/v3_B_base_openrouter_20260729T151228578170.json` |
| 2. Yêu cầu đăng tin lên Telegram | `v0`: Gọi `send` gửi ngay<br>`v3`: Gọi `clarify` (yes_no) xin phép | `v0` tự ý phát tán thông tin. `v3` bắt buộc xin ý kiến xác nhận của người dùng trước khi gọi `send`. | `runs/v3_B_base_openrouter_20260729T151228578170.json` |
| 3. Tính toán biểu thức phức tạp | `v0`: Không có tool tính<br>`v3`: Gọi `calculator` trả kết quả `192.0` | `v3` bổ sung Custom Tool `calculator` cho phép Agent giải quyết chính xác các phép toán biểu thức. | `scripts/quicktest_calculator.py` |
| 4. Xử lý câu hỏi ngoài phạm vi (Bài toán tích phân) | `v0`: Gọi `send` gửi đáp án linh tinh<br>`v3`: `no_tool` (Trả lời trực tiếp) | ở `v0`, Agent bị ngáo tool. `v3` nhận biết câu hỏi không cần tra cứu và trả lời trực tiếp mà không gọi tool. | `runs/v3_B_base_openrouter_20260729T151228578170.json` |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases = 0`, `measured_cases = total_cases`, và kiểm tra `tool_results` không có lỗi không mong muốn.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run File |
|---|---|---|---|---:|---:|---|
| `v0` | Baseline gốc | Đo hành vi chưa tối ưu trước khi sửa | `case_accuracy` | | 0.70 | `runs/v0_B_base_openrouter_20260729T145326469802.json` |
| `v1` | Sửa `system_prompt.md` | Bổ sung quy tắc hỏi lại khi thiếu thông tin và xin xác nhận trước khi gửi | `case_accuracy` | 0.70 | 0.70 | `runs/v1_B_base_openrouter_20260729T151035966426.json` |
| `v2` | Sửa `system_prompt.md` | Khắc phục tác dụng phụ của v1 bằng name-to-handle mapping và ranh giới URL chuẩn | `case_accuracy` | 0.70 | **1.00** | `runs/v2_B_base_openrouter_20260729T151228578170.json` |
| `v3` | Tinh chỉnh `tools.yaml` | Tối ưu hóa mô tả tiếng Việt trong schema `tools.yaml` để tăng độ ổn định | `case_accuracy` | 1.00 | **1.00** | `runs/v3_B_base_openrouter_20260729T151630322111.json` |

## B2. Failure analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R10_missing_handle` | `missing_info` | `timeline(screenname="sama")` | Agent đoán mò tài khoản Sam Altman thay vì hỏi người dùng. | Thêm quy tắc trong `system_prompt.md` yêu cầu gọi `clarify` khi thiếu handle. |
| `R11_missing_url` | `missing_info` | `fetch(url="https://example.com/article")` | Agent bịa ra URL ảo khi thiếu địa chỉ trang web. | Bổ sung hướng dẫn gọi `clarify` khi URL bị thiếu hoàn toàn. |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text="Bản tin này")` | Agent tự ý gọi `send` lên Telegram khi chưa được người dùng xác nhận. | Đưa ra ranh giới bắt buộc gọi `clarify` với `response_type="yes_no"` trước khi `send`. |
| `R08_out_of_scope` | `out_of_scope` | `send(text="Đáp án...")` | Agent tự ý gọi tool `send` cho câu hỏi bài tập tích phân thuần túy. | Quy định rõ các câu hỏi toán học/code không cần gọi tool (`no_tool`). |
| `R01_user_tweets_routing` (ở v1) | `wrong_tool` | `clarify(...)` | Ở v1, prompt quá khắt khe khiến Agent hỏi lại cả tên người nổi tiếng (`Sam Altman`). | Bổ sung quy tắc Name-to-Handle mapping (`Sam Altman` ➔ `sama`) ở v2. |

## B3. Team eval cases

Danh sách 10 test cases tự soạn thảo trong `data/eval_group.json` (Đạt tỷ lệ **10/10 PASS = 100%** ở `v3`):

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_single_calculator_routing` | Định tuyến đúng sang Custom Tool `calculator` | `calculator(expression="25 * 4 + sqrt(144)")` | **PASS** |
| `G02_single_missing_url` | Hỏi người dùng khi thiếu URL trong câu lệnh | `clarify(response_type="text")` | **PASS** |
| `G03_single_telegram_boundary` | Hỏi xác nhận `yes_no` trước khi gửi Telegram | `clarify(response_type="yes_no")` | **PASS** |
| `G04_single_out_of_scope` | Yêu cầu viết mã Python Fibonacci | `no_tool: true` | **PASS** |
| `G05_single_lookup_news_args` | Bóc tách đúng query, topic='news' và timeframe='day' | `lookup(query="công nghệ", topic="news", timeframe="day")` | **PASS** |
| `G06_multi_clarify_then_tweets` | Hỏi username ở lượt 1, gọi `timeline` ở lượt 2 | `timeline(screenname="elonmusk")` | **PASS** |
| `G07_multi_switch_to_fetch` | Người dùng đổi ý chuyển sang đọc URL cụ thể | `fetch(url="https://openai.com/index/gpt-5")` | **PASS** |
| `G08_multi_cancel_request` | Người dùng hủy yêu cầu ở lượt 2 | `no_tool: true` | **PASS** |
| `G09_multi_carryover_and_timeframe` | Giữ nguyên chủ đề và cập nhật timeframe sang `day` | `lookup(query="NVIDIA", topic="news", timeframe="day")` | **PASS** |
| `G10_multi_clarify_then_fetch` | Hỏi URL ở lượt 1, nhận URL và gọi `fetch` ở lượt 2 | `fetch(url="https://deepmind.google")` | **PASS** |

## B4. Live chat evidence

- **Local Web App**: `http://localhost:8501` (Giao diện Streamlit)
- **Tool Execution Trace**: Hiển thị minh bạch từng Round, tên Tool, tham số JSON, trạng thái `✅ SUCCESS` / `⏸️ WAITING FOR USER` / `❌ ERROR`.

## B5. Tool capability evidence

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| **Must-have Custom Tool** | `tools/calculator/calculator.py` | Tính toán chính xác các biểu thức toán học (`sqrt`, `sin/cos`, lũy thừa) | Sử dụng `eval` an toàn với môi trường `__builtins__: None` và whitelist các hàm toán học. |
| **Core Search Tools** | `tools/lookup/tool.py` & `tools/fetch/tool.py` | Tra cứu tin tức qua Tavily API và cào nội dung trang web dạng Markdown qua Firecrawl API | Bắt buộc kiểm tra API Key trước khi gọi; xử lý `HTTPError` mượt mà. |
| **Social Media Tools** | `tools/timeline/tool.py` | Lấy bài đăng mới nhất từ tài khoản X/Twitter qua RapidAPI | Giới hạn số lượng bài đăng `limit` để tránh quá tải ngữ cảnh. |
| **Safety Boundary Tool** | `tools/clarify/tool.py` | Xin ý kiến xác nhận người dùng trước các hành động gửi tin Telegram (`send`) | Bắt buộc quy định `response_type="yes_no"` để ngăn chặn tự ý gửi tin nhắn ngoài ý muốn. |

## B6. Reflection

- **Những sửa đổi thuộc về `system_prompt.md`**: 
  - Quy tắc ranh giới an toàn (Confirmation Boundary cho `send`).
  - Hướng dẫn hỏi lại khi thiếu URL/username (`clarify`).
  - Quy tắc Name-to-Handle Mapping (`Sam Altman` ➔ `sama`).
  - Quy tắc xử lý câu hỏi ngoài phạm vi không dùng tool (`no_tool`).
- **Những sửa đổi thuộc về `tools.yaml`**:
  - Mô tả tiếng Việt chi tiết, rõ ràng cho từng tool giúp LLM hiểu đúng chức năng và chọn đúng tham số (`parameters`).
- **Bài học rút ra**:
  - Tối ưu hóa Agent là một quy trình lặp dựa trên bằng chứng (Evidence-Driven Iteration). Việc sửa một lỗi có thể tạo ra tác dụng phụ (Side-effect) ở case khác (như ở `v1`), nên cần kiểm thử toàn bộ test suite sau mỗi lần thay đổi để điều chỉnh Prompt chính xác ở `v2` và `v3`.
