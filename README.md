# SVM-SpamClassifier

Spam classifier written in python 3 using Support Vector Machine algorithm.

## Data set

Data set consist of 4149 (2752 non-spam and 1397 spam) and is randomly divided into train, cross validation and test subsets (proportions 80%-10%-10%). 

Vocabulary set contain 4239 stemmed most commonly used, both in spam and daily messages. Each word is in separate line and is represented by its line index.

Sources:
* SpamAssassin public corpus emails (url: http://spamassassin.apache.org/old/publiccorpus/)
* WordNet Core english vocabulary (url: http://wordnetcode.princeton.edu/standoff-files/)
* spam vocabulary from Coursera's Machine Learning course

## Usage

Repository contains already trained model in dataset/ directory and script for testing it out.
To classify your own email, copy email contents to some text file and run the command:
```
// from Svm-SpamClassifier directory
$ python scripts/predict.py path/to/email.txt
```

## Requirements

List of used libraries etc. :
* python 3.x
* scikit-learn 0.19.1
* numpy 1.13.3
* stemming 1.0.1
* scipy 0.19.1 
