#! /usr/bin/env python
#
# email_processor.py
#
# Created by Kacper Rączy on 11.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#

import re
from stemming.porter2 import stem


class EmailProcessor(object):
    def __init__(self, word_arr):
        """
        Initialize EmailProcessor object with array or words.
        :param word_arr: array of available words
        """
        object.__init__(self)
        self.word_arr = word_arr


    def process_email(self, contents):
        contents = self.replace_contents(contents)
        #print(contents)
        # Get all the words by ommiting all punctuaction
        #pattern_str = '[ @\$/#.-:&\*\+=\[]\?!\(\){},\'\'">_<;%' + chr(10) + chr(13) + "]+"
        words = re.split("[\W_]+", contents)
        word_indexes = []

        for word in words:
            # Remove all non-alphanumeric chars
            word = re.sub('[\W]', '', word)
            word = re.sub('[_]', '', word)

            # Porter stemming word
            stem_word = stem(word)

            # check if word exist in word_dict
            # if so, append it's index to word_indexes
            if word in self.word_arr:
                index = self.word_arr.index(word)
                word_indexes.append(index)
            #TODO print result email

        return word_indexes

    def email_features(self, indexes):
        """
        Produces email feature vector from word indexes
        :param indexes: indexes of words in email
        :return: email feature vector
        """
        n = len(self.word_arr)
        feature_vec = n * [0]
        for i in indexes:
            feature_vec[i] = 1
        return feature_vec


    def replace_contents(self, contents):
        has_header = True

        # If this is raw email, find email header and remove ( \n\n )
        if has_header:
            header = contents.find(chr(10) + chr(10))
            if not header == -1:
                contents = contents[header:len(contents)]

        # Lower case
        contents = contents.lower()
        # using regular expressions

        # HTML Headers
        # Replace strings that start with < and end with >
        contents = re.sub('<[^<>]+>', ' ', contents)

        # Numbers
        # Replace any one or more chars from 0-9
        contents = re.sub('[0-9]+', 'number', contents)

        # URLs
        # Replace any expressions starting with http:// or https:// and other characters except whitespace
        contents = re.sub('(http|https)://[^\s]*', 'httpaddr', contents)

        # Emails
        contents = re.sub('[^\s]+@[^\s]+', 'emailaddr', contents)

        # $ sign
        contents = re.sub('[$]+', 'dollar', contents)
        # TODO handle other currencies

        return contents