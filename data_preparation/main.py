### This module is designed to prepare the raw data for usage.
### It performs the following actions:
### 1) reads the hand-written dictionary from dict.ods and writes it into
###    another file called "dict.json";
### 2) reads the words from file uk_UA.dic, crops them and writes into the file
###    'ua_words.dic';
### 3) using the words from the file mentioned above, this module filters the
###    file cc.uk.300.vec and rewrites it into filtered.300.vec in order to
###    make sure all the words are valid in ukrainian language and to make the
###    rest of the coursework programs execute faster.
###
### Runtime of this module on my PC is about one minute.


import json
from pyexcel_ods3 import get_data

ASSOC_DCT_ODS = "C:/UCU/SEMESTR_2/Programming/WA/original_data/dict.ods"
ASSOC_DCT_JSON = "C:/UCU/SEMESTR_2/Programming/WA/processed_data/dict.json"
WORDS_ORIGINAL = "C:/UCU/SEMESTR_2/Programming/WA/original_data/uk_UA.dic"
WORDS_RESULT = "C:/UCU/SEMESTR_2/Programming/WA/processed_data/ua.dic"
VEC_ORIGINAL = "C:/UCU/SEMESTR_2/Programming/WA/original_data/cc.uk.300.vec"
VEC_RESULT = "C:/UCU/SEMESTR_2/Programming/WA/processed_data/filtered.300.vec"


def m_f_present(row):
    """
    This function checks if male or female associations are present in the given row.
    If, for example, female associations are present, and male are not, it returns
    (False, True).
    :param row: list, which represents the row
    :return: tuple, that has two boolean values
    """
    try:
        male_present = True
        if not row[1]:
            raise IndexError
    except IndexError:
        male_present = False
    try:
        female_present = True
        if not row[5]:
            raise IndexError
    except IndexError:
        female_present = False

    return male_present, female_present


def create_dict():
    """
    Creates the file "dict.json" from "dict.ods".
    Runtime: 0.57 seconds
    """
    df = get_data(ASSOC_DCT_ODS)

    dct = {}
    current_key = ''
    for row in df["Аркуш1"]:
        # check if reached the end of the document
        if not row:
            break
        # check if the word has any more male and/or female associations
        m_f = m_f_present(row)
        if row[0] != "":
            current_key = row[0]

            if m_f == (True, True):
                dct[current_key] = ([row[3], (row[1], row[2])], [row[7], (row[5], row[6])])
            elif m_f == (True, False):
                dct[current_key] = ([row[3], (row[1], row[2])], [])
            else:
                dct[current_key] = ([], [row[7], (row[5], row[6])])

        else:
            if m_f[0]:
                dct[current_key][0].append((row[1], row[2]))
            if m_f[1]:
                dct[current_key][1].append((row[5], row[6]))

    f = open(ASSOC_DCT_JSON, 'w')
    f.write(json.dumps(dct, ensure_ascii=False, indent=2))
    f.close()


def crop_words_filter_vectors():
    """
    1) Creates the file "ua.dic" from "uk_UA.dic", namely crops the words from the
    original file.
    2) Filters the vectors file using the mentioned words.
    Runtime: 62 seconds
    """
    # load the list of ukrainian words to check if the associations taken from
    # the file are valid, namely are real ukrainian words.
    valid = set()
    with open(WORDS_ORIGINAL, 'r', encoding='utf-8') as original:
        with open(WORDS_RESULT, 'w', encoding='utf-8') as result:
            line = original.readline()
            result.write(line)

            while True:
                line = original.readline()

                if not line:
                    break
                    # same as .vec files, no StopIteration exception

                valid.add(line.split('/')[0].strip())
                result.write(line.split('/')[0].strip() + '\n')

    with open(VEC_ORIGINAL, 'r', encoding='utf-8') as original:
        with open(VEC_RESULT, 'w', encoding='utf-8') as result:
            line = original.readline()  # read the starting line
            result.write('57422 300\n') # launched the another program just to count this value
                                # it is imposiible to insert text into a file
                                # without rewriting it, so it was necessary

            while True:
                line = original.readline()

                if not line:
                    break

                curword = line.split()[0]

                if curword in valid:
                    result.write(line)


if __name__ == "__main__":
    create_dict()
    crop_words_filter_vectors()
