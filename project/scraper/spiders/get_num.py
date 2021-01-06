import scrapy
import html 
# import json
import re
# from scrapy import cmdline

from scraper.items import FundFTID


##global variables
# with open('quotes.json') as f:
#   datas = json.load(f)

class QuotesSpider(scrapy.Spider):
    name = 'issue_no'


    def start_requests(self):
        for ISIN in self.settings['PROJ_USERINPUT_ISINS']:
            yield scrapy.FormRequest(
                f'https://markets.ft.com/data/funds/tearsheet/summary?s={ISIN}:GBP',
                callback=self.parse_ftid
            )

    def parse_ftid(self, response):
        escaped = response.xpath("//div[@class='mod-overview-quote-app-overlay__container']/section[1]/@data-mod-config").get()
        str = html.unescape(escaped)

        yield FundFTID(
                ISIN=re.search(r'symbol\W+(\w*:\w+)', str).group(1),
                FTID=re.search(r'xid\W+(\w*)', str).group(1),
            )




