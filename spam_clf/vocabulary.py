#! /usr/bin/env python
#
# vocabulary.py
#
# Created by Kacper Rączy on 10.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#

import os

def getVocabList():
    """
    Loads the vocabulary list into memory and create array with it's contents
    :return: array containing vocabulary or None if sth went wrong
    """
    project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/dataset"
    fp = project_path + '/vocabulary.txt'
    if os.path.exists(fp):
        with open(fp, 'r') as file:
            vocab_list = []
            for line in file:
                line = line.lower()
                line = line.replace('\n', '')
                if not len(line) == 0:
                    vocab_list.append(line)
            print("Length of vocab: " + str(len(vocab_list)))
            return vocab_list
    return None
