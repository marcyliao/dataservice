import scrapy

class YelpSpider(scrapy.Spider):
    name = 'yelpspider'
    start_urls = ['https://www.yelp.ca/search?find_loc=langley,+BC&cflt=chinese']

    def parse(self, response):
        urls = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li/div/div[1]/div[1]/div/div[2]/h3/span/a/@href').extract()
        for url in urls:
            yield {'url': response.urljoin(url)}

        next_page = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)