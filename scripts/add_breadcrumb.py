# -*- coding: utf-8 -*-
import os, json, re, html

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # browserkit/ 루트로 이동

# slug -> (한글명, 카테고리)  -- gen_tool_og.py의 TOOLS 매핑과 동일
TOOLS = {
    'maskprivacy':            ('개인정보 마스킹', '개인정보'),
    'pdf-tools':               ('PDF 마스킹', '개인정보'),
    'mask-face':               ('얼굴 블러', '개인정보'),
    'mask-doc':                ('텍스트 마스킹', '개인정보'),
    'exif-remover':            ('사진 위치정보 제거기', '개인정보'),
    'image-tools':             ('이미지 변환', '이미지 편집'),
    'crop-image':              ('이미지 자르기', '이미지 편집'),
    'watermark-image':         ('워터마크 추가', '이미지 편집'),
    'color-picker':            ('색상 추출', '이미지 편집'),
    'image-bright':            ('이미지 보정', '이미지 편집'),
    'bg-remove':               ('AI 배경 제거', '이미지 편집'),
    'image-text':              ('이미지 텍스트 추가', '이미지 편집'),
    'image-filter':            ('이미지 필터', '이미지 편집'),
    'image-collage':           ('이미지 모아 붙이기', '이미지 편집'),
    'pixel-art':               ('픽셀 아트 변환', '이미지 편집'),
    'mosaic-maker':            ('모자이크 생성기', '이미지 편집'),
    'favicon-gen':             ('즐겨찾기 아이콘 생성기', '이미지 편집'),
    'svg-to-png':              ('SVG → PNG 변환기', '이미지 편집'),
    'image-compare':           ('이미지 비교 슬라이더', '이미지 편집'),
    'image-frame':             ('이미지 테두리 추가', '이미지 편집'),
    'mockup-frame':            ('디바이스 목업 생성기', '이미지 편집'),
    'pdf-merge':               ('PDF 합치기', '문서·텍스트'),
    'pdf-split':               ('PDF 분할', '문서·텍스트'),
    'text-tools':              ('텍스트 변환', '문서·텍스트'),
    'diff-checker':            ('텍스트 비교', '문서·텍스트'),
    'markdown-editor':         ('마크다운 편집기', '문서·텍스트'),
    'find-replace':            ('찾아 바꾸기', '문서·텍스트'),
    'line-number':             ('줄 번호 추가', '문서·텍스트'),
    'lorem-gen':               ('더미 텍스트 생성기', '문서·텍스트'),
    'csv-json-convert':        ('CSV ↔ JSON 변환기', '문서·텍스트'),
    'yaml-json-convert':       ('YAML ↔ JSON 변환기', '문서·텍스트'),
    'text-stats':              ('텍스트 통계 분석기', '문서·텍스트'),
    'markdown-table-convert':  ('표 변환기', '문서·텍스트'),
    'pdf-password-remove':     ('PDF 비밀번호 해제', '문서·텍스트'),
    'pdf-password-set':        ('PDF 비밀번호 설정', '문서·텍스트'),
    'qr-code':                 ('QR 코드 생성', '유틸리티'),
    'password-gen':            ('비밀번호 생성기', '유틸리티'),
    'unit-convert':            ('단위 변환기', '유틸리티'),
    'date-calc':               ('날짜 계산기', '유틸리티'),
    'world-clock':             ('세계 시계', '유틸리티'),
    'random-picker':           ('랜덤 추첨기', '유틸리티'),
    'pomodoro-timer':          ('집중 · 휴식 타이머', '유틸리티'),
    'qr-scanner':              ('QR 코드 스캐너', '유틸리티'),
    'ladder-game':             ('사다리타기', '유틸리티'),
    'json-format':             ('JSON 포맷터', '개발자'),
    'regex-test':              ('정규식 테스터', '개발자'),
    'base64-tool':             ('Base64 변환', '개발자'),
    'hash-gen':                ('해시 생성기', '개발자'),
    'minifier':                ('코드 압축기', '개발자'),
    'url-encode':              ('URL 인코더', '개발자'),
    'css-unit':                ('CSS 단위 변환기', '개발자'),
    'uuid-gen':                ('UUID 생성기', '개발자'),
    'jwt-decoder':             ('JWT 디코더', '개발자'),
    'cron-helper':             ('Cron 표현식 도우미', '개발자'),
    'sql-formatter':           ('SQL 포맷터', '개발자'),
    'color-converter':         ('색상 코드 변환기', '개발자'),
    'code-snapshot':           ('코드 스니펫 이미지 생성기', '개발자'),
    'chart-maker':             ('차트 생성기', '데이터·시각화'),
    'diagram-maker':           ('다이어그램 생성기', '데이터·시각화'),
    'palette-gen':             ('색상 팔레트 생성기', '데이터·시각화'),
    'word-cloud':              ('워드클라우드 생성기', '데이터·시각화'),
    'salary-calc':             ('연봉 실수령액 계산기', '계산기'),
    'currency-calc':           ('환율 계산기', '계산기'),
    'loan-calc':               ('대출 이자 계산기', '계산기'),
    'savings-calc':            ('적금·예금 만기 계산기', '계산기'),
    'gif-maker':               ('GIF 애니메이션 생성기', '이미지 편집'),
}

changed = 0
for slug, (name_kr, cat) in TOOLS.items():
    p = f'{slug}/index.html'
    if not os.path.exists(p):
        print('MISSING', p); continue
    s = open(p, encoding='utf-8').read()
    if '"BreadcrumbList"' in s:
        print('SKIP already has breadcrumb', p); continue
    m = re.search(r'rel="canonical" href="(.*?)"', s)
    if not m:
        print('NO CANONICAL', p); continue
    url = m.group(1)
    ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://browserkit.online/"},
            {"@type": "ListItem", "position": 2, "name": cat},
            {"@type": "ListItem", "position": 3, "name": name_kr, "item": url}
        ]
    }
    block = '  <script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n  </script>\n</head>'
    s2 = s.replace('</head>', block, 1)
    open(p, 'w', encoding='utf-8', newline='\n').write(s2)
    changed += 1
print('added BreadcrumbList to', changed, 'pages')
