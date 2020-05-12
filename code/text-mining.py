'''
Paper Green Lobby
Text Mining and Natural Language Processing

@claudioalvesmonteiro 2020
'''

# import packages
import pickle
import os
import pandas as pd

# list files
files = os.listdir('data/preprocessed')

# import data and save in list
data = []
for file in files:
        with open('data/preprocessed/{}'.format(file), 'rb') as handle:
            data.append(pickle.load(handle))

#======================
# WORDCOUNT
#=======================

def autoTokenWordCount(data):
    ''' for each data_dict, count the n of word
        in a list and save as csv 
    '''
    for dic in data:
        cat_name = dic['category'].replace(' ', '_')
        count = wordcount(dic['text'])
        # rename columns 
        count.columns = [cat_name, 'freq']
        # save as csv
        count.to_csv('results/tables/{}.csv'.format(cat_name), index=False)


def wordcount(txt_list):
    ''' count words in a list
    '''
    # loop to count
    wordfreq = {}
    for w in txt_list:
        wordfreq[w] = txt_list.count(w)
    # transform in pandas df
    count = pd.DataFrame({'word': list(wordfreq.keys()), 'freq': list(wordfreq.values()) })
    # sort_values in df
    count.sort_values('freq', inplace=True, ascending=False)
    # return df
    return count
    

# execute process and save results
autoTokenWordCount(data)
