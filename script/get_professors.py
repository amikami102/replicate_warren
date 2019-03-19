"""

"""

import requests
import os
import re
from bs4 import BeautifulSoup
from google import google
import sys
import argparse
import logging
import json
sys.path.append("Users/asako/Google Drive/replicate_warren/script")



# set argument parser
parser = argparse.ArgumentParser(description='Get junior faculty for each school.')
parser.add_argument("-outdir", type = str,
                    help = "Directory to store output of this file.",
                    default = "data")
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

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"



        



# try with stanford

        
    
    
    
    
    

# get CV of each junior faculty
list_cv = []
#for name in list_asst:
#    print("Result for {}".format(name))
#    query = "{} cv".format(name)
#    num_page = 1
#    search_results = google.search(query, num_page)
#    for result in search_results[:5]:
#        print(result.link)
list_cv = ["https://stanford.edu/~avidit/cv.pdf",
           "https://scholar.princeton.edu/sites/default/files/mebooth/files/chapman_cv_2014_08_10_0.pdf",
           "https://vfouka.people.stanford.edu/sites/g/files/sbiybj4871/f/june2018.pdf",
           "https://uc9887292edfe511a02d84c2332f.dl.dropboxusercontent.com/cd/0/inline2/AcZvg5aFbdBsWYCIgtBPF7sAnVpSEpPxdaFofA3zMIJrFJIAfe_OwkLfwBdSexY9c3oKQ6IQirwfL_wwwBgHW4pUNDbXmgIWObtGKIF2nrrdDDnSkWiDHqYwV0B_x21Kq3dLiTHzhihYpPoZ5YSAtz3R0a1vYA2WLZKD5PqlZtl63mET7Ucm9oJk5dSwFPKIe8efJLzR9E8IvkExm5E0NiXnv_qMlmGkZ-xuikXq_xhsTULMEcZO2NJ2Tq2tohwKUNWDdu-fOMJChtMQH62i23YaW-NrLRIbE68jU8BWSETfdV5ZSexwE54J99NqCV5WRT3MYIicYciDIzAHXJgTGFO_Q6SKwvpMcLprxUWAeQbKLQ/file#",
           "https://drive.google.com/open?id=1y-CYB-BRW2_Jgv3qBBgncunTk2ttN9Gx",
           "https://kljusko.people.stanford.edu/sites/g/files/sbiybj3501/f/jusko_cv_4.pdf",
           "http://www.lipscy.org/webresume.pdf",
           "https://cap.stanford.edu/profiles/viewCV?facultyId=58191&name=Alison_McQueen",
           "http://www.nallresearch.com/uploads/7/9/1/7/7917910/nall-cv.pdf"
        ]



faculty = dict(zip(list_asst, list_cv))


# download pdf and save meta information in json
def download_cv(professor, url):
    """
    professor (str, name of the professor)
    url (str, url of the professor's CV)
    """
    r = requests.get(url) 
    filename = professor.replace(" ", "").replace(".", "")
    
    # save meta information in json
    with open(os.path.join(args.outdir, "cv", filename + ".json"), "w") as j:
        dict_ = {"date": r.headers["Date"],
             "type": r.headers['Content-Type'], 
             "url": url}
        json.dump(dict_, j)
    
    # download file to pdf 
    if "pdf" in r.headers['Content-Type'].lower():
        with open(os.path.join(args.outdir, "cv", filename + ".pdf"), "wb") as f:
            f.write(r.content)
            log.info("PDF saved for {}".format(professor))
    # if not downloadable, write message
    if "text" in r.headers['Content-Type'].lower():
        log.info("Cannot download cv for {}".format(professor))
        return url 





if __name__ == "__main__":
    for professor, url in faculty.items():
        download_cv(professor, url)
    
    sys.exit()