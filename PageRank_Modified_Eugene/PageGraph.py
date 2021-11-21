import sys
import copy
from collections import deque


class PageGraph:
    def __init__(self):
        self.size = 0
        self.pages = dict()

    def add_page(self, url, num_in_links, num_out_links, out_links):
        self.pages[url] = {"num_in_links": num_in_links, "num_out_links": num_out_links, "out_links": out_links}

    def convert_graph(self, page_graph):
        self.pages = copy.deepcopy(page_graph)