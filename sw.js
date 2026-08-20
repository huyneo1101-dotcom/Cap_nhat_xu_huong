/* Lớp chạy nền cho «Cập nhật xu hướng» — đọc được kho bài khi không có mạng.
 *
 * Trang là một file tĩnh duy nhất, không gọi mạng lúc chạy, nên lớp này chỉ giữ
 * đúng bốn file. Khung trang đi NETWORK-FIRST: kho bài dày lên mỗi tuần và một
 * bản cache cũ đọc lên y hệt bản mới, không dấu hiệu nào cho biết đang đọc bản
 * của tuần trước.
 */
var CACHE = 'xuhuong-v1';
var VO = ['./', './index.html', './manifest.json', './icon.svg', './icon-maskable.svg'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE)
      .then(function (c) { return c.addAll(VO); })
      .catch(function () {})
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (ks) {
      return Promise.all(ks.filter(function (k) {
        return k.indexOf('xuhuong-') === 0 && k !== CACHE;
      }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url;
  try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== location.origin) return;

  var laKhung = req.mode === 'navigate' ||
    url.pathname === '/' || url.pathname.slice(-1) === '/' ||
    url.pathname.slice(-5) === '.html';
  e.respondWith(
    fetch(laKhung ? new Request(req.url, { cache: 'reload' }) : req).then(function (r) {
      if (r && r.ok) {
        var ban = r.clone();
        caches.open(CACHE).then(function (c) {
          c.put(laKhung ? './index.html' : req, ban);
        }).catch(function () {});
      }
      return r;
    }).catch(function () {
      return caches.match(laKhung ? './index.html' : req).then(function (hit) {
        return hit || caches.match('./');
      });
    })
  );
});
