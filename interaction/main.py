"""
Provides interaction with the user.

Libraries and packages:
json
os
"""


import json
import os

INCENTIVES = "../results/inc.list"
RESULT = "../results/RESULT.json"


if __name__ == "__main__":

    if not os.path.isfile(INCENTIVES):
        print("Unfortunately, there is nothing to show yet.")
    else:
        # read the incentives file
        added = []
        with open(INCENTIVES, 'r', encoding='utf-8') as file:
            number = int(file.readline().strip())  # read the number of words available
            word = file.readline().strip()
            while word:
                added.append(word)
                word = file.readline().strip()

        # read the dictionary file
        with open(RESULT) as file:
            dct = json.load(file, encoding='utf-8')

        print("You can find associations to {} words here:".format(number))
        for el in added:
            print(el)

        message = '0'
        print("\nPress ENTER to quit")
        while message:
            message = input("\nIncentive: ")
            if message in added:
                res = ''
                response = dct[message]
                response.sort(key=lambda x: x[1], reverse=True)
                for el in response:
                    res += el[0].ljust(30, ' ') + str(el[1]) + '\n'
                print(res)
            elif message == '':
                pass
            else:
                print("There is no such word in the dictionary")
