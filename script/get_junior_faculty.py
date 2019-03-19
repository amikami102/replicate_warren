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
sys.path.append(os.path.join(os.getcwd(), "script"))
from get_faculty_page import get_faculty_html



# set argument parser
parser = argparse.ArgumentParser(description='Get junior faculty for each school.')
parser.add_argument("-indir", type = str,
                    help = "Directory storing input files.",
                    default = "data/faculty_page")
parser.add_argument("-outdir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data/faculty_dir")
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
loghandler.setFormatter(logging.Formatter("[%(asctime)s %(message)s]"))
log.addHandler(loghandler)


# title pattern
title_pattern = re.compile("Assistant\s(?=Professor)|Associate\s(?=Professor)|Assistant\s(?=Teaching\sProfessor)")



# harvard university, princeton university

def get_jr_faculty0(html_file):
    """
    Parse the html of the faculty page html returned from 
    get_faculty_page.py and create a roster of junior faculty
    members (assistant and associates). Must check whether there's a 
    next page. 
    --------
    html_file (name of the html file to parse)
    """

    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
    
    # get the names of associate/assistant professors
    list_ = []
    for string in soup.find_all(string = title_pattern):
        h = string.find_previous(re.compile("^h"))
        for string in h.stripped_strings:
            list_.append(string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)
    
    
    # check if there's a next page
    if "HARVARD" in html_file:
        li = soup.find("ul", {"class": "pager"}).find("li", {"class": "pager-next"})
        if li.find("a", href = True) != None:
            href = li.find("a", href = True)["href"]
            log.info("Next url for HARVARD is {}".format(href))
            return href
        else:
            log.info("Reached last page")
    if "PRINCETON" in html_file:
        if soup.find("li", {"class": "pager__item pager__item--next"}):
            li = soup.find("li", {"class": "pager__item pager__item--next"})
            href = li.find("a", href = True)["href"]
            log.info("Next url for PRINCETON is {}".format(href))
            return href
        else:
            log.info("Reached last page")
        

# stanford university, mit, columbia university, penn state u, 
# u washington, wisconsin-madison
        
def get_jr_faculty1(html_file):
    """
    Similar to get_juniof_faculty(html_file) but does not have
    multiple pages to parse.
    -----
    html_file (str, name of the html file to parse)
    """
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
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
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)


# university of north carolina, texas a & m

def get_jr_faculty2(html_file):
    """
    Obtains a list of junior faculty members for faculty pages
    with a table. 
    ------
    html_file (str, name of the html file to parse)
    """
    
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all(string = title_pattern):
        tr = string.find_parent("tr")
        if "NORTH CAROLINA" in html_file:
            td = tr.find_all("td")[1]
            list_.append(td.string)
        if "TEXAS A & M" in html_file:
            td = tr.find_all("td")[2]
            if td.find("a").string != None:
                list_.append(td.find("a").string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)
    

# duke university, nyu, ucsd, chicago, illinois, vanderbilt,
# washington u in st. louis
    
def get_jr_faculty3(html_file):
    """
    html_file (str, name of the html file to parse)
    """
    
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = []
    for string in soup.find_all(string = title_pattern):
        a = string.find_previous("a")
        list_.append(a.string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)


# uc berkeley, yale
def get_jr_faculty4(html_file):
    """
    Faculty members are presented in a table, but must check
    for the next page.
    ------
    html_file (str, name of the html file to parse)
    """
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all(string = title_pattern):
        if "BERKELEY" in html_file:
            tr = string.find_parent("tr")
            td = tr.find_all("td")[0]
            list_.append(td.find("a").string)
        if "YALE" in html_file:
            list_.append(string.find_previous("a").string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file 
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)
        
    # check if there's next page
    if soup.find("li", {"class": "pager-next"}):
        li = soup.find("li", {"class": "pager-next"})
        href = li.find("a", href = True)['href']
        log.info("Next url is {}".format(href))
        return href 
    else:
        log.info("Reached last page")

# emory university
def get_emory(html_file = 'EMORY UNIVERSITY_faculty_page.html'):
    """
    Need to open individual faculty's profile to see
    position title.
    -------------
    html_file (str, name of the html file to parse)
    """
    
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
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
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)


# indiana university at bloomington
def get_indiana(html_file = 'INDIANA UNIVERSITY AT BLOOMINGTON_faculty_page.html'):
    """
    html_file (str, name of the html file to parse)
    """
    
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("main"))
    
    list_ = []
    for string in soup.find_all(string = title_pattern):
        name = string.find_previous(["h1", "a"]).string
        list_.append(name)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)





# ucla
def get_ucla(html_file = 'UNIVERSITY OF CALIFORNIA-LOS ANGELES'):
    """
    html_file (str, name of the html file to parse)
    """
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("body"))
    
    # get the names of associate/assistant professors
    list_ = [] 
    for string in soup.find_all("h2", string = title_pattern):
        list_.append(string.find_previous("h1", string = True).string)
    log.info("Junior faculty: \n {}".format(list_))
    
    # save to file 
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)
        
        
# rochester
def get_rochester(html_file = "UNIVERSITY OF ROCHESTER_faculty_page.html"):
    """
    html_file (str, name of the html file to parse)
    """
    with open(os.path.join(args.indir, html_file), "r") as h:
        soup = BeautifulSoup(h, "lxml", parse_only = SoupStrainer("table", {"class": "people-table"}))
    
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
    with open(os.path.join(args.outdir, args.school + ".json")) as j:
        json.dump(list_, j)



if __name__ == "__main__":
    
    html_list = [name for name in os.listdir(args.indir) if name.endswith("html")]
    
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
    
    
    for html in html_list:
        args.school = re.sub("_faculty_page.html", "", html)
        log.info("Parsing {}".foramt(args.school))
        if args.school in gp1:
            get_jr_faculty1(html)
        if args.school in gp2:
            get_jr_faculty2(html)
        if args.school in gp3:
            get_jr_faculty3(html)
        if args.school in gp_:
            log.info("Cannot parse html")
        if "EMORY" in args.school:
            get_emory(html)
        if "INDIANA" in args.school:
            get_indiana(html)
        if "LOS ANGELES" in args.school:
            get_ucla(html)
        if "ROCHESTER" in args.school:
            get_rochester(html)
    sys.exit()
    
    
    
    
    
    
    
    
    
    
    