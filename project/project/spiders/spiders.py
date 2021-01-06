import scrapy
from scrapy.selector import Selector
import json

contents = open('data/issue_no.jl', "r").read() 
datas = [json.loads(str(item)) for item in contents.strip().split('\n')]


class SpiderHistoricalPrice(scrapy.Spider):
    name = 'historical'
    start_urls=[]
    link_format='https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=2018%2F01%2F06&endDate=2021%2F01%2F06&symbol='
    for data in datas:
        internal_id=data["FTID"]
        # isin=data["ISIN"]
        link=link_format+internal_id
        start_urls.append(link)
        # print(isin)

    # def start_requests

    def parse(self, response):
        htmlstr = response.json()['html']
        data = Selector(text=htmlstr)

        for tr in data.xpath('//tr'):
            yield {
                'FTID':response.url.split("=")[-1], 
                'Date': tr.xpath('td/span/text()').get(),
                'Open': tr.xpath('td[2]//text()').get()
            }