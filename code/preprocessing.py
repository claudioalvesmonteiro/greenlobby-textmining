'''
Paper XXX

@claudioalvesmonteiro 2020
'''


# import packages
import pandas as pd

# import data
df = pd.read_csv('data/NDC_database.csv')

# select and rename columns 
df = df[df.columns[[1,2,8,14, 15]] ]
df.columns = ['participation', 'category', 'comments', 'comments_implementation_means', 'criteria_assumptions_principles']

#=============================
# generate text
#=============================

def aggText(df, category, column):
    ''' this function return and save the text 
        aggregated by an auxiliary category in
        a pandas dataframe 
    '''
    # select category data
    data = df[df['category'] == category]
    # cature text from column
    text = ''
    for i in range(len(data)):
        try:
            text += data[column][i] + '\n'
        except:
            print('empty string on line {}.'.format(i)) 
            
    # create string of text information
    text_info ='category:{}\ncolumn:{}\ntext:{}'.format(category, column, text)
    # save as .txt
    arq = open('data/preprocessed/{}_{}.txt'.format(column, category.replace(' ', '_')), 'w' )
    arq.write(text_info)
    arq.close()    
    return text_info


#  apply function to data
for category in df.category.unique():
    for col in df.columns[2:5]:
        aggText(df, category, col)
