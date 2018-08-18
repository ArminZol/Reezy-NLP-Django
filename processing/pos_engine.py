import re
from PyDictionary import PyDictionary as dict
from nltk import pos_tag, RegexpParser
from nltk.corpus import wordnet as wn
import time

NOUN = 'Noun'
VERB = 'Verb'
ADJECTIVE = 'Adjective'
ADVERB = 'Adverb'
DETERMINER = 'Determiner'

POS = [NOUN, VERB, ADJECTIVE, ADVERB]

def get_wordnet_pos(pos):
	if pos == NOUN:
		return wn.NOUN
	elif pos == VERB:
		return wn.VERB
	elif pos == ADJECTIVE:
		return wn.ADJ
	elif pos == ADVERB:
		return wn.ADV
	else:
		return None

def has_one_pos(word):
	pos_count = 0
	current_pos = None

	for pos in POS:
		synsets = wn.synsets(word, pos=get_wordnet_pos(pos))

		if len(synsets) > 0:
			pos_count += 1
			current_pos = pos

		if pos_count > 1:
			return current_pos

	return current_pos

def check_pos(pos, word):
	synsets = wn.synsets(word, pos=get_wordnet_pos(pos))

	if synsets is None:
		return False
	elif len(synsets) > 0:
		return True

	return False

def tag_one(word):
	word_type = [None] * len(word)
	tags = pos_tag(word)

	get_word_types(word_type, word, tags)

	return word_type[0]

def get_pos_tag(word_list, index):
	pos = has_one_pos(word_list[index])

	if pos != None:
		return pos

	word_type = [None] * len(word_list)
	tags = pos_tag(word_list)

	get_word_types(word_type, word_list, tags)
	#formattedSentence = get_formatted_sentence(tags)
	#get_phrases(formattedSentence, word_list, word_type)

	return word_type[index]

def get_pos_tags(word_list):
	word_type = [None] * len(word_list)
	tags = pos_tag(word_list)

	get_word_types(word_type, word_list, tags)

	return word_type

def get_formatted_sentence(tags):
	grammar = """
	VP: {<NN.*><VB>?<DT>+<IN|TO|VB.*|JJ|CD>*<NN.*|JJ>}
		{<NN.*><VB>?<IN>+<TO|VB.*|JJ|CD>+<NN.*>}
		{<NNS|NNP|IN><TO><DT><NN.*>}
		{<NN.*><TO|IN>*<PRP.*>+<NN.*>?}
	"""
	result = RegexpParser(grammar).parse(tags)

	formattedSentence = ""

	for i in range(0, result.__len__()):
		k = result[i]
		formattedSentence += str(k)

	return formattedSentence

def get_word_types(word_type, tokens, tags):
	for i in range(0, tags.__len__()):
		if tags[i].__contains__("VB") or tags[i].__contains__("VBD") or tags[i].__contains__("VBG") or tags[i].__contains__("VBN") or tags[i].__contains__("VBP") or tags[i].__contains__("VBZ") or tokens[i].lower() == "go": 
			if tokens[i].lower() != "is" or tokens[i].lower() != "was" or tokens[i].lower() != "are" or tokens[i].lower() != "each": 
				word_type[i] = VERB

		elif tags[i].__contains__("NN") or tags[i].__contains__("NNP") or tags[i].__contains__("NNPS") or tags[i].__contains__("NNS"):
			word_type[i] = NOUN
			if i >= 1:
				if tags[i - 1].__contains__("TO"):
					word_type[i] = VERB

		elif tags[i].__contains__("DT"):
			word_type[i] = DETERMINER

		elif tags[i].__contains__("JJ") or tags[i].__contains__("JJR") or tags[i].__contains__("JJS"):
			word_type[i] = ADJECTIVE

		elif tags[i].__contains__("RB") or tags[i].__contains__("RBR") or tags[i].__contains__("RBS"):
			word_type[i] = ADVERB

def get_phrases(formattedSentence, tokens, word_type):
	for i in re.finditer('VP', formattedSentence):
		find_phrase(formattedSentence, tokens, word_type, i, "Verb")

def find_phrase(formattedSentence, tokens, word_type, i, type):
	for k in re.finditer('/', formattedSentence):
		if i.end() < k.start():
			word = (formattedSentence[i.end() + 1 : k.start()])
			index = []
			for j in range(0, tokens.__len__()):
				if tokens[j] == word:
					index.append(j)
			if len(index) == 1:
				word_type[index[0]] = type
			else:
				counter = 0
				for j in re.finditer(word, formattedSentence):
					if j.start() - 3 == i.start():
						word_type[index[counter]] = type
						break
					else:
						counter += 1
			break