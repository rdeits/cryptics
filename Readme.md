# Introduction
This is a general cryptic crossword clue solver, written in Python

# Required python packages:

	nose
	web
	nltk
	tk

# Other requirements:

	python (tested with 2.7)
	rake

# Installation:

Clone this repository somewhere convenient, then `cd` to the folder containing this file. 

Run this command to download the Nodebox Linguistics library from [http://nodebox.net/code/index.php/Linguistics](http://nodebox.net/code/index.php/Linguistics) and the python NLTK Wordnet corpus from [http://nltk.org/data.html](http://nltk.org/data.html):

	rake download
	
Generate the n-grams and synonyms datasets by running

	rake data

in the main cryptics folder (this will take a few minutes to finish). 

# Usage:

Web interface: http://localhost:8080/

	rake server

Test cases (requires the python nose package):

	rake test

## Clue format:

For each clue, you _must_ give the number of letters in the answer, and you _may_ give a letter pattern for the answer to follow, where a '.' represents an unknown letter (ignoring spaces). For example:

Clue:

	Initially babies are naked (4)

Answer:

	BARE

Clue: 

	Lees horse galloping to dangerous_coasts (3,6) l.....r..

Answer: 

	LEE_SHORES

You can give the solver a hint that a set of words form a phrase (and need not be treated separately) by combining them with an underscore (as in 'dangerous_coasts' above). 

## Output format: 

The output is given both as a hierarchical representation of the clue structure and as a natural-language description:

	100%: (top (sub (sub_ "initially") (lit "babies") -> B) (lit "are") (d "naked") -> BARE) 
	'initially' means to take a substring of 'babies' to get B. 
	'naked' is the definition. 
	Combine 'b' and 'are' to get BARE. 
	BARE matches 'naked' with confidence score 100%. 

and

	90%: (top (lit "lees") (ana (lit "horse") (ana_ "galloping") -> HORES) (d "to_dangerous_coasts") -> LEE_SHORES) 
	'galloping' means to anagram 'horse' to get HORES. 
	'to_dangerous_coasts' is the definition. 
	Combine 'lees' and 'hores' to get LEE_SHORES. 
	LEE_SHORES matches 'to_dangerous_coasts' with confidence score 90%. 

# More Information

To learn more about how the solver works, see this blog post: [http://blog.robindeits.com/2013/02/11/a-cryptic-crossword-clue-solver/](http://blog.robindeits.com/2013/02/11/a-cryptic-crossword-clue-solver/).


# Acknowledgements

This program uses the English bigrams corpus from [After the Deadline](http://blog.afterthedeadline.com/2010/07/20/after-the-deadline-bigram-corpus-our-gift-to-you/) licensed under the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). 

In addition, it uses the UK Advanced Cryptics Dictionary, Copyright (c) 2009 J Ross Beresford. For license information see `raw_data/UKACD.txt.`

Indicator word lists are from:
http://sutherland-studios.com.au/puzzles/anagram.php
http://www.crosswordunclued.com/2008/09/dictionary.html

# License

See LICENSE.txt

