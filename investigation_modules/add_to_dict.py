### This module is the main module of the work. It composes a dictionary using
### the files from 'processed_data' folder and writes it into a resulting file.
### Since the procedure of composing the result is very long, this program can
### add the new information to a file without losing the previous progress.


import json
import os
from math import log
from bigraph import Bigraph


WORDS_FROM_VECS = 7

VEC_RESULT = "C:/UCU/SEMESTR_2/Programming/word_associations/processed_data/filtered.300.vec"
ASSOC_DCT_JSON = "C:/UCU/SEMESTR_2/Programming/word_associations/processed_data/dict.json"
INCENTIVES = "C:/UCU/SEMESTR_2/Programming/word_associations/results/inc.list"
# contains all the incentives of the resulting file
RESULT = "C:/UCU/SEMESTR_2/Programming/word_associations/results/RESULT.json"


def cut_vector(line):
    return list(map(lambda x: float(x), line.split(' ')[1:]))


def find_delta(lst1, lst2):
    res = 0
    for el in zip(lst1, lst2):
        res += abs(el[0] - el[1])
    return res


def insert_word(word, difference, top, points):
    """
    This function is a helping function for find_closest.
    For example, if we search associations to word 'football' and encountered a
    word 'ball' in the file:

    word: ball

    difference: 82

    top: game
         baseball
         match

    points (differences): 77
                          85
                          101

    the result will be:
    top: game
         ball
         baseball

    points: 77
            82
            85
    """
    current = len(points) - 1
    while points[current] > difference and current > -1:
        current -= 1

    if current < len(points) - 1:
        points.insert(current + 1, difference)
        top.insert(current + 1, word)
        points.pop(-1)
        top.pop(-1)


def find_closest(word, path, amount):
    """
    Finds a given amount of words that are closest to the given word compared
    by word vectors

    precondition:
    amount is less than the number of lines in the file
    """
    with open(path, 'r', encoding='utf-8') as file:
        main_vector = []
        # find the needed vector
        line = file.readline()
        found = False

        while not found:
            line = file.readline()
            try:
                curword = line.split()[0]
            except IndexError:  # IndexError occurs because the end of file has
                break   # empty lines. This is why there is no check for StopIteration
            if curword == word:
                main_vector = cut_vector(line)
                found = True
    if not main_vector:
        return []

    # look through the file and refresh the top-amount list every time
    result = []
    deltas = []
    with open(path, 'r', encoding='utf-8') as file:
        line = file.readline()
        # initialize the two lists
        for i in range(amount + 1):
            result.append('*' * i + "****") # just random values to somehow
            deltas.append(10000) # fill the lists (the number here must be big)

        while True:
            line = file.readline()
            try:
                curword = line.split()[0]
            except IndexError:  # IndexError occurs because the end of file has
                break   # empty lines. This is why there is no check for StopIteration
            curvector = cut_vector(line)

            insert_word(curword, find_delta(curvector, main_vector), result, deltas)

    return result[1:]


def form_response(word, vectors, assoc_dct={}):
    """
    This function returns a set of tuples for one particular incentive word,
    as in the assoc_dct (that one from json file)
    It uses both hand-written dictionary and the vectors file.
    """
    res = {}

    # add the part from hand-written dictionary
    if word in assoc_dct:
        for response in assoc_dct[word][0][1:]:
            res[response[0]] = response[1]
        for response in assoc_dct[word][1][1:]:
            if response[0] in res:
                res[response[0]] = (res[response[0]] + response[1]) // 2
            else:
                res[response[0]] = response[1]

    # add the part from word vectors file
    from_vecs = []
    closest = find_closest(word, vectors, WORDS_FROM_VECS)
    for el in closest:
        if el not in res:
            from_vecs.append(el)

    lowest = 1000
    for el in res:
        if res[el] < lowest:
            lowest = res[el]

    if lowest == 1000:  # if all words from ASSOC_DCT_JSON have been added already
        # compute delta for each pair of words
        deltas = [0] * len(from_vecs)

        # find the vector of word
        with open(VEC_RESULT, 'r', encoding='utf-8') as file:
            line = file.readline()
            while True:
                line = file.readline()
                if line.split()[0].strip() == word:
                    mainvec = cut_vector(line)
                    break

        with open(VEC_RESULT, 'r', encoding='utf-8') as file:
            line = file.readline()
            while True:
                # no IndexError exception will be catched here, because all the
                # searched words definitely are in the file
                line = file.readline()
                if line.split()[0] in from_vecs:
                    deltas[from_vecs.index(line.split()[0])] = \
                    find_delta(mainvec, cut_vector(line))
                    if 0 not in deltas:
                        break

        # just a formula that roughly estimates the number of responses for
        # each response word, that derives from vectors file
        deltas = list(map(lambda x: (25 / x) ** 2, deltas))
        deltas = list(map(lambda x: round(2 * x ** (1 / x ** 0.22)), deltas))
        for el in zip(from_vecs, deltas):
            if el[1] > 0:
                res[el[0]] = el[1]
            else:
                res[el[0]] = 1

        result = []
        for el in res:
            result.append((el, res[el]))

        return sorted(result, key=lambda x: x[1], reverse=True)

    try:
        c = lowest ** (1.0 / len(from_vecs))
    except ZeroDivisionError:  # occurs if from_vecs is empty
        result = []
        for el in res:
            result.append((el, res[el]))

        return sorted(result, key=lambda x: x[1], reverse=True)

    from_vecs.reverse()

    for i in range(len(from_vecs)):
        res[from_vecs[i]] = round(c ** i)

    result = []
    for el in res:
        result.append((el, res[el]))

    return sorted(result, key=lambda x: x[1], reverse=True)


def complete_dct():
    """
    This function adds words to the resulting dictionary till there are some
    of them that are present in hand-written dictionary and absent from the
    result file (or from INCENTIVES file). After that the function adds words
    using vectors file only.
    """
    # some initial preparations
    words_amount = 0
    while not words_amount:
        try:
            words_amount = int(input("How many words do you want to add during this session? (1 word = 20 sec) "))
        except Exception:
            print("Usage: input a positive integer")

    if not os.path.isfile(INCENTIVES):
        with open(INCENTIVES, 'w', encoding='utf-8') as file:
            file.write('0')

    if os.path.isfile(RESULT):
        with open(RESULT) as file:
            dct = json.load(file, encoding='utf-8')
    else:
        dct = {}

    # load the list of added words from INCENTIVES file
    added = []
    with open(INCENTIVES, 'r', encoding='utf-8') as file:
        added_amount = file.readline()  # read the first line
        word = file.readline().strip()
        while word:
            added.append(word)
            word = file.readline().strip()

    # load the list of words from the hand-written dictionary
    with open(ASSOC_DCT_JSON) as file:
        assoc_dct = json.load(file, encoding='utf-8')

    written = sorted(list(assoc_dct.keys()))

    # initialize the Bigraph class instance
    b = Bigraph()

    # check if all the words from the hand-written dictionary have been added
    not_added = []
    for word in written:
        if word not in added:
            not_added.append(word)

    no_assoc = []
    counter = 0
    for word in not_added:
        if counter >= words_amount:
            break

        response = form_response(word, VEC_RESULT, assoc_dct)
        if response:
            b[word] = response
            print("Added word " + word, str(counter + 1) + '/' + str(words_amount))
            counter += 1
        else:
            no_assoc.append(word)

    if not not_added:
        print("The hand-written dict is all added.")
        add_from_vecs = input("Do you want to add the words using word vectors only? (y for yes) ")
        if add_from_vecs == 'y':
            counter = 0
            # form response for each word in the vectors file if it is not added yet
            with open(VEC_RESULT, 'r', encoding='utf-8') as file:
                line = file.readline()
                while counter < words_amount:
                    try:
                        line = file.readline()
                        word = line.split()[0]
                    except IndexError:
                        print("Looks like all the available words have been added")
                        break
                    if word not in added:
                        b[word] = form_response(word, VEC_RESULT, assoc_dct)
                        print("Added word " + word, str(counter + 1) + '/' + str(words_amount))
                        counter += 1
        else:
            return

    # transfer the words and their associations to the files
    for recently_added in b:
        added.append(recently_added)
        dct[recently_added] = b[recently_added]

    with open(RESULT, 'w') as f:
        f.write(json.dumps(dct, ensure_ascii=False, indent=2))

    with open(INCENTIVES, 'w', encoding='utf-8') as f:
        f.write(str(len(added)))
        added.sort()
        for el in added:
            f.write('\n' + el)

    if no_assoc:
        print("These words have no associations: " + ', '.join(no_assoc))

    return


if __name__ == "__main__":
    complete_dct()
