from pycryptics.utils.indicators import INDICATORS

class Production:
    def __init__(self, name, num_args, arg_types, has_ind=False):
        self.name = name
        self.num_args = num_args
        self.arg_types = set(arg_types)
        self.has_ind = has_ind
        self.ind_words = set([])

    def locate(self, parsing):
        positions = []
        if self.has_ind:
            for start in range(len(parsing) - self.num_args + 1):
                for ind_pos in range(self.num_args):
                    if parsing[start + ind_pos][0] in self.ind_words and all(p[0] in self.arg_types for p in parsing[start:start+ind_pos] + parsing[start+ind_pos+1:start+self.num_args]):
                        positions.append((start, ind_pos))
        else:
            for start in range(len(parsing) - self.num_args + 1):
                if all(p[0] in self.arg_types for p in parsing[start:start+self.num_args]):
                    positions.append((start, None))
        return positions

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

known_functions = {
'in': ['ins', 'lit', 'null', 'sub'],
'a': ['lit', 'syn', 'null'],
'is': ['null', 'lit'],
'for': ['null', 'syn'],
'large': ['first', 'syn'],
'primarily': ['sub'],
'and': ['null', 'lit'],
'of': ['null'],
'with': ['null', 'ins']}

def generate_productions(phrases):
    ind_productions = {
        'ana': Production('ana', 2, ['lit'], True),
        'rev': Production('rev', 2, ['lit', 'syn'], True),
        'sub': Production('sub', 2, ['lit', 'syn', 'rev'], True),
        'ins': Production('ins', 3, ['lit', 'ana', 'syn', 'sub', 'first', 'rev'], True)
        }

    base_productions = {
        'first': Production('first', 1, []),
        'lit': Production('lit', 1, []),
        'syn': Production('syn', 1, []),
        'null': Production('null', 1, [])
        }

    top_args = ind_productions.keys() + base_productions.keys() + ['d']
    top_productions = [
        Production('top', 2, top_args),
        Production('top', 3, top_args),
        Production('top', 4, top_args)]

    for p in phrases:
        if p in known_functions:
            for f in known_functions[p]:
                if f in base_productions:
                    base_productions[f].arg_types.add(p)
                elif f in ind_productions:
                    ind_productions[f].ind_words.add(p)
        else:
            found = False
            for kind, words in INDICATORS.items():
                if p in words:
                    found = True
                    ind_productions[kind].ind_words.add(p)
            if not found:
                for kind in ['ana', 'rev', 'sub']:
                    ind_productions[kind].ind_words.add(p)
            for kind in ['first', 'lit', 'syn']:
                base_productions[kind].arg_types.add(p)
    return base_productions.values() + ind_productions.values() + top_productions

if __name__ == '__main__':
    prods = generate_productions('unsuitable paint smeared'.split(' '))
    import pdb; pdb.set_trace()
