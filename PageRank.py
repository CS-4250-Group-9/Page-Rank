
from pandas import *
import numpy

def pageRank(url, numOfLinksFromUrl, outlinks, pageRankStartList):
    pageRanklist = [0.0] * len(url)
    for i in range(0, len(url)):
        for j in range(0, len(url)):
            if url[i] in outlinks[j]:
                pageRanklist[i] += (pageRankStartList[j] / numOfLinksFromUrl[j])  # this line makes sure we have N links for each node 
    return pageRanklist                                                           # also we can change our design to check these conditions only ones
                                                                                  # since  they are the same for all iterations
# reading CSV file
data = read_csv("cpp.csv")
 
# converting column data to list
outlinks = data["out links"].tolist()
url = data['url'].tolist()
numOfLinksFromUrl = data['# links from url'].tolist()

# 50 iterations
pr = [1.0 / len(url)] * len(url)
for i in range(0, 51):
    pr = pageRank(url, numOfLinksFromUrl, outlinks, pr)

max_value = numpy.argmax(pr)
print(url[max_value], " : ", pr[max_value])



    
