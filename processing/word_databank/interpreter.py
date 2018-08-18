from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../')

from sys import path
path.append(DIR)

# from parser import strip_invalid_synonyms
# from master_simplifier import get_synonyms
from global_content import deconstruct, construct
from words_db import Worker

w = Worker()

def simplify(sentence):
	tokens = deconstruct(sentence)

	index = 0

	simpler_tokens = []

	for token in tokens:
		occ = w.find(token)[1]
		if len(token) > 4 and occ != -1 and occ < 100:
			simpler = get_simpler(sentence, tokens, index)
			simpler_tokens.append(simpler)
		else:
			simpler_tokens.append(token)

		index += 1

	return simpler_tokens

def get_simpler(sentence, tokens, index):
	synonyms = get_synonyms(sentence, tokens[index])
	stripped_synonyms = strip_invalid_synonyms(index, tokens, synonyms)

	print 'Synonyms:', synonyms

	word = tokens[index]
	occount = 0

	for synonym in stripped_synonyms:
		occ = w.find(synonym)[1]
		print 'Occurence Count of:', synonym + '---' + str(occ)

		if occ > occount:
			word = synonym
			occount = occ

	return word

def get_simplest(words):
	if words is None or len(words) == 0:
		return []

	common_words = [words[0]]
	occount = 0

	for loop_word in words:
		occ = w.find(loop_word)[1]
		print occ
		print 'Occurence Count of:', loop_word + '---' + str(occ)

		if occ > occount:
			print 'New Occ Standard'
			del common_words[:]
			common_words.append(loop_word)
			occount = occ
		elif occ == occount:
			print 'Old Occ Standard'
			common_words.append(loop_word)

	print 'Common Words:', common_words

	return common_words