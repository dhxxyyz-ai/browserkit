# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os, re, html, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(SCRIPT_DIR))  # browserkit/ 루트로 이동
FONT = os.path.join(SCRIPT_DIR, "GowunDodum.ttf")
W, H = 1200, 630
INK = (0x2a, 0x24, 0x33)
POINT = (0x7b, 0x6c, 0xff)
SUB = (0x5a, 0x50, 0x66)

# 메인 index.html 폴더 팔레트 (파스텔 테마)
CAT_COLORS = {
    '개인정보':      (0xff, 0xd3, 0x6e),
    '이미지 편집':   (0xff, 0xb3, 0xc7),
    '문서·텍스트':   (0xa8, 0xe6, 0xcf),
    '유틸리티':      (0xbc, 0xd4, 0xff),
    '개발자':        (0xe0, 0xc3, 0xff),
    '데이터·시각화': (0xff, 0xd9, 0xa8),
    '계산기':        (0xa0, 0xe8, 0xe0),
    '생활·재미':     (0xff, 0xc2, 0xd6),
}

# slug -> (한글명, 영문명, 카테고리)
TOOLS = {
    'maskprivacy':            ('개인정보 마스킹', 'MaskPrivacy', '개인정보'),
    'pdf-tools':              ('PDF 마스킹', 'MaskPDF', '개인정보'),
    'mask-face':              ('얼굴 블러', 'MaskFace', '개인정보'),
    'mask-doc':               ('텍스트 마스킹', 'MaskDoc', '개인정보'),
    'exif-remover':           ('사진 위치정보 제거기', 'ExifRemover', '개인정보'),
    'image-tools':            ('이미지 변환', 'FitImage', '이미지 편집'),
    'crop-image':             ('이미지 자르기', 'CropImage', '이미지 편집'),
    'watermark-image':        ('워터마크 추가', 'WatermarkImage', '이미지 편집'),
    'color-picker':           ('색상 추출', 'ColorPicker', '이미지 편집'),
    'image-bright':           ('이미지 보정', 'ImageBright', '이미지 편집'),
    'bg-remove':              ('AI 배경 제거', 'BGRemove', '이미지 편집'),
    'image-text':             ('이미지 텍스트 추가', 'ImageText', '이미지 편집'),
    'image-filter':           ('이미지 필터', 'ImageFilter', '이미지 편집'),
    'image-collage':          ('이미지 모아 붙이기', 'ImageCollage', '이미지 편집'),
    'pixel-art':              ('픽셀 아트 변환', 'PixelArt', '이미지 편집'),
    'mosaic-maker':           ('모자이크 생성기', 'MosaicMaker', '이미지 편집'),
    'favicon-gen':            ('즐겨찾기 아이콘 생성기', 'FaviconGen', '이미지 편집'),
    'svg-to-png':             ('SVG → PNG 변환기', 'SVGtoPNG', '이미지 편집'),
    'image-compare':          ('이미지 비교 슬라이더', 'ImageCompare', '이미지 편집'),
    'image-frame':            ('이미지 테두리 추가', 'ImageFrame', '이미지 편집'),
    'mockup-frame':           ('디바이스 목업 생성기', 'MockupFrame', '이미지 편집'),
    'pdf-merge':              ('PDF 합치기', 'PDFMerge', '문서·텍스트'),
    'pdf-split':              ('PDF 분할', 'PDFSplit', '문서·텍스트'),
    'text-tools':             ('텍스트 변환', 'TextTools', '문서·텍스트'),
    'diff-checker':           ('텍스트 비교', 'DiffChecker', '문서·텍스트'),
    'markdown-editor':        ('마크다운 편집기', 'MarkdownEditor', '문서·텍스트'),
    'find-replace':           ('찾아 바꾸기', 'FindReplace', '문서·텍스트'),
    'line-number':            ('줄 번호 추가', 'LineNumber', '문서·텍스트'),
    'lorem-gen':              ('더미 텍스트 생성기', 'LoremGen', '문서·텍스트'),
    'csv-json-convert':       ('CSV ↔ JSON 변환기', 'CSVJSONConvert', '문서·텍스트'),
    'yaml-json-convert':      ('YAML ↔ JSON 변환기', 'YAMLJSONConvert', '문서·텍스트'),
    'text-stats':             ('텍스트 통계 분석기', 'TextStats', '문서·텍스트'),
    'markdown-table-convert': ('표 변환기', 'MarkdownTableConvert', '문서·텍스트'),
    'pdf-password-remove':    ('PDF 비밀번호 해제', 'PDFPasswordRemove', '문서·텍스트'),
    'pdf-password-set':       ('PDF 비밀번호 설정', 'PDFPasswordSet', '문서·텍스트'),
    'qr-code':                ('QR 코드 생성', 'QRCode', '유틸리티'),
    'password-gen':           ('비밀번호 생성기', 'PasswordGen', '유틸리티'),
    'unit-convert':           ('단위 변환기', 'UnitConvert', '유틸리티'),
    'date-calc':              ('날짜 계산기', 'DateCalc', '유틸리티'),
    'world-clock':            ('세계 시계', 'WorldClock', '유틸리티'),
    'random-picker':          ('랜덤 추첨기', 'RandomPicker', '유틸리티'),
    'pomodoro-timer':         ('집중 · 휴식 타이머', 'PomodoroTimer', '유틸리티'),
    'qr-scanner':             ('QR 코드 스캐너', 'QRScanner', '유틸리티'),
    'ladder-game':            ('사다리타기', 'LadderGame', '유틸리티'),
    'json-format':            ('JSON 포맷터', 'JSONFormat', '개발자'),
    'regex-test':             ('정규식 테스터', 'RegexTest', '개발자'),
    'base64-tool':            ('Base64 변환', 'Base64Tool', '개발자'),
    'hash-gen':               ('해시 생성기', 'HashGen', '개발자'),
    'minifier':               ('코드 압축기', 'Minifier', '개발자'),
    'url-encode':             ('URL 인코더', 'URLEncode', '개발자'),
    'css-unit':               ('CSS 단위 변환기', 'CSSUnit', '개발자'),
    'uuid-gen':               ('UUID 생성기', 'UUIDGen', '개발자'),
    'jwt-decoder':            ('JWT 디코더', 'JWTDecoder', '개발자'),
    'cron-helper':            ('Cron 표현식 도우미', 'CronHelper', '개발자'),
    'sql-formatter':          ('SQL 포맷터', 'SQLFormatter', '개발자'),
    'color-converter':        ('색상 코드 변환기', 'ColorConverter', '개발자'),
    'code-snapshot':          ('코드 스니펫 이미지 생성기', 'CodeSnapshot', '개발자'),
    'chart-maker':            ('차트 생성기', 'ChartMaker', '데이터·시각화'),
    'diagram-maker':          ('다이어그램 생성기', 'DiagramMaker', '데이터·시각화'),
    'palette-gen':            ('색상 팔레트 생성기', 'PaletteGen', '데이터·시각화'),
    'word-cloud':             ('워드클라우드 생성기', 'WordCloudGen', '데이터·시각화'),
    'salary-calc':            ('연봉 실수령액 계산기', 'SalaryCalc', '계산기'),
    'currency-calc':          ('환율 계산기', 'CurrencyCalc', '계산기'),
    'loan-calc':              ('대출 이자 계산기', 'LoanCalc', '계산기'),
    'savings-calc':           ('적금·예금 만기 계산기', 'SavingsCalc', '계산기'),
    'gif-maker':              ('GIF 애니메이션 생성기', 'GifMaker', '이미지 편집'),
    'vat-calc':               ('부가세 계산기', 'VatCalc', '계산기'),
    'lotto-gen':              ('로또 번호 생성기', 'LottoGen', '생활·재미'),
    'severance-pay-calc':     ('퇴직금 계산기', 'SeverancePayCalc', '계산기'),
    'bmi-calc':               ('BMI/칼로리 계산기', 'BmiCalc', '계산기'),
    'http-status-ref':        ('HTTP 상태 코드 사전', 'HttpStatusRef', '개발자'),
    'xlsx-csv-convert':       ('엑셀 CSV 변환기', 'XlsxCsvConvert', '문서·텍스트'),
    'pet-age-calc':           ('반려동물 나이 계산기', 'PetAgeCalc', '생활·재미'),
    'split-bill-calc':        ('더치페이 계산기', 'SplitBillCalc', '계산기'),
}


def radial_blob(size, color, alpha=255):
    blob = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(blob)
    cx, cy = size[0] / 2, size[1] / 2
    maxr = max(cx, cy)
    steps = 60
    for i in range(steps, 0, -1):
        r = maxr * i / steps
        a = int(alpha * (1 - i / steps) ** 1.6)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    return blob


def make_bg():
    base = Image.new("RGB", (W, H))
    c1, c2 = (0xe2, 0xcd, 0xff), (0xbf, 0xe7, 0xff)
    for y in range(H):
        for x in range(0, W, 4):
            t = ((x / W) + (y / H)) / 2
            px = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            for xx in range(x, min(x + 4, W)):
                base.putpixel((xx, y), px)
    img = base.convert("RGBA")
    for (cx, cy), rad, color in [
        ((int(W * 0.16), int(H * 0.9)), int(W * 0.62), (0xb6, 0xf0, 0xc6)),
        ((int(W * 0.86), int(H * 0.14)), int(W * 0.60), (0xc7, 0xd6, 0xff)),
        ((int(W * 0.82), int(H * 0.84)), int(W * 0.52), (0xff, 0xc9, 0xde)),
        ((int(W * 0.06), int(H * 0.10)), int(W * 0.45), (0xff, 0xf0, 0xbf)),
    ]:
        img.alpha_composite(radial_blob((rad * 2, rad * 2), color, 190), (cx - rad, cy - rad))
    return img.convert("RGB")


BG = make_bg()  # 배경은 한 번만 계산해 재사용


def get_desc(slug):
    s = open(f'{slug}/index.html', encoding='utf-8').read()
    m = re.search(r'name="description" content="(.*?)"', s)
    d = html.unescape(m.group(1)).strip()
    first = re.split(r'(?<=[.다요])\s', d)[0].rstrip('.')
    return first


def fit_font(draw, text, max_w, start, minimum=34, stroke=2):
    size = start
    while size > minimum:
        f = ImageFont.truetype(FONT, size)
        bb = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
        if bb[2] - bb[0] <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(FONT, minimum)


def wrap_two_lines(draw, text, font, max_w):
    if draw.textbbox((0, 0), text, font=font)[2] <= max_w:
        return [text]
    words = text.split(' ')
    for cut in range(len(words) - 1, 0, -1):
        line1 = ' '.join(words[:cut])
        if draw.textbbox((0, 0), line1, font=font)[2] <= max_w:
            return [line1, ' '.join(words[cut:])]
    return [text]


def wrap_lines(draw, text, font, max_w, max_lines=2):
    words = text.split(' ')
    lines = []
    cur = ''
    i = 0
    while i < len(words):
        w = words[i]
        trial = w if not cur else cur + ' ' + w
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w:
            cur = trial
            i += 1
        else:
            if not cur:
                # 단어 하나가 너무 길면 강제로 소비
                cur = w
                i += 1
            lines.append(cur)
            cur = ''
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
        i = len(words)

    if i < len(words) and lines:
        # 남은 단어가 있으면 마지막 줄을 말줄임표로 축약
        tail = ' '.join(words[i:])
        last = lines[-1]
        combined = (last + ' ' + tail).rstrip()
        if draw.textbbox((0, 0), combined, font=font)[2] <= max_w:
            lines[-1] = combined
        else:
            while draw.textbbox((0, 0), last + '…', font=font)[2] > max_w and len(last) > 1:
                last = last[:-1]
            lines[-1] = last.rstrip() + '…'
    return lines[:max_lines]


def generate(slug):
    name_kr, name_en, cat = TOOLS[slug]
    cat_color = CAT_COLORS[cat]
    desc = get_desc(slug)

    img = BG.copy()
    draw = ImageDraw.Draw(img, "RGBA")

    def bold(xy, text, font, fill, stroke=2):
        draw.text(xy, text, font=font, fill=fill, stroke_width=stroke, stroke_fill=fill)

    # 상단 브랜드
    logo_r = 34
    lx, ly = 108, 96
    draw.ellipse([lx - logo_r, ly - logo_r, lx + logo_r, ly + logo_r], fill=POINT + (255,), outline=INK + (255,), width=5)
    f_logo = ImageFont.truetype(FONT, 38)
    bb = draw.textbbox((0, 0), "B", font=f_logo, stroke_width=2)
    bold((lx - (bb[2] - bb[0]) / 2 - bb[0], ly - (bb[3] - bb[1]) / 2 - bb[1]), "B", f_logo, (255, 255, 255), 2)
    f_brand = ImageFont.truetype(FONT, 34)
    bx = lx + logo_r + 18
    by = ly - 22
    bold((bx, by), "Browser", f_brand, INK, 1)
    bb2 = draw.textbbox((bx, by), "Browser", font=f_brand, stroke_width=1)
    bold((bb2[2], by), "Kit", f_brand, POINT, 1)

    # 카테고리 칩 (우상단)
    f_chip = ImageFont.truetype(FONT, 26)
    chip = f'{cat} 도구'
    cb = draw.textbbox((0, 0), chip, font=f_chip)
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    pad = 16
    cx1 = W - 74 - cw - pad * 2
    cy1 = 70
    draw.rounded_rectangle([cx1, cy1, cx1 + cw + pad * 2, cy1 + ch + pad * 2], radius=999, fill=cat_color + (255,), outline=INK + (255,), width=3)
    draw.text((cx1 + pad - cb[0], cy1 + pad - cb[1]), chip, font=f_chip, fill=INK)

    # 도구 한글명 (자동 축소, 최대 2줄)
    f_h1 = fit_font(draw, name_kr, W - 180, 84)
    lines = wrap_two_lines(draw, name_kr, f_h1, W - 180)
    y = 195 if len(lines) == 1 else 165
    for ln in lines:
        bold((90, y), ln, f_h1, INK, 2)
        y += f_h1.size + 14

    # 영문명 (제목과 넉넉히 띄움)
    f_en = ImageFont.truetype(FONT, 36)
    y += 38
    bold((90, y), name_en, f_en, POINT, 1)
    en_bottom = y + f_en.size  # 영문명 텍스트의 실제 아랫변 (여백 계산 기준점)
    y += 36 + 46

    # 설명 (필요하면 최대 2줄까지 줄바꿈, 배지와 겹치지 않게 자동 축소)
    title_end = y
    badge_top = 524
    desc_top = title_end + 16
    f_d = ImageFont.truetype(FONT, 30)
    while True:
        max_lines = 2 if (badge_top - desc_top) >= f_d.size * 2 + 30 else 1
        d_lines = wrap_lines(draw, desc, f_d, W - 180, max_lines=max_lines)
        line_h = f_d.size + 12
        total_h = line_h * len(d_lines)
        if desc_top + total_h <= badge_top - 14 or f_d.size <= 22:
            break
        f_d = ImageFont.truetype(FONT, f_d.size - 2)
    if len(d_lines) >= 2:
        # 2줄일 때만 영문명 아랫변 - 배지 사이 정중앙에 배치해
        # (영문명↔설명 첫 줄) 여백과 (설명 마지막 줄↔배지) 여백을 동일하게 맞춘다
        available = badge_top - en_bottom
        gap = (available - total_h) / 2
        desc_top = en_bottom + gap
    dy = desc_top
    for dl in d_lines:
        draw.text((90, dy), dl, font=f_d, fill=SUB)
        dy += line_h

    # 하단 주소 배지
    f_badge = ImageFont.truetype(FONT, 27)
    badge = f'browserkit.online/{slug}/'
    bb3 = draw.textbbox((0, 0), badge, font=f_badge, stroke_width=1)
    btw, bth = bb3[2] - bb3[0], bb3[3] - bb3[1]
    pad = 17
    bx0, by0 = 90, badge_top
    draw.rounded_rectangle([bx0, by0, bx0 + btw + pad * 2, by0 + bth + pad * 2], radius=14, fill=(255, 255, 255, 235), outline=INK + (255,), width=3)
    bold((bx0 + pad - bb3[0], by0 + pad - bb3[1]), badge, f_badge, POINT, 1)

    os.makedirs('img/og', exist_ok=True)
    out = f'img/og/{slug}.png'
    img.save(out, "PNG")
    return out


if __name__ == '__main__':
    targets = sys.argv[1:] or list(TOOLS)
    for slug in targets:
        print(generate(slug))
