class Personaliser():
	import os

	FOLDER_NAME = 'ml_svm_word_difficulty'

	DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME)

	from sys import path
	path.append(DIR)

	from word_extractor import get_words
	from classifier import update_clf

	_DEFAULT_CLASSIFIER_NAME = 'default_classifier.pkl'
	_DEFAULT_LABELS_NAME = 'default_labels.pkl'

	_DEFAULT_CLASSIFIER_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME, _DEFAULT_CLASSIFIER_NAME)
	_DEFAULT_LABELS_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME, _DEFAULT_LABELS_NAME)

	_clf = None

	_clf_load_error = None

	_labels_load_error = None

	_word_index = 0

	_labels = None

	_updates = []

	_owner = None

	def __init__(self, owner):
		if self._clf is None:
			self._load_default_clf()

		if self._labels is None:
			self._load_default_labels()

		if self._owner is None:
			self._owner = owner

	def _load_default_clf(self):
		import cPickle as pickle
		try:
			file = open(self._DEFAULT_CLASSIFIER_LOCATION, 'rb')
			self._clf = pickle.load(file)
			file.close()
		except EOFError as eof:
			print eof
			self._clf_load_error = eof
		except IOError as io:
			print io
			self._clf_load_error = io
		except Exception as e:
			print e
			self._clf_load_error = e

	def _load_default_labels(self):
		import cPickle as pickle
		try:
			file = open(self._DEFAULT_LABELS_LOCATION, 'rb')
			self._labels = pickle.load(file)
			file.close()
		except EOFError as eof:
			self._labels_load_error = eof
		except IOError as io:
			self._labels_load_error = io
		except Exception as e:
			self._labels_load_error = e

	def get_clf(self):
		return self._clf

	def get_word_index(self):
		return self._word_index

	def next_word_index(self):
		self._word_index += 1

	def update(self, word, is_hard):
		from labler import HARD, SIMPLE, WordLabelPair

		if is_hard:
			label = HARD
		else:
			label = SIMPLE

		wlp = WordLabelPair(word, label)

		self._updates.append(wlp)

	def _refurbish(self):
		if self._labels is None:
			return

		refurbish = False

		for label in self._labels:
			for update in self._updates:
				if label.word == update.word:
					if label.label != update.label:
						label.label = update.label
						refurbish = True

		if refurbish:
			self._clf = update_clf(self._labels)
			# save()

	def predict(self, word):
		if self._clf_load_error is None:
			from quantifier import quantify
			import numpy as np

			data = quantify(word)
			print 'Quantified Data:', data
			reshaped_data = np.reshape(data, (1, -1))
			print 'Rehaped Data:', reshaped_data
			prediction = self._clf.predict(reshaped_data)
			print 'Prediction Result: ', prediction
			return prediction