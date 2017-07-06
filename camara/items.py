# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VereadorItem(scrapy.Item):
    name = scrapy.Field()
    salary_gross = scrapy.Field()
    salary_liquid = scrapy.Field()
    mesano = scrapy.Field()
    entity_id = scrapy.Field()