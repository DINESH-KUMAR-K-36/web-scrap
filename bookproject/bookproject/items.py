# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()