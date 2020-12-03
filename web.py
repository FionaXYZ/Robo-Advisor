import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000X8RW',
        'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000NGEL',
        'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000MDAJ',
        'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000Y0Q0',
        'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000LWRT',
    ]

    def parse(self, response):
            yield {
                'Name':response.xpath('//div[@id="snapshotTitleDiv"]//div[@class="snapshotTitleBox"]/h1/text()').get(),
                'ISIN':response.xpath('//div[@id="overviewQuickstatsDiv"]//td[contains(.,"ISIN")]/../td[@class="line text"]/text()').get(),
                '3 year annualised': response.xpath('//div[@id="overviewTrailingReturnsDiv"]//td[contains(.,"3 Years Annualised")]/../td[@class="value number"]/text()').get(),             
            }

