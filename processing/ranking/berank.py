from helper_funcs import get_letter_values, get_syllable_count, scale_occurence_count, get_occurence_count, get_similarity, saved_ranges
from math import fsum, e
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

BOLD = '\033[1m'
END = '\033[0m'

def ngram_rank(ngram):
	words = ngram.strip().split()

	if len(words) == 1:
		return berank_value(words[0])

	ranks = []

	for word in words:
		if word not in stopwords:
			rank = berank_value(word)
			ranks.append(rank)

	if len(ranks) == 0:
		return 0

	# final_score = sum(ranks) / (len(ranks) * 10.)

	return min(ranks)

def rank(words):
	ranks = {}

	for word in words:
		value = ngram_rank(word)
		ranks[word] = value
		print '-'*10

	return ranks

def get_simplest(words):
	ranks = rank(words)

	current_highest = 0
	current_word = None

	for word, loop_rank in ranks.iteritems():
		if loop_rank > current_highest:
			current_highest = loop_rank
			current_word = word

	return current_word

def berank_value(word):
	if len(word) <= 0:
		return 0

	print 'Word:', word
	vowel_values = get_letter_values(word)
	# if not silent: print 'Vowel Values:', vowel_values
	value_sum = fsum(vowel_values)
	# if not silent: print 'Value Sum:', value_sum

	vowel_percentage = value_sum / len(word)
	# if not silent: print 'Vowel Percentage:', vowel_percentage
	vowel_assesment = 1 - vowel_percentage
	print 'Vowel Assesment:', vowel_assesment

	syllable_count = get_syllable_count(word)
	print 'Syllables:', syllable_count

	syllable_vowel_rank = pow(vowel_assesment, syllable_count)
	# 'if not silent: print ''Syllable/Vowel Rank:', syllable_vowel_rank

	final_rank = syllable_vowel_rank * scale_occurence_count(word)
	print 'BeRank:', final_rank

	return final_rank

def after_rank(word, original, berank):
	after_rank = berank * get_similarity(original, word)

	print 'After rank of', word, ':', after_rank

	return after_rank

def get_best_after_rank(words, original):
	print BOLD + '-'*10 + '\nAfter Rank\n' + '-'*10 + END

	ranks = []

	for word in words:
		value = berank_value(word, silent=True)
		ranks.append(value)
		print '-'*10

	if len(ranks) == 0:
		return original

	for index in range(len(ranks)):
		ranks[index] *= after_rank(words[index], original, ranks[index])

	max_value = max(ranks)

	occ_count = ranks.count(max_value)

	if occ_count == 1:
		return words[ranks.index(max_value)]
	else:
		simplest_words = []
		index = 0

		for number in ranks:
			if number == max_value:
				simplest_words.append(words[index])

			index += 1

		print BOLD + '-'*10 + '\nBeRank after After Rank\n' + '-'*10 + END

		return get_simplest(simplest_words, silent=True)

def sigmoid_berank(word):
	vowel_values = get_letter_values(word)
	value_sum = fsum(vowel_values)

	x = value_sum / len(word)
	s = get_syllable_count(word)
	p = float(saved_ranges[0] - get_occurence_count(word)) / float(saved_ranges[0] - saved_ranges[1])

	return f(x, s, p)

def f_x(x):
	denominator = 1 + pow(e, 10*(x-0.5))

	return 1. / denominator

def f_s(s):
	denominator = 1 + pow(e, 2.5*(s-3))

	return 1. / denominator

def f_p(p):
	denominator = 1 + pow(e, -10*(p-0.5))

	return 1. / denominator

def f(x, s, p):
	return f_x(x) * f_s(s) * f_p(p)