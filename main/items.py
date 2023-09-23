# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MainItem(scrapy.Item):
    catalog = scrapy.Field()
    car_model = scrapy.Field()
    car_model_link = scrapy.Field()
    production_date = scrapy.Field()
    car_series = scrapy.Field()
    series = scrapy.Field()
    engine = scrapy.Field()
    engine_link = scrapy.Field()
    series_production_date = scrapy.Field()
    series_description = scrapy.Field()
    maingroup = scrapy.Field()
    maingroup_link = scrapy.Field()
    maingroup_img = scrapy.Field()
    link_no = scrapy.Field()
    subgroup_link = scrapy.Field()
    sub_image = scrapy.Field()