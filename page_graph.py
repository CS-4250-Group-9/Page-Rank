from collections import deque
from collections import UserDict

class PageGraph(UserDict):

    def add_page(self, url, num_in_links, in_links, num_out_links, out_links):
        self.data[url] = {"num_in_links": num_in_links,"in_links": in_links, "num_out_links": num_out_links, "out_links": out_links}

# Based of Miro's page rank implementation

