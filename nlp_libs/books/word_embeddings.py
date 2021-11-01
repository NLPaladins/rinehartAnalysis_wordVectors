from gensim.matutils import cossim
import gensim.models
import numpy as np
import pandas as pd
import itertools
from typing import *


def get_distance(word1, word2, wv, dist_type='cosine'):
    distance = wv.similarity(word1, word2) if dist_type == 'cosine' \
        else np.dot(wv[word1], wv[word2])

    return distance


def calculate_differing_distances(sentences, wordpairs):
    vector_dimensions = [50, 100, 200, 300]
    window_dimensions = [2, 5, 3, 10]

    df = pd.DataFrame(columns=['word1', 'word2', 'vectorSize', 'windowSize', 'cosineSim', 'dotSim'])

    for vector_size in vector_dimensions:
        for window_size in window_dimensions:
            model = gensim.models.Word2Vec(
                sentences, vector_size=vector_size, window=window_size, min_count=2)

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
                df = df.append(data, ignore_index=True)

    return df


def get_conf_values(conf: Dict, keys: List[str], get_all_sub_values: bool) -> List[str]:
    for key in keys:
        conf = conf[key]
    if get_all_sub_values:
        return [val for val_list in conf for val in list(val_list.values())[0]]
    else:
        return [val for val in conf]


def get_combinations(conf: Dict, keys_1: List[str], keys_2: List[str],
                     get_all_sub_values_1: bool, get_all_sub_values_2: bool) -> list[tuple[str, str]]:
    values_1 = get_conf_values(conf, keys_1, get_all_sub_values_1)
    values_2 = get_conf_values(conf, keys_2, get_all_sub_values_2)
    combinations = list(itertools.product(values_1, values_2))
    return combinations
