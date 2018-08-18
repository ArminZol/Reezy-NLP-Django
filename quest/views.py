from django.shortcuts import render

from controller import quest_simplify, quest_dict, quest_next_word, quest_save_word, quest_next_word_for_user, quest_save_word_for_user, quest_get_logs

from django.http import HttpResponse

SIMPLIFIER_PAGE = '/simp/'

QUEST_ERR = 'No Resources Found'

def quest(request):
	if request.method == 'GET':
		split = request.path.split('/', 2)[2]
		print split

		if 'survey/' in split:
			if 'next_word' in split:
				json_data = quest_next_word()

				if json_data is None:
					return redirect(SIMPLIFIER_PAGE)

				return HttpResponse(json_data)

			elif 'word' in request.GET and 'is_hard' in request.GET and 'update' not in split:
				word = request.GET['word']
				is_hard = bool(request.GET['is_hard'])

				quest_save_word(word, is_hard)

			elif 'user/' in split:
				if request.user.is_authenticated():
					if 'get' in split:
						json_data = quest_next_word_for_user(request.user)
						return HttpResponse(json_data)

					elif 'update' in split and 'word' in request.GET and 'is_hard' in request.GET:
						quest_save_word_for_user(request.user, request.GET['word'], bool(request.GET['is_hard']))
						json_data = quest_next_word_for_user(request.user)
						return HttpResponse(json_data)

		elif 'logs' in split:
			if request.user.is_authenticated() and request.user.is_superuser:
				logs = quest_get_logs(request.GET['user'])
				return HttpResponse(logs)

		elif 'text' in request.GET:
			if request.user.is_authenticated():
				text = request.GET['text']

				json_data = quest_simplify(text, request.user)

				return HttpResponse(json_data)

		elif 'word' in request.GET:
			word = request.GET['word']

			json_data = quest_dict(word, request.user)

			return HttpResponse(json_data)

	return HttpResponse(QUEST_ERR)