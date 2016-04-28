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

def reorder_groups(groups, word):
    ''' Put senses that have a name similar to word before other senses'''
    for pos in groups:
        match_group = []
        mismatch_group = []
        group = groups[pos]
        for sense in group:
            name_word = sense.name().split('.')[0]
            if name_word == word.lower():
                match_group.append(sense)
            else:
                mismatch_group.append(sense)
        groups[pos] = match_group + mismatch_group

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

def _not_empty_def_filter(definition):
    return len(definition.strip()) > 0

def filter_groups(groups, def_filter_fn=_not_empty_def_filter):
    ''' Remove senses '''
    new_groups = {}
    for pos in groups:
        group = groups[pos]
        new_group = []
        for sense in group:
            if not def_filter_fn(sense.definition()):
                continue
            new_group.append(sense)
        if len(new_group) > 0:
            new_groups[pos] = new_group
    return new_groups
