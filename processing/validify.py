from global_content import word_is_difficult
from popular_data import is_popular
from en import is_noun, is_verb, is_adjective, is_adverb
from simplify_exceptions import simplification_exclusions, simplification_inclusions

def is_valid(word, personaliser=None):
	if word.lower() in simplification_inclusions:
		return True
	elif word.lower() in simplification_exclusions:
		return False

	if not valid_pos(word) or not word_is_difficult(word, None) or is_popular(word):
		return False

	return True

def valid_pos(word):
	if not is_noun(word) and not is_verb(word) and not is_adjective(word) and not is_adverb(word) and len(word) < 7:
		return False

	return True