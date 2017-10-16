import os
from email_processor import EmailProcessor
from vocabulary import  getVocabList
import random
import numpy as np

# Dataset division:
# 60% train set
# 20% cross validation set
# 20% test set

class DatasetExtractor(object):

    ignored = [".DS_Store"]

    def __init__(self, class0_paths, class1_paths, X = None, y = None):
        object.__init__(self)
        self.cp = os.path.dirname(os.path.realpath(__file__)) + "/dataset/"
        self.vocab = getVocabList()
        self.processor = EmailProcessor(self.vocab)
        self.class0_paths = class0_paths
        self.class1_paths = class1_paths

        self.dataset_length = 0
        self.Xval = []
        self.yval = []
        self.Xtest = []
        self.ytest  = []

        if X==None or y==None:
            self.extract_dataset()
        else:
            self.X = X
            self.y = y
            self.dataset_length = len(X)

    def extract_dataset(self):
        X = []
        y = []
        for path in self.class0_paths:
            files = self.list_files(self.cp + path)
            temp = self.extract_features(files)
            X.extend(temp)
            y = y + [0] * len(temp)

        for path in self.class1_paths:
            files = self.list_files(self.cp + path)
            temp = self.extract_features(files)
            X.extend(temp)
            y = y + [1] * len(temp)

        # randomize order
        random_ind = self.random_indices(1, len(X))
        self.X = []
        self.y = []
        for i in range(len(random_ind)):
            self.X.append(X[random_ind[i]])
            self.y.append(y[random_ind[i]])

        self.dataset_length = len(self.X)
        return (self.X, self.y)

    def create_cv_set(self, percent):
        if percent>1 or percent<0:
            return
        end = int(percent*self.dataset_length)
        self.Xval = self.X[0:end]
        del self.X[0:end]
        self.Val = self.y[0:end]
        del self.y[0:end]
        return

    def create_test_set(self, percent):
        if percent>1 or percent<0:
            return
        end = int(percent*self.dataset_length)
        self.Xtest = self.X[0:end]
        del self.X[0:end]
        self.ytest = self.y[0:end]
        del self.y[0:end]
        return


    def save_dataset(self, path=None):
        if self.X == None or self.y == None:
            return
        else:
            if path==None:
                fp = self.cp + "/spamDataset.npz"
            else:
                fp = self.cp + path

            npX = np.array(self.X)
            npy = np.array(self.y)
            npXval = np.array(self.Xval)
            npyval = np.array(self.yval)
            npXtest = np.array(self.Xtest)
            npytest = np.array(self.ytest)
            np.savez(fp, X=npX, y=npy, X_val=npXval, y_val=npyval, X_test=npXtest, y_test=npytest)
            return

    def extract_features(self, paths):
        X_vec = []
        for path in paths:
            path_comp = path.split("/")
            if path_comp[len(path_comp)-1] in self.ignored:
                del path_comp
                continue
            print(path)
            f = open(path, "r", errors="replace")
            content = f.read()
            indexes = self.processor.process_email(content)
            features = self.processor.email_features(indexes)
            X_vec.append(features)
            del content, f
        return (X_vec)

    def elements_with_indices(self, arr, indices):
        result = []
        count = len(arr)
        for ix in indices:
            if ix >= count:
                continue
            else:
                result.append(arr[ix])
        return result

    def random_indices(self, percent, length):
        count = int(percent * length)
        arr = list(range(length))
        result = []
        for i in range(count):
            rand_id = random.choice(arr)
            result.append(rand_id)
            arr.remove(rand_id)
        return result

    def list_files(self, dir):
        file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        path_list = []
        for file in file_list:
            path = dir + "/" + file
            path_list.append(path)
        return path_list

if __name__ == "__main__":
    dsExtractor = DatasetExtractor(["non-spam-easy", "non-spam-hard"], ["spam"])
    dsExtractor.create_cv_set(0.1)
    dsExtractor.create_test_set(0.1)
    dsExtractor.save_dataset()