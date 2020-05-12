'''
Paper XXX
@claudioalvesmonteiro 2020
'''


# import packages
import pandas as pd
import pickle

# import data
df = pd.read_csv('data/NDC_database.csv')

# select and rename columns 
df = df[df.columns[[1,2,8,14, 15]] ]
df.columns = ['participation', 'category', 'comments', 'comments_implementation_means', 'criteria_assumptions_principles']

#=============================
# generate text
#=============================

def aggText(df, category):
    ''' this function return and save the text 
        aggregated by an auxiliary category in
        a pandas dataframe, as json pickle
    '''
    # select category data
    data = df[df['category'] == category]
    # cature text from column
    text = ''
    for col in df.columns[2:5]:
        for i in range(len(data)):
            try:
                text += data[col][i] + '\n'
            except:
                print('empty string on line {}.'.format(i)) 

    # apply text cleaning
    text = cleanTextToken(text)
    # create string of text information
    text_info ={'category': category,
                'text': text}
    # save as json
    category = category.replace(' ', '_')
    with open('data/preprocessed/{}.pickle'.format(category), 'wb') as fp:
        pickle.dump(text_info, fp, protocol=pickle.HIGHEST_PROTOCOL)
    return text_info


def cleanTextToken(text):
    ''' this function cleans the text and returns 
        the words in tokens
    '''
    # characters to lower
    text = text.lower()
    # remove punctuations
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+') # preserve alphanumeric and words
    text = tokenizer.tokenize(text)

    # remove stopwords
    import nltk
    from nltk.corpus import stopwords
    stop = set(stopwords.words('portuguese'))
    text = [w for w in text if not w in stop]

    # stemmezation
    #from nltk.stem import PorterStemmer 
    #ps = PorterStemmer()
    #text = [ps.stem(word) for word in text]
    #for i in range(len(text)):
    #    print(text[i],': ',ps.stem(text[i]))
    return text
    

#  apply function to data
for category in df.category.unique():
    aggText(df, category)