# -*- coding: utf-8 -*-

from os import path

FILE_NAME_2 = 'popular_words_for_simplification.txt'
dirname = path.dirname(path.realpath(__file__))

popular_words_for_simplification = [word.rstrip('\n') for word in open(path.join(dirname, FILE_NAME_2))]

new_data = []

for word in popular_words_for_simplification:
	lower_word = ''

	for letter in word:
		lower_word += letter.lower()

	new_data.append(lower_word)


f = open('popular_words_for_simplification.txt', 'w')

for w in new_data:
	f.write(w)
	f.write('\n')

f.close()