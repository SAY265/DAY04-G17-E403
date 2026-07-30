# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]

**Hướng:** [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở  
**Loại:** [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới  

> *Commit trước 23:59 N1 · Quality bar chốt từ thời điểm nộp.*

---

## §1. User & Job
- **Job executor + workflow** (đính kèm worksheet JTBD / ảnh sơ đồ):
- **Core JTBD** (không tên sản phẩm/AI trong câu): `When [tình huống], I want to [động lực], so I can [kết quả]`
- **Problem statement** (KHÔNG chữ AI): *[Ai - đang làm gì - vướng đâu - hậu quả gì]*
- **Evidence** (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - **Số liệu mining / kết quả khảo sát:** (n = ?, % xác nhận):
  - **≥5 quote/ví dụ nguyên văn + nguồn:**
    1. 
    2. 
    3. 
    4. 
    5. 

---

## §2. Impact & quyết định chọn
- **Bảng impact ≥3 ứng viên** (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):

| Ứng viên bài toán | Số người gặp | Tần suất | Tốn gì mỗi lần | Khả thi build | Kết luận |
|---|---|---|---|---|---|
| 1. | | | | | |
| 2. | | | | | |
| 3. | | | | | |

- **Ứng viên ĐÃ LOẠI + vì sao:**
- **Ứng viên CHỌN + vì sao (bằng số):**

---

## §3. Giải pháp tương tự đã nghiên cứu
- **[Sản phẩm 1]:** 
  - Flow:
  - Đáng học:
  - Đáng né:
  - Mình khác gì:
- **[Sản phẩm 2]:** 
  - Flow:
  - Đáng học:
  - Đáng né:
  - Mình khác gì:

---

## §4. Thiết kế
- **Lát cắt MỘT CÂU** *(1 user · 1 việc · 1 quyết định AI · 1 kết quả)*:
- **Non-goals** *(≥3 thứ KHÔNG build)*:
  1. 
  2. 
  3. 
- **Mức prototype nhắm tới:** [ ] Sketch  [ ] Mock  [ ] Working  
  - *Phần nào mock:*
  - *Phần nào thật:*
- **Automation:** [ ] augment  [ ] conditional  [ ] automate  
  - *Lý do theo cost-of-error (sai thì ai chịu gì, sửa đắt hay rẻ):*

### §4b. Nguyên tắc áp dụng (≥4 — HAX/PAIR, xem guide §2.4)

| Nguyên tắc (HAX/PAIR) | Áp cụ thể vào đâu trong prototype |
|---|---|
| 1. | |
| 2. | |
| 3. | |
| 4. | |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

| Stt | Tình huống cụ thể | Lớp chỗ khó (①/②/③/④) | Hành vi mong muốn (nói gì, hiện gì, cho user làm gì tiếp) | Nguyên tắc áp (HAX/PAIR) |
|---|---|---|---|---|
| 1 | | ① Nguồn sự thật | | |
| 2 | | ① Nguồn sự thật | | |
| 3 | | ② Mơ hồ / thiếu thông tin | | |
| 4 | | ② Mơ hồ / thiếu thông tin | | |
| 5 | | ③ Ngoài phạm vi / thẩm quyền | | |
| 6 | | ③ Ngoài phạm vi / thẩm quyền | | |
| 7 | | ④ Đặc thù domain | | |
| 8 | | ④ Đặc thù domain | | |

---

## §6. Bốn đường đi của trải nghiệm
- **Happy path:**
- **Low-confidence (②):**
- **Failure / không căn cứ (①):**
- **Correction (user sửa):**
- **Khi bị đòi ngoài phạm vi (③):**
- **Case đặc thù domain (④):**

---

## §7. Kiểm thử
- **Chiều chất lượng + định nghĩa kiểm chứng được:**
  - *Chiều 1:*
  - *Chiều 2:*
  - *Chiều 3:*
- **Golden set** *(≥20 case theo cơ cấu trong guide §2.6, file trong `eval/golden-set.json`)*:
- **Quality bar** *(chốt từ 23:59, giữ nguyên sau đó)*: `"Đạt khi ≥ ___% qua bộ, và ___"`
- **Kết quả các lượt chạy** *(bảng % — cập nhật đến trước CP6)*:

| Lượt chạy | Ngày/Giờ | Số case Pass/Tổng | Tỷ lệ Pass (%) | So với Quality Bar | Ghi chú / Failure chính |
|---|---|---|---|---|---|
| Lượt 1 | | / 20 | % | | |
| Lượt 2 | | / 20 | % | | |

---

## §8. Phân công & kế hoạch
- **Phân công có tên:**
  - `spec`: 
  - `evidence`: 
  - `prompt`: 
  - `code`: 
  - `demo`: 
- **Willing users (≥3 tên) + kế hoạch vòng validation CP5:**
  - *Willing users:* 1. ____ · 2. ____ · 3. ____
  - *Kế hoạch CP5:* 3 câu hỏi (Khó hiểu/khó chịu gì? Có tin không vì sao? Có dùng thật không vì sao?) · Người log: ____
- **Multi-prototype (nếu làm):** Trục khác biệt của ≥2 phương án + lý do chọn.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| | | |
