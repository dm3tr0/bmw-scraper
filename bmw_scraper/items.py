import scrapy

class BmwCarItem(scrapy.Item):
    # Detail Page Header fields
    model = scrapy.Field()
    name = scrapy.Field()
    
    # Specification Section fields
    mileage = scrapy.Field()
    registered = scrapy.Field()
    engine = scrapy.Field()
    range = scrapy.Field() # electric only
    exterior = scrapy.Field()
    fuel = scrapy.Field()
    transmission = scrapy.Field()
    registration = scrapy.Field()
    upholstery = scrapy.Field()