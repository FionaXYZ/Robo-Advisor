import scrapy
import html 
import re
import json


#step 4 getting down financial time website id to to search for encrypted website url
#going through the website on spiders.py

contents=open('data/unit.jl',"r").read() 
isins=[json.loads(str(item)) for item in contents.strip().split('\n')]

class QuotesSpider(scrapy.Spider):
    name='ftid_no'


    def start_requests(self):
        for isin in isins:
            yield scrapy.FormRequest(
                f'https://markets.ft.com/data/funds/tearsheet/summary?s={isin["ISIN"]}:{isin["unit"]}',
                callback=self.parse_ftid
            )

    def parse_ftid(self, response):
        escaped=response.xpath("//div[@class='mod-overview-quote-app-overlay__container']/section[1]/@data-mod-config").get()
        str=html.unescape(escaped)

        yield{
            'ISIN':re.search(r'symbol\W+(\w*)', str).group(1),
            'FTID':re.search(r'xid\W+(\w*)', str).group(1)
        }





