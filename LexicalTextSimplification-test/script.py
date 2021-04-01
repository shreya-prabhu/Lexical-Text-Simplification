import re
import pandas as pd
import ujson
import _pickle as pickle
from nltk import sent_tokenize, word_tokenize, pos_tag
import pandas as pd
import gensim

from nltk.corpus import brown
from nltk.probability import *
from nltk.corpus import wordnet
from nltk import sent_tokenize, word_tokenize, pos_tag

import logging

import text_simplification
from conjugation import convert


def concat(row):
    return str(row['w1']) + ' ' + str(row['w2'])


def generate_freq_dict():
    """ Create frequency dictionary based on BROWN corpora. """
    freq_dict = FreqDist()
    for sentence in brown.sents():
        for word in sentence:
            freq_dict[word] += 1
    return freq_dict


if __name__ == '__main__':

    simplifier1 = text_simplification.Simplifier()
    with open('./evaluation/input1.en') as f:
        with open('./evaluation/out0-input1.lsen', 'w') as s0, open('./evaluation/out1-input1.lsen', 'w') as s1, open('./evaluation/out2-input1.lsen', 'w') as s2:
            for input in f:
                simplified0, simplified1, simplified2 = simplifier1.simplify(input)
                s0.writelines(simplified0 + "\n")
                # print("writing output1")
                s1.writelines(simplified1 + "\n")
                # print("writing output2")
                s2.writelines(simplified2 + "\n")
                # print("writing output1")
    simplifier2 = text_simplification.Simplifier()
    with open('./evaluation/input2.sen') as f:
        with open('./evaluation/out0-input2.lsen', 'w') as s0, open('./evaluation/out1-input2.lsen', 'w') as s1, open('./evaluation/out2-input2.lsen', 'w') as s2:
            for input in f:
                simplified0, simplified1, simplified2 = simplifier2.simplify(input)
                s0.writelines(simplified0 + "\n")
                # print("writing output1")
                s1.writelines(simplified1 + "\n")
                # print("writing output2")
                s2.writelines(simplified2 + "\n")
                # print("writing output1")
                
