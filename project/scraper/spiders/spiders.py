import scrapy
from scrapy.selector import Selector
import json

contents = open('data/ftid_no.jl', "r").read() 
datas = [json.loads(str(item)) for item in contents.strip().split('\n')]


class SpiderHistoricalPrice(scrapy.Spider):
    name = 'historical'
    start_urls=[]
    link_format='https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=2018%2F01%2F08&endDate=2021%2F01%2F08&symbol='
    for data in datas:
        internal_id=data["FTID"]
        link=link_format+internal_id
        start_urls.append(link)


    # def start_requests

    def parse(self, response):
        ftid=response.url.split("=")[-1]
        for data in datas:
            if data["FTID"]== ftid:
                isin=data["ISIN"]
                break

        htmlstr = response.json()['html']
        info = Selector(text=htmlstr)

        for tr in info.xpath('//tr'):
            yield {
                'ISIN':isin, 
                'Date': tr.xpath('td/span/text()').get(),
                'Price': tr.xpath('td[2]//text()').get()
            }