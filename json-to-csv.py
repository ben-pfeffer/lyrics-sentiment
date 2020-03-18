# -*- coding: utf-8 -*-

import json
import pandas as pd 

# change working directory to current file directory
import os
os.chdir(os.path.dirname(os.path.abspath('json-to-csv.py')))

# clean up JSON file
# due to the method of appending each artist to an existing JSON file
# we need to replace }{ with ,
filein = 'lyrics-data.json'
fileout = 'lyrics-clean.json'

replacements = {'}{' : ','}

with open(filein, 
          encoding='utf-8') as infile, open(fileout, 'w',
                                            encoding ='utf-8') as outfile:
    for line in infile:
        for src, target in replacements.items():
            line = line.replace(src, target)
        outfile.write(line)

# load clean JSON file 
with open('lyrics-clean.json', 
          encoding = 'utf-8') as F:
    artist_dict = json.load(F)

# transform data from JSON to DataFrame/CSV
data = {'Artist': [], 'Lyrics': []}
for artist in artist_dict:
    data['Artist'].append(artist)
    data['Lyrics'].append(artist_dict[artist])

artist_df = pd.DataFrame(data=data)

# write DataFrame to CSV file for easy retreival in the future
artist_df.to_csv('lyrics-data.csv', encoding='utf-8')
