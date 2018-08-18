from PyDictionary import PyDictionary as dictionary
from nltk.corpus import wordnet as wn

DEF_ERR_MSG = '\nNo Definition Found'
SYN_ERR_MSG = '\nNo Synonyms Found'
EXA_ERR_MSG = '\nNo Examples Found'

def define(word):
	definition = dictionary.meaning(word)
	return format_definition(definition)

def format_definition(definition):
	formatted_string = ''

	if definition is None:
		return DEF_ERR_MSG

	for key in definition.keys():
		formatted_string += '\n' + key + ':'

		for meaning in definition[key]:
			formatted_string += '\n- ' + meaning[0].upper() + meaning[1:]
			if meaning[0] == "(":
				formatted_string += ")"

	print 'Formatted Definition:', formatted_string

	return formatted_string

def synonyms(word):
	synonyms = dictionary.synonym(word)
	return format_synoyms(synonyms)

def format_synoyms(synonyms):
	formatted_string = ''

	if synonyms is None:
		return SYN_ERR_MSG

	for synonym in synonyms:
		formatted_string += '\n- ' + synonym[0].upper() + synonym[1:]

	print 'Formatted Synonyms:', formatted_string

	return formatted_string

def examples(word):
	synsets = wn.synsets(word)

	if synsets is not None and len(synsets) > 0:
		return format_examples(word, synsets[0].examples())

	return EXA_ERR_MSG

def format_examples(word, examples):
	formatted_string = ''

	for example in examples:
		if word in example:
			example = example.replace(word, '<i>' + word + '</i>')
			formatted_string += '\n- ' + example[0].upper() + example[1:]

	return formatted_string