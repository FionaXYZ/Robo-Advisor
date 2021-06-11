import scrapy



#step 3
#find the uint to match the financial times website url in the next step

class QuotesSpider(scrapy.Spider):
    name='unit'
    def start_requests(self):
        for ISIN in self.settings['PROJ_USERINPUT_ISINS']:
            yield scrapy.FormRequest(
                f'https://markets.ft.com/data/search?query={ISIN}',
                callback=self.parse_unit
            )
    def parse_unit(self, response):
        symbol=response.xpath('//div[@id="fund-panel"]//td[@class="mod-ui-table__cell--text"]/text()').get(),
        isin_unit=symbol[0].split(":")
        yield {
            'ISIN':isin_unit[0],
            'unit':isin_unit[1]
        }

