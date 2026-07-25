"""
Generic KO -> EN blog-post transformer for BrowserKit international rollout.
Analogous to gen_en_page.py (reuses the same head-boilerplate / ad-slot / footer /
lang-switcher / lang-banner logic) but adapted for blog post structure:

  - BlogPosting JSON-LD (headline/description/dateModified/mainEntityOfPage/image)
  - separate FAQPage JSON-LD
  - BreadcrumbList JSON-LD where item 3 is the post title, not "Home"
  - <figure> screenshot blocks are stripped entirely (KO screenshots have Korean
    UI baked into the images -- per 해외사업기획서.md §11, EN posts omit them
    rather than showing a broken/confusing image)
  - post-date reformatted from Korean date style ("2026년 7월 22일") to English
    ("July 22, 2026")
  - post-nav prev/next: caller supplies the already-decided href/label REPL pairs
    (this script does not auto-resolve cross-links; batches happen out of order
    so a target post may not exist yet -- see caller-side policy)

Usage: called from a per-post build script that supplies `slug` (tool slug, for
CTA href target), `blog_filename` (e.g. "95-unitpricecalc-howto", no .html) and
a `translations` list of (old, new) exact-substring tuples applied after the
structural transform below.
"""
import re
import sys

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

KO_MONTHS_RE = re.compile(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일')
EN_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']


def _reformat_date(m):
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return f'{EN_MONTHS[mo-1]} {d}, {y}'


def strip_figures(c: str) -> str:
    """Remove <figure ...>...</figure> screenshot blocks entirely (non-greedy, DOTALL)."""
    return re.sub(r'<figure\b.*?</figure>', '', c, flags=re.S)


def transform(ko_html: str, slug: str, blog_filename: str) -> str:
    c = ko_html
    ko_url = f'https://browserkit.online/blog/{blog_filename}'
    en_url = f'https://browserkit.online/en/blog/{blog_filename}'

    # ── screenshots: strip entirely (per 해외사업기획서.md §11) ──
    c = strip_figures(c)

    # ── html lang / kakao script / css / adsense-comment / fonts (same as tool pages) ──
    c = c.replace('<html lang="ko">', '<html lang="en">', 1)
    c = re.sub(r'\s*<script type="text/javascript" src="//t1\.kakaocdn\.net/kas/static/ba\.min\.js" async></script>\n?', '\n', c)
    c = c.replace(
        '<!-- Google AdSense 승인 대기 중 (2026-07-19 주석 처리, 카카오 애드핏으로 임시 전환) — 승인 후 주석 해제',
        '<!-- Google AdSense — pending re-review. Uncomment once approved.'
    )
    c = c.replace(
        '<link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">',
        '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
    c = c.replace(",'Gowun Dodum',sans-serif", '')
    c = c.replace(", 'Gowun Dodum', sans-serif", '')
    c = c.replace("font-family:'Gowun Dodum',sans-serif; ", '')
    c = c.replace("font-family: 'Gowun Dodum', sans-serif; ", '')
    c = c.replace("font:700 18px Gowun Dodum,sans-serif", "font:700 18px Poppins,sans-serif")
    c = c.replace("font:700 16px Gowun Dodum,sans-serif", "font:700 16px Poppins,sans-serif")
    c = c.replace("Gowun Dodum,sans-serif", "Poppins,sans-serif")
    # style.css sibling (handles either version-string suffix already on disk)
    c = re.sub(
        r'(<link rel="stylesheet" href="/css/style\.css\?v=[0-9a-z]+" />)(?!\s*\n\s*<link rel="stylesheet" href="/css/style-en\.css)',
        r'\1\n  <link rel="stylesheet" href="/css/style-en.css?v=20260724a" />',
        c, count=1
    )

    # ── canonical (blog posts have no hreflang alternates) ──
    c = c.replace(f'<link rel="canonical" href="{ko_url}" />', f'<link rel="canonical" href="{en_url}" />')

    # ── BlogPosting / BreadcrumbList / FAQPage JSON-LD structural bits ──
    c = c.replace('"inLanguage": "ko"', '"inLanguage": "en"')
    c = c.replace(f'"mainEntityOfPage": {{ "@type": "WebPage", "@id": "{ko_url}" }}',
                  f'"mainEntityOfPage": {{ "@type": "WebPage", "@id": "{en_url}" }}')
    c = c.replace(f'"item": "{ko_url}"', f'"item": "{en_url}"')
    c = c.replace('"item": "https://browserkit.online/"', '"item": "https://browserkit.online/en/"')
    c = c.replace('"item": "https://browserkit.online/blog/"', '"item": "https://browserkit.online/en/blog/"')
    c = c.replace('"name": "홈"', '"name": "Home"')
    c = c.replace('"name": "블로그"', '"name": "Blog"')

    # ── post-date: KO date style -> English ──
    c = KO_MONTHS_RE.sub(_reformat_date, c)

    # ── lang banner / header brand / header-back / lang switcher ──
    # (blog "ko equivalent" target is /blog/{filename}, not /{slug}/)
    c = c.replace(
        '<span>🌐 This page is also available in <a href="/en/">English</a>.</span>',
        f'<span>🌐 이 페이지는 <a href="/blog/{blog_filename}">한국어</a>로도 볼 수 있습니다.</span>'
    )
    c = c.replace(
        "if (lang.indexOf('ko') === 0) return;",
        "if (lang.indexOf('ko') !== 0) return;"
    )
    c = c.replace('<a href="/" class="header-brand">', '<a href="/en/" class="header-brand">')
    c = c.replace('<a href="/" class="header-back">&#x2190; <span class="header-back-label">BrowserKit 홈으로</span></a>',
                  '<a href="/en/" class="header-back">&#x2190; <span class="header-back-label">Back to BrowserKit</span></a>')
    c = c.replace('<a href="/" class="header-back">← <span class="header-back-label">BrowserKit 홈으로</span></a>',
                  '<a href="/en/" class="header-back">← <span class="header-back-label">Back to BrowserKit</span></a>')
    c = c.replace(
        '<button class="lang-switcher-btn" type="button" data-lang-btn>🌐 <span class="lang-label-full">한국어</span></button>',
        '<button class="lang-switcher-btn" type="button" data-lang-btn>🌐 <span class="lang-label-full">English</span></button>'
    )
    c = c.replace(
        '<a href="/en/">English</a>\n            <a href="#" class="active">한국어</a>',
        f'<a href="#" class="active">English</a>\n            <a href="/blog/{blog_filename}">한국어</a>'
    )
    # blog list "back to blog index" link (entity-arrow and literal-arrow variants)
    c = c.replace('<a href="/blog/" class="back-link">&#x2190; 블로그 목록</a>',
                  '<a href="/en/blog/" class="back-link">&#x2190; Blog</a>')
    c = c.replace('<a href="/blog/" class="back-link">← 블로그 목록</a>',
                  '<a href="/en/blog/" class="back-link">← Blog</a>')

    # ── ad slots (identical constants to gen_en_page.py) ──
    AD_TOP_MARGIN0 = ('<div style="margin:0 0 12px"><!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div></div>')
    AD_TOP_NOMARGIN = ('<div style="margin:12px 0 0"><!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div></div>')
    # blog posts (unlike tool pages) sometimes use a symmetric "margin:12px 0" for the
    # top horizontal ad slot too -- a third variant not seen in tool-page sources.
    AD_TOP_MARGIN12 = ('<div style="margin:12px 0"><!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div></div>')
    AD_COUPANG_SWAP_PREFIX = '<!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><!-- 카카오 애드핏 ('
    AD_COUPANG_SWAP_SUFFIX = ', 쿠팡 파트너스 다이내믹 배너로 교체) — 복원 시 주석 해제: <div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div> --><div class="adfit-h-desktop"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"728","height":"90","tsource":""});</script></div><div class="adfit-h-mobile"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"320","height":"50","tsource":""});</script></div></div>'
    # blog posts sometimes insert "임시" (temporarily) before "교체" -- make that word optional
    AD_COUPANG_SWAP_RE = re.compile(
        r'(?:<div style="margin:0 0 12px">)?'
        + re.escape('<!-- Google AdSense (승인 후 복원): <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="horizontal" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script> --><!-- 카카오 애드핏 (')
        + r'\d{4}-\d{2}-\d{2}'
        + re.escape(', 쿠팡 파트너스 다이내믹 배너로 ')
        + r'(?:임시 )?'
        + re.escape('교체) — 복원 시 주석 해제: <div class="adfit-h-desktop"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-QD4pRIpdIj7i2mbt" data-ad-width="728" data-ad-height="90"></ins></div><div class="adfit-h-mobile"><ins class="kakao_ad_area" style="display:none" data-ad-unit="DAN-R4xA2niTT8HgGjoO" data-ad-width="320" data-ad-height="50"></ins></div> --><div class="adfit-h-desktop"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"728","height":"90","tsource":""});</script></div><div class="adfit-h-mobile"><script src="https://ads-partners.coupang.com/g.js"></script><script>new PartnersCoupang.G({"id":996719,"template":"carousel","trackingCode":"AF9398669","width":"320","height":"50","tsource":""});</script></div></div>')
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

    count = [0]

    def top_sub(_m):
        count[0] += 1
        return h_placeholder('adTop' if count[0] == 1 else f'adExtra{count[0]}')
    c = re.sub(re.escape(AD_TOP_MARGIN0), top_sub, c)
    c = re.sub(re.escape(AD_TOP_NOMARGIN), top_sub, c)
    c = re.sub(re.escape(AD_TOP_MARGIN12), top_sub, c)
    c = AD_COUPANG_SWAP_RE.sub(lambda _m: h_placeholder('adMiddle'), c)
    c = re.sub(re.escape(AD_BOTTOM_RECT_12), lambda _m: bottom_placeholder, c)
    c = re.sub(re.escape(AD_BOTTOM_RECT_00), lambda _m: bottom_placeholder, c)

    if 'kakao_ad_area' in c or 'PartnersCoupang' in c:
        print(f'  [WARN] {blog_filename}: leftover kakao/coupang markup not auto-converted — needs manual fix')

    c = c.replace(
        '.guide-full-link:hover { text-decoration:underline; }',
        '.guide-full-link:hover { text-decoration:underline; }\n\n    .ad-slot { min-height:90px; display:flex; align-items:center; justify-content:center; margin:0 0 12px; }\n    .ad-slot-rect { min-height:250px; }',
        1
    )

    # ── footer (identical to gen_en_page.py) ──
    c = c.replace(
        '<a href="/privacy">개인정보 처리방침</a>\n        <a href="/terms">이용약관</a>\n        <a href="/about">서비스 소개</a>\n        <a href="/blog/">블로그</a>',
        '<a href="/en/privacy.html">Privacy Policy</a>\n        <a href="/en/terms.html">Terms of Service</a>\n        <a href="/en/about.html">About</a>\n        <a href="/en/blog/">Blog</a>'
    )
    c = c.replace(
        '<a href="/privacy">개인정보 처리방침</a><a href="/terms">이용약관</a><a href="/about">서비스 소개</a><a href="/blog/">블로그</a>',
        '<a href="/en/privacy.html">Privacy Policy</a><a href="/en/terms.html">Terms of Service</a><a href="/en/about.html">About</a><a href="/en/blog/">Blog</a>'
    )
    c = c.replace(
        '&#xa9; 2026 BrowserKit. 모든 처리는 브라우저 내에서 이루어집니다.',
        '&#xa9; 2026 BrowserKit. All processing happens in your browser.'
    )
    c = c.replace(
        '© 2026 BrowserKit. 모든 처리는 브라우저 내에서 이루어집니다.',
        '&#xa9; 2026 BrowserKit. All processing happens in your browser.'
    )

    # ── CTA button target: /{slug}/ (KO tool page) -> /en/{slug}/ ──
    c = c.replace(f'<a href="/{slug}/" class="cta-btn"', f'<a href="/en/{slug}/" class="cta-btn"')

    return c
