/* 오프라인 실행용 서비스워커: 처음 한 번 받아 두면 인터넷 없이도 열립니다.
   파일을 고치면 CACHE 이름의 숫자를 올리세요. (build_www.py가 파일 목록을 자동으로 채웁니다) */
const CACHE = 'flat-sun-path-v2';
const FILES = [
  "./",
  "index.html",
  "privacy.html",
  "manifest.webmanifest",
  "fonts/fonts.css",
  "fonts/noto-sans-kr-100-wght-normal.woff2",
  "fonts/noto-sans-kr-101-wght-normal.woff2",
  "fonts/noto-sans-kr-102-wght-normal.woff2",
  "fonts/noto-sans-kr-103-wght-normal.woff2",
  "fonts/noto-sans-kr-104-wght-normal.woff2",
  "fonts/noto-sans-kr-105-wght-normal.woff2",
  "fonts/noto-sans-kr-106-wght-normal.woff2",
  "fonts/noto-sans-kr-107-wght-normal.woff2",
  "fonts/noto-sans-kr-108-wght-normal.woff2",
  "fonts/noto-sans-kr-109-wght-normal.woff2",
  "fonts/noto-sans-kr-110-wght-normal.woff2",
  "fonts/noto-sans-kr-111-wght-normal.woff2",
  "fonts/noto-sans-kr-112-wght-normal.woff2",
  "fonts/noto-sans-kr-113-wght-normal.woff2",
  "fonts/noto-sans-kr-114-wght-normal.woff2",
  "fonts/noto-sans-kr-115-wght-normal.woff2",
  "fonts/noto-sans-kr-116-wght-normal.woff2",
  "fonts/noto-sans-kr-117-wght-normal.woff2",
  "fonts/noto-sans-kr-118-wght-normal.woff2",
  "fonts/noto-sans-kr-119-wght-normal.woff2",
  "fonts/noto-sans-kr-15-wght-normal.woff2",
  "fonts/noto-sans-kr-41-wght-normal.woff2",
  "fonts/noto-sans-kr-43-wght-normal.woff2",
  "fonts/noto-sans-kr-98-wght-normal.woff2",
  "fonts/noto-sans-kr-99-wght-normal.woff2",
  "fonts/noto-sans-kr-latin-wght-normal.woff2",
  "icons/apple-touch-icon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png"
];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
