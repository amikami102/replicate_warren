#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
For each school in the `top25` list from find_programs.py,
find faculty members who are assistant professors or newly
appointed associate professors. Save the list of names to 
json file. 
"""
import sys
import requests
import argparse
import logging
import os
from bs4 import BeautifulSoup, SoupStrainer, NavigableString
import re
import json




# set argument parser
parser = argparse.ArgumentParser(description='Get junior faculty for each school.')
parser.add_argument("-pagedir", type = str,
                    help = "Directory storing input files.",
                    default = "data/faculty_page")
parser.add_argument("-parsedir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data/faculty_names")
parser.add_argument("-school", type = str,
                    help = "Name of the school.")
parser.add_argument("-v", "--verbose", 
                    help = "Set logging level to DEBUG.",
                    action = "store_true")
args = parser.parse_args()


# set logging
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
if args.verbose:
    log.setLevel(logging.DEBUG)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(loghandler)


""" STEP 0 """

def get_html(school, url, count = 0):
    """
    Open the faculty page of polisci/govt department and
    save the html content and the request headers. 
    --------
    school (str, name of the school)
    url (str, url to the faculty page)
    count (int, page count, default is 0)
    """

    r = requests.get(url)
    log.info("Server response for {}: {}".format(school, r.status_code))
    filename = "{}_faculty_page".format(school.replace(" ", "_"))
    
    # save html content to file
    with open(os.path.join(args.pagedir, filename + str(count) + ".html"), "w") as h:
        h.write(r.text)
        
    # save HTTP requests header to file
    with open(os.path.join(args.pagedir, filename + str(count) + ".json"), "w") as t:
        try:
            header = {"date": r.headers['date'],
                 "content-type": r.headers['content-type'],
                 "last modified": r.headers['last-modified']}
        except KeyError:
            header = {"date": None, 
                      "content-type": None,
                      "last-modified" : None}
        json.dump(header, t)
    
    return r.text


"""
STEP 1: Parse html files
"""


# title pattern
title_pattern = re.compile("Assistant\s(?=Professor)|(?<!Adjunct)\sAssociate\s(?=Professor)|Assistant\s(?=Teaching\sProfessor)")



# harvard university, princeton university

def parse_school0(html, count = 0):
    """
    Parse the html of the faculty page html returned from 
    get_faculty_page.py and create a roster of junior faculty
    members (assistant and associates). Must check whether there's a 
    next page. 
    --------
    html_file (name of the html file to parse)
    """

    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    
    # get the names of associate/assistant professors
    list_ = []
    for string in soup.find_all(string = title_pattern):
        h = string.find_previous(re.compile("^h"))
        for string in h.stripped_strings:
            list_.append(string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    filename = args.school.replace(" ", "_") + str(count) + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)
    
    
    # check if there's a next page
    if args.school == 'HARVARD UNIVERSITY':
        li = soup.find("ul", {"class": "pager"}).find("li", {"class": "pager-next"})
        if li.find("a", href = True) != None:
            href = li.find("a", href = True)["href"]
            log.info("Next url for HARVARD is {}".format(href))
            return href
        else:
            log.info("Reached last page")
            return None
    if args.school == 'PRINCETON UNIVERSITY':
        if soup.find("li", {"class": "pager__item pager__item--next"}):
            li = soup.find("li", {"class": "pager__item pager__item--next"})
            href = url + li.find("a", href = True)["href"]
            log.info("Next url for PRINCETON is {}".format(href))
            return href
        else:
            log.info("Reached last page")
            return None
        

# stanford university, mit, columbia university, penn state u, 
# u washington, wisconsin-madison
        
def parse_school1(html):
    """
    Similar to get_juniof_faculty(html_file) but does not have
    multiple pages to parse.
    -----
    html_file (str, name of the html file to parse)
    """
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = []
    for string in soup.find_all(string = title_pattern):
        if string.find_previous(re.compile("^h")).find(re.compile("a|span")):
            h = string.find_previous(re.compile("^h"))
            list_.append(h.string)
        else:
            h = string.find_previous(re.compile("^h"))
            list_.append(h.string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)


# university of north carolina, texas a & m

def parse_school2(html):
    """
    Obtains a list of junior faculty members for faculty pages
    with a table. 
    ------
    html_file (str, name of the html file to parse)
    """
    
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all(string = title_pattern):
        tr = string.find_parent("tr")
        if "NORTH CAROLINA" in args.school:
            td = tr.find_all("td")[1]
            list_.append(td.string)
        if "TEXAS A & M" in args.school:
            td = tr.find_all("td")[2]
            if td.find("a").string != None:
                list_.append(td.find("a").string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)
    

# duke university, nyu, ucsd, chicago, illinois, vanderbilt,
# washington u in st. louis
    
def parse_school3(html):
    """
    html_file (str, name of the html file to parse)
    """
    
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = []
    for string in soup.find_all(string = title_pattern):
        a = string.find_previous("a")
        list_.append(a.string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)


# uc berkeley, yale
def parse_school4(html, count):
    """
    Faculty members are presented in a table, but must check
    for the next page.
    ------
    html_file (str, name of the html file to parse)
    """
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all(string = title_pattern):
        if "BERKELEY" in args.school:
            tr = string.find_parent("tr")
            td = tr.find_all("td")[0]
            list_.append(td.find("a").string)
        if "YALE" in args.school:
            list_.append(string.find_previous("a").string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file 
    filename = args.school.replace(" ", "_") + str(count) + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)
        
    # check if there's next page
    if soup.find("li", {"class": "pager-next"}):
        li = soup.find("li", {"class": "pager-next"})
        href = url + li.find("a", href = True)['href']
        log.info("Next url is {}".format(href))
        return href 
    else:
        log.info("Reached last page")
        return None


# emory university
def parse_emory(html):
    """
    Need to open individual faculty's profile to see
    position title.
    -------------
    html_file (str, name of the html file to parse)
    """
    
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    list_ = []
    div = soup.find("div", {"class": "data-entry"})
    for h3 in div.find_all("h3"):
        href = h3.find("a")["href"]
        base_url = "http://polisci.emory.edu/home/people/faculty/"
        url = base_url + href
        profile = BeautifulSoup(requests.get(url).content, "lxml",
                                parse_only = SoupStrainer("body"))
        title = profile.find("h4", {"itemprop" :"jobTitle"}).string
        if title_pattern.search(title) != None:
            list_.append(h3.find("a").string)
    log.info("Junior faculty: \n {}".format(list_))
        
    # save to file
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)


# indiana university at bloomington
def parse_indiana(html):
    """
    html_file (str, name of the html file to parse)
    """
    
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("main"))
    
    list_ = []
    for string in soup.find_all(string = title_pattern):
        name = string.find_previous(["h1", "a"]).string
        list_.append(name)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)





# ucla
def parse_ucla(html):
    """
    html_file (str, name of the html file to parse)
    """
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all("h2", string = title_pattern):
        list_.append(string.find_previous("h1", string = True).string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file 
    filename = args.school.replace(" ", "_") + ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)
        
        
# rochester
def parse_rochester(html):
    """
    html_file (str, name of the html file to parse)
    """
    soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("table", {"class": "people-table"}))
    
    list_ = []
    for a in soup.find_all("a", {"href": re.compile("people")}):
        href = a['href']
        base_url = "https://www.sas.rochester.edu"
        url = base_url + href
        profile = BeautifulSoup(requests.get(url).content, "lxml", parse_only = SoupStrainer("div", {"id": "content"}))
        title = list(profile.find("p", {"class": "faculty-profile-information-title"}).children)[0]
        if (isinstance(title, NavigableString)) and (title_pattern.search(title) != None):
            list_.append(a.string)
    log.info("Junior faculty: \n {}".format(list_))
     
     
    # save to file 
    filename = args.school.replace(" ", "_") +  ".json"
    with open(os.path.join(args.parsedir, filename), "w") as j:
        json.dump(list_, j)



if __name__ == "__main__":
    
    gp0 = ['HARVARD UNIVERSITY', 'PRINCETON UNIVERSITY']
    gp1 = ['UNIVERSITY OF WISCONSIN-MADISON',
           'STANFORD UNIVERSITY', 'MASSACHUSETTS INSTITUTE OF TECHNOLOGY',
           'COLUMBIA UNIVERSITY IN THE CITY OF NEW YORK',
           'PENN STATE UNIVERSITY', 'UNIVERSITY OF WASHINGTON']
    gp2 = ['TEXAS A & M UNIVERSITY',
           'UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL']
    gp3 = ['DUKE UNIVERSITY', 'NEW YORK UNIVERSITY', 
           'UNIVERSITY OF CALIFORNIA-SAN DIEGO', 
           'UNIVERSITY OF CHICAGO', 
           'UNIVERSITY OF ILLINOIS AT URBANA-CHAMPAIGN',
           'VANDERBILT UNIVERSITY', 'WASHINGTON UNIVERSITY IN ST. LOUIS']
    gp4 = ['UNIVERSITY OF CALIFORNIA-BERKELEY',
           'YALE UNIVERSITY']
    
    gp_ = ['UNIVERSITY OF CALIFORNIA-DAVIS', 
           'UNIVERSITY OF MICHIGAN-ANN ARBOR']
    
    with open("data/faculty_page_links.json") as j:
        dict_ = json.load(j)
    
    for school, url in dict_.items():
        args.school = school
        c = 0
        html = get_html(args.school, url, c)
        if args.school in gp0:
            next_url = parse_school0(html, c)
            while next_url != None:
                c += 1
                html = get_html(args.school, next_url, c)
                next_url = parse_school0(html, c)
        if args.school in gp1:
            parse_school1(html)
        if args.school in gp2:
            parse_school2(html)
        if args.school in gp3:
            parse_school3(html)
        if args.school in gp4:
            next_url = parse_school4(html, c)
            while next_url != None:
                c += 1
                html = get_html(school, next_url, c)
                next_url = parse_school4(html, c)
        if args.school in gp_:
            log.info("Unable to parse html")
        if "EMORY" in args.school:
            parse_emory(html)
        if "LOS ANGELES" in args.school:
            parse_ucla(html)
        if "ROCHESTER" in args.school:
            parse_rochester(html)
    
    sys.exit()
    

    
    
    
    
    
    
    
