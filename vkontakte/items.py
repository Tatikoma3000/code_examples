# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VkontakteItem(scrapy.Item):
    # define the fields for your item here like:
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()
    birthday = scrapy.Field()
    birthyear = scrapy.Field()
    followers = scrapy.Field()
    photo_count = scrapy.Field()
    video_count = scrapy.Field()
    communities = scrapy.Field()
    subscriptions = scrapy.Field()
    id = scrapy.Field()
    photo_link = scrapy.Field()
