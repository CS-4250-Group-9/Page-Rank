from collections import Counter
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider, NotSupported
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
import logging
import os
import re
import page_graph as pg

PAGE_LIMIT=None # Check main function below to set the PAGE_LIMIT variable

LOGGING = False  # change to True to debug

class CPPScraper(CrawlSpider):
    
    name = 'cpp'
    start_urls = ['https://www.cpp.edu/index.shtml']  # cpp home page
    pages_visited = 0
    dictionary = {}      # {url, [out link urls]}
    counts = Counter()   # counts the number of links to a url
    csv_created = False  # used to only create csv once

    page_graph = pg.PageGraph() # Setting up graph object to represent connected nodes of a website
    # { url: { "num_in_links": num_in_links, "num_out_links": num_out_links, "out_links": [out links] } }

    link_extractor = LinkExtractor(allow=r'^https://www.cpp.edu.*')  # extract internal links

    rules = [Rule(link_extractor, callback='parse_start_url', follow=True)]  # follow internal links

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.output_callback = kw.get('args').get('callback')
                
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
                self.create_PageGraph()
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

    def create_PageGraph(self):
        for url in self.dictionary:
            if url in self.counts:
                self.page_graph.add_page(url, self.counts[url], len(self.dictionary[url]), self.dictionary[url])
            else:
                self.page_graph.add_page(url, 0, len(self.dictionary[url]), self.dictionary[url])


    def csv_stats(self):
        relative_path = '.'
        complete_path = relative_path + '/csv'
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)
        file = open(complete_path + '/cpp.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(('url', '# links to url', 'out links'))
        for key in self.dictionary:
            if key in self.counts:
                writer.writerow((key, self.counts[key], self.dictionary[key]))
            else:
                writer.writerow((key, 0, self.dictionary[key]))
        file.close()

    def close(self, spider, reason):
        self.output_callback(self.page_graph)

class CustomCrawler:

    def __init__(self) -> None:
        self.output = None
        self.process = CrawlerProcess()

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls):
        self.process.crawl(cls, args={'callback': self.yield_output})
        self.process.start()

def crawl_static(cls):
    crawler = CustomCrawler()
    crawler.crawl(cls)
    return crawler.output

def scrape_CPP(page_limit):
    global PAGE_LIMIT
    PAGE_LIMIT = page_limit
    process = CrawlerProcess()
    process.crawl(CPPScraper)
    process.start()

def main():

    page_graph = pg.PageGraph()

    scrape_cpp = input('Perform CPP Scraping? (YES): ')
    if scrape_cpp == 'YES':
        global PAGE_LIMIT
        PAGE_LIMIT = 15
        page_graph = crawl_static(CPPScraper)
        page_graph.display_keys()
        
    else:
        print('CPP Scraping skipped')


if __name__ == '__main__':
    main()
