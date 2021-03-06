import argparse
from collections import defaultdict
import random
import re
import string
import sys
import unittest

class Dictionary:
  def __init__(self, path='/usr/share/dict/words'):
    self.words_by_letter = Dictionary.load(path)

  @staticmethod
  def load(path):
    words_by_letter = defaultdict(list)
    with open(path) as dictionary:
      word = dictionary.readline()
      while word:
        word = word.strip().lower()
        first_letter = word[0]
        if Dictionary.is_valid(word):
          words_by_letter[first_letter].append(word)
        word = dictionary.readline()
    return words_by_letter

  def get(self, letter):
    return self.words_by_letter[letter]
  
  @staticmethod
  def is_valid(word):
    return re.match(r'^\w+$', word.strip().lower())


class Demystifier:
  def __init__(self, acronym, dictionary, seed=None):
    self.acronym = acronym
    self.dictionary = dictionary
    self.random = random.Random()
    if seed is not None:
      self.random.seed(seed)

  def acronym_has(self, letter):
    return letter.lower() in self.acronym.lower() 

  def word_that_starts_with(self, letter):
    if not self.dictionary.get(letter):
      raise ValueError("{} not found in dictionary".format(letter))
    return self.random_element_from(self.dictionary.get(letter))

  def random_element_from(self, list):
    return self.random.choice(list)

  def acronym_letters(self):
    return self.acronym.lower()

  def all_but(self, group):
    return set(string.lowercase) - set(group)

  def not_acronym_letters(self):
    return self.all_but(self.acronym_letters())

  def word_for_random_letter(self, letters):
    letter = self.random_element_from(list(letters))
    return letter, self.word_that_starts_with(letter)  
 
  def random_letter_means(self, letters):
    letter, meaning = self.word_for_random_letter(letters)  
    return "The {} in {} stands for {}".format(letter.upper(), self.acronym, meaning.title())

  def meaning_of_letter_not_in(self):
    letters = self.not_acronym_letters()
    return self.random_letter_means(letters)

  def meaning_of_letter_in(self):
    letters = self.acronym_letters()
    return self.random_letter_means(self.acronym_letters())
				
  def random_element_from(self, list):
    return self.random.choice(list)

  def meaning_of_letters(self, n):
    words = []
    for i in range(n):
      if i > len(self.acronym):
        break 
      word = self.word_that_starts_with(self.acronym[i].lower())
      words.append(word)
    first = "The {} in {} stands for {}".format(self.acronym[0], self.acronym, words[0].title())
    more = []
    for i in range(1, len(words)):
      more_text = "and the {} stands for {}".format(self.acronym[i], words[i].title())
      more.append(more_text)
    return first + ' ' + ' '.join(more)
  
  def meaning(self):
    words = []
    for letter in self.acronym_letters():
      words.append(self.word_that_starts_with(letter)) 
    meaning = ' '.join([word.title() for word in words])
    return "{} stands for {}".format(self.acronym, meaning)

  def not_good_meaning(self):
    words = []
    acronym_letters = self.acronym.lower()
    for letter in acronym_letters:
      not_letter_group = self.all_but(letter)
      _, word = self.word_for_random_letter(not_letter_group)
      words.append(word)
    meaning = ' '.join([word.title() for word in words])
    return "{} does not mean {}".format(self.acronym, meaning)


class TestDemystifier(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.dictionary = Dictionary()

  def setUp(self):
    TestDemystifier.dictionary.get('a')
    self.demystifier = Demystifier('MPH', TestDemystifier.dictionary, seed=0)

  def test_letter_not_in_acronym(self):
    self.assertFalse(self.demystifier.acronym_has('i')) 

  def test_letter_in_acronym(self):
    self.demystifier.acronym = 'COOPERATION'
    self.assertTrue(self.demystifier.acronym_has('i'))

  def test_i_starts_with_i(self):
    self.assertEquals("interweave", self.demystifier.word_that_starts_with('i'))

  def test_8_not_in_dictionary(self):
    self.assertRaises(ValueError, self.demystifier.word_that_starts_with, '8')

  def test_can_determine_random_value(self):
    self.assertEqual(3, self.demystifier.random_element_from([1, 2, 3]))

  def test_x_not_in_MPH(self):
    self.assertIn('x', self.demystifier.not_acronym_letters())

  def test_meaning_of_letter_not_in_MPH(self):
    self.assertEquals('The V in MPH stands for Virtuosi', self.demystifier.meaning_of_letter_not_in())

  def test_meaning_of_letter_in_MPH(self):
    self.assertEquals('The H in MPH stands for Hoorays', self.demystifier.meaning_of_letter_in())
   
  def test_meaning_of_MPH(self):
    self.assertEquals('MPH stands for Moralized Press Health', self.demystifier.meaning())

  def test_meaning_of_acronym_with_duplicates(self):
    self.demystifier.acronym = 'AAA'
    self.assertEquals('AAA stands for Aspersions Arbitrate Afterthought', self.demystifier.meaning())

  def test_not_good_meaning(self):
    self.assertEquals("MPH does not mean Virtuosi Josefina Openness", self.demystifier.not_good_meaning())

  def test_meaning_of_letters_in(self):
    self.assertEquals("The M in MPH stands for Moralized and the P stands for Press", self.demystifier.meaning_of_letters(2))


if __name__ == '__main__':
  parser = argparse.ArgumentParser("Explain letters that do/don't show up in acronyms") 
  parser.add_argument("acronym", metavar="ABBV", type=str, nargs=1, help="The acronym to explain") 
  parser.add_argument("-x", "--use-letters-not-in", action="store_true", help="Say what letters NOT in ABBV mean")
  parser.add_argument("-o", "--one-letter", action="store_true", help="Only translate one letter")
  parser.add_argument("--test", action="store_true", help='Run test suite')
  args = parser.parse_args()
  demystifier = Demystifier(args.acronym[0], Dictionary())
  if args.use_letters_not_in:
    if args.one_letter:
      print(demystifier.meaning_of_letter_not_in())
    else:
      print(demystifier.not_good_meaning())
  else:
    if args.one_letter:
      print(demystifier.meaning_of_letter_in())
    else:
      print(demystifier.meaning())

  if args.test:
    sys.argv = [sys.argv[0]]
    unittest.main()
