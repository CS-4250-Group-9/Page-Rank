from collections import Counter
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider, NotSupported
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
import logging
import os
import re

PAGE_LIMIT = 2000
LOGGING = False  # change to True to debug


class CPPScraper(CrawlSpider):

    name = 'cpp'
    start_urls = ['https://www.cpp.edu/index.shtml']  # cpp home page
    pages_visited = 0
    dictionary = {}      # {url, [out link urls]}
    counts = Counter()   # counts the number of links to a url
    csv_created = False  # used to only create csv once

    link_extractor = LinkExtractor(allow=r'^https://www.cpp.edu.*')  # extract internal links

    rules = [Rule(link_extractor, callback='parse_start_url', follow=True)]  # follow internal links

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if not LOGGING:
            logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response, **kwargs):
        pass

    def parse_start_url(self, response, **kwargs):
        try:
            if re.match(r'^https://idp.*', response.url):  # skip idp, counted as an internal link
                return
        except NotSupported:
            return
        if self.pages_visited >= PAGE_LIMIT:
            if not self.csv_created:  # create csv once
                self.csv_stats()
                self.csv_created = True
            raise CloseSpider()  # stop crawling
        out_links = []
        try:
            for link in self.link_extractor.extract_links(response):
                url = link.url.replace('~', '')  # '~' causing problems with how links are counted
                if url not in out_links:         # do not count out links more than once
                    out_links.append(url)
                    if url in self.counts:
                        self.counts[url] += 1
                    else:
                        self.counts[url] = 1
        except AttributeError as e:  # for content that is not a web page
            print(response.url, e)
        self.dictionary[response.url] = out_links
        self.pages_visited += 1

    def csv_stats(self):
        if not os.path.exists('csv'):
            os.makedirs('csv')
        file = open('csv/cpp.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(('url', '# links to url', 'out links'))
        for key in self.dictionary:
            if key in self.counts:
                writer.writerow((key, self.counts[key], self.dictionary[key]))
            else:
                writer.writerow((key, 0, self.dictionary[key]))
        file.close()


def main():
    scrape_cpp = input('Perform CPP Scraping? (YES): ')
    if scrape_cpp == 'YES':
        process = CrawlerProcess()
        process.crawl(CPPScraper)
        process.start()
    else:
        print('CPP Scraping skipped')


if __name__ == '__main__':
    main()
