# @uthor Ahmed Alajrami

import os
import nltk
from collections import Counter
from string import punctuation


class Model():
    def build(self):
        app_root = os.path.dirname(os.path.abspath(__file__))  # get the path to the application root
        files_path = os.path.join(app_root, 'docs/')  # join the root path with the directory for the documents

        files_index, freq_words = self.process_files(files_path)
        final_index = self.invert_index(files_index) # invert the index of file_index to become {word:{file_name:[sentence1, sentence4, ..], ...}, ...}

        return final_index, freq_words


    def process_files(self, files_path):
        # process the text documents and return the files index and the frequency of words
        ignored_tokens = set(nltk.corpus.stopwords.words('english'))  # a list of ignored tokens
        ignored_tokens.add("'s")  # add ('s) to the list of ignored tokens
        ignored_tokens.add("'re")
        ignored_tokens.add("n't")
        ignored_tokens.add("us")
        ignored_tokens.add("'ve")
        freq_words = Counter()  # counter for the frequency of words
        index = {}
        for path, dirs, files in os.walk(files_path):  # get the files in the docs directory
            for file in files:
                full_path = os.path.join(path, file)
                word_index = {}  # dictionary for words and the sentences they appeared in
                with open(full_path) as f:  # open the file
                    sentences = nltk.sent_tokenize(f.read())  # sentence segmentation for the file text
                    for sentence in sentences:
                        tokens = nltk.tokenize.word_tokenize(sentence)  # split sentences to tokens
                        for token in tokens:
                            if token.lower() in word_index.keys():  # update the word_index dictionary
                                word_index[token.lower()].append(sentence)
                            else:
                                word_index[token.lower()] = [sentence]  # add the word and the sentence to the dictionary
                        # count the frequency of each token not in the ignored tokens after removing punctuations
                        freq_words.update([token.lower().rstrip(punctuation) for token in tokens if token.lower() not in ignored_tokens])
                index[file] = word_index  # nested dictionary {file_name:{word:[sentence1, sentence4, ...], ...}, ...}
        return index, freq_words


    def invert_index(self, index):
        # invert the file_index
        inverted_index = {}
        for file_name in index.keys():
            for word in index[file_name].keys():
                if word in inverted_index.keys():
                    if file_name in inverted_index[word].keys():
                        inverted_index[word][file_name].extend(index[file_name][word][:])
                    else:
                        inverted_index[word][file_name] = index[file_name][word]
                else:
                    inverted_index[word] = {file_name: index[file_name][word]}

        return inverted_index