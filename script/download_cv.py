#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""
import sys
import argparse
import logging
import requests
import re
import json
import os


# set argument parser
parser = argparse.ArgumentParser(description='Download CV.')
parser.add_argument("-cvdir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data/faculty_cv")
parser.add_argument("-namesdir", type = str,
                    help = "Directory storing faculty roster.",
                    default = "data/faculty_names")
parser.add_argument("-v", "--verbose", 
                    help = "Set logging level to DEBUG",
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


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"






# download pdf and save meta information in json
def download_cv(name, url):
    """
    name (str, name of the junior faculty)
    url (str, url of the professor's CV)
    """
    r = requests.get(url, headers={
            'Accept': 'text/html; charset=iso-8859-1',
            'User-Agent': user_agent}) 
    filename = name.replace(" ", "").replace(".", "")
    
    # save meta information in json
    with open(os.path.join(args.cvdir, filename + ".json"), "w") as j:
        json.dump(dict(r.headers), j)
    if r.status_code != 200:
        r.raise_for_status()
    else:
        if url.endswith(".pdf"):
            with open(os.path.join(args.cvdir, filename + ".pdf"), "wb") as f:
                f.write(r.content)
        # if not downloadable, write message
        if url.endswith(".html"):
            with open(os.path.join(args.cvdir, filename + ".html"), "w") as h:
                h.write(r.text)
        log.info("CV accessed for {}".format(name))
    


if __name__ == "__main__":
    
    files = [file for file in os.listdir(args.namesdir) if file.endswith(".json")]
    for file in files:
        with open(os.path.join(args.namesdir, file), "r") as f:
            names = json.load(f)
        for name in names:
            if re.search("people", name, re.IGNORECASE):
                continue
            else:
                input_url = str(input("Enter url for {}. If none, enter 'none': ".format(name)))
                if input_url != 'none':
                    download_cv(name, input_url)
                else:
                    log.info("Unable to find stand alone CV")
    sys.exit()