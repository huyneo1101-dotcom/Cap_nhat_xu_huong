# Cập nhật xu hướng

Trang tĩnh cá nhân (`index.html`, tự chứa, không cần build) — nhật ký hàng tuần tóm tắt các cuộc phỏng vấn
chuyên gia đáng chú ý về kinh doanh, công nghệ và tương lai công việc, lấy từ nhiều podcast (Diary of a CEO,
Lex Fridman...).

## Nguyên tắc nội dung

- Mỗi mục là **tóm tắt/diễn giải**, không sao chép nguyên văn nội dung có bản quyền.
- Luôn kèm nguồn để tra lại bản gốc.
- Trang dùng cá nhân, không phải sản phẩm public.
- **Danh sách nguồn quét** nằm ở khối `.week#goi-y` trong `index.html`, và mỗi kênh phải có tên trong `CHAN_ORDER`
  + `CHAN_DESC` (cuối file) thì tab "🎙️ Theo podcast" mới gom bài đúng chỗ. Kênh chưa có bài vẫn hiện ra với nhãn
  "chưa có bài". Từ 17/8/2026 danh sách có 19 nguồn — 18 podcast cộng **The Rundown AI**.
- **The Rundown AI là nguồn chữ, có quy tắc riêng**: phỏng vấn lớn thường có bản chữ đăng thẳng trên `therundown.ai`
  (ví dụ tập Demis Hassabis 27/5/2026) — có bản chữ thì trích bản chữ. Tập nào chưa có bản chữ thì tóm tắt từ
  podcast *Rowan's Notes* trên Spotify (`open.spotify.com/show/2zQpIc96gbruTylpzo9dVY`) và **ghi rõ trong phần
  Nguồn là tóm tắt từ bản nghe**. Đặt `src-tag` là `The Rundown AI` (hoặc `Rowan's Notes`, `baseChan` tự gộp về một
  kênh).
- ⛔ **ĐỘ DÀI THEO LOẠI NỘI DUNG, đừng áp một khuôn cho tất cả** (Huy chốt 17/8/2026: *"tin tức thì cần quái gì
  viết 1000 từ"*). **Tin tức** — bản tin hằng ngày kiểu The Rundown AI — viết dạng **điểm tin**: một câu dẫn, gạch
  đầu dòng cho từng tin kèm số liệu, một dòng liên hệ cửa hàng, tổng khoảng **150-250 từ**. Khuôn ~1000 từ bốn phần
  chỉ dành cho **bài phân tích và phỏng vấn dài** (podcast, bài chuyên đề), nơi có luận điểm để mổ.
- **Mỗi bài tóm tắt khách mời/tập giữ độ dài khoảng 1000 từ**, theo cấu trúc 4 phần: bối cảnh khách mời, nội dung
  chính của tập, giải thích thêm thuật ngữ cho người mới, và vì sao đáng nghe/liên hệ. Xem các bài trong "Tuần 1"
  làm mẫu.

## Mục "Phân tích" (tab thứ ba ở trang chủ)

Ngoài hai tab duyệt bài (theo chủ đề / theo podcast) còn tab **🧭 Phân tích**: bài tổng hợp trả lời câu hỏi
"104 bài podcast cộng 05 số bản tin The Rundown AI này chạm vào cửa hàng Hương Diện ở chỗ nào", gồm 06 mục —
bản đồ kho, bốn chỗ các nguồn tự mâu thuẫn, ảnh hưởng tới cửa hàng (15 tiểu mục, gồm 3.6 số ngành Mẹ & Bé
Việt Nam, 3.7 so giá 04 chuỗi, 3.12 hành vi người mua ở châu Á, Việt Nam, Hà Nội, 3.13 hệ quả mức sinh giảm
với ngành bán lẻ ở Nhật, Hàn, Trung, 3.14 đọc kỹ nhà bán lẻ Kidswant, và 3.15 công cụ tấn công rẻ đi nhanh
hơn công cụ phòng thủ), đưa AI vào cửa hàng (04 chỗ sẽ gãy), bảng quyết định "đúng trong cả hai kịch bản",
và chỗ kho còn thiếu.

⚠ **Bản tin hằng ngày vào mục Phân tích theo đúng một cách** (bản 20/8/2026, khi gộp 05 số Tuần 4): dùng làm
**số kiểm lại** luận điểm podcast đã nêu, **không** làm nguồn cho luận điểm mới — vì tin tức mang số đo chứ
không dựng lập luận. Và cả lớp tin ấy đứng trên đúng một nguồn, chưa có nguồn độc lập kiểm lại, nên mục 06 (v)
khai thẳng chỗ đó; dùng làm *chiều* để hành động sớm ở việc rẻ, đừng dùng làm *mức* để tính toán.

⛔ **Bài chỉ bàn cửa hàng** (Huy chốt 15/8/2026). Bản trước có mục "ảnh hưởng tới công việc và tương lai
của tôi" cùng mục "ảnh hưởng tới cuộc sống" — đã bỏ, cùng với mọi câu mô tả Huy đang quản lý hàng chục
ứng dụng hay viết phân tích quân sự. Thêm nội dung mới thì giữ đúng phạm vi này.

⛔ **REPO NÀY PUBLIC VÀ TRANG CHẠY TRÊN GITHUB PAGES CÔNG KHAI** — ai có đường dẫn đều đọc được,
kể cả mã nguồn. Vì thế **cấm đưa vào đây**: giá bán từng mã, mức chênh với từng chuỗi, giá vốn và
biên, doanh thu theo con số tuyệt đối. Tỷ lệ phần trăm và luận điểm thì được. Vấp thật 15/8/2026:
bảng giá 32 cặp đã bị đẩy lên bản công khai rồi phải gỡ ngay trong lượt, dù file nguồn ghi rõ
*"bản này KHÔNG lên app"*. Nội dung mang số tiền đi bản riêng, gửi qua Google Docs riêng tư.

⚠ **Số ngoài kho phải mang mốc đo ngay cạnh** và có nguồn trên đĩa: nghiên cứu ngành và so giá ở
`App/HuongDienWork/nghien-cuu-thi-truong-va-so-gia-08-08.md`, hành vi người mua ở
`App/HuongDienWork/nghien-cuu-hanh-vi-nguoi-mua-15-08.md` (nguồn của mục 3.12), nhân khẩu học và nhà
bán lẻ châu Á ở `App/HuongDienWork/nghien-cuu-nhan-khau-va-nha-ban-le-15-08.md` (nguồn của mục 3.13,
3.14 và của ba nguồn độc lập thêm vào mục 3.11 (ii)), số bán hàng ở
`App/HuongDien/NEN-KINH-DOANH.md` (chỉ lấy sổ tổng HDTONG, cộng cả ba sổ là thổi doanh thu ~1,8 lần).

⚠ **Hai chỗ số nguồn ngoài tự lệch nhau, đã khai thẳng trong bài, đừng lặng lẽ chọn một bên**: số đếm
cửa hàng mẹ và bé Trung Quốc năm 2024 (129.000 theo nguồn này, 180.000 theo nguồn kia — dùng chiều,
đừng dùng mức, mục 3.13 (ii)); và số điểm bán Con Cưng (~700 điểm năm 2023 theo báo chí, 1.146 điểm
theo phép đếm trên trang tra cứu ngày 12/8/2026 — không xếp thành chuỗi thời gian, cuối mục 3.13).

⚠ **Ba con số quy mô ngành không thể cùng đúng** (33,8 nghìn tỷ cho 04 sàn 2026 · ~7 tỷ USD toàn thị
trường · tỷ trọng bán qua mạng 45-50%). Chưa phân định được số nào sai — mục 3.12 khai thẳng chỗ này,
đừng dùng cả ba trong cùng một luận điểm.

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
