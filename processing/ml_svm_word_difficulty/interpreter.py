from labler import WordLabelPair
import classifier
from quantifier import quantify

from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../')

from sys import path
path.append(DIR)

from personaliser import Personaliser

print 'Enter "q" to quit'

user_input = raw_input('Would you like to train a new module (N) or use an existing one (E)? ')

new = False

run = True

if user_input.lower() == 'n':
	learner = classifier.WordLearner()
	new = True
elif user_input.lower() == 'e':
	personaliser = Personaliser('Test')
else:
	run = False

while run:
	user_input = raw_input('Enter a word to test: ')

	if user_input == 'q':
		break

	if user_input == 'p' and new:
		learner.plot()

	if new:
		label = learner.predict(quantify(user_input))
	else:
		label = personaliser.predict(user_input)

	if label[0] == 0:
		print 'Simple'
	else:
		print 'Hard'