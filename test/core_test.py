import app.tools.core as core
import numpy as np
import unittest

class Test_TestCoreMethods(unittest.TestCase):

    def test_convert_to_numeric_should_return_tree_numbers(self):
        word_list = ["aaa", "bbb", "ccc"]
        numeric_list = core.convert_text_to_numeric_by_presence(word_list)
        self.assertEqual(numeric_list, [1, 2, 3])

    def test_convert_to_numeric_should_return_with_valid_key(self):
        word_list = ["aaa", "bbb", "ccc", "bbb", "aaa"]
        numeric_list = core.convert_text_to_numeric_by_presence(word_list)
        self.assertEqual(numeric_list, [1, 2, 3, 2, 1])

    def test_convert_alphabetically_to_numeric_should_return_tree_numbers(self):
        word_list = ["aaa", "bbb", "ccc"]
        numeric_list = core.convert_text_to_numeric_by_alphabet_order(
            word_list)
        self.assertEqual(numeric_list, [1, 2, 3])

    def test_convert_mixed_alphabetically_to_numeric_should_return_tree_numbers(self):
        word_list = ["ccc", "aaa", "bbb"]
        numeric_list = core.convert_text_to_numeric_by_alphabet_order(
            word_list)
        self.assertEqual(numeric_list, [3, 1, 2])

    def test_discretization_should_return_three_divisions(self):
        num_list = [10, 30, 20, 15, 37, 40]
        discretized_list = core.discretisation(num_list, 3)
        self.assertSequenceEqual(
            tuple(discretized_list), tuple([0, 2, 1, 0, 2, 2]))

    def test_standarize(self):
        num_list = [10, 30, 40, 20]
        discretized_list = core.standarization(num_list)
        self.assertEqual(discretized_list, [-1.34, 0.45, 1.34, -0.45])

    def test_change_data_range(self):
        num_list = [10, 30, 40, 20]
        new_range_list = core.change_data_range(num_list, 1, 4)
        self.assertEqual(new_range_list, [1, 3, 4, 2])

    def test_read_file_should_handle_csv(self):
        df = core.read_file("./example/iris.csv")
        headers = df.columns.to_list()
        expected = ['sepal.length','sepal.width','petal.length','petal.width','variety']
        self.assertSequenceEqual(headers, expected)

    def test_read_file_should_handle_excel(self):
        # functionality is working but module cannot be found in test
        df = core.read_file("./example/iris.xlsx")
        headers = df.columns.to_list()
        expected = ['sepal.length','sepal.width','petal.length','petal.width','variety']
        self.assertSequenceEqual(headers, expected)

    def test_read_file_should_rise_invalid_extension_exception(self):
        with self.assertRaises(FileNotFoundError):
            core.read_file("./example/iris.json")

if __name__ == '__main__':
    unittest.main()
