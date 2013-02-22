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

	['bare', 1, '(top (sub (sub_ "initially") (lit "babies") -> B) (lit "are") (d "naked") -> BARE)'] 

The three elements in the output are: [answer, score, structured clue]. So, in the above example, the answer is "bare", the score is 1 (the highest possible value), and the structured clue involves a substring of "BABIES" added to "ARE" to get "BARE". 

# Solving Method
>"Do the stupidest thing that could possibly work"

Rather than trying to predict the way a particular clue will be solved from its text alone, the solver attempts to try all remotely possible solutions for a given clue, then scores them by how well their answers match the clue. To do that, I make some assumptions:

1. The structure of a cryptic crossword clue can be reasonably well-approximated by a fairly restricted [CFG (context-free grammar)](http://en.wikipedia.org/wiki/Context-free_grammar) and can be parsed into a syntactic tree using that grammar.

2. A clue always consists of two parts: a definition and a wordplay component. 

3. The definition is always the first or last phrase in the clue.

4. The wordplay consists of combinations of known functions, such as substrings, anagrams, synonyms, reversals, insertions, etc.

In practice, these assumptions are pretty good. 



To solve a clue, the solver first determines all possible ways to combine words from the clue into phrases (where a "phrase" is one or more words connected by underscores). For example, one phrasing of the clue "Initially babies are naked" is \["initially", "babies", "are", "naked\], another is \["initially", "babies_are", "naked"\], and another is \["initially", "babies_are_naked"\] 

Next, the definition of the clue is chosen to be the first or last phrase (both possibilities are fully explored by the solver). Finally, the remaining words are passed into the wordplay context-free grammar to determine all of the ways that each word could be used. The CFG used is one that I developed based on my observations about cryptic clues. It encodes various rules which are commonly followed, such as that we almost never take an anagram of anything except a literal word from the clue, but we might insert that anagram into another word. 

For each phrasing, we use the CFG to generate all possible syntactic structures for those words. The CFG is very lenient about allowing words to have a variety of meanings, but it does have lists of common function indicators, which it uses to eliminate unlikely parses. For example, "initially" is almost always a substring indicator, so it will almost certainly not act as an anagram or reversal indicator. 

Such a structure for ["initially", "babies", "are", "naked] is:

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

## Update 2013-02-22:
As of now, the solver has been reimplemented entirely in Python. I've spent some time playing around with the [RunSnakeRun](http://www.vrplumber.com/programming/runsnakerun/) profiling tool, and I've managed to make the pure-Python solver faster than the hybrid Python-Go solver was. 

# Examples

Here are some clues, along with the first few answers returned by the solver. Each answer is given along with its score (from 0 to 1) and the wordplay structures which created it. 

##Spin broken shingle (7) 
Correct answer: ENGLISH

**english**: 1 

	['english', 1, '(top (d "spin") (ana (ana_ "broken") (lit "shingle") -> ENGLISH))'] 
	['english', 0.24, '(top (syn "spin" -> ENGLISH) (d "broken_shingle"))'] 
**violate**: 0.333333333333 

	['violate', 0.3333333333333333, '(top (sub (sub_ "spin") (syn "broken" -> VIOLATED) -> VIOLATE) (d "shingle"))'] 
**reached**: 0.333333333333 

	['reached', 0.3333333333333333, '(top (sub (sub_ "spin") (syn "broken" -> BREACHED) -> REACHED) (d "shingle"))'] 

## M's Rob Titon pitching slider? (10)
Correct answer: TROMBONIST

**trombonist**: 0.631578947368 

	['trombonist', 0.631578947368421, '(top (ana (lit "ms_rob_titon") (ana_ "pitching") -> TROMBONIST) (d "slider"))'] 
**surcharges**: 0.333333333333 

	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon") (rev (syn "pitching" -> SLOPING) (rev_ "slider") -> GNIPOLS) -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (rev (rev_ "titon") (syn "pitching" -> SLOPING) -> GNIPOLS) (sub_ "slider") -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon_pitching") (lit "slider") -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon_pitching") (syn "slider" -> SKIDDER) -> S) -> SURCHARGES)'] 
**manuscript**: 0.25 

	['manuscript', 0.25, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (sub (sub_ "titon") (syn "pitching" -> CANT) -> T) (d "slider") -> MANUSCRIPT)'] 
	['manuscript', 0.25, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (first "titon_pitching" -> T) (d "slider") -> MANUSCRIPT)'] 
	['manuscript', 0.225, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (first "titon" -> T) (d "pitching_slider") -> MANUSCRIPT)'] 

## Sat up, interrupting sibling's balance (6) s.....
Correct answer: STASIS

**stasis**: 1 

	[u'stasis', 1, u'(top (ins (rev (lit "sat") (rev_ "up") -> TAS) (ins_ "interrupting") (syn "siblings" -> SIS) -> STASIS) (d "balance"))'] 
	[u'stasis', 1, u'(top (ana (lit "sat") (ana_ "up_interrupting") -> STA) (syn "siblings" -> SIS) (d "balance") -> STASIS)'] 
**sprout**: 0.533333333333 

	['sprout', 0.5333333333333333, '(top (ins (sub (sub_ "sat") (syn "up" -> SPROUT) -> PROUT) (ins_ "interrupting") (first "siblings" -> S) -> SPROUT) (d "balance"))'] 
	['sprout', 0.5333333333333333, '(top (first "sat" -> S) (sub (syn "up" -> SPROUT) (sub_ "interrupting_siblings") -> PROUT) (d "balance") -> SPROUT)'] 

**sprint**: 0.25 

	['sprint', 0.25, '(top (sub (sub_ "sat") (syn "up" -> SPROUT) -> SPR) (sub (lit "interrupting") (sub_ "siblings") -> INT) (d "balance") -> SPRINT)'] 


# Acknowledgements

This program uses the English bigrams corpus from [After the Deadline](http://blog.afterthedeadline.com/2010/07/20/after-the-deadline-bigram-corpus-our-gift-to-you/) licensed under the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). 

In addition, it uses the UK Advanced Cryptics Dictionary, Copyright (c) 2009 J Ross Beresford. For license information see `raw_data/UKACD.txt.`

Indicator word lists are from:
http://sutherland-studios.com.au/puzzles/anagram.php
http://www.crosswordunclued.com/2008/09/dictionary.html

# License

See LICENSE.txt

