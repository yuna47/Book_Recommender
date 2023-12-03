import time

import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookSpider(scrapy.Spider):
    name = "books"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    def start_requests(self):
        urls = [
            # "https://product.kyobobook.co.kr/category/KOR/01#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/03#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/07#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/09#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/13#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/15#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/17#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/19#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/21#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/23#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/25#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/26#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/27#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/29#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/31#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/32#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/33#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/35#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/38#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/39#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/41#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/42#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/47#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/50#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/53#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/59#?page=1&type=all&per=50&sort=sel",
            # "https://product.kyobobook.co.kr/category/KOR/05#?page=1&type=best&per=50",
            # "https://product.kyobobook.co.kr/category/KOR/08#?page=1&type=best&per=50",
            # "https://product.kyobobook.co.kr/category/KOR/11#?page=1&type=best&per=50"
        ]
        for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse_book_list)
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#homeTabAll a.prod_link'))
            )

            sel = Selector(text=self.driver.page_source)

            book_links = sel.css('#homeTabAll a.prod_link::attr(href)').extract()
            self.log(book_links)

            self.driver.quit()

            for book_link in book_links:
                yield scrapy.Request(url=book_link, callback=self.parse_book)
                time.sleep(0.01)

    def parse_book(self, response):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(response.url)

        title = self.driver.find_element(By.CSS_SELECTOR, 'span.prod_title').text
        image = response.urljoin(
            self.driver.find_element(By.CSS_SELECTOR, 'div.portrait_img_box img').get_attribute('src'))
        author = self.driver.find_element(By.CSS_SELECTOR, 'div.author a').text
        publisher = self.driver.find_element(By.CSS_SELECTOR, 'div.prod_info_text.publish_date a').text
        description_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.intro_bottom div.info_text')
        description_texts = [element.text for element in description_elements]
        description = ' '.join(description_texts)

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        reviews = self.driver.execute_script("""
                    var reviews = document.querySelectorAll('div.comment_text');
                    return Array.from(reviews, function(review) {
                        return review.textContent.trim();
                    });
                    """)

        self.driver.quit()

        yield {
            'title': title,
            'image': image,
            'author': author,
            'publisher': publisher,
            'description': description,
            'reviews': ' '.join(reviews),
        }
