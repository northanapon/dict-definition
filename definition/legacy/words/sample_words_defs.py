import codecs
from random import shuffle
import json
import os
from nltk.corpus import wordnet as wn

input_filepath = '../data/norvig_ngram/count_1w.txt'
gcide_dir = '../output/gcide-entries/'
output_filepath = '../output/sample_100_words_defs.txt'
n_group = 10
group_size = 1000
group_samplig_size = 10

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

def write_defs(word, gcide, ofp):
    gcide_defs = None
    if word in gcide:
        gcide_defs = gcide[word]
    wn_defs = wn.synsets(word)
    if (gcide_defs is None or wn_defs is None
        or len(gcide_defs) == 0 or len(wn_defs) == 0):
        return False
    ngcide = write_gcide_defs(gcide_defs, ofp)
    nwn = write_wn_defs(wn_defs, word, ofp)
    return ngcide + nwn > 0

def write_gcide_defs(defs, ofp):
    total_write_out = 0
    for entry in defs:
        if u'pos' not in entry:
            continue
        count = 0
        for sense in entry[u'senses']:
            ofp.write(entry[u'key'].lower())
            ofp.write('\t')
            ofp.write('gcide\t')
            ofp.write(entry[u'pos'][0])
            ofp.write('\t')
            ofp.write(sense[u'def'])
            ofp.write('\n')
            count = count + 1
            total_write_out = total_write_out + 1
            if count > 1:
                break
    return total_write_out

def write_wn_defs(defs, word, ofp):
    total_write_out = 0
    for sense in defs:
        ofp.write(word)
        ofp.write('\t')
        ofp.write('wordnet\t')
        ofp.write(sense.pos())
        ofp.write('\t')
        ofp.write(sense.definition())
        ofp.write('\n')
        total_write_out = total_write_out + 1
        if total_write_out > 1:
            break
    return total_write_out

words = []
with codecs.open(input_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.append(line.split('\t')[0])
gcide = index_gcide(gcide_dir)

with codecs.open(output_filepath, 'w', 'utf-8') as ofp:
    for g in range(n_group):
        group = words[g*group_size:(g+1)*group_size]
        shuffle(group)
        count = 0
        i = 0
        while count < group_samplig_size:
            if write_defs(group[i], gcide, ofp):
                count = count + 1
            i = i + 1
