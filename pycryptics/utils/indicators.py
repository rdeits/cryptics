INDICATORS = dict()

for kind in ['ana_', 'ins_', 'rev_', 'sub_']:
    INDICATORS[kind] = [s.strip() for s in open('indicators/' + kind, 'r').readlines()]
