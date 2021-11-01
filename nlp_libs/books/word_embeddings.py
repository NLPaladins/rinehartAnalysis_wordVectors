from gensim.matutils import cossim
import gensim.models
import numpy as np
import pandas as pd
import multiprocessing as mp

def calculateAll(sentences, wordpairs, vector_dimension, window_dimension):
    pool = mp.Pool(mp.cpu_count())
    model = gensim.models.Word2Vec(sentences, min_count=2, vector_size=vector_dimension, window=window_dimension)

    results = pool.map(lambda x: get_distance(x[0],x[1], model.wv, 'cosine'))

def get_distance(word1, word2, wv, type='cosine'):
    # print(f"word1:{word1}, word2:{word2}, wv:{wv}, type:{type},",  flush=True)
    distance = wv.similarity(word1, word2) if type == 'cosine' \
        else np.dot(wv[word1], wv[word2])

    return distance


def extract_dot_and_cosine(wordPair, model, vector_size, window_size): 
    cosSimilarity = get_distance(wordPair[0], wordPair[1], model.wv, 'cosine')
    dotSimilarity = get_distance(wordPair[0], wordPair[1], model.wv, 'dot')
    data = [ wordPair[0],wordPair[1], vector_size, window_size, cosSimilarity, dotSimilarity ]
    return data

def calculate_differing_distances(sentences, wordpairs, vector_dimensions=[50, 100, 200, 300], window_dimensions=[2, 5, 3, 10]):
    columns = ['word1', 'word2', 'vectorSize',
               'windowSize', 'cosineSim', 'dotSim']
    df = pd.DataFrame(columns=columns)

    pool = mp.Pool(mp.cpu_count())

## TODO: Calculate the frequency of the words. Take top x% and use the min(frequentWordCount)

    for vector_size in vector_dimensions:
        for window_size in window_dimensions:
            model = gensim.models.Word2Vec(
                sentences, min_count=2, vector_size=vector_size, window=window_size, )

            results = pool.starmap(extract_dot_and_cosine, [
                                   (wordpair, model, vector_size, window_size) for wordpair in wordpairs])

            dataframe = pd.DataFrame(results, columns=columns)
            
            df = pd.concat([df, dataframe])
            
    return df
