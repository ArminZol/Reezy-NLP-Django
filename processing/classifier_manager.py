import cPickle as pickle
import os

FILE_NAME = 'classifiers.pkl'

DICT_LOC = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), FILE_NAME)

BACKUP_DICT_LOC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), FILE_NAME)

def load():
	try:
		file = open(DICT_LOC, 'rb')
		classifiers = pickle.load(file)
		file.close()
	except EOFError:
		return {}
	except IOError:
		return {}

	return classifiers

def save():
	file = open(DICT_LOC, 'wb')
	pickle.dump(classifiers, file)
	file.close()

	backup()

def backup():
	file = open(BACKUP_DICT_LOC, 'wb')
	pickle.dump(classifiers, file)
	file.close()

classifiers = load()