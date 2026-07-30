# Codebase Prototype — Nhóm [XX]

## 📌 Tổng quan Prototype

- **Mức Prototype khai báo:** [ ] Sketch  [ ] Mock  [ ] Working
- **Quyết định trung tâm của AI:** *(Mô tả ngắn quyết định do AI thực hiện)*
- **Thư viện / Model AI sử dụng:** *(Ví dụ: Gemini 1.5 Flash API, OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet...)*
- **Mã nguồn phát triển:** Dự án sử dụng hoặc tích hợp mã nguồn tại thư mục `starter_v0/` hoặc các module custom.

---

## 🔍 Phân định phần Mock vs phần AI thật

| Thành phần / Màn hình | Loại (Mock / AI thật) | Mô tả chi tiết |
|---|---|---|
| Màn hình nhập liệu / UI | Mock / Streamlit | Dựng giao diện tương tác người dùng |
| Xử lý quyết định trung tâm | **AI THẬT** | Gọi API thực tế để suy luận / trả lời |
| Dữ liệu bổ trợ / CSDL | Mock | Sử dụng dữ liệu giả lập hoặc mẫu trích đoạn |

---

## 🛠 Hướng dẫn Chạy Prototype

1. **Chuẩn bị môi trường (Python / Streamlit):**
   ```bash
   cd starter_v0
   pip install -r requirements.txt
   ```

2. **Cấu hình biến môi trường:**
   - Tạo file `.env` từ `.env.example` trong `starter_v0/` (Lưu ý: **KHÔNG** commit API Key lên Github).
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Khởi chạy ứng dụng Streamlit UI:**
   ```bash
   streamlit run app.py
   ```

---

## ⚠️ Quy định An toàn Data & Key
- API Key phải được truyền qua biến môi trường.
- Dữ liệu sử dụng thử nghiệm chỉ nằm trong data pack được cấp hoặc data giả tự sinh.
