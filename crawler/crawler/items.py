# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    description = scrapy.Field()
    review = scrapy.Field()
