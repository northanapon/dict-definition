import codecs
import gcide.gcide_util as gcu
import wordnet.wordnet_util as wnu
from nltk.corpus import wordnet as wn

def filter_word(word):
    if len(word) < 3:
        return False
    return True

def normalized_def2str(norm_def):
    return '\t'.join(norm_def.values())

word_filepath = 'data/norvig_ngram/count_1w.txt'
gcide_dir = 'output/gcide-entries/'

gcide_index = gcu.index_gcide(gcide_dir)
words = []
with codecs.open(word_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.append(line.split('\t')[0])

count = 0
for word in words:
    if not filter_word(word):
        continue
    wn_senses = wn.synsets(word)
    gc_senses = None
    if word in gcide_index:
        gc_senses = gcide_index[word]
    if gc_senses is None or len(wn_senses) == 0:
        continue
    wn_senses = wnu.group_senses_by_pos(wn_senses)
    wnu.reorder_groups(wn_senses, word)
    wn_senses = wnu.filter_groups(wn_senses)
    wn_senses = wnu.topk_groups(wn_senses, 2)
    wn_senses = wnu.normalize_groups(wn_senses, word)
    gc_senses = gcu.filter_entries(gc_senses)
    gc_senses = gcu.topk_senses(gc_senses, 2)
    gc_senses = gcu.normalize_entries(gc_senses)
    if len(wn_senses) == 0 or len(gc_senses) == 0:
        continue
    for sense in wn_senses:
        print(normalized_def2str(sense))
    for sense in gc_senses:
        print(normalized_def2str(sense))
    count = count + 1
    if count > 100:
        break
