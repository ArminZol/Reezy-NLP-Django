from global_content import deconstruct

class Container():
	sentence = ''
	tokens = []

	def contain(self, sentence):
		self.sentence = sentence
		tokens = deconstruct(sentence)
