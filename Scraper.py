from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import requests

def url_to_children(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    page_children = page_soup.find("table", {"class": "results"}).findChildren("tr", recursive=True)
    return page_children

def endpoint_check(time, day):
    if "Starts" in time:
        return "Source"
    elif "Ends" in time:
        return "Destination"
    else:
        return str.strip(time) + " (Day " + day + ")" 

if __name__ == '__main__':
    # Initialize csv
    file_name = "results" + input("What page is the the URL on? ") + ".csv"
    df = pd.DataFrame(columns = ['No.', 'Station Code', 'Station Name', 'Arrival', 'Departure', 'Distance', 'Train No.'])

    # First page: https://www.cleartrip.com/trains/list?field=number&sort=up
    train_page_URL = input("Enter the URL for a page of trains: ")
    train_page_children = url_to_children(train_page_URL)
    for train_child in train_page_children:
        train_id = train_child.find("td")
        if train_id is not None:
            train_id = str.strip(train_id.get_text())
            print("Train ID: ", train_id)
            station_page_URL = "https://www.cleartrip.com/trains/" + train_id
            if station_page_URL != requests.get(station_page_URL).url:
                continue
            station_page_children = url_to_children(station_page_URL)

            for station_child in station_page_children:
                station_children = station_child.findChildren("td", recursive=False)
                if len(station_children) != 0:
                    station_no = str.strip(station_children[0].get_text())
                    station_name, station_code = [" ".join(x.split()) for x in re.split(r'[()]', station_children[1].get_text()) if x.strip()]
                    station_arrive = endpoint_check(station_children[2].get_text(), station_children[6].get_text())
                    station_depart = endpoint_check(station_children[3].get_text(), station_children[6].get_text())
                    station_distance = station_children[5].get_text()
                    df = df.append({'No.': station_no, 'Station Code': station_code, 'Station Name': station_name, 'Arrival': station_arrive, 'Departure': station_depart, 'Distance': station_distance, 'Train No.': train_id}, ignore_index=True)
    df.to_csv(file_name, encoding='utf-8', index=False)