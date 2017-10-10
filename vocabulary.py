import os

def getVocabList():
    """
    Loads the vocabulary list into memory and create array with it's contents
    :return: array containing vocabulary or None if sth went wrong
    """
    project_path = os.path.dirname(os.path.realpath(__file__))
    fp = project_path + '/vocabulary.txt'
    if os.path.exists(fp):
        file = open(fp, 'r')
        vocab_list = []
        for line in file:
            line = line.lower()
            line = line.replace(' ', '')
            if not len(line)==0:
                vocab_list.append(line)
        print(len(vocab_list))
        return vocab_list

    return None
