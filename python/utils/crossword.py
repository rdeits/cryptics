

def split_words(ans, lengths):
    j = 0
    words = []
    for i, l in enumerate(lengths):
        words.append(ans[j:j + l])
        j += l
    return words
