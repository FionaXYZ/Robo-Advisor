import scrapy
import html 
# import json
import re
# from scrapy import cmdline
# from scraper.items import FundFTID

#step 3 getting down financial time website id to to search for encrypted website url
#going through the website on spiders.py

class QuotesSpider(scrapy.Spider):
    name = 'ftid_no'


    def start_requests(self):
        for ISIN in self.settings['PROJ_USERINPUT_ISINS']:
            yield scrapy.FormRequest(
                f'https://markets.ft.com/data/funds/tearsheet/summary?s={ISIN}:GBP',
                callback=self.parse_ftid
            )

    def parse_ftid(self, response):
        escaped = response.xpath("//div[@class='mod-overview-quote-app-overlay__container']/section[1]/@data-mod-config").get()
        str = html.unescape(escaped)

        yield{
            'ISIN':re.search(r'symbol\W+(\w*)', str).group(1),
            'FTID':re.search(r'xid\W+(\w*)', str).group(1)
        }

        
        # yield FundFTID(
        #         ISIN=re.search(r'symbol\W+(\w*:\w+)', str).group(1),
        #         FTID=re.search(r'xid\W+(\w*)', str).group(1),
        #     )




