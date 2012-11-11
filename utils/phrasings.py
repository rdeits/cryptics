def phrasings(remaining):
    if len(remaining) <= 1:
        return [remaining]
    else:
        new_active_set = []
        for i in range(len(remaining)):
            new_phrase = '_'.join(remaining[:i + 1])
            new_remaining = remaining[i + 1:]
            for new_s in phrasings(new_remaining):
                new_active_set.append([new_phrase] + new_s)
        return new_active_set
