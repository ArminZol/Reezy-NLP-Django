from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), '../processing', 'ml_svm_word_difficulty')

from sys import path
path.append(DIR)

from processing import simplifier, statistics, dictionary_api, logger

from pytz import timezone
from datetime import datetime
from pytz import timezone

import json

from processing.classifier_manager import classifiers

from bs4 import BeautifulSoup

def quest_save_word(word, is_hard):
	survey_server.put_given(word, is_hard)
	survey_server.save()

def quest_next_word_for_user(user):
	if user.username in classifiers:
		personaliser = classifiers[user.username]
		word = survey_server.get(personaliser.get_word_index())

		if word is None:
			word = ''

		word_dict = {
			'word': word
		}

		json_data = json.dumps(word_dict)

		return json_data

	return ''

def quest_save_word_for_user(user, word, is_hard):
	if user.username in classifiers:
		personaliser = classifiers[user.username]
		personaliser.update(word, is_hard)
		personaliser.next_word_index()

def quest_next_word():
	word = survey_server.get_next()

	if word is None:
		return None

	word_dict = {
			'word': word
		}

	json_data = json.dumps(word_dict)

	return json_data

def quest_simplify(text, user):
	if has_html(text):
		context = {}

		context['simplification_result'] = ''
		context['time'] = ''
		context['statistics'] = ''
		context['html'] = 'True'

		return json.dumps(context)

	if 'shoop' in classifiers:
		answer = simplifier.choose(text, classifiers['shoop'])
	else:
		answer = simplifier.choose(text)

	# answer = simplifier.choose(text) # comment this out when uncommenting the section above

	context = {}

	context['simplification_result'] = answer[0]
	context['time'] = str(round(answer[1], 2)) + 's'
	context['statistics'] = statistics.get_stats(text)
	context['html'] = 'False'

	log(user.username, text, answer[0], context['time'], context['statistics'])

	json_data = json.dumps(context)

	return json_data

def quest_dict(word, user):
	definition = dictionary_api.define(word)
	synonyms = dictionary_api.synonyms(word)
	examples = dictionary_api.examples(word)

	context = {}

	context['Definition'] = definition
	context['Synonyms'] = synonyms
	context['Examples'] = examples

	json_data = json.dumps(context)

	return json_data

def log(username, hard_text, simple_text, time, stats):
	fmt = '%Y-%m-%d %H:%M:%S %Z%z'

	eastern = timezone('US/Eastern')

	naive_dt = datetime.now()

	loc_dt = datetime.now(eastern)

	current_time = loc_dt.strftime(fmt)

	logger.log(username, hard_text, simple_text, time, stats, current_time)

def quest_get_logs(username):
	logs = logger.fetch(username)

	logs_dict = {}

	logs_dict['logs'] = logs

	json_data = json.dumps(logs_dict)

	return json_data

def has_html(string):
	return bool(BeautifulSoup(string, 'html.parser').find())