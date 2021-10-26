import gensim.models
import numpy as np
import pandas as pd

def get_distance(word1, word2, wv, type='cosine'): 
    distance = wv.similarity(word1, word2) if type == 'cosine' \
        else np.dot(wv[word1], wv[word2])

    return distance

def calculate_differing_distances(sentences, similarityWords): 
    vector_dimensions = [50, 100, 200, 300]
    window_dimensions = [2, 5, 3, 10]

    df = pd.DataFrame(columns = [])

    for vector_size in vector_dimensions: 
        for window_size in window_dimensions: 
            model = gensim.models.Word2Vec(sentences, vector_size=vector_size, window=window_size)

            for key in similarityWords.keys(): 
                cosSimilarity = get_distance(similarityWords[key][0], similarityWords[key][1], 'cosine')
                dotSimilarity = get_distance(similarityWords[key][0], similarityWords[key][1], 'dot')
                print(f"Key: {key} Pair: {similarityWords[key][0]}{similarityWords[key][1]}:")
                print(
                    f"\t V{vector_size} W:{window_size}  cos: {cosSimilarity} dot: {dotSimilarity}")


