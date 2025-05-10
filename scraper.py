from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import random

class NaverBlogScraper:
    TITLE_LIST_SELECTOR = "div.pcol1"  # 글 목록에서 제목 span
    POST_CONTENT_SELECTOR = "div.se-main-container"  # 글 상세에서 본문
    DATE_SELECTOR = "span.se_publishDate.pcol2"
    PAGE_LOAD_WAIT_MIN = 0.2
    PAGE_LOAD_WAIT_MAX = 0.7

    def __init__(self, blog_id, output_dir="raw_content"):
        self.blog_id = blog_id
        self.output_dir = output_dir
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def scrape_page(self, page=1, category_no=0):
        list_url = f"https://blog.naver.com/PostList.naver?from=postList&blogId={self.blog_id}&categoryNo={category_no}&currentPage={page}"
        print(f"[페이지 이동] {list_url}")
        self.driver.get(list_url)
        time.sleep(random.uniform(self.PAGE_LOAD_WAIT_MIN, self.PAGE_LOAD_WAIT_MAX))
        titles = self.driver.find_elements(By.CSS_SELECTOR, self.TITLE_LIST_SELECTOR)
        contents = self.driver.find_elements(By.CSS_SELECTOR, self.POST_CONTENT_SELECTOR)
        dates = self.driver.find_elements(By.CSS_SELECTOR, self.DATE_SELECTOR)
        print(f"[디버그] 추출된 제목 개수: {len(titles)}, 본문 개수: {len(contents)}, 날짜 개수: {len(dates)}")
        posts = []
        for title_elem, content_elem, date_elem in zip(titles, contents, dates):
            title = title_elem.text.strip()
            content = content_elem.text.strip()
            date_full = date_elem.text.strip()
            date_parts = date_full.split() if date_full else []
            date = " ".join(date_parts[:3]) if len(date_parts) >= 3 else ""
            posts.append({"title": title, "date": date, "content": content})
        return posts

    def save_posts(self, posts, batch_name):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        filename = f"{self.output_dir}/{batch_name}_posts.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"[저장] {filename} 저장 완료")
        return filename

    def close(self):
        self.driver.quit()

    def scrape_blog(self, max_pages=1, category_no=0, delay=1, batch_size=100):
        batch_posts = []
        batch_num = 1
        total_posts = 0
        for page in range(1, max_pages + 1):
            print(f"\n[진행] {page}페이지 스크래핑 (카테고리 {category_no})")
            posts = self.scrape_page(page, category_no)
            if not posts:
                print(f"[알림] {page}페이지에 글이 없음")
                break
            batch_posts.extend(posts)
            while len(batch_posts) >= batch_size:
                to_save = batch_posts[:batch_size]
                self.save_posts(to_save, f"batch_{batch_num}")
                total_posts += len(to_save)
                batch_posts = batch_posts[batch_size:]
                batch_num += 1
            time.sleep(delay)
        # 남은 글 저장
        if batch_posts:
            self.save_posts(batch_posts, f"batch_{batch_num}")
            total_posts += len(batch_posts)
        print(f"\n[완료] 스크래핑 종료, 총 {total_posts}개 글 저장 완료")

if __name__ == "__main__":
    # 아래 부분만 본인 계정명으로 바꿔서 사용하면 됩니다.
    blog_id = "skykum2004"  # 네이버 블로그 계정명(예: skykum2004)
    output_dir = "raw_content_date"
    category_no = 6
    scraper = NaverBlogScraper(blog_id, output_dir)
    scraper.scrape_blog(max_pages=143, category_no=category_no, delay=1)
    scraper.close()