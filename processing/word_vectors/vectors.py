from gensim.models import Word2Vec
import cPickle as pickle
from os.path import join, dirname, realpath

FILE_NAME = 'Word2VecModel.pkl'
PATH = join(dirname(realpath(__file__)), FILE_NAME)

model = Word2Vec.load(PATH)

TOP_NUMBER = 100

def get_most_similar(word, amount):
	try:
		return model.most_similar(word, topn=amount)
	except KeyError, e:
		print e

def get_intersection(word, synonyms):
	intersects = []

	try:
		most_similar = model.most_similar(word, topn=TOP_NUMBER)

		for synonym in synonyms:
				for similarities in most_similar:
					if synonym.lower() == similarities[0].lower():
						intersects.append(synonym)
	except KeyError, e:
		print e

	return intersects

def get_similarity(word1, word2):
	try:
		return model.similarity(word1, word2)
	except:
		return 0