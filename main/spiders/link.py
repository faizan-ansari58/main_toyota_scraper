import scrapy
from main.items import MainItem
import re
class LinkSpider(scrapy.Spider):
    name = "link"
    subgroup_link_no = 0

    def start_requests(self):
        url = 'https://catcar.info/toyota/?lang=en&l=bWFya2V0PT1ldXJvfHxzdD09MjB8fHN0cz09eyIxMCI6IlJlZ2lvbiIsIjIwIjoiRXVyb3BlIn0%3D'
        yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        
        catalogs = response.css('tr td:nth-child(1)::text').getall()
        car_models = response.css('tr td:nth-child(2) a::text').getall()
        car_model_links = response.css('tr td:nth-child(2) a::attr(href)').getall()
        production_dates = response.css('tr td:nth-child(3)::text').getall()
        car_seriess = response.css('tr td:nth-child(4)::text').getall()
        for i in range(129,130):
            catalog = catalogs[i]
            car_model = car_models[i]
            car_model_link = car_model_links[i]
            production_date = production_dates[i]
            car_series = car_seriess[i]

            yield scrapy.Request(car_model_link, callback=self.series_page,cb_kwargs={'catalog':catalog,'car_model':car_model,'car_model_link':car_model_link,'production_date':production_date,'car_series':car_series})

    def series_page(self, response,catalog,car_model,car_model_link,production_date,car_series):

        tr_elements = response.css('tr')
        for model in tr_elements[1:]:
            series = model.css('td:nth-child(1)::text').get()
            engine = model.css('td:nth-child(2) a::text').get()
            engine_link = model.css('td:nth-child(2) a::attr(href)').get()
            series_production_date = model.css('td:nth-child(3)::text').get()
            des = model.css('td:nth-child(4)::text').extract()
            cleaned_data = [item.replace(' ','').replace('\n','') for item in des if item.replace(' ','').replace('\n','')]
            series_description = ', '.join(cleaned_data)

            if engine_link:
                yield scrapy.Request(engine_link, callback=self.maingroup_page,cb_kwargs={'catalog':catalog,'car_model':car_model,'car_model_link':car_model_link,'production_date':production_date,'car_series':car_series,
                                                                                      'series':series,'engine':engine,'engine_link':engine_link,'series_production_date':series_production_date,'series_description':series_description
                                                                                      })


    def maingroup_page(self, response,catalog,car_model,car_model_link,production_date,car_series,series,engine,engine_link,series_production_date,series_description):
        pages = response.xpath('//div[@class="content-left"]/ul/li/a/@href').getall()
        if pages:
            for page in pages:
                yield scrapy.Request(page, callback=self.main_page,cb_kwargs={'catalog':catalog,'car_model':car_model,'car_model_link':car_model_link,'production_date':production_date,'car_series':car_series,
                                                                                      'series':series,'engine':engine,'engine_link':engine_link,'series_production_date':series_production_date,'series_description':series_description
                                                                                      })
    def main_page(self,response,catalog,car_model,car_model_link,production_date,car_series,series,engine,engine_link,series_production_date,series_description):
        divs = response.xpath('//div[@class="groups-parts"]/div')
        for div in divs:
            maingroup = div.xpath('a/span[2]/text()').get()
            maingroup_link = div.xpath('a/@href').get()
            maingroup_img = div.xpath('a/span[1]/img/@src').get()
            yield scrapy.Request(maingroup_link, callback=self.subgroup_page,cb_kwargs={'catalog':catalog,'car_model':car_model,'car_model_link':car_model_link,'production_date':production_date,'car_series':car_series,
                                                                                      'series':series,'engine':engine,'engine_link':engine_link,'series_production_date':series_production_date,'series_description':series_description,
                                                                                      'maingroup':maingroup,'maingroup_link':maingroup_link,'maingroup_img':maingroup_img
                                                                                      })


    def subgroup_page(self, response,catalog,car_model,car_model_link,production_date,car_series,series,engine,engine_link,series_production_date,series_description,maingroup,maingroup_link,maingroup_img):
        pages = response.xpath('//div[@class="content-left"]/ul/li/a/@href').getall()
        if pages:
            for page in pages:
                yield scrapy.Request(page, callback=self.page,cb_kwargs={'catalog':catalog,'car_model':car_model,'car_model_link':car_model_link,'production_date':production_date,'car_series':car_series,
                                                                                      'series':series,'engine':engine,'engine_link':engine_link,'series_production_date':series_production_date,'series_description':series_description,
                                                                                      'maingroup':maingroup,'maingroup_link':maingroup_link,'maingroup_img':maingroup_img
                                                                                      })

    def page(self, response,catalog,car_model,car_model_link,production_date,car_series,series,engine,engine_link,
            series_production_date,series_description,maingroup,maingroup_link,maingroup_img):

            subgroup_link = ''
            sub_image = response.xpath('//div[@class="img_wrapper"]/img/@src').get()
            tr_elements = response.css('tr')
            for tr in tr_elements[1:]:
                onclick_attribute = tr.xpath('//tr[@class="pointer"]/@onclick').get()
                if onclick_attribute:
                    match = re.search(r"getArticles\(this, '(.+?)',", onclick_attribute)
                    if match:
                        extracted_value = match.group(1)
                        subgroup_link = extracted_value

                        self.subgroup_link_no+=1
                        item = MainItem()
                        item['catalog'] = catalog
                        item['car_model'] = car_model
                        item['car_model_link'] = car_model_link
                        item['production_date'] = production_date
                        item['car_series'] = car_series
                        item['series'] = series
                        item['engine'] = engine
                        item['engine_link'] = engine_link
                        item['series_production_date'] = series_production_date
                        item['series_description'] = series_description
                        item['maingroup'] = maingroup
                        item['maingroup_link'] = maingroup_link
                        item['maingroup_img'] = maingroup_img
                        item['link_no'] = self.subgroup_link_no
                        item['subgroup_link'] = f'https://catcar.info/toyota/?lang=en&l={subgroup_link}'
                        item['sub_image'] = sub_image
                        
                        
                        yield item
            
