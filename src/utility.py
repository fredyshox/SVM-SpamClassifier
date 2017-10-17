#! /usr/bin/env python
#
# utility.py
#
# Created by Kacper Rączy on 17.10.2017.
# Copyright (c) 2017 Kacper Rączy. All rights reserved.
#
# Utility functions

import os
import random

_IGNORED_FILES = [".DS_Store"]


def elements_with_indices(arr, indices):
    result = []
    count = len(arr)
    for ix in indices:
        if ix >= count:
            continue
        else:
            result.append(arr[ix])
    return result


def random_indices(percent, length):
    count = int(percent * length)
    arr = list(range(length))
    result = []
    for i in range(count):
        rand_id = random.choice(arr)
        result.append(rand_id)
        arr.remove(rand_id)
    return result


def list_files(dir):
    file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    path_list = []
    for file in file_list:
        if file in _IGNORED_FILES:
            continue
        path = dir + "/" + file
        path_list.append(path)
    return path_list
