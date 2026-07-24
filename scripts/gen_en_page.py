"""
Generic KO -> EN tool-page transformer for BrowserKit international rollout.
Usage: called from another script that supplies `slug` and a `translations` dict
of exact Korean substrings -> English replacements (applied after the structural
transform below). Structural transform handles: html lang, font links, ad slot
placeholders, canonical/hreflang, header/footer nav hrefs, lang switcher, lang banner.
"""
import re
import sys

# Windows console may be cp949; make WARN prints never crash the batch.
try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass


def transform(ko_html: str, slug: str) -> str:
    c = ko_html

    # html lang
    c = c.replace('<html lang="ko">', '<html lang="en">', 1)

    # remove kakao script line
    c = re.sub(r'\s*<script type="text/javascript" src="//t1\.kakaocdn\.net/kas/static/ba\.min\.js" async></script>\n?', '\n', c)

    # style.css -> add style-en.css right after
    c = c.replace(
        '<link rel="stylesheet" href="/css/style.css?v=20260724a" />',
        '<link rel="stylesheet" href="/css/style.css?v=20260724a" />\n  <link rel="stylesheet" href="/css/style-en.css?v=20260724a" />',
        1
    )

    # AdSense comment header (top of head) simplify
    c = c.replace(
        '<!-- Google AdSense 승인 대기 중 (2026-07-19 주석 처리, 카카오 애드핏으로 임시 전환) — 승인 후 주석 해제',
        '<!-- Google AdSense — pending re-review. Uncomment once approved.'
    )

    # Gowun Dodum font link -> Poppins + Inter
    c = c.replace(
        '<link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">',
        '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
    # strip Gowun Dodum font-family refs (fall through to inherited Poppins/Inter override)
    c = c.replace(",'Gowun Dodum',sans-serif", '')
    c = c.replace(", 'Gowun Dodum', sans-serif", '')
    c = c.replace("font-family:'Gowun Dodum',sans-serif; ", '')
    c = c.replace("font-family: 'Gowun Dodum', sans-serif; ", '')
    c = c.replace("font:700 18px Gowun Dodum,sans-serif", "font:700 18px Poppins,sans-serif")
    c = c.replace("font:700 16px Gowun Dodum,sans-serif", "font:700 16px Poppins,sans-serif")
    c = c.replace("Gowun Dodum,sans-serif", "Poppins,sans-serif")

    # canonical + hreflang: KO canonical -> becomes EN canonical, ko alt keeps ko url
    ko_canon_pat = re.compile(r'<link rel="canonical" href="https://browserkit\.online/' + re.escape(slug) + r'/" />')
    m = ko_canon_pat.search(c)
    if m:
        ko_url = f'https://browserkit.online/{slug}/'
        en_url = f'https://browserkit.online/en/{slug}/'
        c = ko_canon_pat.sub(f'<link rel="canonical" href="{en_url}" />', c, count=1)
    else:
        ko_url = f'https://browserkit.online/{slug}/'
        en_url = f'https://browserkit.online/en/{slug}/'

    # og:url
    c = c.replace(f'<meta property="og:url" content="{ko_url}" />', f'<meta property="og:url" content="{en_url}" />')

    # inLanguage / priceCurrency in JSON-LD
    c = c.replace('"inLanguage": "ko"', '"inLanguage": "en"')
    c = c.replace('"priceCurrency": "KRW"', '"priceCurrency": "USD"')
    c = c.replace('"priceCurrency":"KRW"', '"priceCurrency":"USD"')

    # WebApplication url field + BreadcrumbList item urls (ko -> en)
    c = c.replace(f'"url": "{ko_url}"', f'"url": "{en_url}"')
    c = c.replace(f'"item": "{ko_url}"', f'"item": "{en_url}"')
    c = c.replace('"item": "https://browserkit.online/"', '"item": "https://browserkit.online/en/"')
    c = c.replace('"name": "홈"', '"name": "Home"')

    # lang banner (top of body): KO page banner offers EN; EN page banner offers KO, and condition flips
    c = c.replace(
        '<span>🌐 This page is also available in <a href="/en/">English</a>.</span>',
        f'<span>🌐 이 페이지는 <a href="/{slug}/">한국어</a>로도 볼 수 있습니다.</span>'
    )
    c = c.replace(
        "if (lang.indexOf('ko') === 0) return;",
        "if (lang.indexOf('ko') !== 0) return;"
    )

    # header brand + back link -> /en/
    c = c.replace('<a href="/" class="header-brand">', '<a href="/en/" class="header-brand">')
    c = c.replace('<a href="/" class="header-back">&#x2190; BrowserKit 홈으로</a>', '<a href="/en/" class="header-back">&#x2190; Back to BrowserKit</a>')
    c = c.replace('<a href="/" class="header-back">&#x2190; <span class="header-back-label">BrowserKit 홈으로</span></a>', '<a href="/en/" class="header-back">&#x2190; <span class="header-back-label">Back to BrowserKit</span></a>')
    c = c.replace('<a href="/" class="header-back">← BrowserKit 홈으로</a>', '<a href="/en/" class="header-back">← Back to BrowserKit</a>')
    c = c.replace('<a href="/" class="header-back">← <span class="header-back-label">BrowserKit 홈으로</span></a>', '<a href="/en/" class="header-back">← <span class="header-back-label">Back to BrowserKit</span></a>')

    # lang switcher: EN active, link to ko slug
    c = c.replace(
        '<button class="lang-switcher-btn" type="button" data-lang-btn>🌐 <span class="lang-label-full">한국어</span></button>',
        '<button class="lang-switcher-btn" type="button" data-lang-btn>🌐 <span class="lang-label-full">English</span></button>'
    )
    c = c.replace(
        '<a href="/en/">English</a>\n            <a href="#" class="active">한국어</a>',
        f'<a href="#" class="active">English</a>\n            <a href="/{slug}/">한국어</a>'
    )

    # ── Known exact ad-block markups (site-wide constants) -> placeholders ──
    AD_TOP_MARGIN0 = ('<div style="margin:0 0 12px"><!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div></div>')
    AD_TOP_NOMARGIN = AD_TOP_MARGIN0.replace('margin:0 0 12px', 'margin:0 0 12px')  # alias, same string
    # NOTE: the coupang-swap comment's date varies per file (whatever date the swap
    # was made on) — matched with a \d{4}-\d{2}-\d{2} wildcard instead of a fixed date.
    AD_COUPANG_SWAP_PREFIX = '<!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><!-- 카카오 애드핏 ('
    AD_COUPANG_SWAP_SUFFIX = ', 쿠팡 파트너스 다이내믹 배너로 교체) — 복원 시 주석 해제: <div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div> --><div class="adfit-h-desktop"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"728","height":"90","tsource":""});</script></div><div class="adfit-h-mobile"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"320","height":"50","tsource":""});</script></div></div>'
    # some KO sources wrap the whole swap block in an extra <div style="margin:0 0 12px">...</div>
    # that isn't part of the constant above — consume it too (both sides optional/independent)
    # so no unclosed wrapper div is left behind in the output.
    AD_COUPANG_SWAP_RE = re.compile(
        r'(?:<div style="margin:0 0 12px">)?'
        + re.escape(AD_COUPANG_SWAP_PREFIX)
        + r'\d{4}-\d{2}-\d{2}'
        + re.escape(AD_COUPANG_SWAP_SUFFIX)
        + r'(?:</div>)?'
    )
    AD_BOTTOM_RECT_12 = ('<div style="margin:12px 0"><!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-format="autorelaxed" data-ad-client="ca-pub-2077977787979506" data-ad-slot="9500090221"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><div class="adfit-rect-wrap"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-oePL4TCj742xAwqT" data-ad-width="300" data-ad-height="250"></ins></div></div>')
    AD_BOTTOM_RECT_00 = AD_BOTTOM_RECT_12.replace('margin:12px 0', 'margin:0 0 12px')

    def h_placeholder(slot_id):
        return (f'<!-- Google AdSense Display Ad — pending approval, reserving space -->\n'
                f'    <div class="ad-slot" id="{slot_id}">\n'
                f'      <!-- <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="TBD" data-ad-format="horizontal" data-full-width-responsive="true"></ins>\n'
                f'      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script> -->\n'
                f'    </div>')

    bottom_placeholder = (
        '<!-- Google AdSense Multiplex Ad — pending approval, reserving space -->\n'
        '    <div class="ad-slot ad-slot-rect" id="adBottom">\n'
        '      <!-- <ins class="adsbygoogle" style="display:block" data-ad-format="autorelaxed" data-ad-client="ca-pub-2077977787979506" data-ad-slot="TBD"></ins>\n'
        '      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script> -->\n'
        '    </div>'
    )

    # replace first occurrence of the plain top ad (hero) as adTop, keep replacing
    # any further plain occurrences as adExtraN; replace coupang-swap block as adMiddle
    count = [0]

    def top_sub(_m):
        count[0] += 1
        return h_placeholder('adTop' if count[0] == 1 else f'adExtra{count[0]}')
    c = re.sub(re.escape(AD_TOP_MARGIN0), top_sub, c)
    c = AD_COUPANG_SWAP_RE.sub(lambda _m: h_placeholder('adMiddle'), c)
    c = re.sub(re.escape(AD_BOTTOM_RECT_12), lambda _m: bottom_placeholder, c)
    c = re.sub(re.escape(AD_BOTTOM_RECT_00), lambda _m: bottom_placeholder, c)

    # safety net: catch any remaining kakao_ad_area / coupang markup not matched above
    if 'kakao_ad_area' in c or 'PartnersCoupang' in c:
        print(f'  [WARN] {slug}: leftover kakao/coupang markup not auto-converted — needs manual fix')

    # add ad-slot CSS (append into first <style> block, right before its closing tag, simplest: add a global rule after guide-full-link:hover)
    c = c.replace(
        '.guide-full-link:hover { text-decoration:underline; }',
        '.guide-full-link:hover { text-decoration:underline; }\n\n    .ad-slot { min-height:90px; display:flex; align-items:center; justify-content:center; margin:0 0 12px; }\n    .ad-slot-rect { min-height:250px; }',
        1
    )

    # footer nav -> /en/ pages
    c = c.replace(
        '<a href="/privacy">개인정보 처리방침</a>\n        <a href="/terms">이용약관</a>\n        <a href="/about">서비스 소개</a>\n        <a href="/blog/">블로그</a>',
        '<a href="/en/privacy.html">Privacy Policy</a>\n        <a href="/en/terms.html">Terms of Service</a>\n        <a href="/en/about.html">About</a>\n        <a href="/en/blog/">Blog</a>'
    )
    c = c.replace(
        '&#xa9; 2026 BrowserKit. 모든 처리는 브라우저 내에서 이루어집니다.',
        '&#xa9; 2026 BrowserKit. All processing happens in your browser.'
    )
    c = c.replace(
        '© 2026 BrowserKit. 모든 처리는 브라우저 내에서 이루어집니다.',
        '&#xa9; 2026 BrowserKit. All processing happens in your browser.'
    )

    return c
