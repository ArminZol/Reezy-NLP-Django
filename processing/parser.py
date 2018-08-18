from en import is_noun, noun, is_adjective, is_adverb
from pos_engine import get_pos_tag, check_pos
from global_content import has_same_meaning

def set_article(tokens, index, article):
	if index <= 0:
		return

	tokens[index - 1] = article

def get_article(word, tokens, index):
	article_index = index - 1

	if index <= 0:
		return tokens[0]

	if not is_noun(word) and not is_adjective(word) and not is_adverb(word):
		return tokens[article_index]

	if tokens[article_index] == 'a' or tokens[article_index] == 'an':
		proper_article = noun.article(word).split()[0]
		return proper_article
		
	return tokens[article_index]

def strip_invalid_synonyms(index, tokens, synonyms):
	word_pos = get_pos_tag(tokens, index)

	print 'POS:', word_pos

	same_pos_synonyms = []

	if word_pos == None or synonyms is None:
		return same_pos_synonyms

	for synonym in synonyms:
		if check_pos(word_pos, synonym) or ' ' in synonym:
			same_pos_synonyms.append(synonym)

	#same_meaning_synonyms = strip_invalid_meaning(tokens[index], same_pos_synonyms, word_pos)

	return same_pos_synonyms

def strip_invalid_meaning(word, same_pos_synonyms, pos):
	same_meaning_synonyms = []

	for same_pos_synonym in same_pos_synonyms:
		if has_same_meaning(word, same_pos_synonym, pos):
			same_meaning_synonyms.append(same_pos_synonym)

	return same_meaning_synonyms

def strip_xyz(synonyms):
	xyz = ['x', 'y', 'z']

	stripped_synonyms = []

	for synonym in synonyms:
		xyz_in_word = False

		for letter in xyz:
			if letter in synonym: 
				xyz_in_word = True

		if not xyz_in_word:
			stripped_synonyms.append(synonym)

	return stripped_synonyms