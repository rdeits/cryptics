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
	export PYTHONPATH="<your-local-path>/cryptics:${PYTHONPATH}"
	
. Then generate the n-grams and synonyms datasets by running

	rake data

in the main cryptics folder (this will take a few minutes to finish). 

# Usage:

Web interface: http://localhost:8080/

	rake server

Test cases (requires the python nose package):

	rake test

# Clue format:

Clue:

	Initially babies are naked (4)

Answer:

	BARE

Clue: 

	Lees horse galloping to dangerous_coasts (3,6) l.....r..

Answer: 

	LEE_SHORES

You can give the solver a hint that a set of words form a phrase (and need not be treated separately) by combining them with an underscore (as in 'dangerous_coasts' above). 


# Acknowledgements

This program uses the English bigrams corpus from [After the Deadline](http://blog.afterthedeadline.com/2010/07/20/after-the-deadline-bigram-corpus-our-gift-to-you/) licensed under the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). 

In addition, it uses the UK Advanced Cryptics Dictionary, Copyright (c) 2009 J Ross Beresford. For license information see `raw_data/UKACD.txt.`

# License

See LICENSE.txt

