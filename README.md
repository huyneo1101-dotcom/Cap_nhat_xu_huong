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
"104 bài này ảnh hưởng gì tới Hương Diện và tới cuộc sống, tương lai của tôi", gồm 07 mục — bản đồ kho,
bốn chỗ các nguồn tự mâu thuẫn, ảnh hưởng tới cửa hàng, tới công việc, tới cuộc sống, bảng quyết định
"đúng trong cả hai kịch bản", và chỗ kho còn thiếu.

- Nội dung nằm trong `<div id="view-phantich">` của `index.html`, viết tay chứ không sinh bằng JS.
- Mọi luận điểm dẫn ngược về bài gốc bằng `<a href="#read/&lt;id&gt;">`. **Thêm liên kết mới thì id phải
  khớp một `<div class="entry" id="...">` có thật**, nếu không bấm vào sẽ rơi về trang chủ mà không báo lỗi.
- Thêm bài mới đáng kể thì soi lại mục 02 (bốn chỗ mâu thuẫn) và mục 07 (chỗ còn thiếu) trước — hai mục đó
  đổi nhanh nhất, và mục 01 có đếm số bài theo chủ đề nên cũng phải cập nhật.

## Cách thêm nội dung tuần mới

Copy khối `.week` mới trong `index.html`, đổi tiêu đề tuần, và thêm các khối `.entry` cho từng tập muốn ghi lại.
Xem "Tuần mẫu" trong file để biết đúng định dạng.

## Chạy thử trên máy

Mở trực tiếp `index.html` bằng trình duyệt, không cần server.

## Đăng lên mạng

Repo đã có sẵn `.github/workflows/deploy-pages.yml` — tự deploy khi push lên `main`. Bật tại Settings → Pages →
Source: GitHub Actions.
