from PyDictionary import PyDictionary as dict
from global_content import get_syllable_count, get_vowel_count, get_last_shortest_word, word_is_difficult, has_same_meaning, has_vowels_side_by_side, has_letters_side_by_side
from participle_engine import get_tense, apply_tense
from parser import strip_invalid_synonyms, strip_xyz, get_article, set_article
from popular_data import get_most_popular_from_misc, get_most_popular_from_pop
from pos_engine import NOUN, VERB, ADJECTIVE, ADVERB, get_pos_tag
from wsd import get_disambiguated_definition, get_disambiguated_synset
from nltk.corpus import wordnet as wn

from os.path import join, dirname, realpath
DIR = join(dirname(realpath(__file__)), 'ranking')

from sys import path
path.append(DIR)

# from interpreter import get_simplest
# from words_db import Worker
from berank import get_simplest

def get_synonyms(sentence, word):
  syn_list = []
  synset = get_disambiguated_synset(sentence, word, None)

  if not (synset is None):
    for lemma in synset.lemmas():
      syn_list.append(lemma.name())

  synonyms = dict.synonym(word)

  if synonyms is None:
    return syn_list

  return synonyms + syn_list

def simplify(sentence, index, tokens):
  word = tokens[index]
  tense = get_tense(word)
  synonyms = get_synonyms(sentence, word)#dict.synonym(word)
  stripped_synonyms = strip_invalid_synonyms(index, tokens, synonyms)

  print 'Tense:', tense
  print 'Synonyms:', synonyms
  print 'Defnition:', dict.meaning(word)

  if stripped_synonyms is None or len(stripped_synonyms) == 0:
    return define(sentence, word, get_pos_tag(tokens, index))

  for stripped_synonym in stripped_synonyms:
    stripped_synonym = apply_tense(stripped_synonym, tense)

  print 'Stripped Synonyms:', stripped_synonyms

  #simplest_syns = get_most_popular_from_misc(stripped_synonyms)
  simple_word = get_simplest(stripped_synonyms)
  # if len(simplest_syns) == 1:
  #   simple_word = simplest_syns[0]
  #   print 'IF 1'
  # else:
  #   print 'ELSE 1'
  #   if simplest_syns is None or len(simplest_syns) == 0:
  #     print 'IF 2'
  #     simple_word = focus_simplifiy(word, stripped_synonyms)
  #   else:
  #     print 'ELSE 2'
      # simple_word = focus_simplifiy(word, simplest_syns)
      # first_simple_word = simple_word
      # print 'First Simplify:', simple_word

      # if (word_is_difficult(simple_word) or len(simple_word) > 7) and len(stripped_synonyms) > 1:
      #   stripped_synonyms.remove(simple_word)
      #   print 'The word', simple_word, 'is difficult, looking for a simpler word'

      #   index = 0

      #   while index < len(stripped_synonyms):
      #     simple_word = focus_simplifiy(stripped_synonyms[index], stripped_synonyms)
      #     print 'Anotha one:', simple_word
      #     is_difficult = word_is_difficult(simple_word)

      #     if (is_difficult or len(simple_word) > 7) and len(stripped_synonyms) > 1:
      #       print 'The word', simple_word, 'is difficult, looking for a simpler word'
      #       print 'Length of the synonyms:', len(stripped_synonyms)
      #       stripped_synonyms.remove(simple_word)
      #       index -= 1
      #     elif (is_difficult or len(simple_word) > 7) and len(stripped_synonyms) == 1:
      #       print 'They\'re all difficult, reverting to initial word:', first_simple_word
      #       #simple_word = first_simple_word
      #       simple_word = get_most_popular_from_pop(simplest_syns)
      #       break
      #     else:
      #       print 'Word', simple_word, 'is a go'
      #       print 'Comparing popularity to:', first_simple_word
      #       final_simple_words = get_most_popular_from_misc([simple_word, first_simple_word])
      #       if len(final_simple_words) > 0:
      #         simple_word = final_simple_words[0]
      #       break

      #     index += 1
      # elif len(stripped_synonyms) == 1:
      #   print 'Word is difficult, only one option though, using definition'
      #   return define(sentence, word, get_pos_tag(tokens, index))

  print 'Simple Word:', simple_word
  article = get_article(simple_word, tokens, index)
  print 'Article:', article
  set_article(tokens, index, article)
  simple_word = apply_tense(simple_word, tense)
  return simple_word.upper()

def define(sentence, word, pos):
  #TODO process for main part

  definition = get_disambiguated_definition(sentence, word, pos)

  return ' "' + word + ' [' + definition + ']"'

def focus_simplifiy(word, stripped_synonyms):
  if stripped_synonyms is None or len(stripped_synonyms) == 0:
    return word

  usual_words = []

  for word in stripped_synonyms:
    if not (has_vowels_side_by_side(word) and len(word) <= 6):
      usual_words.append(word)
      
  print 'Usual Words:', usual_words

  if usual_words is None or len(usual_words) == 0:
    least_syllables = get_least_syllables(stripped_synonyms)
  else:
    least_syllables = get_least_syllables(usual_words)
  
  print 'Least Syllables:', least_syllables

  least_vowels = get_least_vowels(least_syllables)
  
  print 'Least Vowels:', least_vowels

  final_word = get_last_shortest_word(least_vowels)

  print 'Final Word:', final_word

  return final_word

def simplify_word(word):
  tense = get_tense(word)
  synonyms = dict.synonym(word)
  stripped_synonyms = strip_invalid_synonyms(0, [word], synonyms)

  print 'Stripped Synonyms:', stripped_synonyms

  if stripped_synonyms is None or len(stripped_synonyms) == 0:
    return word

  simplest_syns = get_most_popular_from_misc(stripped_synonyms)

  print "Simplest Synonyms:", simplest_syns

  if simplest_syns is None or simplest_syns == '':
    if len(stripped_synonyms) == 1:
      return stripped_synonyms[0]

    least_syllables = get_least_syllables(stripped_synonyms)
    least_vowels = get_least_vowels(least_syllables)
    final_word = get_last_shortest_word(least_vowels)
    return apply_tense(final_word, tense)
  elif len(simplest_syns) > 0:
    return apply_tense(simplest_syns[0], tense)

def get_least_syllables(synonyms):
  simplest_words = [synonyms[0]]
  current_count = get_syllable_count(simplest_words[0])

  for synonym in synonyms:
    syllable_count = get_syllable_count(synonym)

    if syllable_count < current_count:
      del simplest_words[:]
      simplest_words.append(synonym)
      current_count = syllable_count
    elif syllable_count == current_count:
      simplest_words.append(synonym)

  return simplest_words

def get_least_vowels(synonyms):
  simplest_words = [synonyms[0]]
  current_count = get_vowel_count(simplest_words[0]) / float(len(simplest_words[0]))

  for synonym in synonyms:
    vowel_count = get_vowel_count(synonym) / float(len(synonym))

    print '(get_least_vowels) Synonym:', synonym, 'Vowel Count:', vowel_count

    if vowel_count < current_count:
      del simplest_words[:]
      simplest_words.append(synonym)
      current_count = vowel_count
    elif vowel_count == current_count:
      simplest_words.append(synonym)

  return simplest_words