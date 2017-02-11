import unittest

def letter_in_acronym(letter, acronym):
  return letter.lower() in acronym.lower() 

def word_that_starts_with(letter):
  with open('/usr/share/dict/words') as dictionary:
    words = dictionary.readlines()
    for word in words:
      if word.startswith(letter):
        return word.rstrip() 
  raise ValueError("{} not found in dictionary".format(letter))

class TestDemystifier(unittest.TestCase):
  def test_no_i_in_TEAM(self):
    self.assertFalse(letter_in_acronym('i', 'TEAM')) 

  def test_i_in_COOPERATION(self):
    self.assertTrue(letter_in_acronym('i', 'COOPERATION'))

  def test_i_starts_with_i(self):
    self.assertEquals('i', word_that_starts_with('i'))

  def test_8_not_in_dictionary(self):
    self.assertRaises(ValueError, word_that_starts_with, '8')

   
if __name__ == '__main__':
  unittest.main()
