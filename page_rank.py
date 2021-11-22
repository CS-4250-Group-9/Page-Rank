
from pandas import *
import numpy

def pageRank(url, number_link_out, outlinks, start_pageRank):
    pageRanklist = [0.0] * len(url)
    for link in url:
        for sublinks in outlinks:
            if "'" + link + "'" in sublinks:
                pageRanklist[url.index(link)] += start_pageRank[outlinks.index(sublinks)] / number_link_out[outlinks.index(sublinks)]
    return pageRanklist

number_link_in = []                                                    
number_link_out = []                            
# reading CSV file
data = read_csv("cpp.csv")
# converting column data to list
outlinks = data["out links"].tolist()
url = data['url'].tolist()

counter = 0
for i in range(0, len(outlinks)):
    if outlinks[i] == "[]":
        url.pop(i - counter)
        counter += 1

for i in outlinks:
    try:
        outlinks.remove("[]")
    except:
        pass

for i in range(0, len(outlinks)):   
    string = outlinks[i].replace(']', '').replace('[', '').replace("'", "").replace(' ', '').strip()
    li = []
    li = list(string.split(','))
    for link in li:
        if link not in url:
            li.remove(link)
    number_link_out.append(len(li))
    s = ""
    s += "["
    for k in li:
        s += "'"
        s += k
        s += "', "
    s = s[:-2] 
    s += "]"                     
    outlinks[i] = s
    li.clear() 

start_pageRank= [1.0 / len(url)] * len(url)
for i in range(1, 21): #5 iterations
    print(i, ")")
    print(start_pageRank)
    print("sum = ", sum(start_pageRank))
    start_pageRank = pageRank(url, number_link_out, outlinks, start_pageRank)

# print(start_pageRank)
# print('--------------')
# print(sum(start_pageRank))
# print('--------------')
max_value = numpy.argmax(start_pageRank)
print(url[max_value], " : ", start_pageRank[max_value])

    

