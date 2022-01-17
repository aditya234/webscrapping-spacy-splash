# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    hotel_name = scrapy.Field()
    price = scrapy.Field()
    features = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    comment = scrapy.Field()

class HotelDetailItem(scrapy.Item):
    hotel_name = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    hotel_rank = scrapy.Field()
    amenities = scrapy.Field()
    languages = scrapy.Field()
    best_price = scrapy.Field()
    review1 = scrapy.Field()
