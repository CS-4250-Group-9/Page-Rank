from test_crawlers import scrape_CPP, scrape_NFL
import page_graph as pg

graph = scrape_NFL(10)


for key, value in graph.items():
    print(key)
    print(value)



