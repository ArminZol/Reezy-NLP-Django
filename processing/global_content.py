from nltk import word_tokenize
from string import punctuation as punct
from en import noun
from textstat.textstat import textstat
from popular_data import is_popular
from PyDictionary import PyDictionary as dict
from property_checker import starts_with_vowel
from simplify_exceptions import simplification_exceptions, Word

def get_exceptions(word):
	exceptions = []

	for key in simplification_exceptions.keys():
		if key == word.lower():
			exceptions += simplification_exceptions[key].words

	return list(set(exceptions))

def clean_list(words, exceptions):
	print 'Initial words:', words
	print 'Exceptions', exceptions
 	stripped_synonyms = remove('_', words)
	stripped_synonyms = list(set(stripped_synonyms))
	stripped_synonyms = clear_elements(stripped_synonyms, exceptions)
	print 'End words', stripped_synonyms
	return stripped_synonyms

def remove(char, words):
	clean_words = []

	for word in words:
		if char in word:
			clean_words.append(word.replace(char, ' '))
		else:
			clean_words.append(word)

	return clean_words

def clear_elements(words, elements):
	cleared_words = []

	for word in words:
		if word not in elements:
			cleared_words.append(word)

	return cleared_words

def get_vowel_count(word):
	vowels = ['a', 'e', 'i', 'o', 'u']

	count = 0

	for vowel in vowels:
		count += word.count(vowel)

	return count

def has_vowels_side_by_side(word):
	vowels = ['a', 'e', 'i', 'o', 'u']

	just_passed = False

	for letter in word:
		if letter in vowels:
			if just_passed:
				return True

			just_passed = True
		else:
			just_passed = False

	return False

def has_letters_side_by_side(word):
	prev_letter = ''

	for letter in word:
		if letter == prev_letter:
			return True
		else:
			prev_letter = letter

	return False

def get_last_shortest_word(words):
	shortest_length = len(words[0])
	shortest_word = words[0]

	for word in words:
		if len(word) < shortest_length:
			shortest_length = len(word)
			shortest_word = word

	return shortest_word

def word_is_difficult(word, personaliser=None):
	from personaliser import Personaliser
	
	if personaliser is not None:
		HARD = 1
		
		prediction = personaliser.predict(word)[0]

		if prediction == HARD:
			return True

	length = len(word)

	if length > 4:
		syllable_count = get_syllable_count(word)
		print 'Syllable Count:', syllable_count
		vowel_count = get_vowel_count(word)

		if starts_with_vowel(word):
			vowel_count += 1

		#change 2 to 1.7 to make it simplify "augment" but screw up other stuff
		if syllable_count > 2 or vowel_count > length / 3.:#* .15:#length * 0.33
			return True
		return False

	return False

def construct(words):
	sentence = ''

	first_single_quote = False
	first_double_quote = False

	next_space = True

	print 'Constructing...'
	print 'Tokens:', words

	for word in words:
		is_punctuation = False

		if word is None:
			sentence += ' NoneErr'
		else:
			for punctuation in punct:
				if punctuation in word:
					is_punctuation = True
					print "Word With Punctuation:", word
					print "Type of Punctuation:", punctuation
					
					if (word == '\'\'' or punctuation == '`') and len(word) == 2:

						if first_double_quote:
							sentence += '"'
							first_double_quote = False
						else:
							if not next_space: sentence += '"'
							else: sentence += ' "'
							first_double_quote = True
							next_space = False

					elif word == '\'':
						sentence += word

						if not next_space:
							next_space = True

					elif word == '[' or word == '{' or word == '(':
						sentence += ' ' + word
						next_space = False
					elif word == ']' or word == '}' or word == ')':
						sentence += word

						if not next_space:
							next_space = True
					elif len(word) > 3:
						sentence += ' ' + word
					else:
						sentence += word

						if not next_space:
							next_space = True

					break

			if not is_punctuation and next_space:
				sentence += ' ' + word
			elif not is_punctuation and not next_space:
				sentence += word
				next_space = True

	return sentence

def has_same_meaning(word1, word2, pos):
  def1 = dict.meaning(word1)
  def2 = dict.meaning(word2)

  if pos in def1 and pos in def2:
    def1_pos = def1[pos]
    def2_pos = def2[pos]

    def1_len = len(def1_pos)
    def2_len = len(def2_pos)

    if def1_len > def2_len:
      for def_1 in def1_pos:
        if def_1 in def2_pos:
          return True
    else:
      for def_2 in def2_pos:
        if def_2 in def1_pos:
          return True
  else:
    return False

def get_syllable_count(word):
	return textstat.syllable_count(word)

def deconstruct(text):
	return word_tokenize(text)

def to_plural(word):
	return noun.plural(word)

def to_singular(word):
	return noun.singular(word)