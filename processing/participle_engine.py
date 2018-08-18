from en import is_verb, verb, is_noun, noun
from global_content import to_singular, to_plural

EXCEPTIONS = ('kindness', 'permissiveness', 'means')

def get_tense(word, pos=None):
	infinitive_word = apply_tense(word, 'infinitive')
	if is_verb(infinitive_word) and infinitive_word != '':
		return verb.tense(word)
	else:
		singular = to_singular(word)

		if singular != word and (is_noun(singular) or pos == 'Noun'):
			return 'plural noun'
		elif is_noun(word) or pos == 'Noun':
			return 'singular noun'
		else:
			return 'None'

def apply_tense_list(words, tense):
	new_words = []

	for word in words:
		new_words.append(apply_tense(word, tense))

	return new_words

def apply_tense(word, tense):
	if word.lower() in EXCEPTIONS or word[-1].lower() == '':
		return word
	try:
		if '1' in tense:
			return get_from_view(word, tense, 1)
		elif '2' in tense:
			return get_from_view(word, tense, 2)
		elif '3'in tense:
			return get_from_view(word, tense, 3)
		else:
			if tense == 'past':
				return verb.past(word)
			elif tense == 'past participle':
				return verb.past_participle(word)
			elif tense == 'infinitive':
				return verb.infinitive(word)
			elif tense == 'present participle':
				return verb.present_participle(word)
			elif tense == 'past plural':
				return get_custom_word(word, 0, False, True)
			elif tense == 'present plural':
				return get_custom_word(word, 0, False, False)
			elif tense == 'singular noun':
				return get_subject_verb_agreement(word, True)
			elif tense == 'plural noun':
				return get_subject_verb_agreement(word, False)
			else:
				return word
	except:
		return word

def get_from_view(word, tense, view):
	if 'present' in tense:
		return get_custom_word(word, view, True, False)
	elif 'past' in tense:
		return get_custom_word(word, view, True, True)

def get_custom_word(word, view, singular, past):
	if view == 0:
		return get_no_view(word, past)
	else:
		return get_with_view(word, view, past)

def get_subject_verb_agreement(word, singular):
	if singular:
		return to_singular(word)
	else:
		return to_plural(word)

def get_no_view(word, past):
	if past:
		return verb.past(word)
	else:
		return verb.present(word)

def get_with_view(word, view, past):
	if past:
		return verb.past(word, person=view)
	else:
		return verb.present(word, person=view)