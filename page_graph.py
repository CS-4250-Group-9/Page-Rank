from collections import deque
from collections import UserDict

class PageGraph(UserDict):

    def add_page(self, url, num_in_links, in_links, num_out_links, out_links):
        self.data[url] = {"num_in_links": num_in_links,"in_links": in_links, "num_out_links": num_out_links, "out_links": out_links}

    def _page_rank_formula(self, current_page):
        result = 0
        in_links = self.data[current_page]['in_links']
        for link in in_links:
            result += self.data[link]['page_rank'] / self.data[link]['num_out_links']
        return result


    def page_rank(self):
        
        # Set initial page ranks for all pages in graph: iteration 0

        N = len(self.data) # total number of nodes

        for page in self.data:
            self[page]['page_rank'] = 1 / N

        # Start iterative process of calculating page_ranks

        


        
