# Required python packages:

	nose
	web
	nltk

# Installation:

Add the cryptics folder to your PYTHONPATH. Then generate the n-grams and synonyms datasets by running

	rake data

in the main cryptics folder (this will take a few minutes to finish). 

# Usage:

Web interface: http://localhost:8080/

	python crypticweb/server.py

Test cases (requires the python nose package):

	nosetests --nocapture

# Clue format:

Clue:

	Initially babies are naked (4) b.r. 

Answer:

	BARE

Clue: 

	Lees horse galloping to dangerous_coasts (3,6) l.....r..

Answer: 

	LEE_SHORES

You can give the solver a hint that a set of words form a phrase (and need not be treated separately) by combining them with an underscore (as in 'dangerous_coasts' above). 

