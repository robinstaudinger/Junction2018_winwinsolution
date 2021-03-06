# -*- coding: utf-8 -*-
"""extractive_summarizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YSfkJcmyZTLacv-aba9Tdwm8HX7keGCV


### 1. Importing important libraries
"""
import numpy as np
import sys, imp
import networkx as nx
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


class text_summarizer():

  def __init__(self):
    self.temp = []

  def tokenize(self, document):
    # We are tokenizing using the PunktSentenceTokenizer
    # we call an instance of this class as sentence_tokenizer
    doc_tokenizer = PunktSentenceTokenizer()

    # tokenize() method: takes our document as input and returns a list of all the sentences in the document

    # sentences is a list containing each sentence of the document as an element
    sentences_list = doc_tokenizer.tokenize(document)

    return sentences_list

  def summarize(self, document):

    sentences_list = self.tokenize(document)
    cv = CountVectorizer()
    cv_matrix = cv.fit_transform(sentences_list)
    normal_matrix = TfidfTransformer().fit_transform(cv_matrix)
    res_graph = normal_matrix * normal_matrix.T
    nx_graph = nx.from_scipy_sparse_matrix(res_graph)
    ranks = nx.pagerank(nx_graph)
    sentence_array = sorted(((ranks[i], s) for i, s in enumerate(sentences_list)), reverse=True)
    sentence_array = np.asarray(sentence_array)
    rank_max = float(sentence_array[0][0])
    rank_min = float(sentence_array[len(sentence_array) - 1][0])
    temp_array = []
    flag = 0
    if rank_max - rank_min == 0:
        temp_array.append(0)
        flag = 1

    # If the sentence has different ranks
    if flag != 1:
        for i in range(0, len(sentence_array)):
            temp_array.append((float(sentence_array[i][0]) - rank_min) / (rank_max - rank_min))

    threshold = (sum(temp_array) / len(temp_array)) + 0.2
    sentence_list = []
    if len(temp_array) > 1:
        for i in range(0, len(temp_array)):
            if temp_array[i] > threshold:
                    sentence_list.append(sentence_array[i][1])
    else:
        sentence_list.append(sentence_array[0][1])
    model = sentence_list
    summary = " ".join(str(x) for x in sentence_list)
    return summary
