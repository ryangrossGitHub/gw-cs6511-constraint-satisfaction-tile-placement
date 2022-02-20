import os
import unittest

from input_variable_processor import read_landscape_file


class UnitTest(unittest.TestCase):

    # Ensure the lanscape files are being read correctly
    def test_read_landscape_file(self):
        f = open('unittest.txt', 'a')
        f.write('1  \n1 1')
        f.close()

        result = read_landscape_file('unittest.txt')

        # Clean up from test
        os.remove('unittest.txt')
        self.assertEqual(result, [['1', ' '], ['1', '1']])


if __name__ == '__main__':
    unittest.main()