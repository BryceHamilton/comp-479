import os
import sys
import scrapy
from scrapy.crawler import CrawlerProcess

class ConcordiaSpider(scrapy.Spider):
    name = "concordia_spider"
    start_urls = ["https://www.concordia.ca"]
    crawled_urls = dict()
    num_downloaded = 0

    custom_settings = {
      'ROBOTSTXT_OBEY': True,
    }

    
    def parse(self, response):
        limit = int(getattr(self, 'limit', None))
        if self.num_downloaded > limit:
            return
        
        lang = response.css("html::attr(lang)").get()
        if lang == 'en':
            title = response.css('title::text').get()
            filename = f"docs_html/{title}.html"
            with open(filename, 'wb') as f:
                f.write(response.body)
            
            self.num_downloaded += 1
            self.log(f'Saved file {filename}')

        for url in response.css('a::attr(href)'):
            if self.num_downloaded > limit:
                return
            
            if url and url not in self.crawled_urls:
                self.crawled_urls[url] = True
                yield response.follow(url, callback=self.parse)


def main(limit):
    print(f"Starting crawler process, limit: {limit}")
    process = CrawlerProcess()
    process.crawl(ConcordiaSpider, limit=limit)
    process.start() 
    

if __name__ == '__main__':
    limit = 300
    if len(sys.argv) > 1:
        limit = sys.argv[1]
    main(limit)