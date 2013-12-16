import os
from collections import defaultdict

INDICATORS = defaultdict(lambda: [])

print "Loading indicators from file..."
for kind in os.listdir('indicators/'):
    INDICATORS[kind] = [s.strip() for s in open('indicators/' + kind, 'r').readlines()]
print "...done."
