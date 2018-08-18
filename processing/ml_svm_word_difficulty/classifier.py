from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from labler import WordLabelPair, load_labels, get_train_ready_labels
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
import numpy as np

def get_features_labels(labels=None):
	from vectorizer import get_organized_features_and_names
	from word_extractor import get_words

	if labels is None:
		labels = load_labels(automatic=True)
		labels = get_train_ready_labels(labels)

	return get_organized_features_and_names(get_words(len(labels)))[0], labels

def optimize(svr):
	paramaters = {'kernel':('rbf', 'linear', 'poly'), 'C':tuple(range(1, 10))}
	clf = GridSearchCV(svr, paramaters)
	print 'Best Parameters:', clf.get_params()
	return clf

def update_clf(labels):
	features, train_labels = get_features_labels(labels)

	svr = SVC()

	svr.fit(features, train_labels)

	return svr

class WordLearner():
	def __init__(self):
		#create support vector machine classifier
		self.svr = SVC() #DecisionTreeClassifier()
		self.features, self.labels = get_features_labels()

		print 'Amount of Features:', len(self.features)

		#cross-validation (data splitting)
		self.features_train, self.features_test, self.labels_train,  self.labels_test = train_test_split(self.features, self.labels, test_size=0.3, random_state=42)

		print 'Amount of Training Features:', len(self.features_train)
		print 'Amount of Tesing Features:', len(self.features_test)

		#grid search optimization
		self.clf = self.svr#optimize(svr)

		#fitting
		self.clf.fit(self.features_train, self.labels_train)

		print 'Fitted'

		#accuracy
		self.accuracy = self.clf.score(self.features_test, self.labels_test)
		print 'Accuracy:', self.accuracy

		#dimensionality reduction with pca
		self.pca = PCA(n_components=2).fit(self.features)
		self.features_pca = self.pca.transform(self.features)

	#visualising
	def plot(self):
		for i in range(len(self.labels)):
			xy = (self.features_pca[i, 0], self.features_pca[i, 1])
			plt.scatter(xy[0], xy[1], c=self.labels[i])
			plt.annotate(self.labels[i], xy=xy)

		plt.scatter(self.features_pca[:,0], self.features_pca[:,1], c=self.labels)

		plt.show()

	#predicting
	def predict(self, data):
		reshaped_data = np.reshape(data, (1, -1))
		return self.clf.predict(reshaped_data)

def save():
	import cPickle as pickle
	from os.path import join, dirname, realpath

	learner = WordLearner()

	CLF_LOCATION = join(dirname(realpath(__file__)), 'default_classifier.pkl')
	LABELS_LOCATION = join(dirname(realpath(__file__)), 'default_labels.pkl')

	file = open(CLF_LOCATION, 'wb')
	pickle.dump(learner.clf, file)
	file.close()

	file = open(LABELS_LOCATION, 'wb')
	pickle.dump(learner.labels, file)
	file.close()