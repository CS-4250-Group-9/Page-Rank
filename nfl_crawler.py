from collections import Counter
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
import re

PAGE_LIMIT = 100


class NFLScraper(CrawlSpider):
    name = 'nfl'
    start_urls = ['https://www.nfl.com/']
    counts = Counter()
    pages_visited = 0
    printed = False

    # deny both /fantasy and /fantasyfootball, both link to fantasy.nfl.com
    link_extractor = LinkExtractor(allow=r'^https://www.nfl.com/.*', deny=r'^https://www.nfl.com/fantasy(football)?')

    rules = [Rule(link_extractor, callback='parse', follow=True)]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        logging.getLogger('scrapy').setLevel(logging.WARNING)  # comment out to debug, uncomment to turn off

    def parse(self, response, **kwargs):
        if self.pages_visited >= PAGE_LIMIT:
            if not self.printed:
                for k, v in self.counts.most_common():
                    print(v, k)
                self.printed = True
            raise CloseSpider()
        for link in response.css('a').xpath('@href').extract():
            if re.match(r'(^https://www.nfl.com)?/teams/.*', link) and not re.match('https://www.nfl.com/teams/', link):
                if re.match(r'^(https://www.nfl.com)?/teams/.*/.*', link):
                    link = re.search(r'^(https://www.nfl.com)?/teams/.*/', link).group(0)
                    link = link.replace('-', '')
                    if link in self.counts:
                        self.counts[link] += 1
                    else:
                        self.counts[link] = 1
        self.pages_visited += 1


def main():
    process = CrawlerProcess()
    process.crawl(NFLScraper)
    process.start()


if __name__ == '__main__':
    main()
