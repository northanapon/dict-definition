from nltk.corpus import wordnet as wn
import re
from copy import deepcopy

def is_person(sense):
    return (sense.lexname() == 'noun.person' and
            all(map(lambda x: x[0].isupper(),
                    sense.lemma_names())))

def remove_person_name(senses):
    new_senses = []
    for sense in senses:
        if is_person(sense):
            continue
        new_senses.append(sense)
    return new_senses

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
        for sense in groups[pos]:
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

def split_and_clean_norm_entries(norm_entries, keep_one=False):
    new_norm_entries = []
    for e in norm_entries:
        defs = e['def'].split(';')
        defs = clean_defs(defs, e['word'])
        if len(defs) == 0:
            continue
        for d in defs:
            new_e = deepcopy(e)
            if new_e['pos'] == 'v':
                d = u'to ' + d
            new_e['def'] = d
            new_norm_entries.append(new_e)
            if keep_one:
                break
    return new_norm_entries

def clean_defs(defs, word):
    paren_regex = re.compile(r'^\(.+\)')
    regex = re.compile(r'\b'+word+r'\b')
    new_defs = []
    for d in defs:
        d = d.strip().lower()
        d = d.replace('_', ' ')
        d = re.sub(r'[\'"`\(\)]', '', d)
        m = paren_regex.match(d)
        if m is not None:
            d = d[m.end():]
        if len(d) == 0:
            continue
        if regex.search(d) is not None:
            continue
        new_defs.append(d)
    return new_defs
