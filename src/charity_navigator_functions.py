import numpy as np
import pandas as pd
import random
from nltk.corpus import stopwords
from collections import defaultdict
from gensim import corpora, models, similarities
import pickle

def process_corpus(text_corpus):
    '''
    '''
    # Create a set of frequent words
#     stoplist = ""
#     stoplist = set('for a of the and to in is our with we that by their through as\
#                    are mission on'.split(' '))

    min_words=2
    max_percent=0.1

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_',
                   'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice',
                   'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want',
                   'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])


    # Lowercase each document, split it by white space and filter out stopwords
    texts = ""
    texts = [[word for word in document.lower().split() if word not in stop_words] for document in text_corpus]

    # Count word frequencies
    frequency = defaultdict(int)

    for text in texts:
        for token in text:
            frequency[token] += 1

    words_df = pd.DataFrame(list(frequency.items()), columns= ['Words','count']).sort_values('count',ascending=False)

    ten_percent_cutoff = (int(len(text_corpus)*max_percent))

    # Only keep words that appear more than once, are in less than 10% of documents, and are alphabetical strings
    processed_corpus = []

    for text in texts:
        token_list = []
        for token in text:
            if frequency[token] > min_words and frequency[token] < ten_percent_cutoff and str.isalpha(token):
                token_list.append(token)
        processed_corpus.append(token_list)

    return processed_corpus


def create_index_from_corpus(processed_corpus):
    '''
    '''
    dictionary = corpora.Dictionary(processed_corpus)
    features = (len(dictionary))

    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]

    # train the model
    tfidf = models.TfidfModel(bow_corpus)

    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=features)

    return index, dictionary, tfidf


def find_similar_charities_combined(train_df,test_df):
    '''
    '''
    total = 0
    category_counter = {1:0,2:0,3:0}
    document_min_words_cutoff = 200

    print("1. Processing Training Corpus")
#     char_desc_trimmed = []

#     for doc in train_df['corpus']:
#         if len(doc) >= document_min_words_cutoff:
#             char_desc_trimmed.append(doc)

    corpus = np.array(train_df['corpus'])

    processed_corpus = process_corpus(corpus)

    print("2. Creating Index from Training Corpus")
    index, dictionary, tfidf = create_index_from_corpus(processed_corpus)

    print("3. Starting Test Corpus Similarity Analysis\n")
    for ind, document in enumerate(test_df['corpus']):
        total +=1
        if total % 500 == 0:
            print("Analyzed",total,"documents...")


        query_bow = dictionary.doc2bow(document.split())
        sims = index[tfidf[query_bow]]

        top_3_sim = dict()
        count = 3

        for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[1:4]:

            if count > 0:
                top_3_sim[document_number] = score
            count -= 1

        category_count = 1

        print("Top 3 Charities Similar to:\nName:", test_df['name'].iloc[ind])
        print('Category:', test_df['category'].iloc[ind],'\n')

        for doc, score in top_3_sim.items():
            print("Name:",train_df['name'].iloc[doc])
            print("Category:", train_df['category'].iloc[doc])
            print("Score:",score)

            if train_df['category'].iloc[doc] == test_df['category'].iloc[ind]:
                category_counter[category_count] += 1
            category_count +=1
        print("")

    # Print Scores

    first_rec_score = round((category_counter[1] / total)*100,2)
    second_rec_score = round((category_counter[2] / total)*100,2)
    third_rec_score = round((category_counter[3] / total)*100,2)

    print ("\nFirst Recommendation Score:", first_rec_score,"%")
    print ("Second Recommendation Score:", second_rec_score,"%")
    print ("Third Recommendation Score:", third_rec_score,"%\n")

    print ("AVG Recommendation Score:", round((first_rec_score+second_rec_score+third_rec_score)/3,2),"%")

    return top_3_sim, dictionary

def find_similar_charities_from_search(train_df,search_text):
    '''
    Function
    --------
    Train Model on "corpus" column - composed of charity category, description, motto and state

    Parameters
    ----------
    train_df : DataFrame to Train LDA Model
    test_df : DataFrame to Test and Score Model

    Returns:
    -------
    top_3_sim : DataFrame of Top 3 Most Similar Charities
    '''
    total = 0
    category_counter = {1:0,2:0,3:0}
    document_min_words_cutoff = 200

    print("1. Processing Training Corpus")

    char_desc_trimmed = np.array(train_df['corpus'])

    corpus = char_desc_trimmed
    processed_corpus = process_corpus(corpus)

    print("2. Creating Model from Training Corpus")
    index, dictionary, tfidf = create_index_from_corpus(processed_corpus)

    print("3. Starting Test Corpus Similarity Analysis\n")

    total +=1
    if total % 500 == 0:
        print("Analyzed",total,"documents...")

    query_bow = dictionary.doc2bow(search_text.split())
    sims = index[tfidf[query_bow]]

    top_3_sim = dict()
    count = 3

    for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[1:4]:

        if count > 0:
            top_3_sim[document_number] = score
        count -= 1

    category_count = 1

    for doc, score in top_3_sim.items():
        category_counter[category_count] += score
        category_count +=1

    first_rec_score = round((category_counter[1] / total)*100,2)
    second_rec_score = round((category_counter[2] / total)*100,2)
    third_rec_score = round((category_counter[3] / total)*100,2)

    print ("\nFirst Recommendation Score:", first_rec_score,"%")
    print ("Second Recommendation Score:", second_rec_score,"%")
    print ("Third Recommendation Score:", third_rec_score,"%\n")

    print ("AVG Recommendation Score:", round((first_rec_score+second_rec_score+third_rec_score)/3,2),"%")

    return top_3_sim, dictionary

def create_sim_word_dict(text1, text2, dictionary):
    '''
    '''

    text1_array = text1.lower().split()
    text2_array = text2.lower().split()

    dict_list = []
    for i in range(len(dictionary)):
        dict_list.append(dictionary[i])
    dict_list = np.array(dict_list)

    similar_words = dict()

    for word in text2_array:
        if word in text1_array and word in dict_list:
            if word not in similar_words:
                similar_words[word] = 1
            else:
                similar_words[word] +=1

    return similar_words


def get_recs_from_pickled_model(document):
    '''
    '''
    # load the model from disk
    loaded_model = pickle.load(open('src/finalized_model.sav', 'rb'))
    # load the index from disk
    loaded_index = pickle.load(open('src/finalized_index.sav', 'rb'))
    # load the dictionary from disk
    loaded_dict = pickle.load(open('src/finalized_dict.sav', 'rb'))

    document = document.iloc[0]

    print(document)

    print(document.split())

    query_bow = loaded_dict.doc2bow(document.split())

    sims = loaded_index[loaded_model[query_bow]]

    top_3_sim = dict()

    for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[1:4]:
        top_3_sim[document_number] = score

    return top_3_sim, loaded_dict
