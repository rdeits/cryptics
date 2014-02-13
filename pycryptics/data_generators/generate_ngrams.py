import msgpack
from pycryptics.utils.synonyms import SYNONYMS

initial_ngrams = dict()
ngrams = dict()

for word in SYNONYMS:
    if '_' in word:
        continue
    l = len(word)
    for i in range(len(word) + 1):
        initial_ngrams.setdefault(l, set([])).add(word[:i])
        for j in range(len(word) - i + 1):
            ngrams.setdefault(l, set([])).add(word[j: j + i])

for k in initial_ngrams:
    initial_ngrams[k] = list(initial_ngrams[k])
for k in ngrams:
    ngrams[k] = list(ngrams[k])

with open('data/initial_ngrams.msgpack', 'w') as f:
    msgpack.dump(initial_ngrams, f)

with open('data/ngrams.msgpack', 'w') as f:
    msgpack.dump(ngrams, f)

