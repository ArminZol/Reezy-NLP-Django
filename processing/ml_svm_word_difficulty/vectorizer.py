import quantifier
from sklearn.feature_extraction import DictVectorizer

# def vectorize_features(words):
# 	features, feature_names = get_organized_features_and_names(words)

# 	dicts = to_dict(features, feature_names)

# 	return vectorize_dicts(dicts)

def get_organized_features_and_names(words):
	features = []

	for word in words:
		adjacent_vowels = quantifier.quantify_adjacent_vowels(word)
		syllable_count = quantifier.quantifiy_syllable_count(word)
		#quantified_words = quantifier.quantify_word(words)
		popularity = quantifier.quantifiy_popularity(word)
		# synonyms = quantifier.quantify_synonyms(word)
		feature = [adjacent_vowels, syllable_count, popularity]
		features.append(feature)

	feature_names = ['adjacent_vowels', 'syllable_count', 'popularity']

	return features, feature_names

def to_dict(features, feature_names):
	dicts = []

	word_count = len(features[0])
	feature_count = len(features)

	for i in range(word_count):
		word_features = {}

		for x in range(feature_count):
			word_features[feature_names[x]] = features[x][i]

		dicts.append(word_features)

	return dicts

def vectorize_dicts(dicts):
	dv = DictVectorizer()
	sparse_matrix = dv.fit_transform(dicts)
	return sparse_matrix