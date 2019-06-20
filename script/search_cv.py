"""
Look up junior faculty's resumes online, save the 
pdf or html file, and parse them.
"""


import os
from googlesearch import search
import sys
import argparse
import logging
import json
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time


# set argument parser
parser = argparse.ArgumentParser(description=
                                 'Download and parse CVs.')
parser.add_argument("-namesdir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data/faculty_names")
parser.add_argument("-cvdir", type = str,
                    help = "Directry to store CV's.",
                    default = "data/faculty_CV")
parser.add_argument("-school", type = str, help = "Name of school.")
parser.add_argument("-v", "--verbose", 
                    help = "Set logging level to DEBUG.",
                    action = "store_true")
args = parser.parse_args()



# set logging
logging.basicConfig(filename = "data/faculty_CV/search_cv.log",
                            filemode='a',
                            format='%(asctime)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
logging.info("Google searching CV's")
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
if args.verbose:
    log.setLevel(logging.DEBUG)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s %(message)s]"))
log.addHandler(loghandler)






"""STEP 0: Google search CV and open each search result in web browser"""

#filename = "STANFORD_UNIVERSITY.json"
#with open(os.path.join(args.namesdir, filename), "r") as j:
#    names = json.load(j)

def search_cv(name, school):
    """
    name (str, name of the faculty)
    """
    result = []
    query = name + " CV"  + " pdf"
    for r in search(query, tld = "com", num = 5, stop = 1, pause = 2):
        if re.search(".pdf$", str(r)):
            result.append(str(r))
        elif re.search(".pdf?dl=0$", str(r)):
            raw_url = str(r)
            new_url = raw_url.replace(".pdf?dl=0$", ".pdf$")
            result.append(new_url)
        elif re.search("drive.google.com", str(r)):
            result.append(str(r))
    return result


"""STEP 1: download CV"""

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
        
        elif url.endswith(".html"):
            with open(os.path.join(args.cvdir, filename + ".html"), "w") as h:
                h.write(r.text)
        else:
            with open(os.path.join(args.cvdr, filename), "wb") as g:
                g.write(r.content)
        log.info("CV accessed for {}".format(name))



if __name__ == "__main__":
    
    (_, _, filenames) = next(os.walk(args.namesdir))
    filenames.remove('.DS_Store')
    
    
    
    for file in filenames:
        args.school = file.replace('.json', '')
        with open(os.path.join(args.namesdir, file), "r") as f:
            names = json.load(f)
        for name in names:
            if re.search('people', name, re.IGNORECASE):
                continue
            else:
                urls = search_cv(name, args.school)
                log.info("{}, {}:\n {}".format(name, args.school, urls))
                options = webdriver.FirefoxOptions()
                options.add_argument("disable-infobars")
                options.add_argument("--disable-notifications")
                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.tabs.remote.autostart",
                                       False)
                profile.set_preference("browser.tabs.remote.autostart.1",
                                       False)
                profile.set_preference("browser.tabs.remote.autostart.2",
                                       False)
                browser = webdriver.Firefox(options = options, 
                                            firefox_profile = profile)
                for u in urls:
                    browser.get(u)
                    time.sleep(2)
                    elem = browser.find_element_by_tag_name('body')
                    elem.send_keys(Keys.COMMAND + "t")
                    windows = browser.window_handles
                    browser.switch_to.window(windows[1])
                    time.sleep(2)
            cv_url = input("Enter the url or press F: ")
            if cv_url == 'f':
                continue
            else:
                try:
                    download_cv(name, cv_url)
                except requests.exceptions.HTTPError:
                    log.warning("HTTP error at {}".format(cv_url))
            browser.quit()
            
            
    sys.exit()
    