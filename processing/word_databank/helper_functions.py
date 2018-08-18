from os.path import join, dirname, realpath
from string import punctuation, ascii_lowercase
import cPickle as pickle

words = []

FILE_NAME = 'words.pkl'

PATH = join(dirname(realpath(__file__)), '../' + FILE_NAME)

try:
	file = open(PATH, 'rb')
	words = pickle.load(file)
	file.close()
except EOFError:
	print 'Failed to get words (EOFError)'

contractions = ['\'m', '\'re', '\'s', '\'ll', '\'d', '\'ve', '\'ve', 'n\'t']

def save_words():
	file = open(PATH, 'wb')
	pickle.dump(clean_words(), file)
	file.close()

def clean_words():
	clean_words = []

	for word in words:
		if len(word) > 2 and word not in clean_words and not hasNumbers(word):
			clean_words.append(word.lower())

	return clean_words

def concat_contract(tokens):
	tokens_length = len(tokens)

	concat_list = []
	
	for index in range(tokens_length):
		token = tokens[index]

		if token in contractions and index > 0:
			print 'Contraction:', token
			concat_list_length = len(concat_list)
			concat_list_last_index = concat_list_length - 1
			print 'Concatenating to:', concat_list[concat_list_last_index] + token
			concat_list[concat_list_last_index] = concat_list[concat_list_last_index] + token
		else:
			concat_list.append(token)

	return concat_list

def preprocess(tokens):
	processed = []

	for token in tokens:
		token_to_add = token

		if '-' in token:
			split = token.split('-')
			processed += split
		else:
			processed.append(token)

	print 'Pre-Processed:', processed

	return processed

def clean_nonwords(tokens):
	clean = []

	for token in tokens:
		valid = True

		for char in token:
			if char not in ascii_lowercase:
				valid = False
				break

		if valid:
			clean.append(token)

	return clean

def get_string_count(tokens):
	words_counts = {}

	for token in tokens:
		if token not in words_counts.keys():
			words_counts[token] = 1
		else:
			words_counts[token] += 1

	return words_counts

MIN_LENGTH = 1

def get_valid(tokens):
	valid_tokens = []

	for token in tokens:
		if len(token) > MIN_LENGTH and is_word(token):
			valid_tokens.append(token)

	return valid_tokens

def is_word(word):
	if word in words:
		return True
	return False

def full_process(tokens):
	concat_tokens = concat_contract(tokens)

	print 'Tokens:', concat_tokens
	
	valid_tokens = get_valid(concat_tokens)
	cleaned_tokens = clean_nonwords(valid_tokens)
	processed_tokens = preprocess(cleaned_tokens)

	print 'Processed Tokens:', processed_tokens

	return processed_tokens

def get_ngrams(tokens, gram):
	token_count = len(tokens)

	ngrams = []

	for i in range(token_count):
		ngram = ''

		if i + gram <= token_count:
			for j in range(gram):
				ngram += ' ' + tokens[i + j]
				ngram = ngram.strip()

		ngrams.append(ngram)

		if i + gram == token_count:
			break

	return ngrams