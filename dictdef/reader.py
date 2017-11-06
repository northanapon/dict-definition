import os
from functools import partial
from collections import namedtuple
from collections import defaultdict


def _chunklist(t, size=2):
        it = iter(t)
        return list(zip(*[it]*size))


def open_skip_split(path, skip=' ', sep=None):
    with open(path) as lines:
        for line in lines:
            if line.startswith(skip):
                continue
            yield line.split(sep)


def wordnet_db_reader(dir):
    """ Read  WordNet database directory downloaded from
    https://wordnet.princeton.edu/wordnet/download """
    WNIndexEntry = namedtuple(
        'WNIndexEntry', 'lemma pos pointers num_tagsenes synset_offsets')
    WNSenseEntry = namedtuple(
        'WNSenseEntry', 'offset lexname synset_type words pointers gloss')
    WNWord = namedtuple('WNWord', 'word lex_id')
    WNPointer = namedtuple('WNPointer', 'pointer offset source target')
    pos_names = ('noun', 'verb', 'adj', 'adv')
    synset_types = (None, 'n', 'v', 'a', 'r', 's')
    dpath = partial(os.path.join, dir)
    # read lexicographer
    lexnames = {}
    for parts in open_skip_split(dpath('lexnames'), skip=' ', sep='\t'):
        lexnames[parts[0]] = parts[1]
    idx_entries = defaultdict(list)
    sense_entries = {}
    # read index entries and sense entries
    for pos_name in pos_names:
        for parts in open_skip_split(dpath(f'index.{pos_name}'), skip=' ', sep=None):
            _ap = 4 + int(parts[3])
            entry = WNIndexEntry(
                parts[0], parts[1], parts[4:_ap], int(parts[_ap + 1]),
                tuple(f'{pos_name}-{offset}' for offset in parts[_ap + 2:]))
            idx_entries[entry.lemma].append(entry)
        for parts in open_skip_split(dpath(f'data.{pos_name}'), skip=' ', sep=None):
            _num_words = int(parts[3], 16)
            _num_pointers = int(parts[4 + _num_words * 2])
            _pp = 4 + _num_words * 2 + 1
            _gloss_p = parts.index('|') + 1
            words = tuple(
                WNWord(word, lex_id) for word, lex_id in _chunklist(parts[4:_pp - 1]))
            pointers = tuple(
                WNPointer(p, o, s, t) for p, o, s, t in _chunklist(
                    parts[_pp:_pp + _num_pointers * 4], 4))
            entry = WNSenseEntry(
                parts[0], lexnames[parts[1]], parts[2], words, pointers,
                ' '.join(parts[_gloss_p:]))
            sense_entries[f'{pos_name}-{parts[0]}'] = entry
    # read sense numbers
    sense_numbers = {}
    for parts in open_skip_split(dpath('index.sense'), skip=' ', sep=' '):
        lemma, key = parts[0].split('%')
        synset_type = synset_types[int(key[0])]
        offset = parts[1]
        sense_numbers[f'{lemma}-{synset_type}-{offset}'] = int(parts[2])
    get_fn = partial(
        get_wordnet_entries, idx_entries=idx_entries, sense_entries=sense_entries,
        sense_numbers=sense_numbers)
    return get_fn, idx_entries, sense_entries, sense_numbers


def get_wordnet_entries(word, idx_entries, sense_entries, sense_numbers):
    WNEntry = namedtuple(
        'WNEntry',
        'surface lemma lexname synset_type sense_number surfaces examples definition')
    indices = idx_entries[word]
    entries = []
    if indices:
        for idx in indices:
            for offset in idx.synset_offsets:
                sense = sense_entries[offset]
                sense_key = f'{idx.lemma}-{sense.synset_type}-{sense.offset}'
                surfaces = tuple(e.word for e in sense.words)
                if word in surfaces:
                    surface = word
                elif word.capitalize() in surfaces:
                    surface = word.capitalize()
                else:
                    surface = word
                parts = sense.gloss.split('; "')
                entry = WNEntry(
                    surface, idx.lemma, sense.lexname, sense.synset_type,
                    sense_numbers[sense_key], surfaces,
                    tuple(ex.strip(' "') for ex in parts[1:]), parts[0])
                entries.append(entry)
    return entries
