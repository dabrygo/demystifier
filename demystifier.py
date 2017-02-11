from random import Random
import string
import unittest

def letter_in_acronym(letter, acronym):
  return letter.lower() in acronym.lower() 

def random_element_from(list, seed=None):
  random = Random()
  if seed is not None:
    random.seed(seed)
  return random.choice(list)

def word_that_starts_with(letter, seed=None):
  with open('/usr/share/dict/words') as dictionary:
    words = dictionary.readlines()
    valid_words = []
    for word in words:
      if word.startswith(letter):
        valid_words.append(word.rstrip()) 
  if not valid_words:
    raise ValueError("{} not found in dictionary".format(letter))
  return random_element_from(valid_words, seed)

def letter_not_in(acronym):
  return set(string.lowercase) - set(acronym.lower()) 

def meaning_of_letter_not_in(acronym, seed=None):
  letters = letter_not_in(acronym) 
  letter = random_element_from(list(letters), seed)
  meaning = word_that_starts_with(letter, seed)  
  return "The {} in {} stands for {}".format(letter.upper(), acronym, meaning.title())


class TestDemystifier(unittest.TestCase):
  def test_no_i_in_TEAM(self):
    self.assertFalse(letter_in_acronym('i', 'TEAM')) 

  def test_i_in_COOPERATION(self):
    self.assertTrue(letter_in_acronym('i', 'COOPERATION'))

  def test_i_starts_with_i(self):
    self.assertEquals('intoxicant', word_that_starts_with('i', seed=0))

  def test_8_not_in_dictionary(self):
    self.assertRaises(ValueError, word_that_starts_with, '8')

  def test_can_determine_random_value(self):
    self.assertEqual(3, random_element_from([1, 2, 3], seed=0))

  def test_x_not_in_MPH(self):
    self.assertIn('x', letter_not_in('MPH'))

  def test_meaning_of_letter_not_in_MPH(self):
    self.assertEquals('The V in MPH stands for Vocalize', meaning_of_letter_not_in('MPH', seed=0))
   
if __name__ == '__main__':
  unittest.main()
