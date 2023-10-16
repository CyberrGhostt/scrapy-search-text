# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



# class SearchtextItem(scrapy.Item):

#     pass


class SearchTextSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    domain_name = scrapy.Field()
    total_links = scrapy.Field()
    related_links = scrapy.Field()

