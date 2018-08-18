import requests
import json

app_id = 'c020d551'
app_key = 'c49ac235a74eea4d02f26284cf2b1e7c'

language = 'en'

# print("code {}\n".format(r.status_code))
# print "text \n" + r.text
# print("json \n" + json.dumps(r.json()))

# print r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['synonyms']

def get_synonyms(word):
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + un_inflect(word.lower()) + '/synonyms;antonyms'

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

 	if r.status_code == 404:
 		return []

	senses = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]

	if 'subsenses' in senses.keys():
		synonym_dict = senses['subsenses'][0]['synonyms']
	elif 'synonyms' in senses.keys():
		synonym_dict = senses['synonyms']
	else:
		return [word]

	syns = []

	for syn in synonym_dict:
		syns.append(syn['text'])

	return syns

def un_inflect(word):
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/inflections/' + language + '/' + word.lower()

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	if r.status_code == 404:
		return word

	original = r.json()['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']

	return original