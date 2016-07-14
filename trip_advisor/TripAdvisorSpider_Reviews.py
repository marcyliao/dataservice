import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

class TripAdvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    offset = 0
    base_url = 'https://www.tripadvisor.ca/Search?q=chinese+restaurant&geo=181724&ajax=search'

    # geo=181724&pid=3826 for Langley City, British Columbia
    start_urls = [base_url]

    def parse(self, response):
        urls = response.xpath('//*[@id="taplc_search_results_0"]/div/div/div/div[2]/div[2]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_contents)

        next_page = response.xpath('//*[@class="currentPageNumber pageNumber"]')
        if next_page:
            self.offset += 30
            url =  self.base_url + "&o=" + str(self.offset)
            yield scrapy.Request(url, self.parse)

    def parse_contents(self, response):
        name = self.extract_text(response.xpath('//*[@id="HEADING"]/text()'))

        reviews_sections = response.xpath("//div[contains(@class,'reviewSelector')]")
        for sel in reviews_sections: 
            reviews_user     = self.extract_text(sel.xpath('div/div[1]/div[1]/div[1]/div[2]/span/text()'))
            # reviews_user_url #TODO: This one is really hard to get...
            reviews_title    = self.extract_text(sel.xpath('div/div[2]/div[1]/div/div[1]/a/span/text()'))
            reviews_date     = self.extract_text(sel.xpath('div/div[2]/div[1]/div/div[2]/span[2]/text()'))
            reviews_stars    = self.extract_text(sel.xpath('div/div[2]/div[1]/div/div[2]/span[1]/img/@alt'))
            reviews_contents = self.extract_text(sel.xpath('div/div[2]/div[1]/div/div[3]/p/text()'))

            yield {  
               'name': name,
               'reviews_user': reviews_user,
               #'reviews_user_url': '#' #TODO
               'reviews_title': reviews_title,
               'reviews_date': reviews_date,
               'reviews_stars': reviews_stars,
               'reviews_contents': reviews_contents,
               'restaurant_url': response.url
            }

        review_next_page = response.xpath("//div[contains(@class,'pagination')]/a[contains(@class,'next')]/@href")
        if review_next_page:
            yield scrapy.Request(response.urljoin(review_next_page[0].extract()), self.parse_contents)


    def extract_text(self, xpath):
        return ' '.join(xpath.extract()).strip()

      
          
