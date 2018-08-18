from labler import WordLabelPair, save_labels, HARD, SIMPLE, load_labels

class SurveyServer():
	from os.path import join, dirname, realpath
	DIR = join(dirname(realpath(__file__)), 'ml_svm_word_difficulty')

	from sys import path
	path.append(DIR)

	import cPickle as pickle

	from word_extractor import get_words

	labels = load_labels()

	words = get_words()

	given_words = []

	def get(self, index):
		if index >= 0 and index < len(self.words):
			return self.words[index]

	def get_next(self):
		for word in self.words:
			if not self.is_saved(word):
				if word not in self.given_words:
					self.given_words.append(word)
				return word.lower()

		return None

	def put_given(self, word, is_hard):
		original_word = word.lower()

		if original_word not in self.given_words or self.is_saved(original_word):
			return

		if is_hard:
			self.labels.append(WordLabelPair(original_word, HARD))
		else:
			self.labels.append(WordLabelPair(original_word, SIMPLE))

		self.given_words.remove(original_word)

	def is_saved(self, word):
		for label in self.labels:
			if label.word.lower() == word.lower():
				return True

		return False

	def save(self):
		save_labels(self.labels)

	def clear(self):
		self.given_words = []
		self.labels = []
		save_labels(self.labels)