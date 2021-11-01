from gensim.test.utils import common_texts
import gensim.models
import numpy as np
import pandas as pd
import itertools
from typing import *


def get_distance(word1, word2, wv, skipped_words: List[str], dist_type='cosine'):
    if word1 not in wv.index_to_key:
        if word1 not in skipped_words:
            print(f"{word1} not in vocabulary! Skipping..")
            skipped_words.append(word1)
        return None
    elif word2 not in wv.index_to_key:
        if word2 not in skipped_words:
            print(f"{word2} not in vocabulary! Skipping..")
            skipped_words.append(word2)
        return None
    else:
        distance = wv.similarity(word1, word2) if dist_type == 'cosine' \
            else np.dot(wv[word1], wv[word2])
        return distance


def calculate_differing_distances(wordpairs, sentences):
    """ If sentences is None, use pretrained"""
    if sentences is None:
        sentences = common_texts
    skipped_words = []
    vector_dimensions = [50, 100, 200, 300]
    window_dimensions = [2, 5, 3, 10]

    df = pd.DataFrame(columns=['word1', 'word2', 'vectorSize', 'windowSize', 'cosineSim', 'dotSim'])

    for vector_size in vector_dimensions:
        for window_size in window_dimensions:
            model = gensim.models.Word2Vec(
                sentences, vector_size=vector_size, window=window_size, min_count=2)

            for wordPair in wordpairs:
                cosSimilarity = get_distance(wordPair[0], wordPair[1],
                                             model.wv, skipped_words, 'cosine')
                dotSimilarity = get_distance(wordPair[0], wordPair[1],
                                             model.wv, skipped_words, 'dot')
                if cosSimilarity is None or dotSimilarity is None:
                    continue
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


def get_conf_values(conf: Dict, keys: List[str], get_all_sub_values: bool,
                    ignore_words_with_spaces: bool) -> List[str]:
    for key in keys:
        conf = conf[key]
    if get_all_sub_values:
        return [val for val_list in conf
                for val in list(val_list.values())[0]
                if not (ignore_words_with_spaces and ' ' in val)]
    else:
        return [val for val in conf if not (ignore_words_with_spaces and ' ' in val)]


def get_combinations(conf: Dict, keys_1: List[str], keys_2: List[str],
                     get_all_sub_values_1: bool, get_all_sub_values_2: bool,
                     ignore_words_with_spaces: bool) -> list[tuple[str, str]]:
    values_1 = get_conf_values(conf, keys_1, get_all_sub_values_1, ignore_words_with_spaces)
    values_2 = get_conf_values(conf, keys_2, get_all_sub_values_2, ignore_words_with_spaces)
    combinations = list(itertools.product(values_1, values_2))
    return combinations
