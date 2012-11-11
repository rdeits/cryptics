
def pull_from_file(file_name):
    abbreviation_dictionary = {}
    with open(file_name, "r") as reader:
        for line in reader.readlines():
            tokens = line.upper().replace(","," ").split()
            syn = False
            definition = []
            abbs = []
            for token in tokens:
                if not syn:
                    if token == "=":
                        syn = True
                    else:
                        definition.append(token)
                else:
                    if token[0] == "(" or token[-1] == ")":
                        pass
                    else:
                        abbs.append(token)
            if len(definition) == 1:
                defi = definition[0]
            elif len(definition) == 0:
                print 'We have a problem', tokens, line
            else:
                defi = definition[0]
                for j in definition[1:]:
                    defi += "_" + j

            if not defi in abbreviation_dictionary.keys():
                if len(abbs) == 0:
                    print 'We have a problem'
                    print line
                else:
                    abbreviation_dictionary[defi] = [abbs[0]]
            for abb in abbs:
                if not abb in abbreviation_dictionary[defi]:
                    if not abb == defi[0]:
                        abbreviation_dictionary[defi] = abbreviation_dictionary[defi] + [abb]
    return abbreviation_dictionary

abbr_dict = pull_from_file('abbr_text_list.txt')

def write_to_json(file_name, abbreviations):
    with open(file_name, "w") as writer:
        writer.write('{\n')
        for key in abbreviations.keys():
            writer.write('"'+key+'"'+':[\n')
            last = abbreviations[key][-1]
            for val in abbreviations[key]:
                if not val == last:
                    writer.write('"'+val+'",\n')
                else:
                    writer.write('"'+val+'"\n')
            writer.write('],\n')


        writer.write('}')

write_to_json('abbreviations.json', abbr_dict)
