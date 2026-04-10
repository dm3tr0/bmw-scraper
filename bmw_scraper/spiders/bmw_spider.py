import scrapy
from scrapy_playwright.page import PageMethod

class BmwSpider(scrapy.Spider):
    name = "bmw_spider"
    
    def start_requests(self):
        base_url = "https://usedcars.bmw.co.uk/result/?payment%20type=cash&size=23&source=home"
        
        for page_number in range(1, 6):
            page_url = f"{base_url}&page={page_number}"
            
            self.logger.info(f"Queuing Page {page_number}...")
            
            yield scrapy.Request(
                url=page_url, 
                meta={
                    "playwright": True,
                    "playwright_include_page": False, 
                    "playwright_page_methods": [
                        # wait for the cars to render
                        PageMethod("wait_for_selector", "p[itemprop='name']", timeout=20000),
                    ],
                }, 
                callback=self.parse,
                dont_filter=True # so scrapy doesn't accidentally skip URLs that look similar
            )

    def parse(self, response):
        models = response.css('p[itemprop="name"]::text').getall()
        names = response.css('h3.uvl-c-advert-overview__title a::text').getall()
        links = response.css('h3.uvl-c-advert-overview__title a::attr(href)').getall()
        
        for model, name, link in zip(models, names, links):
            car_url = response.urljoin(link)
            
            car_item = {
                'model': model.strip() if model else '',
                'name': name.strip() if name else '',
                'link': car_url,
            }

            yield scrapy.Request(
                url=car_url,
                callback=self.parse_detail,
                meta={
                    "playwright": True,
                    "playwright_include_page": False,
                    "playwright_page_methods": [
                        # wait specifically for the spec data to render
                        PageMethod("wait_for_selector", "div.uvl-c-specification-overview__value", timeout=20000) 
                    ],
                    "car_item": car_item # pass the data we already collected
                }
            )

    def parse_detail(self, response):
        item = response.meta["car_item"]
        
        item['mileage'] = response.xpath('//div[span[text()="Mileage"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['registered'] = response.xpath('//div[span[text()="Registered"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['engine'] = response.xpath('//div[span[text()="Engine"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['range'] = response.xpath('//div[span[text()="Range"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['exterior'] = response.xpath('//div[span[text()="Exterior"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['fuel'] = response.xpath('//div[span[text()="Fuel"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['transmission'] = response.xpath('//div[span[text()="Transmission"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['registration'] = response.xpath('//div[span[text()="Registration"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        item['upholstery'] = response.xpath('//div[span[text()="Upholstery"]]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get()

        yield item