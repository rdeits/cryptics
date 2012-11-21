import re


def matches_pattern(word, pattern):
    """
    Pattern is a very basic regex, which must have a letter-for-letter mapping with the target string. For example, '.s...a.' is good, but '.s.*a.' will not work.
    """
    if pattern == '':
        return True
    else:
        return bool(re.match(pattern[:len(word)], word))


def split_words(ans, lengths):
    j = 0
    words = []
    for i, l in enumerate(lengths):
        words.append(ans[j:j + l])
        j += l
    return words


def partial_answer_test(ans, phrasing, lengths, pattern, initial_ngrams):
    words = split_words(ans, lengths)
    return len(ans) <= sum(lengths) and matches_pattern(ans, pattern) and all(words[i] in initial_ngrams[l][len(words[i])] for i, l in enumerate(lengths)) and not any(w in phrasing for w in words)


def answer_test(ans, lengths, pattern, word_list):
    return len(ans) == sum(lengths) and matches_pattern(ans, pattern) and all(w in word_list for w in split_words(ans, lengths)) and 
