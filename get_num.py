import scrapy
import html 
import json
import re


class QuotesSpider(scrapy.Spider):
    name = 'issue_no'
    start_urls = [
        'https://markets.ft.com/data/funds/tearsheet/summary?s=LU0712206050:GBP',
    ]

    def parse(self, response):
        escaped = response.xpath("//div[@class='mod-overview-quote-app-overlay__container']/section[1]/@data-mod-config").get()
        str = html.unescape(escaped)

        yield {
            'ISIN': re.search('symbol\W+(\w*:\w+)', str).group(1),
            'internal_id' : re.search('xid\W+(\w*)', str).group(1),      
        }

