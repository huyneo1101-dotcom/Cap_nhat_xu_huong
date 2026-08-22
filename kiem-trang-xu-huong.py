#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cổng kiểm trang «Cập nhật xu hướng» — soi bản tĩnh trước khi đẩy lên Pages.

    python3 kiem-trang-xu-huong.py            soi bản thật trong thư mục app
    python3 kiem-trang-xu-huong.py --ca       chạy bộ ca, in bảng ca đỏ
    python3 kiem-trang-xu-huong.py --tu-kiem  dựng từng bản hỏng, đòi đúng ca của nó đỏ

Bốn luật của app này (`CLAUDE.md`) đều hỏng theo lối KHÔNG phát ra tiếng, tức đẩy
lên rồi trang vẫn mở được, vẫn đọc được bài, chỉ sai ở chỗ phải có người mở đúng
máy đúng cảnh mới thấy:

  · màu ghi cứng giữa CSS ⇒ chế độ tối không với tới ⇒ chữ trắng trên nền trắng,
    chỉ lộ khi mở bằng máy đang để chế độ tối;
  · cặp chữ/nền tụt dưới 4,5:1 ⇒ vẫn đọc được với mắt tốt, chỉ người đọc mắt kém
    hoặc đọc ngoài nắng mới chịu trận;
  · `icon.svg` khai `purpose: maskable` ⇒ Android cắt cụt bốn góc, mà trên máy tính
    và trên máy Huy thì không thấy gì bất thường;
  · lớp chạy nền bỏ network-first ⇒ trang bày bài của tuần trước, đọc lên y hệt bản
    mới, không dấu hiệu nào cho biết đang đọc bản cũ;
  · file khai trong `VO` mà thiếu trên đĩa ⇒ `cache.addAll` trượt CẢ LÔ trong im
    lặng, tức mất luôn khả năng đọc khi không có mạng.
"""

import io
import os
import re
import sys

THU_APP = os.path.dirname(os.path.abspath(__file__))

# Cặp chữ/nền phải đạt WCAG AA. Bảng này là phần KHAI của luật «đổi màu thì đo lại,
# đừng ước lượng bằng mắt» — thêm cặp màu mới vào giao diện thì thêm dòng vào đây.
CAP_MAU = (
    ('--ink', '--bg'), ('--ink', '--card'),
    ('--muted', '--bg'), ('--muted', '--card'),
    ('--accent', '--bg'), ('--accent', '--card'),
    ('--tren-accent', '--accent'), ('--hero-chu', '--accent-dam'),
    ('--nhan-vang-chu', '--nhan-vang-nen'),
    ('--the-ok-chu', '--the-ok-nen'),
    ('--the-warn-chu', '--the-warn-nen'),
    ('--the-bad-chu', '--the-bad-nen'),
)
NGUONG_TUONG_PHAN = 4.5

MAU_TRONG_CSS = re.compile(r'#[0-9a-fA-F]{3,8}\b|\brgba?\([^)]*\)|\bhsla?\([^)]*\)')
MAU_BIEN = re.compile(r'(--[\w-]+)\s*:\s*([^;}]+)')


def _doc(duong):
    try:
        with io.open(duong, encoding='utf-8') as f:
            return f.read()
    except OSError:
        return None


def _css(html):
    """Gộp mọi khối <style> của trang, đã bỏ chú thích CSS."""
    khoi = re.findall(r'<style[^>]*>(.*?)</style>', html or '', re.S)
    return re.sub(r'/\*.*?\*/', '', '\n'.join(khoi), flags=re.S)


def _vung_root(css):
    """Vị trí đầu/cuối mọi thân khối `:root{...}`, kể cả khối nằm trong @media."""
    ra = []
    for m in re.finditer(r':root\s*\{', css):
        i, sau = m.end(), 1
        while sau and i < len(css):
            if css[i] == '{':
                sau += 1
            elif css[i] == '}':
                sau -= 1
            i += 1
        ra.append((m.start(), i))
    return ra


def _khoi_bien(css):
    """Danh sách từ điển biến của từng khối `:root`, theo đúng thứ tự xuất hiện."""
    return [dict(MAU_BIEN.findall(css[a:b])) for a, b in _vung_root(css)]


def _sang(hex_mau):
    h = (hex_mau or '').strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) < 6:
        return None
    try:
        kenh = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    except ValueError:
        return None
    quy = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in kenh]
    return 0.2126 * quy[0] + 0.7152 * quy[1] + 0.0722 * quy[2]


def tuong_phan(mau_a, mau_b):
    """Tỉ số tương phản WCAG của hai màu hex. Trả None khi một bên không đọc được."""
    a, b = _sang(mau_a), _sang(mau_b)
    if a is None or b is None:
        return None
    cao, thap = max(a, b), min(a, b)
    return (cao + 0.05) / (thap + 0.05)


def soi(thu=THU_APP):
    """Soi bản tĩnh trong `thu`. Trả danh sách câu mô tả lỗi, rỗng là sạch."""
    loi = []
    html = _doc(os.path.join(thu, 'index.html'))
    if html is None:
        return ['không đọc được index.html']
    css = _css(html)
    if not css.strip():
        loi.append('index.html không có khối <style> nào — CSS đã rời khỏi file tĩnh')

    # ── luật 1: mọi màu khai ở :root, ngoài đó cấm ghi cứng ────────────────────
    vung = _vung_root(css)
    ngoai = [m.group(0) for m in MAU_TRONG_CSS.finditer(css)
             if not any(a <= m.start() < b for a, b in vung)]
    if ngoai:
        loi.append('%d màu ghi cứng ngoài :root (%s…) — chế độ tối không với tới'
                   % (len(ngoai), ', '.join(sorted(set(ngoai))[:4])))

    # ── luật 2: khối tối chỉ ĐỔI GIÁ TRỊ, không khai biến mới ──────────────────
    khoi = _khoi_bien(css)
    if len(khoi) < 2:
        loi.append('CSS chỉ có %d khối :root — thiếu khối chế độ tối' % len(khoi))
    else:
        sang, toi = khoi[0], khoi[1]
        la = sorted(set(toi) - set(sang))
        if la:
            loi.append('khối tối khai %d biến KHÔNG có ở bản sáng (%s) — bản sáng sẽ '
                       'đọc phải biến rỗng' % (len(la), ', '.join(la[:4])))

    # ── luật 3: mọi cặp chữ/nền đã khai phải đạt WCAG AA ───────────────────────
    for ten_khoi, bien in zip(('sáng', 'tối'), khoi[:2]):
        for chu, nen in CAP_MAU:
            if chu not in bien or nen not in bien:
                loi.append('bản %s thiếu biến %s' % (ten_khoi,
                                                    chu if chu not in bien else nen))
                continue
            ti = tuong_phan(bien[chu], bien[nen])
            if ti is None:
                loi.append('bản %s: cặp %s/%s không đọc được giá trị màu'
                           % (ten_khoi, chu, nen))
            elif ti < NGUONG_TUONG_PHAN:
                loi.append('bản %s: cặp %s trên %s chỉ %.2f:1, dưới ngưỡng %.1f'
                           % (ten_khoi, chu, nen, ti, NGUONG_TUONG_PHAN))

    # ── luật 4: trang tĩnh, không dịch mã trong trình duyệt (quy tắc chung 29) ──
    if 'babel' in html.lower():
        loi.append('trang nạp Babel — cấm dịch mã trong trình duyệt')

    # ── luật 5: icon bo góc CẤM khai maskable ─────────────────────────────────
    loi += _soi_manifest(thu)

    # ── luật 6: lớp chạy nền network-first, và vỏ khai đủ file có thật ─────────
    loi += _soi_sw(thu)
    return loi


def _soi_manifest(thu):
    loi = []
    noi = _doc(os.path.join(thu, 'manifest.json'))
    if noi is None:
        return ['không đọc được manifest.json']
    import json
    try:
        man = json.loads(noi)
    except ValueError as e:
        return ['manifest.json không phải JSON hợp lệ: %s' % e]
    icon = man.get('icons') or []
    che = [i for i in icon if 'maskable' in (i.get('purpose') or '')]
    for i in che:
        if i.get('src') == 'icon.svg':
            loi.append('icon.svg khai purpose maskable — hình đã bo góc sẵn, Android '
                       'cắt cụt bốn góc mà trên máy tính không thấy gì bất thường')
    if not che:
        loi.append('manifest không khai icon maskable nào — Android tự cắt icon thường')
    for i in icon:
        src = i.get('src') or ''
        if src and not os.path.exists(os.path.join(thu, src)):
            loi.append('manifest khai icon %s nhưng file không có trên đĩa' % src)
    return loi


def _soi_sw(thu):
    loi = []
    sw = _doc(os.path.join(thu, 'sw.js'))
    if sw is None:
        return ['không đọc được sw.js']
    if "cache: 'reload'" not in sw and 'cache: "reload"' not in sw:
        loi.append('sw.js không ép tải lại khung trang — mất network-first, trang bày '
                   'bài của tuần trước mà đọc lên y hệt bản mới')
    if '.catch(' not in sw or 'caches.match' not in sw:
        loi.append('sw.js không có nhánh rơi về bản đã lưu — mất mạng là trắng trang')

    m = re.search(r"CACHE\s*=\s*'([^']+)'", sw) or re.search(r'CACHE\s*=\s*"([^"]+)"', sw)
    if not m:
        loi.append('sw.js không khai tên cache')
    else:
        ten = m.group(1)
        tien_to = re.findall(r"indexOf\('([^']+)'\)\s*===\s*0", sw)
        if tien_to and not any(ten.startswith(t) for t in tien_to):
            loi.append('tên cache «%s» không mang tiền tố dọn dẹp %s — bản cũ không bao '
                       'giờ bị xoá' % (ten, tien_to))

    m = re.search(r'VO\s*=\s*\[([^\]]*)\]', sw)
    if not m:
        loi.append('sw.js không khai danh sách file vỏ')
    else:
        for f in re.findall(r"'([^']+)'", m.group(1)):
            duong = os.path.join(thu, f[2:] if f.startswith('./') else f)
            if f not in ('./', '/') and not os.path.exists(duong):
                loi.append('sw.js khai file vỏ %s nhưng không có trên đĩa — cache.addAll '
                           'trượt CẢ LÔ trong im lặng' % f)
    return loi


# ── Bộ ca ────────────────────────────────────────────────────────────────────

DEM_CA = {'tong': 0}


def _ca(so, ten, dat):
    DEM_CA['tong'] += 1
    print('  %s ca %-3d %s' % ('✓' if dat else '✗', so, ten))
    return dat


class app_hong(object):
    """Chép app thật sang thư mục tạm rồi bẻ đúng một chỗ."""

    def __init__(self, doi):
        self.doi = doi          # {tên file: hàm nhận nội dung cũ, trả nội dung mới}

    def __enter__(self):
        import shutil
        import tempfile
        self.thu = tempfile.mkdtemp(prefix='_thu-xuhuong-')
        for ten in ('index.html', 'manifest.json', 'sw.js', 'icon.svg', 'icon-maskable.svg'):
            goc = os.path.join(THU_APP, ten)
            if os.path.exists(goc):
                shutil.copy2(goc, os.path.join(self.thu, ten))
        for ten, sua in self.doi.items():
            duong = os.path.join(self.thu, ten)
            if sua is None:
                if os.path.exists(duong):
                    os.unlink(duong)
                continue
            with io.open(duong, encoding='utf-8') as f:
                cu = f.read()
            with io.open(duong, 'w', encoding='utf-8') as f:
                f.write(sua(cu))
        return self.thu

    def __exit__(self, *a):
        import shutil
        shutil.rmtree(self.thu, ignore_errors=True)
        return False


def _co(loi, manh):
    return any(manh in x for x in loi)


def chay_ca():
    """Chạy bộ ca, trả danh sách số ca ĐỎ."""
    do = []

    # ── đối chứng: bản THẬT phải sạch. Thiếu vế này thì cổng chặn oan mà không ai biết.
    that = soi(THU_APP)
    if not _ca(1, 'ĐỐI CHỨNG: bản thật đang đẩy lên Pages phải sạch (%s)'
               % ('sạch' if not that else that[0]), not that):
        do.append(1)

    # ── luật 1: màu ghi cứng ngoài :root ──────────────────────────────────────
    with app_hong({'index.html': lambda s: s.replace(
            'background:var(--card)', 'background:#ffffff', 1)}) as t:
        if not _ca(2, 'PHẢI CHẶN: một màu ghi cứng giữa CSS (chế độ tối không với tới)',
                   _co(soi(t), 'màu ghi cứng ngoài :root')):
            do.append(2)

    # ── luật 2: khối tối khai biến lạ ─────────────────────────────────────────
    with app_hong({'index.html': lambda s: s.replace(
            '--accent:#7BA7F5;', '--accent:#7BA7F5; --vien-moi:#123456;', 1)}) as t:
        if not _ca(3, 'PHẢI CHẶN: khối tối khai biến KHÔNG có ở bản sáng',
                   _co(soi(t), 'khối tối khai')):
            do.append(3)

    # ── luật 3: tương phản ────────────────────────────────────────────────────
    with app_hong({'index.html': lambda s: s.replace(
            '--accent:#7BA7F5;', '--accent:#2563eb;', 1)}) as t:
        if not _ca(4, 'PHẢI CHẶN: bản tối lấy lại màu nhấn của bản sáng (2,6:1)',
                   _co(soi(t), 'dưới ngưỡng')):
            do.append(4)
    with app_hong({'index.html': lambda s: s.replace(
            '--muted:#5b6a82;', '--muted:#a8b4c6;', 1)}) as t:
        if not _ca(5, 'PHẢI CHẶN: màu chữ phụ bản sáng nhạt đi, tụt dưới 4,5:1',
                   _co(soi(t), 'dưới ngưỡng')):
            do.append(5)
    # Mốc đối chứng lấy #767676 chứ không lấy đen/trắng: cặp đen/trắng ra đúng 21:1 kể
    # cả khi bỏ bước quy tuyến tính, nên nó KHÔNG phân biệt được công thức đúng với công
    # thức sai. #767676 trên nền trắng là mốc WCAG công bố sẵn, đúng công thức ra 4,54:1,
    # bỏ bước quy tuyến tính ra 2,05:1 — chênh đủ xa để một ca bắt được.
    if not _ca(6, 'ĐỐI CHỨNG: phép đo khớp mốc WCAG công bố (#767676 trên trắng = 4,54)',
               abs(tuong_phan('#767676', '#ffffff') - 4.54) < 0.01
               and abs(tuong_phan('#000000', '#ffffff') - 21.0) < 0.01):
        do.append(6)

    # ── luật 5: manifest ──────────────────────────────────────────────────────
    with app_hong({'manifest.json': lambda s: s.replace(
            '"src": "icon-maskable.svg"', '"src": "icon.svg"', 1)}) as t:
        if not _ca(7, 'PHẢI CHẶN: icon.svg (đã bo góc) khai purpose maskable',
                   _co(soi(t), 'cắt cụt bốn góc')):
            do.append(7)
    with app_hong({'manifest.json': lambda s: s.replace(
            '"purpose": "maskable"', '"purpose": "any"', 1)}) as t:
        if not _ca(8, 'PHẢI CHẶN: manifest không còn icon maskable nào',
                   _co(soi(t), 'không khai icon maskable')):
            do.append(8)
    with app_hong({'icon-maskable.svg': None}) as t:
        # Đòi ĐÚNG câu của nhánh manifest: lớp chạy nền cũng khai file ấy trong vỏ và
        # cũng kêu «không có trên đĩa», nên một phép so lỏng sẽ xanh cả khi nhánh
        # manifest đã bị gỡ — ca mất răng mà bảng vẫn đẹp.
        if not _ca(9, 'PHẢI CHẶN: manifest khai icon mà file không có trên đĩa',
                   _co(soi(t), 'manifest khai icon')):
            do.append(9)

    # ── luật 6: lớp chạy nền ──────────────────────────────────────────────────
    with app_hong({'sw.js': lambda s: s.replace(
            "new Request(req.url, { cache: 'reload' })", 'req', 1)}) as t:
        if not _ca(10, 'PHẢI CHẶN: sw.js bỏ ép tải lại khung ⇒ bày bài của tuần trước',
                   _co(soi(t), 'mất network-first')):
            do.append(10)
    with app_hong({'sw.js': lambda s: s.replace(
            "var CACHE = 'xuhuong-v1';", "var CACHE = 'v2';", 1)}) as t:
        if not _ca(11, 'PHẢI CHẶN: tên cache lệch tiền tố dọn dẹp ⇒ bản cũ không bao giờ xoá',
                   _co(soi(t), 'không mang tiền tố dọn dẹp')):
            do.append(11)
    with app_hong({'sw.js': lambda s: s.replace(
            "'./icon-maskable.svg'", "'./icon-chua-co.svg'", 1)}) as t:
        if not _ca(12, 'PHẢI CHẶN: vỏ khai file không có trên đĩa ⇒ addAll trượt cả lô',
                   _co(soi(t), 'trượt CẢ LÔ')):
            do.append(12)

    # ── luật 4: dịch mã trong trình duyệt ─────────────────────────────────────
    with app_hong({'index.html': lambda s: s.replace(
            '<style', '<script src="https://unpkg.com/@babel/standalone"></script><style', 1)}) as t:
        if not _ca(13, 'PHẢI CHẶN: trang nạp Babel (quy tắc chung mục 29)',
                   _co(soi(t), 'nạp Babel')):
            do.append(13)

    # ── ĐƯỜNG GẮN: cổng dựng xong mà main() không gọi thì nằm không ───────────
    import subprocess
    with app_hong({'sw.js': lambda s: s.replace(
            "new Request(req.url, { cache: 'reload' })", 'req', 1)}) as t:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--thu-muc', t],
                           capture_output=True, text=True)
        if not _ca(14, 'ĐƯỜNG GẮN: chạy thẳng trên bản hỏng thì thoát khác 0',
                   p.returncode != 0):
            do.append(14)
    return do


def tu_kiem():
    for goc in (os.path.expanduser('~/Claude/HeThong'), '/Users/Huy/Claude/HeThong'):
        if os.path.isdir(goc):
            sys.path.insert(0, goc)
            break
    from khung_tu_kiem import vong_ban_hong

    sys.dont_write_bytecode = True
    print('— bản ĐÚNG —')
    DEM_CA['tong'] = 0
    do = chay_ca()
    print('  %d/%d ca đạt' % (DEM_CA['tong'] - len(do), DEM_CA['tong']))
    if do:
        print('✗ bản đúng đã đỏ ở ca %s — sửa mã trước khi xét bản hỏng' % do)
        return 1
    return vong_ban_hong(__file__, os.path.abspath(__file__), BAN_HONG,
                         lenh=lambda duong: [sys.executable, duong, '--ca'],
                         do_rong=78,
                         tieu_de='dựng bản kiem-trang-xu-huong.py đã gỡ dòng bảo vệ')


def main():
    if '--tu-kiem' in sys.argv:
        return tu_kiem()
    if '--ca' in sys.argv:
        return 1 if chay_ca() else 0
    thu = THU_APP
    if '--thu-muc' in sys.argv:
        thu = sys.argv[sys.argv.index('--thu-muc') + 1]
    loi = soi(thu)
    if not loi:
        print('✓ trang «Cập nhật xu hướng» sạch: %d cặp màu đạt WCAG AA ở cả hai bản, '
              'không màu ghi cứng ngoài :root, icon và lớp chạy nền đúng luật'
              % (len(CAP_MAU) * 2))
        return 0
    print('✗ %d lỗi:' % len(loi))
    for x in loi:
        print('  · %s' % x)
    return 1


# ── Bảng bản hỏng đặt CUỐI file, sau mã (quy ước bắt buộc) ───────────────────

BAN_HONG = (
    # ⚠ Neo BẮT BUỘC trải ≥02 dòng và viết bằng `\n` thoát: bảng này nằm CÙNG file với
    # mã nó nhắm tới, neo một dòng sẽ tự khớp thêm chính dòng khai ⇒ «2 chỗ khớp» và
    # bản hỏng bị từ chối, tức phép tự kiểm mất răng mà bảng trông như bộ test hỏng.

    ('bỏ phép dò màu ghi cứng ngoài :root',
     "    ngoai = [m.group(0) for m in MAU_TRONG_CSS.finditer(css)\n"
     "             if not any(a <= m.start() < b for a, b in vung)]\n    if ngoai:",
     "    ngoai = []\n"
     "    vung = vung\n    if ngoai:",
     (2,)),

    ('bỏ phép so tập biến giữa khối tối và khối sáng',
     "        la = sorted(set(toi) - set(sang))\n        if la:",
     "        la = []\n        if la:",
     (3,)),

    ('hạ ngưỡng tương phản xuống 1 — mọi cặp màu đều đạt',
     "NGUONG_TUONG_PHAN = 4.5\n\nMAU_TRONG_CSS",
     "NGUONG_TUONG_PHAN = 1.0\n\nMAU_TRONG_CSS",
     (4, 5)),

    ('không cặp màu nào được đo — bảng còn đó mà vòng lặp chạy rỗng',
     "        for chu, nen in CAP_MAU:\n            if chu not in bien or nen not in bien:",
     "        for chu, nen in ():\n            if chu not in bien or nen not in bien:",
     (4, 5)),

    ('phép tính tương phản bỏ bước quy tuyến tính (dùng thẳng giá trị kênh)',
     "    quy = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in kenh]\n"
     "    return 0.2126 * quy[0]",
     "    quy = kenh\n"
     "    return 0.2126 * quy[0]",
     (6,)),

    ('bỏ nhánh chặn icon bo góc khai maskable',
     "        if i.get('src') == 'icon.svg':\n            loi.append('icon.svg khai purpose maskable",
     "        if False:\n            loi.append('icon.svg khai purpose maskable",
     (7,)),

    ('bỏ nhánh đòi phải có ít nhất một icon maskable',
     "    if not che:\n        loi.append('manifest không khai icon maskable nào",
     "    if False:\n        loi.append('manifest không khai icon maskable nào",
     (8,)),

    ('bỏ nhánh đối chiếu icon khai trong manifest với file trên đĩa',
     "        if src and not os.path.exists(os.path.join(thu, src)):\n"
     "            loi.append('manifest khai icon",
     "        if False:\n"
     "            loi.append('manifest khai icon",
     (9,)),

    ('bỏ nhánh đòi khung trang đi network-first',
     "    if \"cache: 'reload'\" not in sw and 'cache: \"reload\"' not in sw:\n"
     "        loi.append('sw.js không ép tải lại khung trang",
     "    if False:\n"
     "        loi.append('sw.js không ép tải lại khung trang",
     (10, 14)),

    ('bỏ nhánh so tên cache với tiền tố dọn dẹp',
     "        if tien_to and not any(ten.startswith(t) for t in tien_to):\n"
     "            loi.append('tên cache",
     "        if False:\n"
     "            loi.append('tên cache",
     (11,)),

    ('bỏ nhánh đối chiếu danh sách vỏ với file trên đĩa',
     "            if f not in ('./', '/') and not os.path.exists(duong):\n"
     "                loi.append('sw.js khai file vỏ",
     "            if False:\n"
     "                loi.append('sw.js khai file vỏ",
     (12,)),

    ('bỏ nhánh chặn dịch mã trong trình duyệt',
     "    if 'babel' in html.lower():\n"
     "        loi.append('trang nạp Babel",
     "    if False:\n"
     "        loi.append('trang nạp Babel",
     (13,)),

    ('main() không gọi cổng nữa, luôn thoát 0 — cổng dựng xong mà nằm không',
     "    loi = soi(thu)\n    if not loi:",
     "    loi = []\n    if not loi:",
     (14,)),
)


if __name__ == '__main__':
    sys.exit(main())
