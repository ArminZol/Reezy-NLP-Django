from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../')

from sys import path
path.append(DIR)

from global_content import word_is_difficult

import cPickle as pickle

HARD = 1
SIMPLE = 0

from os.path import join, dirname, realpath, splitext, basename

LABEL_LOC = join(dirname(realpath(__file__)), 'labels.pkl')
AUTOMATIC_LABELS_LOC = join(dirname(realpath(__file__)), 'automatic_labels.pkl')

def load_labels(automatic=False):
	try:
		if automatic:
			file = open(AUTOMATIC_LABELS_LOC, 'rb')
		else:
			file = open(LABEL_LOC, 'rb')
		labels = pickle.load(file)
		file.close()
	except EOFError:
		return []
	except IOError:
		return []

	return labels

def get_train_ready_labels(labels):
	clean_labels = []
	
	for label in labels:
		clean_labels.append(label.label)

	return clean_labels

def generate_custom_labels(words):
	from nltk.corpus import wordnet as wn
	from PyDictionary import PyDictionary as pydict
	from vectorizer import get_organized_features_and_names

	labels = load_labels()

	features, feature_names = get_organized_features_and_names(words)

	print 'Answer "y" for hard and "n" for simple, anything else to quit'
	
	feature_count = len(feature_names)
	word_count = len(words)
	start = len(labels)

	for i in range(start, word_count):
		word = words[i]
		print 'Word:', word

		print 'Info:'

		for j in range(feature_count):
			print '\t-' + feature_names[j] + ':', features[i][j]

		# lemmas = []

		# for synset in wn.synsets(word):
		# 	for lemma in synset.lemmas():
		# 		lemmas.append(lemma.name())

		# print 'Synonyms:', lemmas, pydict.synonym(word)

		answer = raw_input('Is the word "' + word + '"" hard? ')

		if answer.lower() == 'y':
			labels.append(WordLabelPair(word, HARD))#hard
		elif answer.lower() == 'n':
			labels.append(WordLabelPair(word, SIMPLE))#simple
		else:
			break

		print '-------------------'

	save_labels(labels)

	return labels

def self_train():
	from word_extractor import get_words

	words = get_words()

	labels = []

	for word in words:
		if word_is_difficult(word):
			labels.append(WordLabelPair(word, HARD))
		else:
			labels.append(WordLabelPair(word, SIMPLE))

	file = open(AUTOMATIC_LABELS_LOC, 'wb')
	pickle.dump(labels, file)
	file.close()

def save_labels(labels):
	file = open(LABEL_LOC, 'wb')
	pickle.dump(labels, file)
	file.close()

def remove_copies(words):
	return list(set(words))

def update_auto_labels(wlp):
	auto = load_labels(automatic=True)

	wlp = remove_copies(wlp)

	index = 0

	for label in auto:
		index = 0

		for word_label_pair in wlp:
			if label.word == word_label_pair.word:
				label.label = word_label_pair.label
				del wlp[index]

			index += 1

	for word_label_pair in wlp:
		auto.append(word_label_pair)

	auto = remove_copies(auto)

	file = open(AUTOMATIC_LABELS_LOC, 'wb')
	pickle.dump(auto, file)
	file.close()

class WordLabelPair:
	word = ''

	label = SIMPLE

	def __init__(self, word, label):
		__module__ = splitext(basename(__file__))[0]
		print __module__

		self.word = word

		if label == HARD or label == SIMPLE:
			self.label = label

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.word + ' : ' + str(self.label)