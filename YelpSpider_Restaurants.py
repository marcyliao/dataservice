# encoding: utf-8
import scrapy

class YelpSpider(scrapy.Spider):
    name = 'yelpspider'
    start_urls = ['https://www.yelp.ca/search?find_loc=langley,+BC&cflt=chinese',
                  'https://www.yelp.ca/search?find_loc=Vancouver,+BC,+Canada&cflt=chinese',
                  'https://www.yelp.ca/search?find_loc=Burnaby,+BC,+Canada&cflt=chinese',
                  'https://www.yelp.ca/search?find_loc=Richmond,+BC,+Canada&cflt=chinese']

    def parse(self, response):
        urls = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li/div/div[1]/div[1]/div/div[2]/h3/span/a/@href').extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_contents)
            # yield {'url': response.urljoin(url)}

        next_page = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_contents(self, response):
        name = ' '.join(response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/h1/text()').extract()).strip('\n')
        address = ' '.join(response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]/div/strong/address//text()').extract()).strip('\n')
        phone = ' '.join(response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/li[3]/span[3]/text()').extract()).strip('\n')
        review_counts = response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span/span/text()').extract()
        review_stars = response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/meta/@content').extract()
        yield {'name': name,
               'address': address,
               'phone': phone,
               'ranking':'',
               'review_counts': review_counts,
               'review_stars': review_stars,
               'url': response.url
               }