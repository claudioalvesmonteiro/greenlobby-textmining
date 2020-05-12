'''
Paper Green Lobby
Text Mining and Natural Language Processing

@claudioalvesmonteiro 2020
'''

# import packages
import pandas as pd
import pickle
import os

# list files
files = os.listdir('data/raw')

# import data and save in list
data = []
for file in files:
        with open('data/raw/{}'.format(file), 'rb') as handle:
            handle = handle.read().decode().replace('\xa0', '').replace('\n', ' ')
            data.append(handle)

#=============================
# generate text
#=============================

def aggText(text_string, category, lemmatizer):
    ''' this function return and save the text 
        aggregated by an auxiliary category in
        a pandas dataframe, as json pickle
    '''
    # apply text cleaning to string
    text = cleanTextToken(text_string, lemmatizer = lemmatizer)
    # create string of text information
    text_info ={'category': category,
                'text': text}
    # format name of sector for filesave
    category = category.lower().replace(' ', '_')
    # save as pickle
    with open('data/preprocessed/{}.pickle'.format(category), 'wb') as fp:
        pickle.dump(text_info, fp, protocol=pickle.HIGHEST_PROTOCOL)
    return text_info


def cleanTextToken(text, lemmatizer = False):
    ''' this function cleans the text and returns 
        the words in tokens
    '''
    # characters to lower
    text = text.lower()
    # remove numbers
    text = ''.join([i for i in text if not i.isdigit()]) 

    # remove punctuations
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+') # preserve alphanumeric and words
    text = tokenizer.tokenize(text)

    # remove stopwords
    import nltk
    from nltk.corpus import stopwords
    stop = set(stopwords.words('english'))
    text = [w for w in text if not w in stop]

    # lemmatization
    if lemmatizer == True:
        from nltk.stem import WordNetLemmatizer 
        lemmatizer = WordNetLemmatizer() 
        text = [lemmatizer.lemmatize(word) for word in text]
    
    # return result
    return text
    

#  apply function to data
for i in range(len(data)):
    aggText(data[i], files[i][:-4],  lemmatizer = True)