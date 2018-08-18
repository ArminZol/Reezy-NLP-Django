from polyglot.text import Text
from time import time

def get_named_entities(sentence):
	t0 = time()

	words = []

	try:
		text = Text(sentence)
		entities = text.entities

		words = []

		for entity in entities:
			for word in entity:
				words.append(word.lower())
	except:
		pass

	print 'Time for NER:', time() - t0

	return words