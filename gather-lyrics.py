# -*- coding: utf-8 -*-

# change working directory to current file directory
import os
os.chdir(os.path.dirname(os.path.abspath('gather-lyrics.py')))

import lyricsgenius # API wrapper for genius.com
#import nltk for word processing 
from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer
import json # for saving artist:lyrics data
import pandas as pd 
from keys import genius_api_key

# set up Regular Expression tokenizer for lyric cleaning
tokenizer = RegexpTokenizer(r'\w+') # keep all words. discard punctuation
stop_words = set(stopwords.words('english'))

# load genius API and settings
api = lyricsgenius.Genius(genius_api_key)
api.remove_section_headers = True
api.verbose = False

def main():
    artist_list = pd.read_csv('artist_list.csv', 
                           usecols = ['Artist']).values.tolist()
    
    # use this line instead of above to pare down failed_artists
    # artist_list = pd.read_csv('failed_artists.csv',
                            #  usecols = ['Failures']).values.tolist()
    
    # ensure we capture all artists whose queries fail
    failed_artists = []
    failed_artists = getLyrics(artist_list, failed_artists)
    
    # write the list of failures to a CSV for analysis & recapture
    df = pd.DataFrame(failed_artists, columns=['Failures'])
    df.to_csv('failed_artists.csv', index=False)

# scrape and store lyrics for all artists on the artist list
def getLyrics(artist_list, failed_artists):
    for artist_name in artist_list:
        # scrape artist data
        try:
            artist = api.search_artist(artist_name, max_songs=25,
                                       sort="popularity")

            # clean up lyrics and create single master list for the artist
            (art, lyrics) = gatherArtistText(artist)
            save_dictionary = {art: lyrics}
            
            # append dictionary to JSON file
            with open('lyrics-data.json', 'a', encoding='utf-8') as f:
                json.dump(save_dictionary, f, ensure_ascii=False, indent=4)
        
        except:
            failed_artists.append(artist_name)
            
        print('Finished ' +str(artist_list.index(artist_name) + 1) +  
                  ' of ' + str(len(artist_list)))             
            
    return failed_artists

# build tuple of (artist name, cleaned lyrics) for one artist
def gatherArtistText(artist):
    artist_text = []
    # for each of the songs by the artist:
    for i in range(0, len(artist.songs)):
        # select the song
        text = artist.songs[i].to_text()
        # clean up the song text
        cleaned_text = cleanText(text)
        # add all remaining words to list associated with the artist
        artist_text.extend(cleaned_text) 
    
    return (artist.name, artist_text)
    
# remove punctuation, one word per token, remove stop words
def cleanText(text):
    # remove punctuation and symbols
    tokenized_text = tokenizer.tokenize(text)
    # make all words lower case
    tokenized_text = [token.lower() for token in tokenized_text]
    # remove stop words
    filtered_text = []
    for word in tokenized_text:
        if word not in stop_words:
            filtered_text.append(word)
    return filtered_text # an array of all the non-stopwords
 

if __name__ == "__main__":
    main()      
