from textstat.textstat import textstat

EMPTY_TEXT_STANDARD = ''

def get_stats(sentence):
	syllables = textstat.syllable_count(sentence)
	words = textstat.lexicon_count(sentence, True)
	sentence_count = textstat.sentence_count(sentence)

	if sentence_count > 0:
		text_standard = textstat.text_standard(sentence)
	else:
		text_standard = EMPTY_TEXT_STANDARD

	text_standard = fix_grammar_errors(text_standard)

	return combine(syllables, words, sentence_count, text_standard)

def combine(syllables, words, sentence_count, text_standard):
	str1 = 'SYLLABLES: ' + str(int(syllables))
	str2 = 'WORD COUNT: ' + str(words)
	str3 = 'SENTENCE COUNT: ' + str(sentence_count)

	if text_standard is not EMPTY_TEXT_STANDARD:
		str4 = 'READABILITY: ' + text_standard
	else:
		str4 = text_standard

	combination = '<br>'.join([str1, str2, str3, str4])
	return combination

def fix_grammar_errors(stat):
	if '-' in stat or ('0th' in stat and '10th' not in stat and '20th' not in stat):
		stat = '1st grade'

	if '11' not in stat:
		stat = stat.replace('1th', '1st')

	if '12' not in stat:
		stat = stat.replace('2th', '2nd')

	return stat