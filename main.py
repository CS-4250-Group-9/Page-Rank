from crawlers import scrape_CPP, scrape_NFL
import page_graph as pg

graph_cpp = scrape_CPP(100)

graph_cpp.page_rank(50)

# itr = iter(graph_cpp)
# first_item = next(itr)

# for page in graph_cpp:
#     print(graph_cpp[page]['page_rank'])

sorted_ranks = graph_cpp.get_sorted_rankings()


with open('page_rankings.txt', 'w') as file:

    for url in sorted_ranks:
        rank = graph_cpp[url]['page_rank']
        file.write(f"{rank}: {url}\n")

