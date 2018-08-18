from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../word_databank')
# DIR2 = join(dirname(realpath(__file__)), '../word_vectors')

from sys import path
path.append(DIR)
# path.append(DIR2)

from textstat.textstat import textstat
from words_db import Worker, Analyzer

# import vectors

w = Worker()
a = Analyzer(w)

vowels = ['a', 'e', 'i', 'o', 'u']
letters = ['z', 'x']

largest, smallest = a.calculate_ranges()
occurence_range = largest['occount'] - smallest['occount']
saved_ranges = (largest['occount'], smallest['occount'], occurence_range)

def get_occurence_count(word):
	count = w.find(word)[1]

	# if not silent: print 'Occurence Count:', count

	if count <= 0:
		return 0

	return count

def scale_occurence_count(text):
	occurence_count = float(get_occurence_count(text))

	occurence_range = float(saved_ranges[2])
	max_occurence = float(saved_ranges[0])

	if occurence_count <= 0:
		return 0

	if occurence_count == max_occurence - occurence_range:
		return occurence_count / max_occurence

	scaled_value = 1 - ((max_occurence - occurence_count) / occurence_range)

	return scaled_value

def get_syllable_count(word):
	return textstat.syllable_count(word)

def get_significant_letter_rank_and_weight(word):
	letter_rank = []
	letter_weights = []

	index = 0

	for letter in word:
		if letter in vowels:
			next_letter = check_next_vowel(word, index)
			letter_rank.append(1.)

			if next_letter != False:
				if next_letter == letter:
					letter_weights.append(.25)
				else:
					letter_weights.append(.75)
			else:
				letter_weights.append(.5)
		elif letter in letters:
			if letter == 'x':
				letter_rank.append(.9)
			else:
				letter_rank.append(1.)
			letter_weights.append(.85)

		index += 1

	return letter_rank, letter_weights

def get_letter_values(word):
	rank_and_weights = get_significant_letter_rank_and_weight(word)

	values = []

	for i in range(len(rank_and_weights[0])):
		letter_rank = rank_and_weights[0][i]
		letter_weight = rank_and_weights[1][i]
		values.append(letter_rank*letter_weight)

	return values

def check_next_vowel(word, index):
	word_length = len(word)

	for i in range(index, word_length):
		if i < word_length - 1:
			letter = word[i+1]

			if letter in vowels:
				return letter
			else:
				return False

	return False

def get_similarity(word1, word2):
	return None#vectors.get_similarity(word1, word2)