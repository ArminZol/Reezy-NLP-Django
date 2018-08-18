from nltk.data import path
from os import path as ospath

path.insert(0, '/home/daniel/nltk_data')

FILE_NAME_SMALL = '3845_most_popular_words.txt'
dirname = ospath.dirname(ospath.realpath(__file__))

popular_words_small = [word.rstrip('\n') for word in open(ospath.join(dirname, FILE_NAME_SMALL))]

def get_most_popular_from_misc(words):
	popular = []

	for word in words:
		for pop_word in popular_words_small:
			if word.lower().decode('utf-8') == pop_word.decode('utf-8'):
				popular.append(word)
				break
		# if word.lower() in popular_words_large:
		# 	popular.append(word)

	return popular #get_most_popular_from_pop(popular)#order_popular_words(popular)

def get_most_popular_from_pop(pop_words):
	for popular_word in popular_words_small:
		for pop_word in pop_words:
			if pop_word == popular_word.lower():
				return pop_word

	return None

def is_popular(word):
	return word.lower() in popular_words_small

# def order_popular_words(pop_words):
# 	indexes = []
# 	current_num = 0

# 	for pop_word in pop_words:
# 		added = False
# 		for index in range(len(popular_words_large)):
# 			if pop_word == popular_words_large[index]:
# 				indexes.append(index)
# 				added = True
# 				break
# 		if not added:
# 			pop_words.remove(pop_word)

# 	ordered_list = []

# 	loop_range = len(indexes)

# 	for num in range(loop_range):
# 		min_num = min(indexes)
# 		min_num_index = indexes.index(min_num)

# 		ordered_list.append(pop_words[min_num_index])

# 		indexes.pop(min_num_index)
# 		pop_words.pop(min_num_index)

# 	return ordered_list