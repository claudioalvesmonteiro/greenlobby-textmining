'''
Paper XXX

@claudioalvesmonteiro 2020
'''

# import packages
import pickle
import os
import pandas as pd

#=======================
# wordcount 
#=======================

# list files
files = os.listdir('data/preprocessed')

# import dictionaries and save in list
data = []
for file in files:
        with open('data/preprocessed/{}'.format(file), 'rb') as handle:
            data.append(pickle.load(handle))

#======================
# Functions
#=======================

def autoTokenWordCount(data):
    ''' for each data_dict, count the n of word
        in a list and save as csv 
    '''
    for dic in data:
        colname = dic['column'] +'_'+ dic['category']
        count = wordcount(dic['text'])
        # rename columns 
        count.columns = [colname, 'freq']
        # save as csv
        count.to_csv('results/tables/{}.csv'.format(colname), index=False)


# wordcount
def wordcount(txt_list):
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

#================================================================
# COMPARAR AS agreg_resp CADA GRUPO COM O DOCUMENTO PDF
# https://medium.com/@adriensieg/text-similarities-da019229c894
#=================================================================

# agg to count
def aggregateText(data, variable, value):
    list_agg = []
    for i in range(len(data)):
        if data[i][variable] == value:
            for w in data[i]['text']:
                list_agg.append(w)
    return list_agg
