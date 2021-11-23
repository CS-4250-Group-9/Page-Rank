from crawlers import scrape_CPP, scrape_NFL
import page_graph as pg

# graph_cpp = scrape_CPP(100)

# graph_cpp.page_rank(50)

# # itr = iter(graph_cpp)
# # first_item = next(itr)

# # for page in graph_cpp:
# #     print(graph_cpp[page]['page_rank'])

# sorted_ranks = graph_cpp.get_sorted_rankings()


# with open('page_rankings_cpp.txt', 'w') as file:

#     for url in sorted_ranks:
#         rank = graph_cpp[url]['page_rank']
#         file.write(f"{rank}: {url}\n")

#########################################################

graph_NFL = scrape_NFL(100)

graph_NFL.page_rank(50)

# itr = iter(graph_NFL)
# first_item = next(itr)

# for page in graph_NFL:
#     print(graph_NFL[page]['page_rank'])

sorted_ranks = graph_NFL.get_sorted_rankings()


with open('page_rankings_NFL.txt', 'w') as file:

    for url in sorted_ranks:
        rank = graph_NFL[url]['page_rank']
        file.write(f"{rank}: {url}\n")

