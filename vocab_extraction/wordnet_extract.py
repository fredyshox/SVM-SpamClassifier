#! /usr/bin/env python
#
# wordnet_extract.py
#
# Created by Kacper Rączy on 10.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#
# Simple script for extracting vocabulary data from wordnet core database.

import re
from stemming.porter2 import stem
import os

def getWordnetVocab(path):
    """
    Extracts words from wordnet core file, then stem it.
    :param path: path to wordnet core file
    :return: list of stemmed extracted words
    """
    f = open(path, "r")
    vocab_list = []
    for line in f:
        temp = re.search('\[[\w]+\]', line)
        if not temp == None:
            str = re.sub('[\[\]]', '', temp.group())
            str = stem(str)
            if not str in vocab_list:
                vocab_list.append(str)
    f.close()
    return vocab_list

def addSpamWords(path, vocab_list):
    """
    Adds to vocab_list collection of spam words containing keywords(httpaddr etc.)
    :param path: path to file containing spam words
    :param vocab_list: current vocabulary list
    :return: extended vocabulary list
    """
    f = open(path, "r")
    for line in f:
        line = line.replace("\n", "")
        if len(line)>0:
            line = stem(line)
            if not line in vocab_list:
                vocab_list.append(line)
    vocab_list.sort(key=str.lower)
    f.close()
    return vocab_list

def main():
    """

    :return:
    """
    currentPath = os.path.dirname(os.path.realpath(__file__))
    wordnet_inputPath = currentPath + "/core-wordnet.txt"
    span_inputPath = currentPath + "/spam_words.txt"
    vocab_list = addSpamWords(span_inputPath, getWordnetVocab(wordnet_inputPath))

    converted = ""
    for word in vocab_list:
        converted = converted + word + "\n"


    path_comp = currentPath.split("/")
    outputPath = "/".join(path_comp[0:len(path_comp)-1]) + "/vocabulary.txt"
    output = open(outputPath, "w")
    output.write(converted)
    output.close()

if __name__=="__main__":
    main()