import scrapy
import json
import re

contents = open('data/mornst_id.jl', "r").read() 
datas = [json.loads(str(item)) for item in contents.strip().split('\n')]

#step 3
#find the uint to match the financial times website url in the next step

class QuotesSpider(scrapy.Spider):

    name='unit'
    start_urls=[]
    link_format='https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='
    for data in datas:
        internal_id=data["mornst_id"]
        link=link_format+internal_id
        start_urls.append(link)


    def parse(self, response):
        yield {
            'ISIN':response.xpath('//div[@id="overviewQuickstatsDiv"]//td[contains(.,"ISIN")]/../td[@class="line text"]/text()').get(),
            'unit':response.xpath('//div[@id="overviewQuickstatsDiv"]//td[contains(.,"NAV")]/../td[@class="line text"]/text()').get().split()[0]     
        }

