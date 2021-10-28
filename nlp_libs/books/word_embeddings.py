from gensim.matutils import cossim
import gensim.models
import numpy as np
import pandas as pd


def get_distance(word1, word2, wv, type='cosine'):
    distance = wv.similarity(word1, word2) if type == 'cosine' \
        else np.dot(wv[word1], wv[word2])

    return distance


def calculate_differing_distances(sentences, wordpairs):
    vector_dimensions = [50, 100, 200, 300]
    window_dimensions = [2, 5, 3, 10]

    df = pd.DataFrame(columns=['word1', 'word2', 'vectorSize', 'windowSize' ,'cosineSim', 'dotSim'])


    for vector_size in vector_dimensions:
        for window_size in window_dimensions:
            model = gensim.models.Word2Vec(
                sentences, min_count=1, vector_size=vector_size, window=window_size)

            for wordPair in wordpairs: 
                cosSimilarity = get_distance(wordPair[0], wordPair[1], model.wv, 'cosine')
                dotSimilarity = get_distance(wordPair[0], wordPair[1], model.wv, 'dot')
                data = {
                    "word1": wordPair[0],
                    "word2": wordPair[1],
                    "vectorSize": vector_size,
                    "windowSize": window_size,
                    "cosineSim": cosSimilarity,
                    "dotSim": dotSimilarity,
                }
                df = df.append(data , ignore_index=True)

    return df