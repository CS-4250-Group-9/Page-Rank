from crawlers import scrape_CPP, scrape_NFL
import page_graph as pg


#########################################################
#
# Instructions:
# 
# Uncomment one of the scrapers (CPP or NFL) below and
# and run. 
# 
# Note: 
# Both Scrapers cannot be run at the same time.
#
#########################################################

######  CPP Scraper #####################################

# graph_CPP = scrape_CPP(1000)

# graph_CPP.page_rank(50)

# sorted_ranks = graph_CPP.get_sorted_rankings()

# # Validate the Page Rank Total is equal to 1

# with open('page_rankings_CPP.txt', 'w') as file:

#     sum = 0

#     for i, url in enumerate(sorted_ranks):
#         rank = graph_CPP[url]['page_rank']
#         sum += rank
#         if i <= 99:
#             file.write(f"{rank}: {url}\n")
        
#     print(f'The total of the page ranks are: {sum}')      

###### End of CPP Scraper ###############################

######  NFL Scraper #####################################

graph_NFL = scrape_NFL(1000)

graph_NFL.page_rank(50)

sorted_ranks = graph_NFL.get_sorted_rankings()

# Validate the Page Rank Total is equal to 1

with open('page_rankings_NFL.txt', 'w') as file:

    sum = 0

    for i, url in enumerate(sorted_ranks):
        rank = graph_NFL[url]['page_rank']
        sum += rank
        if i <= 99:
            file.write(f"{rank}: {url}\n")
        
    print(f'The total of the page ranks are: {sum}')   

###### End of NFL Scraper ###############################

