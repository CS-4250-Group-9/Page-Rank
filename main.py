from crawlers import scrape_CPP, scrape_NFL
import page_graph as pg

graph_CPP = scrape_CPP(20)

graph_CPP.page_rank(50)

# itr = iter(graph_CPP)
# first_item = next(itr)

# for page in graph_CPP:
#     print(graph_CPP[page]['page_rank'])

sorted_ranks = graph_CPP.get_sorted_rankings()


with open('page_rankings_CPP.txt', 'w') as file:

    for i, url in enumerate(sorted_ranks):
        rank = graph_CPP[url]['page_rank']
        file.write(f"{rank}: {url}\n")
        if i >= 99:
            break

#########################################################

# graph_NFL = scrape_NFL(2000)

# graph_NFL.page_rank(50)

# # itr = iter(graph_NFL)
# # first_item = next(itr)

# # for page in graph_NFL:
# #     print(graph_NFL[page]['page_rank'])

# sorted_ranks = graph_NFL.get_sorted_rankings()


# with open('page_rankings_NFL.txt', 'w') as file:

#     for i, url in enumerate(sorted_ranks):
#         rank = graph_NFL[url]['page_rank']
#         file.write(f"{rank}: {url}\n")
#         if i >= 99:
#             break


