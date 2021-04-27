import textstat
import nltk
import readability
from readability import Readability

with open('./data/input3.txt','r',encoding='utf-8') as file:
        test_data = file.read()
        x = Readability(test_data)
        fk = x.flesch_kincaid()
        print('score',fk.score)
        print('grade level',fk.grade_level)
        print('difficult words',textstat.difficult_words(test_data))

with open('./evaluation/output10.txt','r') as file:
        test_data = file.read()
        x = Readability(test_data)
        fk = x.flesch_kincaid()
        print('score',fk.score)
        print('grade level',fk.grade_level)
        print('difficult words',textstat.difficult_words(test_data))

with open('./evaluation/output11.txt','r') as file:
        test_data = file.read()
        x = Readability(test_data)
        fk = x.flesch_kincaid()
        print('score',fk.score)
        print('grade level',fk.grade_level)
        print('difficult words',textstat.difficult_words(test_data))

with open('./evaluation/output12.txt','r') as file:
        test_data = file.read()
        x = Readability(test_data)
        fk = x.flesch_kincaid()
        print('score',fk.score)
        print('grade level',fk.grade_level)
        print('difficult words',textstat.difficult_words(test_data))