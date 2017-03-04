import codecs
import StringIO
import os
import json
from copy import deepcopy
import re

def index_gcide(gcide_dir):
    index = {}
    for fn in os.listdir(gcide_dir):
        fp = os.path.join(gcide_dir, fn)
        if not os.path.isfile(fp):
            continue
        with codecs.open(fp, 'r', 'utf-8') as ifp:
            for line in ifp:
                entry = json.loads(line)
                key = entry[u'key'].lower()
                if key not in index:
                    index[key] = []
                index[key].append(entry)
    return index

def normalize_entries(entries):
    new_entries = []
    for entry in entries:
        for sense in entry[u'senses']:
            new_entry = {}
            new_entry['word'] = entry[u'key'].lower()
            new_entry['source'] = 'gcide'
            if u'pos' not in entry:
                new_entry['pos'] = ''
            else:
                new_entry['pos'] = entry[u'pos'][0]
            new_entry['def'] = sense[u'def']
            new_entries.append(new_entry)
    return new_entries

def split_and_clean_norm_entries(norm_entries, keep_one=False):
    new_norm_entries = []
    for e in norm_entries:
        defs = e['def'].split(';')
        defs = clean_defs(defs, e['word'])
        if len(defs) == 0:
            continue
        for d in defs:
            new_e = deepcopy(e)
            new_e['def'] = d
            new_norm_entries.append(new_e)
            if keep_one:
                break
    return new_norm_entries


def clean_defs(defs, word,
               bad_starts=['--', 'see', 'formerly', 'thus', 'for example'],
               replace_starts=['also', 'now commonly', 'hence', 'or',
                               'especially', ',', ':', '(', ')'],
               replace_dict={'esp.': 'especially',
                             'pl.': 'plural',
                             'specif.': 'specifically',
                             'e.g.': 'for example',
                             'e. g.': 'for example',
                             'illust.': 'illustration',
                             'cf.': 'confer',
                             'fig.:': '', "pl,"
                             'etc.': 'etc'}):
    regex = re.compile(r'\b'+word+r'\b')
    new_defs = []
    for d in defs:
        d = d.lower()
        for word in replace_dict:
            d = d.replace(word, replace_dict[word])
        parts = d.split('.')
        d = parts[0].strip()
        if any(map(d.startswith, bad_starts)):
            continue
        for phrase in replace_starts:
            if d.startswith(phrase):
                d = d.replace(phrase, '')
                d = d.strip()
        if len(d) == 0:
            continue
        if regex.search(d) is not None:
            continue
        new_defs.append(d)
    return new_defs

def _not_empty_def_filter(sense):
    definition = sense[u'def']
    return len(definition.strip()) > 0

def _not_plural_def_filter(sense):
    definition = sense[u'def']
    if definition.strip().lower().startswith('pl. of'):
        return False
    return _not_empty_def_filter(sense)

def filter_entries(entries, def_filter_fn=_not_plural_def_filter):
    ''' Remove entries with empty definition or POS '''
    new_entries = []
    for entry in entries:
        if u'pos' not in entry:
            continue
        if len(entry[u'pos'][0].strip()) == 0:
            continue
        if u'senses' not in entry:
            continue
        senses = []
        for sense in entry[u'senses']:
            if u'def' not in sense:
                continue
            if not def_filter_fn(sense):
                continue
            senses.append(sense)
        if len(senses) > 0 and len(senses) != len(entry[u'senses']):
            new_entry = deepcopy(entry)
            new_entry[u'senses'] = senses
            new_entries.append(new_entry)
        elif len(senses) > 0:
            new_entries.append(entry)
    return new_entries

def topk_senses(entries, k):
    ''' Select top k definition for each entries '''
    new_entries = []
    for entry in entries:
        new_entry = deepcopy(entry)
        senses = entry[u'senses']
        e = k
        if len(senses) < e:
            e = len(senses)
        new_entry[u'senses'] = senses[:e]
        new_entries.append(new_entry)
    return new_entries
