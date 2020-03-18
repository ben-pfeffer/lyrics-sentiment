# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# build the URL for the billboard chart for each year
def buildURL(year):
    # https://www.billboard.com/charts/year-end/1969/hot-100-artists
    pre = 'https://www.billboard.com/charts/year-end/'
    post = '/hot-100-artists'
    return pre + str(year) + post


# thanks to johnwmillr for the getArtistsFromList() function
# https://github.com/johnwmillr/trucks-and-beer/blob/master/downloadLyrics.py
def getArtistsFromList(URL):    
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser")    
    chart_items = html.find_all("div", class_="ye-chart-item__title")
    return [item.get_text().strip() for item in chart_items] 

def buildArtistList():
    
    artist_list = []
    
    # gives list for years 1970 to 2019
    year_list = list(range(1970, 2020))
    year_list.reverse() # to scrape newer years first
    
    for year in year_list:
        top_for_year = getArtistsFromList(buildURL(year))
        print(str(year) + ': ' + str(len(top_for_year)) + ' artists scraped')
        if len(top_for_year) == 0:
            print('Bad Year: ' + str(year))
        for artist in top_for_year:
            artist_list.append(artist)
    
    return artist_list

def main():
    artist_list = buildArtistList()
    artist_list.to_csv('artist_list.csv', index=False)

if __name__ == "__main__":
    main()  