import nltk

WORDS = set(word.lower() for word in nltk.corpus.words.words())


# def middle_letters(word):
#     if len(word) % 2 == 0:
#         return word[len(word) // 2 - 1:len(word) // 2]
#     else:
#         return word[len(word) // 2]

# word_functions = {
#     'literal': lambda x: x,
#     'first': lambda x: x[0],
#     'last': lambda x: x[-1],
#     'outside': lambda x: x[0] + x[-1],
#     'middle': middle_letters,
#     'synonym': synonyms,
#     'null': lambda x: ''
#     }


# def possible_answers(words, length):
#     answers = set([])
#     for word in [words[0], words[-1]]:
#         answers.update(synonyms(word))
#     return answers



# def constructed_answers(words):
#     if len(words) == 0:
#         return ['']
#     answers = set([])
#     for action in word_functions:
#         for substring in constructed_answers(words[1:]):
#             answers.add(action(words[0]) + substring)
#     return answers
