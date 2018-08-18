from PyDictionary import PyDictionary as dict
from participle_engine import get_tense, apply_tense, apply_tense_list
from parser import strip_invalid_synonyms, get_article, set_article
from popular_data import get_most_popular_from_misc
from wsd import get_disambiguated_synset, get_disambiguated_definition
from global_content import clean_list, get_exceptions
from pos_engine import get_pos_tag
import oxf_synonyms

from time import time

from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), 'ranking')

from sys import path
path.append(DIR)

from berank import get_simplest, get_best_after_rank

def get_synonyms(word, synset):
	syn_list = []

	if not (synset is None):
		for lemma in synset.lemmas():
			syn_list.append(lemma.name())

	# for hype in synset.hypernyms():
	# 	for lemma in hype.lemmas():
	# 		syn_list.append(lemma.name())

	# for hypo in synset.hyponyms():
	# 	for lemma in hypo.lemmas():
	# 		syn_list.append(lemma.name())

	try:
		synonyms = dict.synonym(word)
	except:
		synonyms = None

	if synonyms is None:
		return syn_list

	return synonyms + syn_list

def simplify(sentence, index, tokens, exceptions=[None, ''], personaliser=None):
	word = tokens[index]
	pos = get_pos_tag(tokens, index)
	tense = get_tense(word, pos)
	t0 = time()
	synset = get_disambiguated_synset(sentence, word, None)
	synonyms = get_synonyms(word, synset) #+ oxf_synonyms.get_synonyms(word)
	print 'Time for Synonyms:', time() - t0

	exceptions += get_exceptions(word)
	print 'Exceptions:', exceptions

	t0 = time()
	clean_stripped_synonyms = clean_list(synonyms, exceptions)
	stripped_synonyms = tense_or_define(index, tokens, clean_stripped_synonyms, tense)
	print 'Time for Stripped Synonyms:', time() - t0

	if stripped_synonyms is None or len(stripped_synonyms) == 0:
		return define(word, synset), None

	print 'Tense:', tense
	print 'Stripped Synonyms:', stripped_synonyms
	print 'Defnition:', dict.meaning(word)

	t0 = time()

	simplest_word = get_simplest(stripped_synonyms)

	# if simplest_word != word:
	# 	stripped_synonyms = filter(lambda a: a != word, stripped_synonyms)
	# 	simplest_word = get_best_after_rank(stripped_synonyms, word)

	# simplest_word = ''

	# if personaliser is not None:
	# 	print 'Simple Predictions'

	# 	for synonym in stripped_synonyms :
	# 		prediction = personaliser.predict(synonym)

	# 		if prediction == 0:
	# 			print 'Simple Word:', synonym
	# 			simplest_word = synonym

	print 'Time for Simplest Word:', time() - t0
	
	if simplest_word == None:
		return word, None

	stored_word = simplest_word
	simplest_word = apply_tense(simplest_word, tense)
	print 'Simplest Word After Tense:', simplest_word

	if simplest_word in exceptions:
		exceptions.append(stored_word)
		simplification = simplify(sentence, index, tokens, exceptions=exceptions)
		simplest_word = simplification[0]
		article = simplification[1]

	print 'Simple Word:', simplest_word
	article = get_article(simplest_word, tokens, index)
	print 'Article:', article
	set_article(tokens, index, article)

	if simplest_word.lower() == word.lower():
		return define(word, synset), article
	elif ' ' in simplest_word:
		return word + ' (' + simplest_word + ')', article
	else:
		return simplest_word.upper(), article

def tense_or_define(index, tokens, clean_stripped_synonyms, tense):
	stripped_synonyms = strip_invalid_synonyms(index, tokens, clean_stripped_synonyms)

	if stripped_synonyms is None or len(stripped_synonyms) == 0:
		applied_tense_stripped_synonyms = apply_tense_list(clean_stripped_synonyms, tense)
		stripped_synonyms = strip_invalid_synonyms(index, tokens, applied_tense_stripped_synonyms)

	return stripped_synonyms

def define(word, synset):
  if synset is None:
		return word

  return ' ' + word + ' [' + synset.definition() + ']'

def simplify_word(word):
	tense = get_tense(word)
	synonyms = dict.synonym(word)

	print 'Synonyms:', synonyms

	if synonyms is None or len(synonyms) == 0:
		return word

	for synonym in synonyms:
		synonym = apply_tense(synonym, tense)

	simplest_word = get_simplest(synonyms)

	if simplest_word == None:
		return word

	return simplest_word