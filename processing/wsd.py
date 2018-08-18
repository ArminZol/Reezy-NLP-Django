from pywsd.lesk import adapted_lesk
from pos_engine import NOUN, VERB, ADJECTIVE, get_wordnet_pos

def get_disambiguated_definition(sentence, word, pos):
	translated_pos = get_wordnet_pos(pos)
	try:
		synset = adapted_lesk(sentence, word, pos=translated_pos)
	except:
		synset = None
		
	if synset is None:
		return word
	else:
		return synset.definition()

def get_disambiguated_synset(sentence, word, pos):
	translated_pos = get_wordnet_pos(pos)
	synset = adapted_lesk(sentence, word, pos=translated_pos)
	return synset
