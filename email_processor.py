import numpy as np
import re
from stemming.porter2 import stem


class EmailProcessor(object):
    def __init__(self, word_arr):
        """
        Initialize EmailProcessor object with array or words.
        :param word_arr: array of available words
        """
        super.__init__()
        self.word_arr = word_arr


    def process_email(self, contents):
        contents = "test_contents"#Test
        contents = self.replace_contents(contents)

        # Get all the words by ommiting all punctuaction
        pattern_str = ' @$/#.-:&*+=[]?!(){},''">_<;%' + chr(10) + chr(13)
        words = re.split(pattern_str, contents)
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


    def replace_contents(self, contents):
        contents = "test_contents"#Test
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