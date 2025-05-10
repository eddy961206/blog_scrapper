

# Naver Blog  Scraper

이 프로젝트는 네이버 블로그의 특정 카테고리 글을 자동으로 수집하여 JSON 파일로 저장하는 Python 스크래퍼입니다.

## 주요 기능

- 네이버 블로그의 글 제목과 본문을 자동으로 추출
- 한 번에 여러 페이지를 순회하며 글을 수집
- 사용자가 지정한 개수(batch_size)만큼 글을 하나의 JSON 파일로 저장
- Selenium을 이용한 크롤링

## 사용 방법

### 1. 환경 준비

- Python 3.x
- Selenium
- webdriver-manager

필요 패키지 설치:
```bash
pip install selenium webdriver-manager
```

### 2. 코드 사용법

```python
from scraper import NaverBlogScraper

blog_id = "your_blog_id_here"  # 네이버 블로그 계정명
output_dir = "raw_content"
category_no = 6  # 크롤링할 카테고리 번호
scraper = NaverBlogScraper(blog_id, output_dir)
scraper.scrape_blog(max_pages=10, category_no=category_no, delay=1, batch_size=100)
scraper.close()
```

- `blog_id`: 네이버 블로그 계정명(예: skykum2004)
- `output_dir`: 결과 파일이 저장될 폴더명
- `category_no`: 크롤링할 카테고리 번호
- `max_pages`: 크롤링할 최대 페이지 수
- `delay`: 각 페이지 크롤링 후 대기 시간(초)
- `batch_size`: 한 파일에 저장할 글 개수

### 3. 결과물

- `output_dir` 폴더에 `batch_1_posts.json`, `batch_2_posts.json` 등으로 저장됩니다.
- 각 파일에는 최대 `batch_size`개의 글이 포함됩니다.

## 참고 사항

- 네이버 블로그 구조가 변경될 경우, CSS 선택자(`TITLE_LIST_SELECTOR`, `POST_CONTENT_SELECTOR`)를 수정해야 할 수 있습니다.
- 크롤링 대상 블로그가 비공개/로그인 제한/성인 인증 등으로 보호된 경우, 정상적으로 동작하지 않을 수 있습니다.

        