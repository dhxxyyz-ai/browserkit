# Google AdSense 광고 현황

## 기본 정보

- **Publisher ID**: `ca-pub-2077977787979506`
- **AdSense 스크립트** (`<head>` 공통 삽입):
  ```html
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2077977787979506" crossorigin="anonymous"></script>
  ```

---

## 광고 슬롯

### 디스플레이 광고 (BrowserKit_Display)
- **슬롯 ID**: `6825825428`
- **형식**: `auto` / `data-full-width-responsive="true"`

```html
<div style="margin:0"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2077977787979506" data-ad-slot="6825825428" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>
```

### 멀티플렉스 광고
- **슬롯 ID**: `9500090221`
- **형식**: `autorelaxed`

```html
<div style="margin:0"><ins class="adsbygoogle" style="display:block" data-ad-format="autorelaxed" data-ad-client="ca-pub-2077977787979506" data-ad-slot="9500090221"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>
```

---

## 파일별 광고 위치

### index.html (PC 메인 SPA)
> JS 렌더링 방식. `SHOW_ADSENSE = true` 조건부 삽입.

| 슬롯 | 위치 설명 |
|------|-----------|
| `6825825428` | 폴더 목록 상단 (horizontal) |
| `6825825428` | 파일 뷰어 상단 |
| `6825825428` | 뷰어 상단 오버레이 (horizontal) |
| `9500090221` | 뷰어 하단 오버레이 |
| `9500090221` | 폴더 목록 하단 |

### mobile.html (모바일 전용)
> JS 렌더링 방식. `.bk-ad-top` / `.bk-ad-bottom` 클래스로 초기화 제어.

| 슬롯 | 위치 설명 |
|------|-----------|
| `6825825428` | 상단 sticky 헤더 하단 (디스플레이) |
| `9500090221` | 하단 고정 바 (멀티플렉스) |

---

### 도구 페이지 (25개)
> 공통 패턴: `.hero` div 닫힘 태그 직후 → 디스플레이 광고 / `</div></main>` 직전 → 멀티플렉스 광고

| 파일 | 디스플레이 위치 | 멀티플렉스 위치 |
|------|----------------|----------------|
| `base64-tool/index.html` | hero 섹션 하단 | main 하단 |
| `bg-remove/index.html` | hero 섹션 하단 | main 하단 |
| `chart-maker/index.html` | hero 섹션 하단 | main 하단 |
| `color-picker/index.html` | hero 섹션 하단 | main 하단 |
| `crop-image/index.html` | hero 섹션 하단 | main 하단 |
| `date-calc/index.html` | hero 섹션 하단 | main 하단 |
| `diff-checker/index.html` | hero 섹션 하단 | main 하단 |
| `find-replace/index.html` | hero 섹션 하단 | main 하단 |
| `hash-gen/index.html` | hero 섹션 하단 | main 하단 |
| `image-bright/index.html` | hero 섹션 하단 | main 하단 |
| `image-tools/index.html` | hero 섹션 하단 | main 하단 |
| `json-format/index.html` | hero 섹션 하단 | main 하단 |
| `markdown-editor/index.html` | hero 섹션 하단 | main 하단 |
| `mask-doc/index.html` | hero 섹션 하단 | main 하단 |
| `mask-face/index.html` | hero 섹션 하단 | main 하단 |
| `maskprivacy/index.html` | hero 섹션 하단 | main 하단 |
| `password-gen/index.html` | hero 섹션 하단 | main 하단 |
| `pdf-merge/index.html` | hero 섹션 하단 | main 하단 |
| `pdf-tools/index.html` | hero 섹션 하단 | main 하단 |
| `qr-code/index.html` | hero 섹션 하단 | main 하단 |
| `regex-test/index.html` | hero 섹션 하단 | main 하단 |
| `text-tools/index.html` | hero 섹션 하단 | main 하단 |
| `unit-convert/index.html` | hero 섹션 하단 | main 하단 |
| `watermark-image/index.html` | hero 섹션 하단 | main 하단 |
| `world-clock/index.html` | hero 섹션 하단 | main 하단 |

---

### 블로그 포스트 (38개)
> 공통 패턴: post-date 직후 → 디스플레이 / 2번째 h2 태그 직전 → 디스플레이 / post-nav 직전 → 멀티플렉스

| 파일 | 상단 디스플레이 | 중간 디스플레이 | 하단 멀티플렉스 |
|------|----------------|----------------|----------------|
| `blog/01-privacy-law-intro.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/02-rrn-leak-danger.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/03-id-photo-masking.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/04-resume-privacy.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/05-privacy-leak-cases.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/06-image-masking-guide.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/07-maskprivacy-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/08-worker-privacy-law.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/09-hospital-privacy.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/10-contract-masking.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/11-kakao-id-photo.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/12-privacy-policy-guide.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/13-masking-tool-compare.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/14-local-processing.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/15-privacy-report-guide.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/16-maskpdf-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/17-fitimage-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/18-pdfmerge-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/19-maskface-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/20-texttools-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/21-maskdoc-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/22-watermarkimage-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/23-colorpicker-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/24-qrcode-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/25-jsonformat-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/26-passwordgen-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/27-base64tool-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/28-diffchecker-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/29-unitconvert-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/30-markdowneditor-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/31-imagebright-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/32-regextest-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/33-bgremove-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/34-datecalc-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/35-worldclock-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/36-hashgen-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/37-findreplace-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |
| `blog/38-chartmaker-howto.html` | post-date 직후 | 2번째 h2 앞 | post-nav 앞 |

---

### blog/index.html
> 블로그 목록 페이지

| 슬롯 | 위치 설명 |
|------|-----------|
| `6825825428` | blog-hero 섹션 하단 |
| `6825825428` | 두 카테고리 섹션 사이 (🔒 개인정보 보호 / 🛠️ 도구 활용 가이드) |
| `9500090221` | main 하단 |

---

## 광고 없는 파일

| 파일 | 이유 |
|------|------|
| `404.html` | 에러 페이지 |
| `privacy.html` | 개인정보 처리방침 |
| `terms.html` | 이용약관 |
| `about.html` | 소개 페이지 |
