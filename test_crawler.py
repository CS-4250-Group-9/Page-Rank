import httplib2
import time
import os
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer

def isAlreadyIncludedOrVisited(url, frontier, sites_visited):
    return ( url not in frontier ) and ( url not in sites_visited )

def linkExtraction(url, response, frontier, sites_visited):

    num_of_links_extracted = 0

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser'):
        
        if link.has_attr('href') and len(link['href']) > 1:
            
            if link['href'][0] == '/':
                
                if url[-1] == '/':
                    extracted_url = url + link['href'][1:]
                elif url[-1] != '/':
                    extracted_url = url + link['href']

                if isAlreadyIncludedOrVisited(extracted_url, frontier, sites_visited): # Avoiding duplicate links and redundancy
                    frontier.append(extracted_url)
                    num_of_links_extracted += 1

            elif link['href'][:4] == 'http':
                
                extracted_url = link['href']

                if isAlreadyIncludedOrVisited(extracted_url, frontier, sites_visited): 
                    frontier.append(extracted_url)
                    num_of_links_extracted += 1

    return num_of_links_extracted

def printFrontier(frontier):
    print('Stored Links:')
    for i, link in enumerate(frontier):
        print(i, link)

def saveHtmlFile(repository_path, response, status, current_html_number):
           
    directory_exists = os.path.isdir(repository_path)

    # Get Web Document Encoding
    encoding = status['content-type'][status['content-type'].lower().find('utf'):].lower()

    if status['content-type'] == 'text/html':
        encoding = 'utf-8'
    
    if directory_exists:

        html_file_name = "{:04d}".format(current_html_number) + "_html_file.html"
        full_path_name = repository_path + html_file_name
        html_file = open(full_path_name, 'w')
        
        try:

            html_file.write(response.decode(encoding))
            
        except:

            return False

        html_file.close()

    else:

        Path(repository_path).mkdir(parents=True, exist_ok=True)

        html_file_name = "{:04d}".format(current_html_number) + "_html_file.html"
        full_path_name = repository_path + html_file_name
        html_file = open(full_path_name, 'w')
        
        try:

            html_file.write(response.decode(encoding))
            
        except:

            return False

        html_file.close()

    return True   

def http_crawler(seed, crawl_limit, repository_path):
        
    frontier = []
    frontier.append(seed)

    visited_sites = []
    number_of_outlinks_per_site = []

    http_obj = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

    pages_crawled = 0

    current_html_file_number = 0
    
    while len(frontier) > 0 and pages_crawled < crawl_limit:
        
        url = frontier.pop(0)

        try:
            status, response = http_obj.request(url)
        except:
            status = {'status':'400'}


        if status['status'] == '200':

            if saveHtmlFile(repository_path, response, status, current_html_file_number):

                current_html_file_number += 1

                num_of_links_extracted = linkExtraction(url, response, frontier, visited_sites)
                pages_crawled += 1

                # Parallel lists for to maintain peformance of checking urls against visited sites
                visited_sites.append(url)
                number_of_outlinks_per_site.append(num_of_links_extracted)

        # Politiness Rule: 350 millisecond pause
        time.sleep(0.500)

    return list(zip(visited_sites, number_of_outlinks_per_site))