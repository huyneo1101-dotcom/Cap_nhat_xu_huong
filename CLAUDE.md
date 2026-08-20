# Cập nhật xu hướng — luật kỹ thuật của mảng này

Luật về **NỘI DUNG** (nguồn quét, độ dài từng loại bài, phạm vi mục Phân tích) nằm ở
`README.md`, đừng chép sang đây. File này chỉ giữ phần giao diện và phát hành.

- **Trên mạng:** <https://huyneo1101-dotcom.github.io/Cap_nhat_xu_huong>
- **Kho:** `huyneo1101-dotcom/Cap_nhat_xu_huong`, thư mục trên máy `~/Claude/App/Trendy`
- **Đẩy:** push lên `main` là `.github/workflows/deploy-pages.yml` tự dựng và phát hành
  **cả thư mục**. Không có danh sách file phát hành, nên thêm file tĩnh mới không cần
  khai ở đâu cả — khác hẳn mấy app đẩy bằng `wrangler`.

## 1. Trang là MỘT file tĩnh, không build, không gọi mạng lúc chạy

`index.html` tự chứa: bài viết, CSS, JS đều nằm trong đó. `grep -c 'fetch('` ra **0**.

⚠ Vì thế mốc **"có báo đang tải và báo lỗi"** của Bảng app **không áp được** cho app này
— không có gì để chờ thì không có gì để báo. Đừng nhét một dòng «Đang tải…» chết vào
trang chỉ để mốc ấy chuyển xanh: cổng nào phải mở cờ mới qua được là cổng chết
(`~/.claude/CLAUDE.md` mục 17).

## 2. ⛔ MỌI MÀU KHAI Ở `:root`, KHỐI TỐI CHỈ ĐỔI GIÁ TRỊ

Chế độ tối cắm 21/08/2026, đi theo `prefers-color-scheme` của máy. Trước đó CSS có **22
chỗ ghi cứng màu** ngoài `:root` (`#fff` trên nút, gradient `#1e3a8a → #2563eb` ở đầu
trang, ba cặp màu thẻ trạng thái, sáu bóng đổ); tất cả đã kéo thành token.

Một màu ghi cứng giữa CSS là một chỗ chế độ tối **không với tới**, và nó hỏng theo kiểu
chữ trắng trên nền trắng chứ không kiểu trang không mở được — tức phải có người mở trang
lên bằng máy đang để chế độ tối mới thấy. Thêm thành phần mới thì khai màu ở `:root`
trước, dùng `var(--…)` sau.

**Bảng màu tối đã đo, không phải chọn theo cảm giác.** Mọi cặp chữ/nền đều ≥ 4,5:1 theo
WCAG, chỗ thấp nhất là 6,02:1 — nhỉnh hơn bản sáng ở mọi ô (bản sáng có hai ô 4,48 và
4,51:1). Riêng màu nhấn phải đổi từ `#2563eb` sang `#7BA7F5`: giữ nguyên thì trên nền tối
chỉ còn 2,6:1. Đổi màu thì đo lại, đừng ước lượng bằng mắt.

## 3. ⛔ `icon.svg` LÀ HÌNH BO GÓC — CẤM KHAI `purpose: maskable` CHO NÓ

Manifest bản cũ khai `icon.svg` ba lần, lần thứ ba mang `purpose: maskable`. Android cắt
icon maskable theo hình mặt nạ của máy, nên một hình đã bo góc sẵn bị **cắt cụt bốn góc**
— mà trên máy Huy hay trên trình duyệt máy tính thì không thấy gì bất thường. Nay có
`icon-maskable.svg` riêng: nền tràn hết khung, hình thu về 68% ở giữa.

## 4. Lớp chạy nền: khung trang NETWORK-FIRST

`sw.js`, cache `xuhuong-v1`. Kho bài dày lên mỗi tuần và **một bản cache cũ đọc lên y hệt
bản mới** — không dấu hiệu nào cho biết đang đọc bài của tuần trước. Vì thế khung trang
luôn hỏi mạng trước, chỉ rơi về bản đã lưu khi mất mạng. Đổi cách lưu thì bump tên cache.
