/* 홈페이지 언어 처리: 첫 방문 시 기기 언어로 ko/en 페이지를 자동 선택하고,
   수동으로 고른 언어는 기억한다. (?lang=ko|en 으로 강제 지정 가능)
   검색 로봇은 리다이렉트하지 않는다. */
(function () {
  var K = 'fe.hub.lang';
  function get() { try { return localStorage.getItem(K); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(K, v); } catch (e) {} }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-set-lang]');
    if (a) set(a.getAttribute('data-set-lang'));
  });

  var page = (document.documentElement.lang || 'ko').slice(0, 2);
  var q = /[?&]lang=(ko|en)\b/.exec(location.search);
  var want = q ? q[1] : get();
  if (q) set(q[1]);
  if (!want) {
    if (/bot|crawl|spider|slurp|lighthouse|facebookexternalhit|kakaotalk/i.test(navigator.userAgent)) return;
    var nl = (navigator.languages && navigator.languages[0]) || navigator.language || 'ko';
    want = /^ko/i.test(nl) ? 'ko' : 'en';
  }
  if (want !== page) location.replace(page === 'ko' ? 'en/' : '../');
})();
