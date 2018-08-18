from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../')
DIR2 = join(DIR, 'word_databank')

from sys import path
path.append(DIR)
path.append(DIR2)

from global_content import get_syllable_count
from words_db import Worker

from nltk.corpus import wordnet as wn

vowels = ['a', 'e', 'i', 'u', 'o']

w = Worker()

def quantify_adjacent_vowels(word):
	represetation = 0
	
	vowels_array = [False, False, False]

	for letter in word:
		if letter in vowels:
			if not vowels_array[0]:
				vowels_array[0] = True
			elif not vowels_array[1]:
				vowels_array[1] = True
			elif not vowels_array[2]:
				vowels_array[2] = True
		else:
			if vowels_array[0] and vowels_array[1] and not vowels_array[2]:
				represetation = 1
				break
			vowels_array = [False, False, False]

	return represetation

def quantifiy_syllable_count(word):
	return get_syllable_count(word)

# def quantify_words(words):
# 	represetation = []

# 	for word in words:
# 		represetation.append(w.numerify(word))

# 	return represetation

def quantify_synonyms(word):
	count = 0

	for synset in wn.synsets(word):
		for lemma in synset.lemmas():
			count+=1

	return count

def quantifiy_popularity(word):
	return w.find(word)[1]

def quantify(word):
	return quantify_adjacent_vowels(word), quantifiy_syllable_count(word), quantifiy_popularity(word)#, quantify_synonyms(word)

#quantifiy_popularity(['hello', 'yes', 'augment', 'eaisdfg', 'eafue'])