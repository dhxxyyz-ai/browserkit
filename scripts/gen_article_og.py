# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_tool_og import (W, H, INK, POINT, SUB, FONT, BG, fit_font, wrap_lines)
from PIL import Image, ImageDraw, ImageFont
import os as _os

_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))  # browserkit/ 루트로 이동

CAT_COLOR = (0xff, 0xd3, 0x6e)  # '개인정보' 톤과 통일

ARTICLES = {
    '01-privacy-law-intro':   ('개인정보보호법이란?', '핵심만 쉽게 정리',
        '개인정보보호법의 주요 내용과 위반 시 처벌 수위를 알기 쉽게 정리했습니다.'),
    '02-rrn-leak-danger':     ('주민번호가 유출되면', '어떻게 되나요?',
        '주민등록번호 유출 시 발생하는 피해 유형과 즉시 취해야 할 대처 방법을 안내합니다.'),
    '03-id-photo-masking':    ('신분증 사진 보낼 때', '꼭 마스킹해야 하는 이유',
        '신분증 사진을 전송하기 전 꼭 마스킹해야 하는 이유와 올바른 방법을 안내합니다.'),
    '04-resume-privacy':      ('이력서 개인정보,', '어디까지 써야 할까?',
        '이력서에 꼭 필요한 정보와 불필요한 정보를 구분하는 안전한 작성 가이드입니다.'),
    '05-privacy-leak-cases':  ('국내 개인정보 유출', '실제 사례 분석',
        '카드3사·인터파크 등 실제 유출 사례의 원인·피해·예방법을 구체적으로 분석합니다.'),
    '06-image-masking-guide': ('이미지 속 개인정보,', '상황별 마스킹 가이드',
        '신분증·계약서·진단서 이미지 공유 시 숨어있는 위험과 마스킹 방법을 설명합니다.'),
    '08-worker-privacy-law':  ('직장인이 꼭 알아야 할', '개인정보보호법 5가지',
        '업무 중 자주 발생하는 실수와 직장인이 꼭 알아야 할 핵심 5가지를 정리했습니다.'),
    '09-hospital-privacy':    ('병원 서류', '개인정보 처리 방법',
        '진료 기록, 처방전 등 의료 서류의 개인정보를 안전하게 처리하는 법을 안내합니다.'),
    '10-contract-masking':    ('계약서 개인정보', '마스킹하는 법',
        '계약서를 공유하기 전 반드시 처리해야 할 개인정보 항목과 방법을 안내합니다.'),
    '11-kakao-id-photo':      ('카카오톡으로 신분증', '보내도 될까?',
        '카카오톡으로 신분증을 전송할 때의 위험성과 안전한 대안을 알아봅니다.'),
    '12-privacy-policy-guide':('개인정보 처리방침', '어떻게 만드나요?',
        '개인정보 처리방침의 필수 항목과 작성 방법을 알기 쉽게 설명합니다.'),
    '13-masking-tool-compare':('무료 개인정보', '마스킹 툴 비교',
        '다양한 무료 마스킹 도구를 비교하고 상황에 맞는 툴을 선택하는 법을 안내합니다.'),
    '14-local-processing':    ('서버 없이 개인정보', '처리하는 방법',
        '클라이언트 사이드 처리 방식이 왜 더 안전한지 원리와 장점을 설명합니다.'),
    '15-privacy-report-guide':('개인정보보호위원회', '신고 방법 안내',
        '개인정보 침해를 당했을 때 신고하는 방법과 절차를 단계별로 안내합니다.'),
}

GUIDE_CAT_COLOR = (0xbc, 0xd4, 0xff)  # '유틸리티' 톤 - 개인정보 칼럼과 구분
GUIDE_ARTICLES = {
    '40-mainui-guide': ('BrowserKit 홈 화면', '사용법 완전 가이드',
        '바탕화면처럼 꾸며진 홈에서 도구상자, 검색, 시작 메뉴, 창 조작까지 살펴봅니다.'),
}


def generate(slug):
    if slug in GUIDE_ARTICLES:
        line1, line2, desc = GUIDE_ARTICLES[slug]
        chip_text, chip_color = 'BrowserKit 가이드', GUIDE_CAT_COLOR
    else:
        line1, line2, desc = ARTICLES[slug]
        chip_text, chip_color = '개인정보 보호 칼럼', CAT_COLOR
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
    chip = chip_text
    cb = draw.textbbox((0, 0), chip, font=f_chip)
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    pad = 16
    cx1 = W - 74 - cw - pad * 2
    cy1 = 70
    draw.rounded_rectangle([cx1, cy1, cx1 + cw + pad * 2, cy1 + ch + pad * 2], radius=999, fill=chip_color + (255,), outline=INK + (255,), width=3)
    draw.text((cx1 + pad - cb[0], cy1 + pad - cb[1]), chip, font=f_chip, fill=INK)

    # 제목 2줄 (고정 레이아웃 - 자동 축소)
    f_h1 = fit_font(draw, max(line1, line2, key=len), W - 180, 74, minimum=44)
    y = 175
    bold((90, y), line1, f_h1, INK, 2)
    y += f_h1.size + 14
    bold((90, y), line2, f_h1, INK, 2)
    title_end = y + f_h1.size
    desc_top = title_end + 58

    # 설명 (최대 2줄, 배지와 겹치지 않게 자동 축소)
    badge_top = 524
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
        # 2줄일 때만 제목-배지 사이 정중앙에 배치해 위/아래 여백을 동일하게 맞춘다
        min_gap = 16
        available = badge_top - title_end
        gap = max(min_gap, (available - total_h) / 2)
        desc_top = title_end + gap
    dy = desc_top
    for dl in d_lines:
        draw.text((90, dy), dl, font=f_d, fill=SUB)
        dy += line_h

    # 하단 주소 배지
    f_badge = ImageFont.truetype(FONT, 27)
    badge = f'browserkit.online/blog/{slug}'
    bb3 = draw.textbbox((0, 0), badge, font=f_badge, stroke_width=1)
    btw, bth = bb3[2] - bb3[0], bb3[3] - bb3[1]
    pad = 17
    bx0, by0 = 90, badge_top
    draw.rounded_rectangle([bx0, by0, bx0 + btw + pad * 2, by0 + bth + pad * 2], radius=14, fill=(255, 255, 255, 235), outline=INK + (255,), width=3)
    bold((bx0 + pad - bb3[0], by0 + pad - bb3[1]), badge, f_badge, POINT, 1)

    os.makedirs('img/og', exist_ok=True)
    out = f'img/og/blog-{slug}.png'
    img.save(out, "PNG")
    return out


if __name__ == '__main__':
    targets = sys.argv[1:] or list(ARTICLES)
    for slug in targets:
        print(generate(slug))
