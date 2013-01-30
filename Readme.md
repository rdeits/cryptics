# Introduction
This is a general cryptic crossword clue solver, written in a mix of Python and Go. 

# Required python packages:

	nose
	web
	nltk
	tk

# Other requirements:

	python (tested with 2.7)
	rake
	git
	go (tested with v.1.0.2)

# Installation:

Add the appropriate folders to your various PATH variables:

	export GOPATH="<your-local-path>/cryptics/go:${GOPATH}"
	export PATH="<your-local-path>/cryptics/go/bin:${PATH}"
	export PYTHONPATH="<your-local-path>/cryptics/pycryptics:${PYTHONPATH}"
	
Then generate the n-grams and synonyms datasets by running

	rake data

in the main cryptics folder (this will take a few minutes to finish). 

# Usage:

Web interface: http://localhost:8080/

	rake server

Test cases (requires the python nose package):

	rake test

## Clue format:

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

The output is in the form of a solved, structured clue in the following form: 

	['bare', 1, ('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')] 

The three elements in the output are: [answer, score, structured clue]. So, in the above example, the answer is "bare", the score is 1 (the highest possible value), and the structured clue involves a substring of "BABIES" added to "ARE" to get "BARE". 

# Solving Method

>"Do the stupidest thing that could possibly work"

Rather than trying to predict the way a particular clue will be solved from its text alone, this solver attempts to try all remotely possible solutions for a given clue, then scores them by how well their answers match the clue. To do that, I make some assumptions:

1. The structure of a cryptic crossword clue can be reasonably well-approximated by a fairly restricted CFG (context-free grammar) and can be parsed into a syntactic tree using that grammar.

2. A clue always consists of two parts: a definition and a wordplay component. 

3. The definition is always the first or last phrase in the clue.

4. The wordplay consists of combinations of known functions, such as substrings, anagrams, synonyms, reversals, insertions, etc.

In practice, these assumptions are pretty good. 

Given a clue, we first break the clue up into phrases (where a "phrase" is one or more words connected by underscores). For example, one phrasing of the clue "Initially babies are naked" is ["initially", "babies", "are", "naked], and another is ["initially", "babies_are", "naked"]. For each phrasing, we use the CFG to generate all possible syntactic structures for those words. For example, a structure for ["initially", "babies", "are", "naked] is:

	('top', 
	  (sub, 
	  	('sub_', 'initially'), 
	  	('lit', 'babies')), 
	  ('lit', 'are'), 
	  ('d', 'naked')
	). 

'top' means to concatenate the strings produced by all of its arguments, and is always the top-level structure in a cryptic clue.

'sub' indicates a substring

'sub_' identifies the substring indicator word ("initially")

'lit' returns a word literally

'd' indicates the definition part of the clue

So, this structure says: "combine a substring of BABIES with ARE to get a word that means NAKED". Evaluating this for all substrings of BABIES, we come up with a single answer which is actually a word: B + ARE = BARE. Since BARE and NAKED are truly synonyms, we give this answer the maximal score of 1. 


The output format of the solver gives not only this score, but also the substrings which each part of the clue yielded: 

	['bare', 
	 1, 
	 ('top', 
	   ('sub', 
	     ('sub_', 'initially', ''), 
	     ('lit', 'babies', 'BABIES'), 
	   	  'B'), 
	   ('lit', 'are', 'ARE'), 
	   ('d', 'naked', ''), 
	  'BARE')
	] 

Of course, we are certain to produce a great many bad answers using this method, for example: 

	['evil', 
	 0, 
	 ('top', 
	   ('d', 'initially', ''), 
	   ('rev', 
	     ('rev_', 'babies', ''), 
	     ('syn', 'are', 'LIVE'), 
	    'EVIL'), 
	   ('null', 'naked', ''), 
	  'EVIL')
	]

The above says: "Take a synonym of 'are': LIVE, reverse it: EVIL to get a word meaning INITIALLY. However, the similarity in meaning between EVIL and INITIALLY is essentially zero, so this answer gets a score of 0. 
In this way, we generate the most probable interpretation and solution for a given clue. 

# Internal Implementation

Currently, the solver is implemented in a mix of Python (for its fantastic Natural Language Toolkit) and Go (for its speed and concurrency). The web server, CFG parser, and answer scoring are implemented in Python, while the solving mechanics are all implemented in Go. The Go code runs as a subprocess spawned from Python and communicates over Stdin/Stdout.  Structured clues, such as: 

	('top', (sub, ('sub_', 'initially'), ('lit', 'babies')), ('lit', 'are'), ('d', 'naked'))

are generated in Python and sent to the Go solver over Stdin, and solved structured clues, such as: 

	('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')

are returned from the Go solver to Python to have their answers scored and displayed. 


# Acknowledgements

This program uses the English bigrams corpus from [After the Deadline](http://blog.afterthedeadline.com/2010/07/20/after-the-deadline-bigram-corpus-our-gift-to-you/) licensed under the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). 

In addition, it uses the UK Advanced Cryptics Dictionary, Copyright (c) 2009 J Ross Beresford. For license information see `raw_data/UKACD.txt.`

Indicator word lists are from:
http://sutherland-studios.com.au/puzzles/anagram.php
http://www.crosswordunclued.com/2008/09/dictionary.html

# License

See LICENSE.txt

