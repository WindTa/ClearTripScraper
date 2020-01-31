from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import re

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

if __name__ == '__main__':
    # Initialize dataframe with column names to convert to csv later
    df = pd.DataFrame(columns = ["Station No.", "Station Code", "Station Name", 
                                 "Station State", "Arrival Time", "Departure Time",
                                 "Distance", "Day of Arrival", "Train No."])
    
    # Get list of trains
    trains = pd.read_csv("Train_URL.csv", dtype={"Train_No": "str", "Train_URL": "str"})
        
    # Iterate through each train
    for train in trains.values:
        
        # Get train's url and request access
        url = train[1]
        request = requests.get(url)
        print(url)
        
        # Error checks
        if url != request.url:
            print("\tPage redirected. Going to the next train.")
            continue
        if request.status_code == 404:
            print("\t404 error. Going to the next train.")
            continue
        if len(url_to_children(url, "div", {"class": "alert alert-block alert-danger"})) > 0:
            print("\tTrain discontinued. Going to the next train.")
            continue
        
        # Successfully accessed web page. Pull data
        print("\tSuccessful. Pulling data.")
        tables = url_to_children(url, "table", {"class": "table-station-list table table-striped t-xsmall"})
        
        # Get list of tr elements
        for table in tables:
            rows = table.findChildren("tr", recursive=True)
            
            # Get list of td elements
            iterrows = iter(rows)
            next(iterrows)
            for row in iterrows:
                row = row.findChildren("td", recursive=True)
                station_no = str.strip(re.sub("[^0-9]", "", row[0].get_text()))
                station_code = str.strip(row[1].get_text())
                station_name = str.strip(row[2].get_text())
                station_state = str.strip(row[3].get_text())
                arrival_time = str.strip(row[4].get_text())
                departure_time = str.strip(row[5].get_text())
                distance = str.strip(row[7].get_text())
                day_of_arrival = str.strip(row[8].get_text())
                train_no = train[0]
                
                # Add data to dataframe and save to csv
                df = df.append({"Station No.": station_no, "Station Code": station_code, 
                        "Station Name":station_name, "Station State": station_state, 
                        "Arrival Time": arrival_time, "Departure Time": departure_time,
                        "Distance": distance, "Day of Arrival": day_of_arrival, 
                        "Train No.": train_no}, ignore_index=True)
        
    df.to_csv("Train_Data.csv", index=False)
    print("Data pull complete.")