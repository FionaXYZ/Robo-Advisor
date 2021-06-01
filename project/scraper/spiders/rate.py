import scrapy
import json
import re

contents = open('data/mornst_id.jl', "r").read() 
datas = [json.loads(str(item)) for item in contents.strip().split('\n')]

#step 2
# getting down year annualised rate and standard deviation from morningstar website

class QuotesSpider(scrapy.Spider):

    name='rate_sd'
    start_urls=[]
    link_format='https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='
    for data in datas:
        internal_id=data["mornst_id"]
        link=link_format+internal_id
        start_urls.append(link+'&tab=1')
        start_urls.append(link+'&tab=2')



    def parse(self, response):

        morn_id=response.url.split("=")[-2][:-4]
        for data in datas:
            if data["mornst_id"]==morn_id:
                isin=data["ISIN"]
                break

        if response.url.split("=")[-1]=="1":
            yield {
                'ISIN':isin,
                '3_year_annualised':response.xpath('//div[@id="returnsTrailingDiv"]//td[contains(.,"3 Years Annualised")]/../td[@class="col2 value number"]/text()').get(),
            }
        elif response.url.split("=")[-1]=="2":
            yield {
                'ISIN':isin,
                '3_year_sd': response.xpath('//div[@id="ratingRiskLeftDiv"]//td[contains(.,"3-Yr Std Dev")]/../td[@class="value number"]/text()').get()            
            }


