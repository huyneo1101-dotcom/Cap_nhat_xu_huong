# Cập nhật xu hướng

Trang tĩnh cá nhân (`index.html`, tự chứa, không cần build) — nhật ký hàng tuần tóm tắt các cuộc phỏng vấn
chuyên gia đáng chú ý về kinh doanh, công nghệ và tương lai công việc, lấy từ nhiều podcast (Diary of a CEO,
Lex Fridman...).

## Nguyên tắc nội dung

- Mỗi mục là **tóm tắt/diễn giải**, không sao chép nguyên văn nội dung có bản quyền.
- Luôn kèm nguồn để tra lại bản gốc.
- Trang dùng cá nhân, không phải sản phẩm public.
- **Mỗi bài tóm tắt khách mời/tập giữ độ dài khoảng 1000 từ**, theo cấu trúc 4 phần: bối cảnh khách mời, nội dung
  chính của tập, giải thích thêm thuật ngữ cho người mới, và vì sao đáng nghe/liên hệ. Xem các bài trong "Tuần 1"
  làm mẫu.

## Mục "Phân tích" (tab thứ ba ở trang chủ)

Ngoài hai tab duyệt bài (theo chủ đề / theo podcast) còn tab **🧭 Phân tích**: bài tổng hợp trả lời câu hỏi
"104 bài này chạm vào cửa hàng Hương Diện ở chỗ nào", gồm 06 mục — bản đồ kho, bốn chỗ các nguồn tự mâu
thuẫn, ảnh hưởng tới cửa hàng (11 tiểu mục, gồm 3.6 số ngành Mẹ & Bé Việt Nam và 3.7 so giá 04 chuỗi),
đưa AI vào cửa hàng, bảng quyết định "đúng trong cả hai kịch bản", và chỗ kho còn thiếu.

⛔ **Bài chỉ bàn cửa hàng** (Huy chốt 15/8/2026). Bản trước có mục "ảnh hưởng tới công việc và tương lai
của tôi" cùng mục "ảnh hưởng tới cuộc sống" — đã bỏ, cùng với mọi câu mô tả Huy đang quản lý hàng chục
ứng dụng hay viết phân tích quân sự. Thêm nội dung mới thì giữ đúng phạm vi này.

⚠ **Số ngoài kho phải mang mốc đo ngay cạnh** và có nguồn trên đĩa: nghiên cứu ngành và so giá ở
`App/HuongDienWork/nghien-cuu-thi-truong-va-so-gia-08-08.md`, số bán hàng ở `App/HuongDien/NEN-KINH-DOANH.md`
(chỉ lấy sổ tổng HDTONG, cộng cả ba sổ là thổi doanh thu ~1,8 lần).

- Nội dung nằm trong `<div id="view-phantich">` của `index.html`, viết tay chứ không sinh bằng JS.
- Mọi luận điểm dẫn ngược về bài gốc bằng `<a href="#read/&lt;id&gt;">`. **Thêm liên kết mới thì id phải
  khớp một `<div class="entry" id="...">` có thật**, nếu không bấm vào sẽ rơi về trang chủ mà không báo lỗi.
- Thêm bài mới đáng kể thì soi lại mục 02 (bốn chỗ mâu thuẫn) và mục 06 (chỗ còn thiếu) trước — hai mục đó
  đổi nhanh nhất, và mục 01 có đếm số bài theo chủ đề nên cũng phải cập nhật.

## Cách thêm nội dung tuần mới

Copy khối `.week` mới trong `index.html`, đổi tiêu đề tuần, và thêm các khối `.entry` cho từng tập muốn ghi lại.
Xem "Tuần mẫu" trong file để biết đúng định dạng.

## Chạy thử trên máy

Mở trực tiếp `index.html` bằng trình duyệt, không cần server.

## Đăng lên mạng

Repo đã có sẵn `.github/workflows/deploy-pages.yml` — tự deploy khi push lên `main`. Bật tại Settings → Pages →
Source: GitHub Actions.
