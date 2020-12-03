import scrapy
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = 'historical'
    start_urls = [
        'https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=2017%2F12%2F02&endDate=2020%2F12%2F03&symbol=535675951',
    ]

    def parse(self, response):
        htmlstr = response.json()['html']
        print(htmlstr)
        data = Selector(text=htmlstr)
        # print(data)

        for tr in data.xpath('//tr'):
            # tds = tr.xpath('td').getall()

            # assert len(tds)==6, f"missing tds (shoud be 6, get {tds})"

            yield {
                'name': tr.xpath('td/span/text()').get(),
                'open': tr.xpath('td[2]//text()').get(),
                'close': tr.xpath('td[5]//text()').get(),
            }