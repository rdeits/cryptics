import msgpack

with open('data/ngrams.msgpack', 'r') as f:
    NGRAMS = msgpack.load(f, use_list=False)
    for k in NGRAMS:
        NGRAMS[k] = set(NGRAMS[k])

with open('data/initial_ngrams.msgpack', 'r') as f:
    INITIAL_NGRAMS = msgpack.load(f, use_list=False)
    for k in INITIAL_NGRAMS:
        INITIAL_NGRAMS[k] = set(INITIAL_NGRAMS[k])
