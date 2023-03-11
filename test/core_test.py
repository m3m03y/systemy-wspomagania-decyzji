import app.tools.core as core

import unittest

class Test_TestCoreMethods(unittest.TestCase):

   def test_convert_to_numeric_should_return_tree_numbers(self):
      word_list=["aaa", "bbb", "ccc"]
      numeric_list = core.convert_text_to_numeric_by_presence(word_list)
      self.assertEqual(numeric_list, [1,2,3])    

   def test_convert_to_numeric_should_return_with_valid_key(self):
      word_list=["aaa", "bbb", "ccc", "bbb", "aaa"]
      numeric_list = core.convert_text_to_numeric_by_presence(word_list)
      self.assertEqual(numeric_list, [1,2,3,2,1])   

   def test_convert_alphabetically_to_numeric_should_return_tree_numbers(self):
      word_list=["aaa", "bbb", "ccc"]
      numeric_list = core.convert_text_to_numeric_by_alphabet_order(word_list)
      self.assertEqual(numeric_list, [1,2,3])    

   def test_convert_mixed_alphabetically_to_numeric_should_return_tree_numbers(self):
      word_list=["ccc", "aaa", "bbb"]
      numeric_list = core.convert_text_to_numeric_by_alphabet_order(word_list)
      self.assertEqual(numeric_list, [3,1,2]) 

if __name__ == '__main__':
      unittest.main()
