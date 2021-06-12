import scrapy
from scrapy.selector import Selector
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

contents=open('data/ftid_no.jl',"r").read() 
datas=[json.loads(str(item)) for item in contents.strip().split('\n')]

# step 5 
# find the historical data of the stocks
# on the ft webpage, only up to one year data can be scraped at one time
# by finding ft id, data can be scraped according to startDate and endDate input, hence data in the past 3 year can be found at one time
class SpiderHistoricalPrice(scrapy.Spider):
    name='historical'
    start_urls=[]
    start_date=datetime.today()-relativedelta(years=3)
    end_date=datetime.today()
    start_date=datetime.strftime(start_date,"%Y%%2F%m%%2F%d")
    end_date=datetime.strftime(end_date,"%Y%%2F%m%%2F%d")
    link_format=f'https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={start_date}&endDate={end_date}&symbol='
    for data in datas:
        internal_id=data["FTID"]
        link=link_format+internal_id
        start_urls.append(link)


    def parse(self,response):
        ftid=response.url.split("=")[-1]
        for data in datas:
            if data["FTID"]==ftid:
                isin=data["ISIN"]
                break

        htmlstr=response.json()['html']
        info=Selector(text=htmlstr)

        for tr in info.xpath('//tr'):
            yield {
                'ISIN':isin, 
                'Date':tr.xpath('td/span/text()').get(),
                'Price':tr.xpath('td[2]//text()').get()
            }