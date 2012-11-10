def phrasings(remaining, active_set):
    if len(remaining) == 0:
        return active_set
    else:
        for i in range(len(remaining) - 1):
            active_set.extend(phrasings(rema
