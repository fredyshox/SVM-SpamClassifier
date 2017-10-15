import os
from email_processor import EmailProcessor
from vocabulary import  getVocabList
import random

# Dataset division:
# 60% train set
# 20% cross validation set
# 20% test set

class DatasetExtractor(object):

    def __init__(self, class0_paths, class1_paths, X = None, y = None):
        object.__init__(self)
        self.cp = os.path.dirname(os.path.realpath(__file__)) + "/dataset"
        self.vocab = getVocabList()
        self.processor = EmailProcessor(self.vocab)
        self.class0_paths = class0_paths
        self.class1_paths = class1_paths
        self.X = X
        self.y = y

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
            self.X[i] = X[random_ind[i]]
            self.y[i] = y[random_ind[i]]

        return (self.X, self.y)

    def save_dataset(self):
        #TODO
        if self.X == None or self.y == None:
            return


    def extract_features(self, paths):
        X_vec = []
        for path in paths:
            f = open(path, "r")
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
