'''
Paper Green Lobby
Text Mining and Natural Language Processing
https://medium.com/@adriensieg/text-similarities-da019229c894

@claudioalvesmonteiro 2020
'''

#=================================
# preprocess
#===============================

# import packages
import pickle
import os
import pandas as pd
import numpy as np

# list files
files = os.listdir('data/preprocessed')

# import data and save in list
data = []
for file in files:
        with open('data/preprocessed/{}'.format(file), 'rb') as handle:
            data.append(pickle.load(handle))

#=================================
# TEXT SIMILARITY ALGORITHM
#===============================

# import glove model
import gensim.downloader as api
word_vectors = api.load("glove-wiki-gigaword-100")      

# glove cleaning
def gloveBasedClean(vector):
    ''' verifiy if each word in vector is
        identified on model Glove, if not,
        do not append to vector
    '''
    vector_clean = []
    for word in vector:
        try:
            word_vectors[word]
            vector_clean.append(word)
        except:
            print('{} is not a valid word in Glove'.format(word))
    #vector_clean = list(set(vector_clean))
    return vector_clean

# Jaccard Similarity Index Function
def jaccardSimilarity(wordvec1, wordvec2):
    ''' takes two lists of words and 
        calculate Jaccard Similarity Coefficient
        based on word intersection
    '''
    intersection = set(wordvec1 ).intersection(set(wordvec2))
    union = set(wordvec1).union(set(wordvec2))
    jaccard_index = round(len(intersection)/len(union)*100, 4)
    return jaccard_index

# Glove Native Similarity Index
def gloveSimilarity(wordvec1, wordvec2):
    ''' takes two lists of words and 
        calculate similarity coefficient
        based on glove model
    '''
    glove_index = word_vectors.n_similarity(wordvec1, wordvec2)
    return round(glove_index*100, 4)

# Cosine Glove-based Similarity Index
def cosineGloveSimilarity(wordvec1, wordvec2):
    ''' takes two lists of words and 
        calculate cosine similarity  
        coefficient based on glove word vectorization
    '''
    import scipy
    wordvec1 = np.mean([word_vectors[word] for word in wordvec1], axis=0)
    wordvec2 = np.mean([word_vectors[word] for word in wordvec2], axis=0)
    cosine = scipy.spatial.distance.cosine(wordvec1, wordvec2)
    cosine_index = round((1-cosine)*100,4)
    return cosine_index

#==================================
# execute models and save results
#=================================

def executeSimilarityModels(data):
    # build data
    similarity_data = {'category':[], 
                       'jaccard_index_model':[], 
                       'word2vec_glove_model':[], 
                       'word2vec_glove_scipy_consine_model':[]}
    # clean document text
    wordvec2 = gloveBasedClean(data[1]['text'])
    # execute models
    for info in data:
        if info['category'] != 'Documento':
            # clean vector
            wordvec1 = gloveBasedClean(info['text'])
            # append category to dict
            similarity_data['category'].append(info['category'])
            # execute models
            similarity_data['jaccard_index_model'].append(jaccardSimilarity(wordvec1, wordvec2))
            similarity_data['word2vec_glove_model'].append(gloveSimilarity(wordvec1, wordvec2))
            similarity_data['word2vec_glove_scipy_consine_model'].append(cosineGloveSimilarity(wordvec1, wordvec2))
    # save data
    similarity_data = pd.DataFrame(similarity_data)
    similarity_data.to_csv('results/tables/similarity_data.csv', index=False)
    # return data
    return similarity_data

# execute
executeSimilarityModels(data)