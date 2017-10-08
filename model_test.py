# @uthor Ahmed Alajrami

import unittest
import os
from model import Model

model = Model()

class MyTestCase(unittest.TestCase):
    def test_process_files(self):
        app_root = os.path.dirname(os.path.abspath(__file__))
        files_path = os.path.join(app_root, 'test/')

        files_index, freq_words = model.process_files(files_path)

        self.assertEqual(len(files_index.keys()), 1) # we have just one text file to test
        self.assertEqual(freq_words.most_common(1), [('test', 3)]) # 'test' word is the most common word and appeared 3 times

    def test_invert_index(self):
        test_in = {'file_name':{'word':['sent1','sent5']}}
        test_out = {'word': {'file_name': ['sent1', 'sent5']}}

        index = model.invert_index(test_in)

        self.assertEqual(index,test_out)

if __name__ == '__main__':
    unittest.main()
