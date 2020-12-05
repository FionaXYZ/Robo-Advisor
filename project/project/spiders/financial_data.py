import scrapy
from scrapy.selector import Selector
import json

contents = open('issue_no.jl', "r").read() 
datas = [json.loads(str(item)) for item in contents.strip().split('\n')]


class QuotesSpider(scrapy.Spider):
    name = 'historical'
    start_urls=[]
    link_format='https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=2017%2F12%2F02&endDate=2020%2F12%2F03&symbol='
    for data in datas:
        internal_id=data["internal_id"]
        link=link_format+internal_id
        start_urls.append(link)

    def parse(self, response):
        htmlstr = response.json()['html']
        data = Selector(text=htmlstr)

        for tr in data.xpath('//tr'):
            yield {
                'Date': tr.xpath('td/span/text()').get(),
                'Open': tr.xpath('td[2]//text()').get(),
                'Close': tr.xpath('td[5]//text()').get(),
            }