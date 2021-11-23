from crawlers import scrape_CPP, scrape_NFL
import page_graph as pg

graph = scrape_CPP(10)

graph.page_rank(100)

# itr = iter(graph)
# first_item = next(itr)

for page in graph:
    print(graph[page]['page_rank'])



