#! /usr/bin/env python
#
# predict.py
#
# Created by Kacper Rączy on 26.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#
# Simple script for checking spam prediction to given email.
#

from spam_clf.classifier import spam_predict, MODEL_PATH
import pickle
import sys
import os


def main():
    if len(sys.argv)<2:
        print("No path provided. Usage: predict.py <path_to_email_file>")
        return 1
    path = sys.argv[1]
    if not os.path.exists(path):
        path = os.getcwd() + path

    with open(MODEL_PATH, "rb") as clf_f:
        clf = pickle.loads(clf_f.read())
        prediction = spam_predict(clf, path)
        if prediction[0]:
            print("This is spam.")
        else:
            print("This isn't spam")
    return 0


if __name__=="__main__":
    sys.exit(main())
