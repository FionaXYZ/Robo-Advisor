import scrapy
import html 
import json
import re
from scrapy import cmdline


##global variables
with open('quotes.json') as f:
  datas = json.load(f)

class QuotesSpider(scrapy.Spider):
    name = 'issue_no'
    start_urls=[]
    link_format='https://markets.ft.com/data/funds/tearsheet/summary?s='
    for data in datas:
        isin=data["ISIN"]
        link=link_format+isin+':GBP'
        start_urls.append(link)

    def parse(self, response):
        escaped = response.xpath("//div[@class='mod-overview-quote-app-overlay__container']/section[1]/@data-mod-config").get()
        str = html.unescape(escaped)

        yield {
            'ISIN': re.search('symbol\W+(\w*:\w+)', str).group(1),
            'internal_id' : re.search('xid\W+(\w*)', str).group(1),      
        } 



