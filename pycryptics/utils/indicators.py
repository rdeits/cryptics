INDICATORS = dict()

for kind in ['ana', 'ins', 'rev', 'sub']:
    INDICATORS[kind] = [s.strip() for s in open('indicators/' + kind + '_', 'r').readlines()]
