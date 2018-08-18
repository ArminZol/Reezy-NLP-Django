from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../processing', 'ml_svm_word_difficulty')

from sys import path
path.append(DIR)

from processing import personaliser

from personaliser import Personaliser

classifier = Personaliser('testing')

def predict(word):
	return classifier.predict(word)