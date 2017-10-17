import os
from email_processor import EmailProcessor
from vocabulary import  getVocabList
import utility
import numpy as np

# Dataset division:
# 60% train set
# 20% cross validation set
# 20% test set


class DatasetExtractor(object):

    def __init__(self, class0_paths, class1_paths, X=None, y=None):
        object.__init__(self)
        self.cp = os.path.dirname(os.path.realpath(__file__)) + "/dataset/"
        self.vocab = getVocabList()
        self.processor = EmailProcessor(self.vocab)
        self.class0_paths = class0_paths
        self.class1_paths = class1_paths

        self.dataset_length = 0
        self.Xval = np.array([])
        self.yval = np.array([])
        self.Xtest = np.array([])
        self.ytest = np.array([])

        if X is None or y is None:
            self.extract_dataset()
        else:
            self.X = X
            self.y = y
            self.dataset_length = len(X)

    def extract_dataset(self):
        Xtemp = []
        ytemp = []
        for path in self.class0_paths:
            files = utility.list_files(self.cp + path)
            temp = self.extract_features(files)
            Xtemp.extend(temp)
            ytemp = ytemp + [0] * len(temp)

        for path in self.class1_paths:
            files = utility.list_files(self.cp + path)
            temp = self.extract_features(files)
            Xtemp.extend(temp)
            ytemp = ytemp + [1] * len(temp)

        # randomize order
        random_ind = utility.random_indices(1, len(Xtemp))
        self.X = np.array([], dtype="uint8")
        self.X.resize(len(Xtemp),len(self.vocab))
        self.y = np.array([], dtype="uint8")
        self.y.resize(len(ytemp))

        for i in range(len(random_ind)):
            self.X[i] = np.array(Xtemp[random_ind[i]], dtype="uint8")
            self.y[i] = np.array(ytemp[random_ind[i]], dtype="uint8")

        self.dataset_length = len(self.X)
        return (self.X, self.y)

    def create_cv_set(self, percent):
        if percent > 1 or percent < 0:
            return
        end = int(percent*self.dataset_length)
        self.Xval = np.array(self.X[0:end])
        self.X = np.delete(self.X, range(end), axis=0)
        self.yval = np.array(self.y[0:end])
        self.y = np.delete(self.y, range(end), axis=0)
        return

    def create_test_set(self, percent):
        if percent > 1 or percent < 0:
            return
        end = int(percent*self.dataset_length)
        self.Xtest = np.array(self.X[0:end])
        self.X = np.delete(self.X, range(end), axis=0)
        self.ytest = np.array(self.y[0:end])
        self.y = np.delete(self.y, range(end), axis=0)
        return

    def save_dataset(self, path=None):
        if self.X is None or self.y is None:
            return
        else:
            if path is None:
                fp = self.cp + "/spam_dataset.npz"
            else:
                fp = self.cp + path

            np.savez_compressed(fp, X=self.X, y=self.y, X_val=self.Xval, y_val=self.yval, X_test=self.Xtest, y_test=self.ytest)
            return

    def extract_features(self, paths):
        X_vec = []
        for path in paths:
            print(path)
            with open(path, "r", errors="replace") as f:
                content = f.read()
                indexes = self.processor.process_email(content)
                features = self.processor.email_features(indexes)
                X_vec.append(features)
                del content
        return np.array(X_vec, dtype="uint8")

if __name__ == "__main__":
    dsExtractor = DatasetExtractor(["non-spam-easy", "non-spam-hard"], ["spam"])
    dsExtractor.create_cv_set(0.1)
    dsExtractor.create_test_set(0.1)
    dsExtractor.save_dataset()