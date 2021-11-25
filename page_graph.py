'''
Primary Author: Eugene Mondkar
Page Rank method based on orginal page rank algorithm work by Miro Abdalian

'''

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

    def page_rank(self, num_of_iter=50):

        # Dangling links checked at the crawlers.py, refer to create_PageGraph() method
        
        # Set initial page ranks for all pages in graph: iteration 0

        N = len(self.data) # total number of nodes

        for page in self.data:
            self.data[page]['page_rank'] = 1 / N

        # Start iterative process of calculating page_ranks
        for iteration in range(num_of_iter):
            
            updated_rankings = {} # temporarily stores the updated intermediate page_ranks

            for page in self.data:

                updated_page_rank = self._page_rank_formula(page)
                updated_rankings[page] = updated_page_rank

            # Update all page ranks for current iteration
            for page in updated_rankings:
                self.data[page]['page_rank'] = updated_rankings[page]

    def get_sorted_rankings(self):

        # Sort according to page rank
        sorted_pages = sorted(self.data.keys(), key=lambda x: self.data[x]['page_rank'], reverse=True)
        return sorted_pages
        

    def _test_page_rank_formula(self, test_graph, current_page):
        result = 0
        in_links = test_graph[current_page]['in_links']
        for link in in_links:
            result += test_graph[link]['page_rank'] / test_graph[link]['num_out_links']
        return result

    def _test_page_rank(self, _iterations=3):
        test_graph = {  'A': {"num_in_links": 3, "in_links": ['B', 'D', 'C'], "num_out_links": 1, "out_links": ['B']}, 
                        'B': {"num_in_links": 2, "in_links": ['A', 'C'], "num_out_links": 2, "out_links": ['A', 'D']}, 
                        'C': {"num_in_links": 1, "in_links": ['D'], "num_out_links": 3, "out_links": ['A','D','B']}, 
                        'D': {"num_in_links": 2, "in_links": ['B', 'C'], "num_out_links": 2, "out_links": ['A', 'C']} 
                    }
        
        N = len(test_graph) # total number of nodes

        for page in test_graph:
            test_graph[page]['page_rank'] = 1 / N


        for iteration in range(_iterations):
            
            updated_rankings = {} # temporarily stores the updated intermediate page_ranks

            for page in test_graph:

                updated_page_rank = self._test_page_rank_formula(test_graph, page)
                updated_rankings[page] = updated_page_rank

            # Update all page ranks for current iteration
            for page in updated_rankings:
                test_graph[page]['page_rank'] = updated_rankings[page]

        test_sorted_list = sorted(test_graph.keys(), key=lambda x: test_graph[x]['page_rank'], reverse=True)

        sum = 0
        for i, url in enumerate(test_sorted_list):
            rank = test_graph[url]['page_rank']
            print(f"{rank}: {url}\n")
            sum += rank

        print(f'The total of the page ranks are: {sum}')


if __name__ == '__main__':
    pg = PageGraph()

    for iter in range(5):
        print(f'###### iteration: {iter} ###########')
        pg._test_page_rank(iter)
        print(f'###############################')
