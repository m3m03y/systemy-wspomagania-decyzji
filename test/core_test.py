import app.tools.core as core

import unittest

class Test_TestCoreMethods(unittest.TestCase):

   def test_convert_to_numeric_should_return_tree_numbers(self):
      word_list=["aaa", "bbb", "ccc"]
      numeric_list = core.convert_text_to_numeric(word_list)
      self.assertEqual(numeric_list, [1,2,3])    

if __name__ == '__main__':
      unittest.main()
