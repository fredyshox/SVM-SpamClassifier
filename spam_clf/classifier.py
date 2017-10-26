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


#tbc kernel function for future use
def gaussian_kernel(x1, x2, sigma):
    sim = 0
    arr = (x1 - x2)
    sim = sim + np.sum(np.power(arr, 2))
    sim = sim/(2*(sigma*sigma))
    sim = np.exp(sim)
    return sim


def train_model():
    # import extracted dataset
    ds = import_dataset()
    X = ds["X"]
    y = ds["y"]

    print("Imported train set.")
    # svm parameters
    C = 1.0
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
