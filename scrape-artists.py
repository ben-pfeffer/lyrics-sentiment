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

# In[ ]:





# How many artists did we scrape? 

# In[90]:


len(artist_list)# total artists


# How many unique artists did we scrape? 
# 

# In[1]:


# filter out unique artists
artist_list = set(artist_list)
len(artist_list) # unique artists


# We save our artist_list to a CSV file.

# In[109]:


import pandas as pd
df = pd.DataFrame(artist_list, columns = ['Artist'])
df.to_csv('artist_list.csv')


# We end up with 1540 unique artists when everything goes well. 
# 
# Now we want to grab the lyrics for many songs by each artist. 
# We use the Genius API

# In[1]:


import pandas as pd
artist_list = pd.read_csv("artist_list.csv", usecols =['Artist'])


# In[37]:

from keys import genius_api_key
import lyricsgenius
api = lyricsgenius.Genius(genius_api_key)
api.remove_section_headers = True
api.skip_non_songs = True,
api.excluded_terms = ["(Remix)", "(Live)", "(Take)", "Video"]

artist_name = "The Beatles"
artist = api.search_artist(artist_name, max_songs=20, sort="popularity")


# In[38]:


song = genius.search_song(artist.song, artist.name)


# In[17]:



song = genius.search_song("Act Naturally!", artist.name)
api.remove_section_headers = True
print(song.lyrics)

