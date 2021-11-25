'''
Primary Author: Carl Fukawa
Modifications: Eugene Mondkar

'''

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

####################################

class CPPScraper(CrawlSpider):
    
    name = 'cpp'
    start_urls = ['https://www.cpp.edu/index.shtml']  # cpp home page
    pages_visited = 0
    out_link_dictionary = {}      # {url, [out link urls]} 
    in_link_dictionary = {}      # {url, [in link urls]} # in_links 
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
            
            self.create_PageGraph()
            raise CloseSpider()  # stop crawling          
         
        out_links = []

        try:

            modified_url = response.url.replace('~','')

            for link in self.link_extractor.extract_links(response):
                url = link.url.replace('~', '')  # '~' causing problems with how links are counted
                
                if url not in out_links:         # do not count out links more than once
                    
                    out_links.append(url)
                    
                    if url in self.counts:
                        self.counts[url] += 1
                        self.in_link_dictionary[url].append(modified_url) # in_links
                    else:
                        self.counts[url] = 1
                        self.in_link_dictionary[url] = [modified_url] # in_links

                    if url not in self.out_link_dictionary:
                        self.out_link_dictionary[url] = []
        
            self.out_link_dictionary[modified_url] = out_links
            self.pages_visited += 1

        except AttributeError as e:  # for content that is not a web page
            print(response.url, e)
        
        
    # For page graph manipulation # in_links
    def create_PageGraph(self):

        # Clean up
        dangling_links = []
        for url in self.out_link_dictionary:
            if len(self.out_link_dictionary[url]) == 0:
                dangling_links.append(url)

        for url in self.out_link_dictionary:
            self.out_link_dictionary[url] = list(set(self.out_link_dictionary[url]) - set(dangling_links))

        for url in self.out_link_dictionary:
            if (len(self.out_link_dictionary[url]) > 0):
                if url in self.counts:
                    self.page_graph.add_page(url, self.counts[url], self.in_link_dictionary[url], len(self.out_link_dictionary[url]), self.out_link_dictionary[url])
                else:
                    self.page_graph.add_page(url, 0, list(), len(self.out_link_dictionary[url]), self.out_link_dictionary[url])


    def close(self, spider, reason):
        self.output_callback(self.page_graph)

####################################

class NFLScraper(CrawlSpider):
    name = 'nfl'
    # custom_settings = {'CONCURRENT_REQUESTS': '35'}  # set to 35 to get all 32 teams, 3 extra links
    start_urls = ['https://www.nfl.com/teams/']
    pages_visited = 0
    out_link_dictionary = {}      # {url, [out link urls]}
    in_link_dictionary = {}      # {url, [in link urls]} # in_links 
    counts = Counter()   # counts the number of links to a url
    csv_created = False  # used to only create csv once

    page_graph = pg.PageGraph() # Setting up graph object to represent connected nodes of a website
    # { url: { "num_in_links": num_in_links, "num_out_links": num_out_links, "out_links": [out links] } }

    # extract internal links, deny both /fantasy and /fantasyfootball, both link to fantasy.nfl.com
    link_extractor = LinkExtractor(allow=(r'^https://www.nfl.com/teams/([-A-Za-z0-9]*)?(/)?$',
                                          r'https://www.nfl.com(/)?$', r'^https://www.nfl.com/news/.*'),
                                   deny=r'^https://www.nfl.com/fantasy(football)?')

    # follow internal links
    rules = [Rule(link_extractor, callback='parse_start_url', follow=True)]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.output_callback = kw.get('args').get('callback')

        if not LOGGING:
            logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response, **kwargs):
        pass

    def parse_start_url(self, response, **kwargs):

        if self.pages_visited >= PAGE_LIMIT:
            
            self.create_PageGraph()
            raise CloseSpider()  # stop crawling
        
        out_links = []
        
        try:
            for link in self.link_extractor.extract_links(response):
                url = link.url

                if url not in out_links:  # do not count out links more than once

                    out_links.append(url)
                    
                    if url in self.counts:
                        self.counts[url] += 1
                        self.in_link_dictionary[url].append(response.url) # in_links
                    else:
                        self.counts[url] = 1
                        self.in_link_dictionary[url] = [response.url] # in_links

                    if url not in self.out_link_dictionary:
                        self.out_link_dictionary[url] = []

            self.out_link_dictionary[response.url] = out_links
            self.pages_visited += 1

        except AttributeError as e:  # for content that is not a web page
            print(response.url, e)

    def create_PageGraph(self):

        # Clean up
        dangling_links = []
        for url in self.out_link_dictionary:
            if len(self.out_link_dictionary[url]) == 0:
                dangling_links.append(url)

        for url in self.out_link_dictionary:
            self.out_link_dictionary[url] = list(set(self.out_link_dictionary[url]) - set(dangling_links))

        for url in self.out_link_dictionary:
            if (len(self.out_link_dictionary[url]) > 0):
                if url in self.counts:
                    self.page_graph.add_page(url, self.counts[url], self.in_link_dictionary[url], len(self.out_link_dictionary[url]), self.out_link_dictionary[url])
                else:
                    self.page_graph.add_page(url, 0, list(), len(self.out_link_dictionary[url]), self.out_link_dictionary[url])

  
    def close(self, spider, reason):
        self.output_callback(self.page_graph)

####################################

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

####################################

def scrape_CPP(page_limit):
    global PAGE_LIMIT
    PAGE_LIMIT = page_limit
    page_graph = crawl_static(CPPScraper)
    return page_graph

def scrape_NFL(page_limit):
    global PAGE_LIMIT
    PAGE_LIMIT = page_limit
    page_graph = crawl_static(NFLScraper)
    return page_graph

# def main():

#     page_graph = pg.PageGraph()

#     scrape_cpp = input('Perform Scraping? (YES): ')
#     if scrape_cpp == 'YES':
#         global PAGE_LIMIT
#         PAGE_LIMIT = 15
#         page_graph = crawl_static(NFLScraper)
#         page_graph.display_keys()
        
#     else:
#         print('CPP Scraping skipped')


# if __name__ == '__main__':
#     main()
