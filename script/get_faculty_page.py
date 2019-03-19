#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open the faculty pages and save the html to file. 
"""
import sys
import argparse
import logging
import requests
import os
import json

# set argument parser
parser = argparse.ArgumentParser(
        description='Get the html of faculty page for each school.'
        )
parser.add_argument("-outdir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data/faculty_page")
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




# load the json file containing faculty page links
def get_faculty_html(school, url, count = 0):
    """
    Open the faculty page of polisci/govt department and
    save the html content and request headers to files.
    --------
    school (str, name of the school)
    url (str, url to the faculty page)
    """

    r = requests.get(url)
    log.info("Server response for {}: {}".format(school, r.status_code))
    filename = "{}_faculty_page".format(school)
    
    # save html content to file
    with open(os.path.join(args.outdir, filename + str(count) + ".html"), "w") as h:
        h.write(r.text)
    # save HTTP requests header to file
    with open(os.path.join(args.outdir, filename + str(count) + ".json"), "w") as t:
        try:
            header = {"date": r.headers['date'],
                 "content-type": r.headers['content-type'],
                 "last modified": r.headers['last-modified']}
        except KeyError:
            header = {"date": None, 
                      "content-type": None,
                      "last-modified" : None}
        json.dump(header, t)
    
    # get next page for Harvard, Princeton, UC berkeley, Yale
    

if __name__ == "__main__":
    
    with open("data/faculty_page_links.json") as j:
        dict_ = json.load(j)
    
    for school, url in dict_.items():
        c = 0
        get_faculty_html(school, url[c], count = c)
    
    sys.exit()