from nltk.corpus import wordnet as wn

def group_senses_by_pos(senses):
    ''' Group senses by Part of speech '''
    group = {}
    for sense in senses:
        pos = sense.pos()
        if pos not in group:
            group[pos] = []
        group[pos].append(sense)
    return group

def normalize_groups(groups, word):
    ''' Extract word, POS, and definition from groups of senses '''
    entries = []
    for pos in groups:
        for sense in g[pos]:
            entry = {}
            entry['word'] = word.lower()
            entry['source'] = 'wordnet'
            entry['pos'] = sense.pos()
            entry['def'] = sense.definition()
            entries.append(entry)
    return entries

def topk_groups(groups, k):
    ''' Select only top k of each group '''
    new_groups = {}
    for pos in groups:
        group = groups[pos]
        e = k
        if len(group) < e:
            e = len(group)
        new_groups[pos] = group[:e]
    return new_groups
