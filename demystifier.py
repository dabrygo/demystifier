import unittest

def letter_in_acronym(letter, acronym):
  return letter.lower() in acronym.lower() 

class TestDemystifier(unittest.TestCase):
  def test_no_i_in_TEAM(self):
    self.assertFalse(letter_in_acronym('i', 'TEAM')) 

  def test_i_in_COOPERATION(self):
    self.assertTrue(letter_in_acronym('i', 'COOPERATION'))


if __name__ == '__main__':
  unittest.main()
