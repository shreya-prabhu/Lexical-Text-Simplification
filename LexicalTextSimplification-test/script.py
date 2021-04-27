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
import text_simplification
from conjugation import convert


def generate_freq_dict():
    """ Create frequency dictionary based on BROWN corpora. """
    freq_dict = FreqDist()
    for sentence in brown.sents():
        for word in sentence:
            freq_dict[word] += 1
    return freq_dict


if __name__ == '__main__':

    simplifier1 = text_simplification.Simplifier()
    with open('./data/input.txt',encoding='utf-8') as f:
        with open('./evaluation/output10.txt', 'w') as s0, open('./evaluation/output11.txt', 'w') as s1, open('./evaluation/output12.txt', 'w') as s2:
            for input in f:
                simplified0, simplified1, simplified2 = simplifier1.simplify(input)
                s0.writelines(simplified0 + "\n")
                s1.writelines(simplified1 + "\n")
                s2.writelines(simplified2 + "\n")
        
    
    simplifier2 = text_simplification.Simplifier()
    with open('./data/input2.txt',encoding='utf-8') as f:
        with open('./evaluation/output21.txt', 'w') as s0, open('./evaluation/output22.txt', 'w') as s1, open('./evaluation/output23.txt', 'w') as s2:
            for input in f:
                simplified0, simplified1, simplified2 = simplifier2.simplify(input)
                s0.writelines(simplified0 + "\n")
                s1.writelines(simplified1 + "\n")
                s2.writelines(simplified2 + "\n")
                
