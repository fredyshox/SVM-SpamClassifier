#! /usr/bin/env python
#
# classifier.py
#
# Created by Kacper Rączy on 25.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#

from sklearn import svm
import numpy as np
import pickle
from spam_clf.email_processor import EmailProcessor
from spam_clf.dataset import import_dataset
from spam_clf.vocabulary import getVocabList
import os

MODEL_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/dataset/clf_model"

DEFAULT_C = 0.03

#tbc kernel function for future use
def gaussian_kernel(x1, x2, sigma):
    sim = 0
    arr = (x1 - x2)
    sim = sim + np.sum(np.power(arr, 2))
    sim = sim/(2*(sigma*sigma))
    sim = np.exp(sim)
    return sim

def linear_params():
    ds = import_dataset()
    X = ds["X"]
    y = ds["y"]

    X_val = ds["X_val"]
    y_val = ds["y_val"]

    possible_C = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]

    error = (1, 1)  # (C, error)
    for C in possible_C:
        clf = svm.SVC(C=C, kernel="linear")
        clf.fit(X, y)
        predictions = clf.predict(X_val)
        temp = 1 - np.mean((predictions == y_val))
        print("C: " + str(C) + " error: " + str(temp))
        if temp < error[1]:
            error = (C, temp)
    print("Error = " + str(error))
    return error[0]


def train_model(C = DEFAULT_C):
    # import extracted dataset
    ds = import_dataset()
    X = ds["X"]
    y = ds["y"]

    print("Imported train set.")
    # svm parameters
    # sigma = 0.0  # for gaussian kernel

    # training
    classifier = svm.SVC(C=C, kernel="linear")
    classifier.fit(X, y)

    print("Fitting data set...")
    # saving model
    with open(MODEL_PATH, "wb") as model_f:
        model = pickle.dumps(classifier)
        model_f.write(model)

    return classifier


def test_model(classifier):
    ds = import_dataset()
    # preparing test set
    X_test = ds["X_test"]
    y_test = ds["y_test"]
    print("Testing...")
    # testing
    predictions = classifier.predict(X_test)
    temp = (predictions == y_test)
    predict_accuracy = np.mean(temp)

    print("ML Model Test accuracy: " + str(predict_accuracy))
    return predict_accuracy


def spam_predict(classifier, path, has_header=False):
    if not os.path.exists(path):
        path = os.getcwd() + path
    words = getVocabList()
    processor = EmailProcessor(words)
    with open(path, "r") as f:
        content = f.read()
        e_indices = processor.process_email(content, has_header=has_header)
        vector = processor.email_features(e_indices)
        prediction = classifier.predict(np.array([vector]))
        print(path + " prediction: " + str(prediction))
    return prediction

if __name__=="__main__":
    clf = train_model()
    test_model(clf)
