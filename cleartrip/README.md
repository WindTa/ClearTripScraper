# Clear Trip Scraper
This program is designed to obtain some data from cleartrip.com using Python 3.7.2

## Steps

1. Install lxml library
   a) Open cmd
   b) Type `pip install lxml`
2. Run Scraper.py
3. Enter page number (file name purposes)
4. Enter web page
5. csv file will be saved in same directory as location of Scraper.py

## Changing name of exported csv file

Look for variable `file_name` and change to whatever you want. It is currently set to `"results" + input("What page is the URL on? ") + ".csv"

## Applying Scraper.py to another website

### Page Number

This only applied to cleartrip.com. Your goal may not have multiple pages to sift through. In this case, remove lines 41-55.

### url_to_children

Happened to apply to both the pages and the train's stations. In this case, the data was found in the HTML tag `<table></table>`, with class `class: results`, with rows of data (children) in the HTML tag `tr`. Specific values were broken into HTML tag `td`. Adjust it accordingly.

### Changing values to store to csv

The column names are initialized at the beginning of the main function. Specific column values that are stored can be changed in lines 61-69.