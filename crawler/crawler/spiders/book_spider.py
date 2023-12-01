import scrapy


class BookSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            "https://product.kyobobook.co.kr/category/KOR/01#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/03#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/05#?page=1&type=best&per=50",
            "https://product.kyobobook.co.kr/category/KOR/07#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/08#?page=1&type=best&per=50",
            "https://product.kyobobook.co.kr/category/KOR/09#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/11#?page=1&type=best&per=50",
            "https://product.kyobobook.co.kr/category/KOR/13#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/15#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/17#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/19#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/21#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/23#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/25#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/26#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/27#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/29#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/31#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/32#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/33#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/35#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/38#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/39#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/41#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/42#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/47#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/50#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/53#?page=1&type=all&per=50&sort=sel",
            "https://product.kyobobook.co.kr/category/KOR/59#?page=1&type=all&per=50&sort=sel"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        book_links = response.css(
            'ol.prod_list li.prod_item div.prod_area div.prod_thumb_box a.prod_link::attr(href)').extract()
        for book_link in book_links:
            yield scrapy.Request(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        title = response.css('span.prod_title::text').get()
        image = response.urljoin(response.css('div.portrait_img_box portrait img::attr(src)').get())
        author = response.css('div.author a::text').get()
        publisher = response.css('div.prod_info_text publish_date a::text').get()
        description = ' '.join(response.css('div.intro_bottom div.info_text::text').extract())

        review_text = response.css('div.comment_text::text').extract()

        page_links = response.css('div.pagination a.btn_page_num')
        for page_link in page_links:
            page_url = response.urljoin(page_link.attrib['href'])
            yield scrapy.Request(url=page_url, callback=self.parse_review_page)

        print("--------title: ", title)

        yield {
            'title': title,
            'image': image,
            'author': author,
            'publisher': publisher,
            'description': description,
            'reviews': ' '.join(review_text),
        }

    def parse_review_page(self, response):
        review_text = response.css('div.comment_text::text').extract()
        yield {'reviews': ' '.join(review_text)}
