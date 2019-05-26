# Word associations

Coursework by Bohdan Pysko


This project was created as an e-version of the dictionary
of associations for Ukrainian language.

1. The purpose of this program is to create an e-version of
association dictionary for Ukrainian language. The user can
input any word, and if that word is in the dictionary, he
will get the list of associations to that word and amount
of ocurrences for each association.

2. The program gets a dictionary in .ods file as input.
Also it gets a word embeddings file (.300.vec) and a list
of ukrainian words in a .list file.
The result of this program's work is two files, one is a
.json file - the dictionary itself, and the second is a
.list file - the list of available incentives.

3. The project contains following folders:
	data_preparation
	interaction
	investigation_modules
	original_data
	processed_data
	results

Folders original_data and processed_data are absent from
the repo because they contain too large files.
Now let's discuss every folder one by one:
data_preparation contains file main.py which processes
files from original_data folder and writes them into
processed_data folder. 
interaction folder has main.py file
in it, and this file provides possibility for the user to
interact with the program.
investigation_modules contains following files:
	add_to_dict.py - creates the resulting dictionary
	bigraph.py - ADT, used in add_to_dict.py
	bigraph_test.py - unittests for the ADT
	use_bigraph_example.py - an example of my ADT usage
original_data:
	cc.uk.300.vec - word embeddings (2 000 000 words)
	dict.ods - hand-written table (data from paper
					dictionary)
	uk_UA.dic - list of ukrainian words, used to filter
		    the embeddings file (111 403 words)
processed_data:
	dict.json - processed dict.ods
	filtered.300.vec - processed cc.uk.300.vec
			   (57 422 words)
	ua.dic - processed uk_UA.dic (same 111 403 words)
results:
	RESULT.json - the resulting dictionary
	inc.list - contains all the incentives from
		   RESULT.json (842 words and will grow)

4. To start the program execute the main.py module in the
interaction folder. To add words to the resulting file
execute the add_to_dict.py module in investigation_modules.

4*. To download the program you can download the .exe file
from folder dist.

5. You can find the documentation for this project in
docs/build/html/rst.