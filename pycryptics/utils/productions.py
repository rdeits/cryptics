class Production:
    def __init__(self, name, num_args, arg_types, ind_words=[]):
        self.name = name
        self.num_args = num_args
        self.arg_types = arg_types
        self.ind_words = ind_words
        if ind_words:
            self.has_ind = True
        else:
            self.has_ind = False

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
        return __str__(self)

ana_prod = Production('ana', 2, ['lit'], ['smeared'])
lit_prod = Production('lit', 1, ['paint'])
top_prod = Production('top', 2, ['ana', 'd'])

PRODUCTIONS = [ana_prod, lit_prod, top_prod]
