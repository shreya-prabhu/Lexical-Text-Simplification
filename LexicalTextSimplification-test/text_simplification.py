""" Simple text simplification approach based on frequency.
Choose 30% top low frequent words in the sentence,
replace them with the most frequent candidate from wordnet """

import pandas as pd
import gensim
from nltk.corpus import brown,wordnet
from nltk.probability import *
from nltk import sent_tokenize, word_tokenize, pos_tag
from conjugation import convert




def generate_brown_frequency_dictionary():
    """ Create frequency distribution of BROWN corpora. """

    brown_frequency_dictionary = FreqDist()
    for sentence in brown.sents():
        for word in sentence:
            brown_frequency_dictionary[word] += 1

    corpus_frequency_distribution = pd.DataFrame(list(brown_frequency_dictionary.items()), columns = ["Word","Frequency"])
    corpus_frequency_distribution.sort_values("Frequency")
    corpus_frequency_distribution.to_csv('corpus_frequency.csv')
    return brown_frequency_dictionary


class Simplifier:
    def __init__(self):
        ''' The ngram frequency dictionary is annotated as
        frequency, word1...wordn, pos1...posn'''

        ngrams = pd.read_csv('./results/ngrams.csv')
        ngrams = ngrams.drop_duplicates(subset='bigram', keep='first')

        self.bigrams_brown_frequency_dictionary = dict(zip(ngrams.bigram, ngrams.freq))

        bigrams_distribution = pd.DataFrame(list(self.bigrams_brown_frequency_dictionary.items()), columns = ["Bigram","Frequency"])
        bigrams_distribution.to_csv('bigrams_frequency.csv')
        self.brown_frequency_dictionary = generate_brown_frequency_dictionary()
        self.steps = open('steps.txt', 'w')

    def check_if_word_fits_the_context(self, context, token, replacement):
        """ Check if bigram with the replacement exists.
        Check for word preceeding and succeeding the replacement in the bigram dictionary. """
        
        if len(context) == 3:
            if (context[0] + ' ' + replacement).lower() in self.bigrams_brown_frequency_dictionary.keys() or (replacement + ' ' + context[2]).lower() in self.bigrams_brown_frequency_dictionary.keys() :
                return True
            else:
                return False
        else:
            return False

    def return_bigram_score(self, context, token, replacement):
        """ Return the averaged frequency of left- and right-context bigram. """
        score = 0
        if (context[0] + ' ' + replacement).lower() in self.bigrams_brown_frequency_dictionary.keys():
            score += self.bigrams_brown_frequency_dictionary[(context[0] + ' ' + replacement).lower()]
        if (replacement + ' ' + context[2]).lower() in self.bigrams_brown_frequency_dictionary.keys():
            score += self.bigrams_brown_frequency_dictionary[(replacement + ' ' + context[2]).lower()]
        return score / 2

    def check_if_replacable(self, word):
        """ Check POS, we only want to replace nouns, adjectives and verbs. """
        word_tag = pos_tag([word])
        if 'NN' in word_tag[0][1] or 'JJ' in word_tag[0][1] or 'VB' in word_tag[0][1]:
            return True
        else:
            return False

    def generate_wordnet_candidates(self, word):
            """ Generate wordnet candidates for each word in input. """
            candidates = set()
            if self.check_if_replacable(word):
                for synset in wordnet.synsets(word):
                    for lemma in synset.lemmas():
                        converted = convert(lemma.name().lower(), word)
                        if converted != word and converted != None:
                            candidates.add(converted)
            return candidates

    def check_pos_tags(self, sent, token_id, replacement):
        old_tag = pos_tag(sent)[token_id][1]
        sent[token_id] = replacement
        new_tag = pos_tag(sent)[0][1]
        if new_tag == old_tag:
            return True
        else:
            return False


    
    def simplify(self, input):
        simplified0 = ''
        simplified1 = ''
        simplified2 = ''

        sents = sent_tokenize(input)  # Split by sentences

        '''Top 40 % least frequency score (rarer) words of the input corpus are taken as difficult words'''

        top_n = int(40/100*(len(input)))
        freq_top_n = sorted(self.brown_frequency_dictionary.values(), reverse=True)[top_n - 1]
        for sent in sents:
            self.steps.write(sent + '\n')
            tokens = word_tokenize(sent)  # Split a sentence by words

            #Store all difficult words
            difficultWords = [t for t in tokens if self.brown_frequency_dictionary[t] < freq_top_n]
            self.steps.write('difficultWords:' + str(difficultWords) + '\n')

            all_options = {}
            for difficultWord in difficultWords:
                replacement_candidate = {}

                '''Collect WordNet synonyms for each difficult word, 
                    along with their brown corpus frequency.'''

                for option in self.generate_wordnet_candidates(difficultWord):
                    replacement_candidate[option] = self.brown_frequency_dictionary.freq(option)

                '''store all these candidates in all_options '''

                all_options[difficultWord] = replacement_candidate
            all_options_list =  [(k, v) for k, v in all_options.items()]
            self.steps.write('all_options:')
            self.steps.write(str(all_options_list))

            ''' Populate best candidates dictionary if it is a bigram, and add bigram score '''
            best_candidates = {}
            for token_id in range(len(tokens)):
                token = tokens[token_id]

                best_candidates[token] = {}
                if token in all_options:
                    for opt in all_options[token]:
                        if token_id != 0 and token_id != len(tokens):  # if not the first or the last word in the sentence
                            if self.check_if_word_fits_the_context(tokens[token_id - 1:token_id + 2], token, opt):
                                
                                best_candidates[token][opt] = self.return_bigram_score(tokens[token_id - 1:token_id + 2], token, opt)
            # self.steps.write('best_candidates:' + str(best_candidates) + '\n')
            best_candidates_list = [(k, v) for k, v in best_candidates.items()]
            self.steps.write("hi")
            self.steps.write('best_candidates:')

            '''Generate steps0 - take the word with the highest bigram score'''
            output = []
            for token in tokens:
                if token in best_candidates:
                    if token.istitle() is False and best_candidates[token] != {}:
                        # Choose the one with the highest bigram score
                        best = max(best_candidates[token], key=lambda i: best_candidates[token][i])
                        self.steps.write('best v1:' + str(token) + ' -> ' + str(best) + '\n')
                        output.append(best)
                    else:
                        output.append(token)
                else:
                    output.append(token)
            simplified0 += ' '.join(output)

            '''Generate steps1 - take the word with the highest frequency + check the context'''
            output = []
            for token_id in range(len(tokens)):
                token = tokens[token_id]
                if token in all_options and len(all_options[token]) > 0 and token in difficultWords and token.istitle() is False:
                    if token_id != 0 and token_id != len(tokens):
                        # Choose most frequent and check if fits the context
                        best_filtered = {word: all_options[token][word] for word in all_options[token] if
                                         self.check_if_word_fits_the_context(tokens[token_id - 1:token_id + 2], token, word)
                                         and self.check_pos_tags(tokens, token_id, word)}
                        if best_filtered != {}:  # if not empty
                            best = max(best_filtered, key=lambda i: best_filtered[i])
                            self.steps.write('best v2:' + str(token) + ' -> ' + str(best) + '\n')
                            output.append(best)
                        else:
                            output.append(token)
                    else:
                        output.append(token)
                else:
                    output.append(token)
            simplified1 += ' '.join(output)

            '''Generate steps2  - take the synonym with the highest frequency'''
            output = []
            for token in tokens:
                # Replace word if in is difficult and a candidate was found
                if token in all_options and len(all_options[token]) > 0 and token in difficultWords and token.istitle() is False:
                    best = max(all_options[token], key=lambda i: all_options[token][i])
                    self.steps.write('best v3:' + str(token) + ' -> ' + str(best) + '\n')
                    output.append(best)
                else:
                    output.append(token)
            simplified2 += ' '.join(output)

        return simplified0, simplified1, simplified2


if __name__ == '__main__':

    simplifier = Simplifier()
    

#     with open('wiki_input_2.txt') as f:
#         with open('wiki_output_zepp.csv', 'w') as w:
#             for input in f:
#                 simplified0, simplified1, simplified2 = simplifier.simplify(input)
#                 w.write(simplified0 + '\t' + simplified1 + '\t' + simplified2 + '\n')


