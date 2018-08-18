# -*- coding: utf-8 -*-

from os.path import join, dirname, realpath
from nltk import word_tokenize
import helper_functions

class Analyzer():
	worker = None

	def __init__(self, worker):
		self.worker = worker

	def fitfile(self, file):
		for line in file.readlines():
			stripped_line = line.strip('\n').strip()
	
			self.fit(stripped_line)

	def fit_corpus(self, corpus):
		processed_tokens = helper_functions.full_process(corpus)

		string_counts = helper_functions.get_string_count(processed_tokens)

		for key, value in string_counts.iteritems():
			self.worker.save(key, occurence_count=value)
			print 'Added:', key
			print 'Occurence Count:', value
			print '-'*20

	def fit(self, text):
		tokens = self.get_tokens(text)

		processed_tokens = helper_functions.full_process(tokens)

		string_counts = helper_functions.get_string_count(processed_tokens)

		for key, value in string_counts.iteritems():
			self.worker.save(key, occurence_count=value)
			print 'Added:', key
			print 'Occurence Count:', value
			print '-'*20

	def get_tokens(self, text):
		try:
			text = text.encode('utf-8').strip()
			tokens = word_tokenize(text)
			print 'Pre tokens:', tokens
			return tokens
		except:
			print 'Skipping due to decoding error:', text
			return []

	def calculate_ranges(self):
		self.worker.cursor.execute('SELECT * FROM words')

		most_common = {'word':0, 'occount':0}
		least_common = {'word':0, 'occount':1000000}

		fetched = self.worker.cursor.fetchall()

		for word in fetched:
			if word[1] > most_common['occount']:
				most_common['occount'] = word[1]
				most_common['word'] = word[0]

			if word[1] < least_common['occount']:
				least_common['occount'] = word[1]
				least_common['word'] = word[0]

		return most_common, least_common

class Worker():
	from string import ascii_lowercase
	from math import pow
	import sqlite3

	alphabet = list(ascii_lowercase + "'")

	TEST = 'test.db'
	MAIN_DB = 'word_info (large).db'
	SMALL_DB = 'word_info.db'

	PATH = join(dirname(realpath(__file__)), SMALL_DB)

	database = sqlite3.connect(PATH, check_same_thread=False)
	cursor = database.cursor()

	def __init__(self):
		self.cursor.execute("SELECT name from sqlite_master WHERE type='table' AND name='words'")
		
		if self.cursor.fetchone() == None:
			self.cursor.execute('''CREATE TABLE words (word, occurence_count)''')

	def numerify(self, word):
		word_length = len(word)
		word = word.lower()

		total = 0

		alphabet_length = len(self.alphabet)

		for char_index in range(word_length):
			char = word[char_index]

			if char not in self.alphabet: return 0

			alphabet_value = pow(alphabet_length, char_index)

			try:
				final_value = float(alphabet_value * self.alphabet.index(char))
			except:
				print '------------------'
				print 'Word:', word, 'cannot be converted to a number'
				return 0

			final_value /= 1000000.

			total += final_value

		print 'Number', total, 'represents word "' + word + '"'

		return total

	def db_contains(self, text):
		self.cursor.execute('SELECT * FROM words WHERE word=?', (text,))
		
		value = self.cursor.fetchone()

		if value == None:
			return False
		else :
			return value

	def find(self, text):
		value = self.db_contains(text)

		if not value:
			return (-1, -1)
		else:
			return value

	def save(self, word, occurence_count=1):
		if not self.db_contains(word):
			self.cursor.execute('INSERT INTO words VALUES (?, ?)', (word, occurence_count))
		else:
			word_occurence_pair = self.cursor.execute('SELECT * FROM words WHERE word=?', (word,))
			saved_occurence_count = word_occurence_pair.fetchone()[1] # int cast when using test db
			self.cursor.execute('UPDATE words SET occurence_count=? WHERE word=?', (saved_occurence_count+occurence_count, word)) # str cast when using test db

	def finish(self):
		# self.clean_junk()
		self.database.commit()
		print 'Committing Changes...'
		self.database.close()
		print 'Database Connection Closed...'

	def clean_junk(self):
		self.cursor.execute('DELETE FROM words WHERE occurence_count=0')
		print 'Cleaning Junk...'

	def tota_occ(self):
		self.cursor.execute('SELECT * FROM words')
		total = 0
		
		for word in self.cursor.fetchall():
			total += word[1]

		return total

	def max_occ(self):
		self.cursor.execute('SELECT * FROM words')
		max_num = 0
		
		for word in self.cursor.fetchall():
			if word[1] > max_num:
				max_num = word[1]

		return max_num

# w = Worker()
# a = Analyzer(w)

# from nltk.corpus import webtext
# from nltk.corpus import nps_chat
# from nltk.corpus import brown
# from nltk.corpus import reuters
# from nltk.corpus import gutenberg

# def get_webtext():
# 	return webtext.words()

# def get_nps_chats():
# 	return nps_chat.words()

# def get_brown_corpus():
# 	return brown.words()

# def get_reuters_corpus():
# 	return reuters.words()

# def get_gutenberg():
# 	return gutenberg.words()

# def get_all():
# 	return get_webtext() + get_brown_corpus() + get_reuters_corpus() + get_gutenberg()

# print 'Imported'

# all_corpora = get_all()

# print 'Retrieved All'

# a.fit_corpus(all_corpora)

# w.finish()