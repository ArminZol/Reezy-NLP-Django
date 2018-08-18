from PyDictionary import PyDictionary as dict
from global_content import *
from container import Container
from validify import is_valid
from ner import get_named_entities
from master_simplifier import simplify, simplify_word
import logging

from time import time

from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), 'ner')

from sys import path
path.append(DIR)

def simplify_weak(word):
	simplest_syn = word
	synonyms = dict.synonym(simplest_syn)

	if synonyms is None:
		return simplest_syn

	for synonym in synonyms:
		if len(synonym) < len(simplest_syn):
			simplest_syn = synonym

	return simplest_syn

def simplify_moderate(word):
	simplest_syn = [word]
	vowel_percent = get_vowel_count(simplest_syn[0]) / float(len(simplest_syn))
	synonyms = dict.synonym(simplest_syn[0])

	if synonyms is None:
		return simplest_syn[0]

	for synonym in synonyms:
		syn_vowel_percent = get_vowel_count(synonym) / float(len(synonym))
		if syn_vowel_percent < vowel_percent:
			del simplest_syn[:]
			vowel_percent = syn_vowel_percent
			simplest_syn.append(synonym)
		elif syn_vowel_percent == vowel_percent:
			simplest_syn.append(synonym)

	shortest_word = get_last_shortest_word(simplest_syn)

	return shortest_word

def simplify_strong(word):
	simplest_syn = [word]
	syllable_count = get_syllable_count(simplest_syn[0])
	synonyms = dict.synonym(simplest_syn[0])

	if synonyms is None:
		return simplest_syn[0]

	for synonym in synonyms:
		if is_popular(synonym):
			return synonym

		syn_syllable_count = get_syllable_count(synonym)
		
		if syn_syllable_count < syllable_count:
			del simplest_syn[:]
			syllable_count = syn_syllable_count
			simplest_syn.append(synonym)
		elif syn_syllable_count == syllable_count:
			simplest_syn.append(synonym)

	shortest_word = get_last_shortest_word(simplest_syn)

	return shortest_word

def simplify_sentence(sentence, personaliser=None):
	entities = [] #get_named_entities(sentence)
	print 'Named Entities:', entities

	t0 = time()

	tokens = deconstruct(sentence)

	print 'Time for tokenization:', time() - t0

	simple_sentence = []

	for index in range(len(tokens)):
		word = tokens[index]
		print '-'*50
		print 'Word:', word

		simpler_word = word

		if is_valid(word, personaliser) and word.lower() not in entities:
			print 'Is Valid'
			word_info = simplify(sentence, index, tokens, personaliser=personaliser)
			simpler_word = word_info[0]

			if index > 0 and (word_info[1] == 'a' or word_info[1] == 'an'):
				simple_sentence[index - 1] = word_info[1]

		simple_sentence.append(simpler_word)
		print 'Appended:', simpler_word

	if simple_sentence == tokens:
		constructed_sentence = sentence
	else:
		constructed_sentence = construct(simple_sentence)

	return constructed_sentence

def choose(text, personaliser=None):
	start_time = time()

	if text.strip().lower() == 'hard':
		answer = 'Easy'
	else:
		if len(text.split()) <= 1:
			answer = simplify_word(text)
		else:
			answer = simplify_sentence(text, personaliser)

	end_time = time() - start_time

	print 'Total Time:', end_time

	return answer, end_time

def test():
	sentences = [
		'The eccentric characteristic of a teacher is insufficient to mitigate the abhorrent phenomenon of partaking in the mass cultural construct that is education.',
		'Be cognisant of products you frequently use and complain about.',
		'It is imperative to allow researchers to maximise their potential through experimental science.',
		'The exponentially more convoluted technological complexion mustn\'t have permissiveness to intertwine its knowledge.',
		'Schrodinger\'s cat is a thought experiment, sometimes described as a paradox, devised by Austrian physicist Erwin Schrodinger in 1935.',
		'Your idiosyncrasies only augment the ambiguous instructions that you\'ve unsuccessfully relayed to the masses.',
		'You will soon speak more eloquently about a greater number of contentious contemporary issues due to your erudition.',
		'Don\'t let an abstruse lexicon heighten your trepidation. reezyapp.com can assuage your anxiety.',
		'I used to loathe and eschew perusing English.',
		'The ravenous throng scampered toward the delectable viands, which was impeccably arrayed on the table.',
		'To ameliorate this problem, for text heavy pages, we\'ve created a class that fluidly scales text size and line-height to optimise readability for the user.',
		'This is an indubitably impeccable matter that is also captious and capricious'
	]

	file = open('../../test_results_with_brackets.txt', 'w')

	for sentence in sentences:
		original = simplify_sentence(sentence)

		file.write(original + '\n\n')