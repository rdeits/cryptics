import msgpack

with open('data/synonyms.msgpack', 'r') as f:
    SYNONYMS = msgpack.load(f, use_list=False)


def cached_synonyms(x, length=None):
    x = x.lower()
    if x in SYNONYMS:
        syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
        return set(syns)
    else:
        return set([])
