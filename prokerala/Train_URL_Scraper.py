from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import OrderedDict
import pandas as pd

'''
Breaks down a url to the children elements we want
'''
def url_to_children(url, element, name):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    page_children = page_soup.find_all(element, name)
    return page_children

'''
Gets the train id's and sorts them
'''
def train_data(train_page_children):
    trains = []
    # Check through each table
    for train_page_child in train_page_children:
        td_children = train_page_child.findChildren("td", recursive=True)
        
        # Start at the second index for the train_no
        i = 1
        while i < len(td_children):
            id = td_children[i].get_text()
            # Check we are not looking at the column names
            if id.isnumeric():
                id = int(id)
                # Store train_no and train_url
                if (12000 <= id < 13000) or (22000 <= id < 23000):
                    url = "https://www.prokerala.com" + td_children[i+1].find("a")["href"]
                    trains.append( {"Train_No": id, "Train_URL": url} )
            # Go to the next train
            i += 5
    
    # Sort based on train_no, then return the values/url
    return trains

if __name__ == '__main__':
    print("Accessing website...")
    train_page_url = "https://www.prokerala.com/travel/indian-railway/trains/#tourist-trains"
    
    print("\tgrabbing data...")
    train_page_children = url_to_children(train_page_url, "table", {"class": "table t-xsmall table-striped"})
    trains = train_data(train_page_children)
    print("\tdata grabbed successfully")        
        
    df = pd.DataFrame(trains)
    df.to_csv("Train_URL.csv", index=False)
    print("\tdata transferred to file")