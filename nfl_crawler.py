from collections import Counter
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
import logging
import os

PAGE_LIMIT = 2000
LOGGING = False  # change to True to debug


class NFLScraper(CrawlSpider):
    name = 'nfl'
    custom_settings = {'CONCURRENT_REQUESTS': '35'}  # set to 35 to get all 32 teams, 3 extra links
    start_urls = ['https://www.nfl.com/teams/']
    pages_visited = 0
    dictionary = {}      # {url, [out link urls]}
    counts = Counter()   # counts the number of links to a url
    csv_created = False  # used to only create csv once

    # extract internal links, deny both /fantasy and /fantasyfootball, both link to fantasy.nfl.com
    link_extractor = LinkExtractor(allow=(r'^https://www.nfl.com/teams/([-A-Za-z0-9]*)?(/)?$',
                                          r'https://www.nfl.com(/)?$', r'^https://www.nfl.com/news/.*'),
                                   deny=r'^https://www.nfl.com/fantasy(football)?')

    # follow internal links
    rules = [Rule(link_extractor, callback='parse_start_url', follow=True)]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if not LOGGING:
            logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response, **kwargs):
        pass

    def parse_start_url(self, response, **kwargs):
        if self.pages_visited >= PAGE_LIMIT:
            if not self.csv_created:  # create csv once
                self.csv_stats()
                self.csv_created = True
            raise CloseSpider()  # stop crawling
        out_links = []
        for link in self.link_extractor.extract_links(response):
            url = link.url
            if url not in out_links:  # do not count out links more than once
                out_links.append(url)
                if url in self.counts:
                    self.counts[url] += 1
                else:
                    self.counts[url] = 1
        self.dictionary[response.url] = out_links
        self.pages_visited += 1

    def csv_stats(self):
        if not os.path.exists('csv'):
            os.makedirs('csv')
        file = open('csv/nfl.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(('url', '# links to url', 'out links'))
        for key in self.dictionary:
            if key in self.counts:
                writer.writerow((key, self.counts[key], self.dictionary[key]))
            else:
                writer.writerow((key, 0, self.dictionary[key]))
        file.close()

    # Graph Construction
    


def main():
    scrape_nfl = input('Perform NFL Scraping? (YES): ')
    if scrape_nfl == 'YES':
        process = CrawlerProcess()
        process.crawl(NFLScraper)
        process.start()
    else:
        print('NFL Scraping skipped')


if __name__ == '__main__':
    main()
