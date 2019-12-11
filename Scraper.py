from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import requests

'''
Breaks down a url to the children elements we want
'''
def url_to_children(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    page_children = page_soup.find("table", {"class": "results"}).findChildren("tr", recursive=True)
    return page_children

'''
Combines time and day
'''
def endpoint_check(time, day):
    if "Starts" in time:
        return "Source"
    elif "Ends" in time:
        return "Destination"
    else:
        return str.strip(time) + " (Day " + day + ")" 

if __name__ == '__main__':
    # Initialize dataframe with column names to convert to csv later
    file_name = "results" + input("What page is the the URL on? ") + ".csv"
    df = pd.DataFrame(columns = ['No.', 'Station Code', 'Station Name', 'Arrival', 'Departure', 'Distance', 'Train No.'])

    # First page: https://www.cleartrip.com/trains/list?field=number&sort=up
    
    # Takes the URL and breaks down to the children we expect
    train_page_URL = input("Enter the URL for a page of trains: ")
    train_page_children = url_to_children(train_page_URL)

    # Go through every train
    for train_child in train_page_children:
        train_id = train_child.find("td")
        # Accounts for empty elements in the document
        if train_id is not None:
            train_id = str.strip(train_id.get_text())
            print("Train ID: ", train_id)
            station_page_URL = "https://www.cleartrip.com/trains/" + train_id
            # Accounts for url that redirects to an unexpected page
            if station_page_URL != requests.get(station_page_URL).url:
                print("\tPage redirected. Going to next train.")
                continue
            print("\tTrain found. Going through stations.")
            # Takes the URL and breaks down to the children we expect
            station_page_children = url_to_children(station_page_URL)

            # Go through every station a train goes through and saves all the data to a dictionary
            for station_child in station_page_children:
                station_values = station_child.findChildren("td", recursive=False)
                # Accounts for empty elements in the document
                if len(station_values) != 0:
                    # Creates all values to add to dictionary
                    station_no = str.strip(station_values[0].get_text())
                    station_name, station_code = [" ".join(x.split()) for x in re.split(r'[()]', station_values[1].get_text()) if x.strip()]
                    station_arrive = endpoint_check(station_values[2].get_text(), station_values[6].get_text())
                    station_depart = endpoint_check(station_values[3].get_text(), station_values[6].get_text())
                    station_distance = station_values[5].get_text()
                    # Adds dictionary to the dataframe
                    df = df.append({'No.': station_no, 'Station Code': station_code, 'Station Name': station_name, 'Arrival': station_arrive, 'Departure': station_depart, 'Distance': station_distance, 'Train No.': train_id}, ignore_index=True)
    
    # Converts dataframe to csv
    df.to_csv(file_name, encoding='utf-8', index=False)