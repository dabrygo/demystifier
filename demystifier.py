from collections import defaultdict
from random import Random
import string
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
        words_by_letter[first_letter].append(word)
        word = dictionary.readline()
    return words_by_letter

  def get(self, letter):
    #print(letter, self.words_by_letter[letter])
    return self.words_by_letter[letter]
  
class Demystifier:
  def __init__(self, acronym, dictionary, seed=None):
    self.acronym = acronym
    self.dictionary = dictionary
    self.random = Random()
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
    return set(self.acronym.lower())

  def not_acronym_letters(self):
    return set(string.lowercase) - self.acronym_letters()

  def random_letter_means(self, letters):
	  letter = self.random_element_from(list(letters))
	  meaning = self.word_that_starts_with(letter)  
	  return "The {} in {} stands for {}".format(letter.upper(), self.acronym, meaning.title())

  def meaning_of_letter_not_in(self):
    letters = self.not_acronym_letters()
    return self.random_letter_means(letters)

  def meaning_of_letter_in(self):
    letters = self.acronym_letters()
    return self.random_letter_means(letters)
				
  def random_element_from(self, list):
    return self.random.choice(list)


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
    self.assertEquals("interviewee's", self.demystifier.word_that_starts_with('i'))

  def test_8_not_in_dictionary(self):
    self.assertRaises(ValueError, self.demystifier.word_that_starts_with, '8')

  def test_can_determine_random_value(self):
    self.assertEqual(3, self.demystifier.random_element_from([1, 2, 3]))

  def test_x_not_in_MPH(self):
    self.assertIn('x', self.demystifier.not_acronym_letters())

  def test_meaning_of_letter_not_in_MPH(self):
    self.assertEquals('The V in MPH stands for Viral', self.demystifier.meaning_of_letter_not_in())

  def test_meaning_of_letter_in_MPH(self):
    self.assertEquals('The H in MPH stands for Hookup', self.demystifier.meaning_of_letter_in())
   
if __name__ == '__main__':
  unittest.main()
