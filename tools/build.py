#!/usr/bin/env python3
"""홈페이지(index.html, en/index.html), sitemap.xml, robots.txt, favicon.svg 생성기.
새 시뮬레이터를 추가하려면 아래 SIMS 목록에 항목 하나를 넣고 `python3 tools/build.py` 를 실행한다.
(저장소 루트에서 실행. 배포되는 결과물은 모두 정적 파일이다.)"""
import html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://woonykorea-ctrl.github.io/woony-s-world/"
YEAR = "2026"
PLAY_URL = ""   # 구글 플레이 앱 출시 후 스토어 주소를 여기에 넣으면 '곧 출시'가 링크로 바뀐다.

# ---- 시뮬레이터 목록 (여기에 추가) -------------------------------------------
# status: "live" | "soon".  thumb: 아래 THUMBS의 키.  href는 루트 기준 파일명.
SIMS = [
    dict(id="globe", href="globe-sun-path.html", status="live", thumb="globe", tag=dict(ko="태양·지구", en="Sun · Earth"),
         title=dict(ko="지구본 3D 태양 시뮬레이터", en="Globe 3D Sun Simulator"),
         desc=dict(ko="태양빛은 고정, 지구본은 지축 23.44°로 자전합니다. 도시를 고르고 날짜를 움직이며 낮의 길이와 태양 고도, 계절 변화를 확인하세요.",
                   en="The sunlight stays fixed while the globe spins on its 23.44° axis. Pick a city, scrub through the year, and watch day length, sun elevation and the seasons change."),
         play=False),
    dict(id="flat", href="flat-sun-path.html", status="live", thumb="flat", tag=dict(ko="태양·지구", en="Sun · Earth"),
         title=dict(ko="평면 모델 태양 경로 3D 시뮬레이터", en="Flat Map Model: Sun Path 3D"),
         desc=dict(ko="평면 지구 지도 모델에서 태양이 그리는 경로를 3D로 봅니다. 도시를 고르면 그 위치를 기준으로 하루의 태양 움직임이 나타납니다.",
                   en="See the sun's path on a flat-map model of the Earth in 3D. Choose a city and follow the sun's movement over the day from that location."),
         play=True),
    dict(id="orbit", href="orbit-sun-earth.html", status="live", thumb="orbit", tag=dict(ko="궤도", en="Orbits"),
         title=dict(ko="지구 공전 궤도 시뮬레이터", en="Earth Orbit Simulator"),
         desc=dict(ko="날짜 슬라이더로 태양 둘레를 도는 지구와 기울어진 지축을 따라가며 계절이 생기는 이유를 확인합니다. 달의 궤적도 켜 볼 수 있습니다.",
                   en="Follow Earth around the Sun with a date slider and see how its tilted axis causes the seasons. You can also switch on the Moon's path."),
         play=False),
    dict(id="compare", href="compare-flat-vs-globe.html", status="live", thumb="compare", tag=dict(ko="비교", en="Compare"),
         title=dict(ko="평면 모델 vs 지구본 나란히 비교", en="Flat Model vs Globe, Side by Side"),
         desc=dict(ko="같은 도시, 같은 날짜, 같은 시각에서 두 모델이 계산한 태양 고도와 낮·밤을 한 지도 위에 겹쳐 비교합니다.",
                   en="Overlay the sun elevation and day/night that the two models calculate for the same city, date and time on one map."),
         play=False),
]

# 질문별 짧은 설명: links는 SIMS의 id 목록
QA = [
    dict(q=dict(ko="왜 낮과 밤이 생길까요?", en="Why do we have day and night?"),
         a=dict(ko="지구가 하루에 한 바퀴 자전하면서, 태양빛을 받는 쪽과 받지 못하는 쪽이 번갈아 바뀌기 때문입니다. 지구본 시뮬레이터를 재생하면 도시가 밝은 면과 어두운 면을 오가는 모습을 볼 수 있습니다.",
                en="Because the Earth turns once a day, each place moves in and out of the sunlit side. Play the globe simulator and watch a city travel from the bright side to the dark side."),
         links=["globe"]),
    dict(q=dict(ko="계절은 왜 바뀔까요?", en="Why do the seasons change?"),
         a=dict(ko="지축이 약 23.44° 기울어 있어서, 일 년 동안 태양빛이 가장 직접 닿는 위도가 남북으로 오갑니다. 날짜 슬라이더를 춘분·하지·추분·동지로 옮겨 보세요.",
                en="The Earth's axis is tilted by about 23.44°, so the latitude where sunlight arrives most directly shifts north and south through the year. Move the date slider to the equinoxes and solstices."),
         links=["orbit", "globe"]),
    dict(q=dict(ko="같은 날인데 도시마다 해의 높이가 다른 이유는?", en="Why does the sun's height differ from city to city on the same day?"),
         a=dict(ko="도시마다 위도와 경도가 달라서 같은 순간에도 현지 시각과 태양을 보는 각도가 다릅니다. 도시를 바꿔 가며 태양 고도와 낮의 길이를 비교해 보세요.",
                en="Each city has a different latitude and longitude, so the local time and the angle to the sun differ at the same moment. Switch cities and compare sun elevation and day length."),
         links=["globe", "flat", "compare"]),
    dict(q=dict(ko="백야와 극야는 어떻게 생길까요?", en="How do midnight sun and polar night happen?"),
         a=dict(ko="지축이 기울어 있어서 여름의 극지방은 하루 종일 해가 떠 있고, 겨울에는 해가 뜨지 않습니다. 지구본을 ‘북극 위에서’ 시점으로 놓고 날짜를 움직여 보세요.",
                en="Because of the axial tilt, the polar regions see the sun all day in summer and not at all in winter. Set the globe to the view from above the North Pole and move the date."),
         links=["globe"]),
    dict(q=dict(ko="평면 모델에서 태양은 어떻게 움직이나요?", en="How does the sun move in a flat-map model?"),
         a=dict(ko="평면 지구 지도 모델에서 태양이 하루 동안 그리는 경로를 3D로 보여 줍니다. 도시를 골라 그 위치에서 해가 어떻게 지나가는지 확인할 수 있습니다.",
                en="This simulator shows the path the sun traces over a day in a flat-map model, in 3D. Pick a city to see how the sun passes from that location."),
         links=["flat"]),
    dict(q=dict(ko="두 모델은 무엇이 다르게 보일까요?", en="How do the two models differ?"),
         a=dict(ko="같은 도시와 날짜를 두고 두 시뮬레이터를 번갈아 열어 보면 태양의 움직임이 어떻게 다른지 직접 비교할 수 있습니다. 한 지도 위에 겹쳐 보는 비교 페이지도 있습니다.",
                en="Open both simulators with the same city and date to compare how the sun moves in each. A comparison page overlays both on one map."),
         links=["globe", "flat", "compare"]),
    dict(q=dict(ko="여름에는 지구가 태양에 더 가까울까요?", en="Is Earth closer to the Sun in summer?"),
         a=dict(ko="아닙니다. 지구는 1월 초에 태양과 가장 가깝고 7월 초에 가장 멉니다. 계절은 거리가 아니라 지축의 기울기 때문에 생깁니다. 공전 시뮬레이터에서 날짜를 움직이며 태양까지 거리를 확인해 보세요.",
                en="No. Earth is closest to the Sun in early January and farthest in early July. The seasons come from the tilt of the axis, not from distance. Move the date in the orbit simulator and watch the distance."),
         links=["orbit"]),
    dict(q=dict(ko="달은 태양 둘레를 어떻게 움직일까요?", en="How does the Moon move around the Sun?"),
         a=dict(ko="달은 지구 둘레를 약 27.3일에 한 바퀴 돌면서 지구와 함께 태양 둘레를 돕니다. 태양 쪽에서 보면 달의 길은 고리를 만들지 않고 완만하게 휘어 있습니다. 시뮬레이터에서 달 궤적을 켜 볼 수 있습니다. 달 거리는 과장해서 그렸습니다.",
                en="The Moon circles Earth in about 27.3 days while travelling with Earth around the Sun. Seen from the Sun, its path never loops and only curves gently. Switch on the Moon path in the simulator. The Moon's distance is exaggerated."),
         links=["orbit"]),
]

T = dict(
    ko=dict(
        site="우니의 과학 시뮬레이터",
        page_title="우니의 과학 시뮬레이터 — 3D 태양·지구 시뮬레이션 모음",
        page_desc="지구본 3D 태양 시뮬레이터와 평면 모델 태양 경로 시뮬레이터를 브라우저에서 바로 실행하세요. 낮과 밤, 계절, 도시별 태양 고도를 직접 확인할 수 있습니다.",
        eyebrow="설치 없이 · 가입 없이 · 무료",
        h1='해는 어떻게 <em>움직일까?</em>',
        lead="브라우저에서 바로 돌려 보는 3D 시뮬레이터 모음입니다. 도시를 고르고, 날짜를 움직이고, 시점을 바꿔 가며 직접 확인해 보세요.",
        cta="시뮬레이터 보기", cta2="자주 묻는 질문",
        sims_h="시뮬레이터", sims_sub="카드를 누르면 각 시뮬레이터가 열립니다.",
        open="열기 →", soon="준비 중", play_soon="Google Play · 곧 출시", play="Google Play",
        qa_h="이런 질문에 답해요", qa_sub="질문마다 알맞은 시뮬레이터로 바로 이동할 수 있습니다.",
        go="열기", about="우니가 직접 만든 과학 시뮬레이터 모음입니다. 새 시뮬레이터가 계속 추가됩니다.",
        privacy="개인정보처리방침", lang_name="한국어", other="English", rights="© %s Woony." % YEAR,
        aria_lang="언어 선택", home_label="우니의 과학 시뮬레이터 홈",
    ),
    en=dict(
        site="Woony's Science Simulators",
        page_title="Woony's Science Simulators — 3D Sun & Earth Simulations",
        page_desc="Run a 3D globe sun simulator and a flat-map sun path simulator right in your browser. Explore day and night, the seasons and sun elevation in different cities.",
        eyebrow="No install · No sign-up · Free",
        h1='How does the sun <em>move?</em>',
        lead="A collection of 3D simulators that run right in your browser. Pick a city, move through the year, and change your viewpoint to see for yourself.",
        cta="Browse simulators", cta2="Common questions",
        sims_h="Simulators", sims_sub="Tap a card to open the simulator.",
        open="Open →", soon="Coming soon", play_soon="Google Play · coming soon", play="Google Play",
        qa_h="Questions we answer", qa_sub="Each question links to the simulator that shows it best.",
        go="Open", about="A growing collection of science simulators made by Woony.",
        privacy="Privacy Policy", lang_name="English", other="한국어", rights="© %s Woony." % YEAR,
        aria_lang="Language", home_label="Woony's Science Simulators home",
    ),
)

THUMBS = dict(
    globe='''<svg viewBox="0 0 240 148" role="img" aria-hidden="true"><defs>
<radialGradient id="gl" cx="72%" cy="40%" r="75%"><stop offset="0" stop-color="#7fb8ff"/><stop offset=".45" stop-color="#2a5fa8"/><stop offset="1" stop-color="#0a1830"/></radialGradient>
<radialGradient id="gs" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd23d"/><stop offset="1" stop-color="#ffa24a" stop-opacity="0"/></radialGradient></defs>
<circle cx="214" cy="30" r="26" fill="url(#gs)" opacity=".9"/><circle cx="214" cy="30" r="9" fill="#ffd23d"/>
<g stroke="#ffd23d" stroke-opacity=".35" stroke-width="1.2"><path d="M188 42 L150 62"/><path d="M190 30 L148 36"/><path d="M196 54 L158 84"/></g>
<circle cx="110" cy="76" r="54" fill="url(#gl)"/>
<path d="M110 76 m0 -54 a54 54 0 0 0 0 108 a30 54 0 0 1 0 -108z" fill="#000" opacity=".5"/>
<ellipse cx="110" cy="76" rx="54" ry="14" fill="none" stroke="#fff" stroke-opacity=".18"/>
<line x1="96" y1="14" x2="124" y2="138" stroke="#8fdcff" stroke-width="1.6" stroke-dasharray="4 3"/>
<circle cx="134" cy="66" r="3.4" fill="#ffa24a"/><circle cx="134" cy="66" r="7" fill="none" stroke="#ffa24a" stroke-opacity=".6"/></svg>''',
    flat='''<svg viewBox="0 0 240 148" role="img" aria-hidden="true"><defs>
<linearGradient id="fd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f5d3a"/><stop offset="1" stop-color="#143222"/></linearGradient></defs>
<ellipse cx="120" cy="104" rx="98" ry="30" fill="url(#fd)" stroke="#3b4a66"/>
<ellipse cx="120" cy="104" rx="64" ry="19" fill="none" stroke="#fff" stroke-opacity=".14"/>
<ellipse cx="120" cy="104" rx="30" ry="9" fill="none" stroke="#fff" stroke-opacity=".14"/>
<path d="M30 92 C 60 8, 180 8, 210 92" fill="none" stroke="#ffd23d" stroke-width="2" stroke-dasharray="5 4"/>
<circle cx="150" cy="22" r="14" fill="#ffa24a" opacity=".25"/><circle cx="150" cy="22" r="8" fill="#ffd23d"/>
<circle cx="150" cy="104" r="3.2" fill="#8fdcff"/><line x1="150" y1="30" x2="150" y2="101" stroke="#ffd23d" stroke-opacity=".3" stroke-dasharray="2 3"/></svg>''',
    orbit='''<svg viewBox="0 0 240 148" role="img" aria-hidden="true"><defs>
<radialGradient id="os" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd23d"/><stop offset=".55" stop-color="#ffa24a"/><stop offset="1" stop-color="#ffa24a" stop-opacity="0"/></radialGradient></defs>
<circle cx="120" cy="74" r="32" fill="url(#os)" opacity=".85"/><circle cx="120" cy="74" r="10" fill="#ffd23d"/>
<circle cx="120" cy="74" r="62" fill="none" stroke="#f0be3c" stroke-opacity=".6" stroke-width="1.6"/>
<line x1="120" y1="74" x2="170" y2="110" stroke="#ffd23d" stroke-opacity=".3" stroke-dasharray="3 3"/>
<circle cx="170" cy="110" r="6.5" fill="#2f7bd0"/><path d="M170 103.5 a6.5 6.5 0 0 0 0 13 a3.6 6.5 0 0 1 0 -13z" fill="#0a1a33" opacity=".8"/>
<line x1="170" y1="110" x2="170" y2="94" stroke="#fff" stroke-opacity=".6" stroke-dasharray="2 2"/>
<circle cx="182" cy="116" r="2.4" fill="#e6e6e0"/></svg>''',
    compare='''<svg viewBox="0 0 240 148" role="img" aria-hidden="true">
<ellipse cx="62" cy="86" rx="46" ry="14" fill="#143222" stroke="#3b4a66" stroke-dasharray="4 3"/>
<path d="M22 80 C 34 28, 90 28, 102 80" fill="none" stroke="#ffd23d" stroke-width="1.6" stroke-dasharray="4 3"/>
<circle cx="180" cy="74" r="40" fill="#1d4a86" stroke="#3b4a66" stroke-dasharray="4 3"/>
<path d="M180 34 a40 40 0 0 0 0 80 a22 40 0 0 1 0 -80z" fill="#000" opacity=".45"/>
<text x="120" y="80" fill="#8b93a7" font-size="16" text-anchor="middle" font-family="sans-serif">vs</text></svg>''',
)

LOGO = '<svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="#0b0e17" stroke="#262c3b"/><circle cx="20" cy="12" r="5.5" fill="#ffd23d"/><path d="M5 22 a13 13 0 0 0 22 4 a16 16 0 0 1 -22 -4z" fill="#8fdcff" opacity=".85"/></svg>'

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0b0e17"/><circle cx="20" cy="12" r="6" fill="#ffd23d"/><path d="M5 23 a13 13 0 0 0 22 3 a16 16 0 0 1 -22 -3z" fill="#8fdcff"/></svg>
'''

e = html.escape


def sim_by_id(i):
    return next(s for s in SIMS if s["id"] == i)


def build(lang):
    t = T[lang]
    pre = "../" if lang == "en" else ""          # 루트 파일을 가리키는 접두어
    self_url = BASE + ("en/" if lang == "en" else "")
    ko_url, en_url = BASE, BASE + "en/"
    og_img = BASE + "assets/og-card.png"

    cards = []
    for s in SIMS:
        thumb = '<div class="thumb">%s</div>' % THUMBS[s["thumb"]]
        tag = '<span class="tag">%s</span>' % e(s["tag"][lang])
        h3 = '<h3>%s</h3>' % e(s["title"][lang])
        p = '<p>%s</p>' % e(s["desc"][lang])
        if s["status"] == "live":
            actions = ['<a class="open" href="%s%s">%s</a>' % (pre, s["href"], t["open"])]
            if s["play"]:
                if PLAY_URL:
                    actions.append('<a class="chip" href="%s" rel="noopener">%s</a>' % (e(PLAY_URL), t["play"]))
                else:
                    actions.append('<span class="chip off" data-play-slot>%s</span>' % t["play_soon"])
            cards.append('<article class="card">%s<div class="body">%s%s%s<div class="actions">%s</div></div></article>' % (thumb, tag, h3, p, "".join(actions)))
        else:
            cards.append('<article class="card soon" aria-disabled="true">%s<div class="body"><span class="badge">%s</span>%s%s</div></article>' % (thumb, t["soon"], h3, p))

    qas = []
    for qa in QA:
        links = "".join('<a href="%s%s">%s → %s</a>' % (pre, sim_by_id(i)["href"], t["go"], e(sim_by_id(i)["title"][lang])) for i in qa["links"])
        qas.append('<article><h3>%s</h3><p>%s</p><div class="go">%s</div></article>' % (e(qa["q"][lang]), e(qa["a"][lang]), links))

    ld = ('{"@context":"https://schema.org","@type":"WebSite","name":"%s","url":"%s","inLanguage":"%s"}'
          % (t["site"].replace("'", "’"), self_url, lang))

    play_foot = ('<a href="%s" rel="noopener">%s</a>' % (e(PLAY_URL), t["play"])) if PLAY_URL else '<span class="off">%s</span>' % t["play_soon"]

    lang_nav = ('<nav class="lang" aria-label="%s">'
                '<a href="%s" lang="ko" hreflang="ko" data-set-lang="ko"%s>한국어</a>'
                '<a href="%s" lang="en" hreflang="en" data-set-lang="en"%s>English</a></nav>') % (
        t["aria_lang"],
        "./" if lang == "ko" else "../", ' aria-current="true"' if lang == "ko" else "",
        "en/" if lang == "ko" else "./", ' aria-current="true"' if lang == "en" else "")

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["page_title"])}</title>
<meta name="description" content="{e(t["page_desc"])}">
<link rel="canonical" href="{self_url}">
<link rel="alternate" hreflang="ko" href="{ko_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{ko_url}">
<meta name="theme-color" content="#05060a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(t["site"])}">
<meta property="og:title" content="{e(t["page_title"])}">
<meta property="og:description" content="{e(t["page_desc"])}">
<meta property="og:url" content="{self_url}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{"ko_KR" if lang == "ko" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{pre}assets/site.css">
<script src="{pre}assets/site.js"></script>
<script type="application/ld+json">{ld}</script>
<!-- [애드센스 자리 1/2] 승인 후 여기에 애드센스 <script async ...> 한 줄을 넣는다. 지금은 비워 둔다. -->
</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="brand" href="./" aria-label="{e(t["home_label"])}">{LOGO}<span>{e(t["site"])}</span></a>
    {lang_nav}
  </header>

  <main>
    <section class="hero">
      <p class="eyebrow">{e(t["eyebrow"])}</p>
      <h1>{t["h1"]}</h1>
      <p class="lead">{e(t["lead"])}</p>
      <a class="btn" href="#sims">{e(t["cta"])}</a>
      <a class="btn ghost" href="#qa">{e(t["cta2"])}</a>
    </section>

    <!-- [애드센스 자리 2/2] 승인 후 광고 코드를 넣고 class="on" 을 붙이면 나타난다. 지금은 화면에 나오지 않는다. -->
    <div data-ad-slot="home-top" aria-hidden="true"></div>

    <section class="block" id="sims">
      <h2>{e(t["sims_h"])}</h2>
      <p class="sub">{e(t["sims_sub"])}</p>
      <div class="grid">
        {"".join(cards)}
      </div>
    </section>

    <section class="block" id="qa">
      <h2>{e(t["qa_h"])}</h2>
      <p class="sub">{e(t["qa_sub"])}</p>
      <div class="qa">
        {"".join(qas)}
      </div>
    </section>

    <p class="about">{e(t["about"])}</p>
  </main>

  <footer class="foot">
    <nav>
      <a href="{pre}privacy.html">{e(t["privacy"])}</a>
      {play_foot}
    </nav>
    <span>{t["rights"]}</span>
  </footer>
</div>
</body>
</html>
'''


def main():
    (ROOT / "index.html").write_text(build("ko"), encoding="utf-8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(build("en"), encoding="utf-8")
    (ROOT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    urls = [BASE, BASE + "en/"] + [BASE + s["href"] for s in SIMS if s["status"] == "live"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % "".join(
        "  <url><loc>%s</loc></url>\n" % u for u in urls)
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % BASE, encoding="utf-8")
    print("built:", ", ".join(urls))


if __name__ == "__main__":
    main()
