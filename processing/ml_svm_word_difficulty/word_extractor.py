from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../word_databank')

from sys import path
path.append(DIR)

import cPickle as pickle

from words_db import Worker
from nltk.corpus import wordnet as wn

WORDS_LOC = join(dirname(realpath(__file__)), '../words.pkl')

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def generate_words_list():
	words = []
	w = Worker()

	for synset in list(wn.all_synsets()):
		for lemma in synset.lemmas():
			if w.find(lemma.name().lower())[1] > 0 and not hasNumbers(lemma.name()) and lemma.name().lower() not in words:
				print 'Appending word:', lemma.name().lower()
				words.append(lemma.name().lower())

	save(words)

def get_words(num=-1):
	words = []

	try:
		file = open(WORDS_LOC, 'rb')
		words = pickle.load(file)
		file.close()
	except EOFError:
		print 'Failed to get words (EOFError)'

	count = 0

	return_words = []

	for word in words:
		if num == count and num != -1:
			break
		
		return_words.append(word)

		count += 1

	return return_words