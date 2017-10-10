#! /usr/bin/env python
#
# wordnet_extract.py
#
# Created by Kacper Rączy on 10.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#
# Simple script for extracting vocabulary data from wordnet core database.

import re
import os

def main():

    currentPath = os.path.dirname(os.path.realpath(__file__))
    inputPath = currentPath + "/core-wordnet.txt"
    fp = open(inputPath, "r")
    converted = ""
    for line in fp:
        temp = re.search('\[[\w]+\]', line)
        if not temp == None:
            str = re.sub('[\[\]]', '', temp.group())
            converted = converted + str + "\n"
    outputPath = currentPath + "/vocabulary.txt"
    output = open(outputPath, "w")
    output.write(converted)
    output.close()

if __name__=="__main__":
    main()