import scrapy
import re
from wine.items import WineItem


class ShinsegaeSpider(scrapy.Spider):
    name = 'shinsegae'
    start_url =['http://www.shinsegae-lnb.com']

    
    def __init__(self, name=None, **kwargs):
        
        self.start_page=[] # 크롤링이 진행 될 페이지
        
        for page in range(1,84):
            self.start_page.append("http://www.shinsegae-lnb.com/product/wine?currentPage={}&orderBy=2&listSize=12&selectedWineType=0&selectedWineNation=0&selectedSugar=0&searchText=#orderby".format(page))
        super().__init__(name, **kwargs)


    def start_requests(self):
        for url in self.start_page:
            yield scrapy.Request(url=url,callback=self.parse)


    ''#크롤링 해야 하는 요소
    def parse(self, response):
        item = WineItem()
        
        #한 페이지 내에 존재하는 와인의 개수를 구하기 위한 작업
        wine_cnt=len(response.xpath('//*[@class="list"]/li'))
        
        for i in range(1,wine_cnt+1):
            
            #크롤링 할 와인의 요소를 구하기 위한 작업
            wine=response.xpath(f'//*[@class="list"]/li[{i}]/div/a/@href').extract()
            
            get_wine=self.start_url[0]+wine[0]
            yield scrapy.Request(get_wine,callback=self.get_items)
            

            
    def get_items(self,get_wine):
        
        item=WineItem()
        #url 에서 id만 빼내오기 위한 과정
        search_id=str(get_wine)
        id=re.sub(r'[^0-9]', '', search_id) #숫자만 취급
        item['wine_id']=id[3:]

        #와인 이미지 저장 
        item['image']=get_wine.xpath('//*[@id="section2"]/div/div[1]/img/@src')[0].extract()

        #와인 이름 k 저장
        item['name_k']=get_wine.xpath('//*[@id="section2"]/div/div[2]/div[1]/dl/dt/text()')[0].extract()
        
        #와인 이름 e저장
        item['name_e']=get_wine.xpath('//*[@id="section2"]/div/div[2]/div[1]/dl/dd[1]/text()')[0].extract()


        #와인의 세부 항목 저장 
        element=[]

            #세부항목이 표시되지 않은 것은 "-"로 대체 
        for i in range(1,6):
            character = get_wine.xpath(f'//*[@id="section2"]/div/div[2]/div[2]/ul/li[{i}]/span/descendant-or-self::*/text()').extract()
            if len(character)!=2:
                element.append(f"{character[0]} : -")
            else:
                element.append(f" {character[0]} : {character[1]}")

        element="\n".join(element)
        item['detail']=element


        #와인 맛 저장 
        flavor=[]
            #맛이 표시되지 않은 것은 "-"로 대체 
        for t in range(1,4):
            level= get_wine.xpath(f'//*[@class="box3"]/dl[{t}]/dd/span/p[2]/descendant-or-self::*/text()').extract()
            if len(level)!=1:
                flavor.append("-")
            else:
                flavor.append(*level)
        
        flavor="\n".join(flavor)
        item['taste']=flavor


        #정보
        info_store=[]

        info_store.append(get_wine.xpath('//*[@id="section3"]/div/div[1]/dl/dd/descendant-or-self::*/text()').extract())  
        info_store="".join(info_store[0])
        info_store=re.sub("\r|\n|\t|","",info_store)
        info_store.split("\n")

        item['information']=info_store

        
        #수상
        value=get_wine.xpath('//*[@id="section3"]/div/div[2]/dl/dd/ul/li/descendant-or-self::*/text()').extract()

        if len(value)==0:
            value.append("-")
            value="".join(value)
        else:
            value="\n".join(value)

        item['awards']=value
        
        yield item
        
        