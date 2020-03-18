# -*- coding: utf-8 -*-

# set working directory to current folder
import os
os.chdir(os.path.dirname(os.path.abspath('sentiment-analysis.py')))

import pandas as pd 
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize

def clean_lyrics_add_wordcounts(artist_df):
    # clean up lyrics. Remove unhelpful symbols
    word_count = [] 
    unique_words = []
    
    for i in range(0, len(artist_df)):
        lyrics = artist_df.iloc[i,1] # reformat lyrics for every row 
        lyrics = lyrics.replace("[", "")
        lyrics = lyrics.replace("]", "")
        lyrics = lyrics.replace(",", "")
        lyrics = lyrics.replace("'", "") # maybe replace w/ regex 
                                         # to keep apostrophes?
        word_count.append(len(lyrics.split()))
        unique_words.append(len(set(lyrics.split())))
        artist_df.iloc[i,1] = lyrics
    
    # add a word count variable to the dataframe
    artist_df['Word Count'] = word_count   
    artist_df['Unique Words'] = unique_words
    
    # we  remove artists who have no lyrics
    # if Lyrics is empty then drop row
    df = artist_df[artist_df.Lyrics != '']
    df = df.reset_index(drop=True) # reset index to avoid missing numbers
    
    return df   

# thanks to Greg Rafferty's Harry Potter sentiment analysis 
# for much of the code below
# https://github.com/raffg/harry_potter_nlp/blob/master/sentiment_analysis.ipynb
def calc_emotion_scores(artist_df):
    
    # read in NRC emotional association lexicon
    emolex_df = pd.read_csv('NRC-lexicon.txt',
                            names=["word", "emotion", "association"],
                            sep='\t')
    
    # pivot data table to have all emotions on one row
    emolex_words = emolex_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
    # create list of emotions
    emotions = emolex_words.columns.drop('word')
    
    # create data frame to store emotion counters
    emo_df = pd.DataFrame(0, index=artist_df.index, columns=emotions)
    
    stemmer = SnowballStemmer("english")
    
    # perform the sentiment analysis
    for i in range(0, len(artist_df)):
    # for each row in the df
        # create tokenized list of all lyrics
        lyric_library = word_tokenize(artist_df.Lyrics[i])
        # for each word in lyrics
        for lyric in lyric_library:
            # remove suffexes etc. with stemmer
            word = stemmer.stem(lyric)
            # check emotional association for each emotion
            emo_score = emolex_words[emolex_words.word == word]
            # increment for appropriate emotion counters
            if not emo_score.empty:
                        for emotion in list(emotions):
                            emo_df.at[i, emotion] += emo_score[emotion]
        print('Finished with ' + str(i) + ' of ' + str(len(artist_df)))
    
    # concatenate the two data frames together
    new_df = pd.concat([artist_df, emo_df], axis=1)
    # divide each emotion by word count to obtain percentages
    new_df['pos pct']      = new_df['positive']/new_df['Word Count']
    new_df['neg pct']      = new_df['negative']/new_df['Word Count']
    new_df['anger pct']    = new_df['anger']/new_df['Word Count']
    new_df['anticp pct']   = new_df['anticipation']/new_df['Word Count']
    new_df['disgust pct']  = new_df['disgust']/new_df['Word Count']
    new_df['fear pct']     = new_df['fear']/new_df['Word Count']
    new_df['joy pct']      = new_df['joy']/new_df['Word Count']
    new_df['sadness pct']  = new_df['sadness']/new_df['Word Count']
    new_df['surprise pct'] = new_df['surprise']/new_df['Word Count']
    new_df['trust pct']    = new_df['trust']/new_df['Word Count']

    return new_df


# read in artist and lyric data
artist_df = pd.read_csv('lyrics-data.csv', 
                            usecols = ['Artist', 'Lyrics'])
# clean up lyrics and add wordcounts 
artist_df = clean_lyrics_add_wordcounts(artist_df)

# calculate artist emotion scores from lyrics
new_df = calc_emotion_scores(artist_df)

# drop raw counts. we will keep only proportions
new_df = new_df.drop(['anger','negative', 'anticipation', 'disgust', 
                      'sadness', 'fear','joy', 'positive', 
                      'surprise', 'trust'], 
              axis=1)

# rename columns for better readability
new_df.rename(columns={'pos pct': 'positive', 'neg pct': 'negative',
                       'anger pct': 'anger', 'anticp pct': 'anticipation',
                       'disgust pct': 'disgust', 'fear pct': 'fear',
                       'joy pct': 'joy', 'sadness pct': 'sadness',
                       'surprise pct': 'surprise', 'trust pct': 'trust'}, 
                 inplace=True)

# add 'Lyrical Diversity' column and rearrange columns
new_df['Lyrical Diversity'] = new_df['Unique Words']/new_df['Word Count']

new_df = new_df[['Artist','Lyrics','Word Count','Unique Words',
                 'Lyrical Diversity','positive','negative','anger',
                 'anticipation','disgust','fear','joy',
                 'sadness','surprise','trust']]

# write final dataset to CSV for analysis
new_df.to_csv('sentiment-data-clean.csv', encoding='utf-8')
