import scrapy

class WineItem(scrapy.Item):
   
    wine_id=scrapy.Field()
    name_k=scrapy.Field()
    name_e=scrapy.Field()
    image=scrapy.Field()
    
    detail=scrapy.Field()
    taste=scrapy.Field()
    information=scrapy.Field()
    awards=scrapy.Field()