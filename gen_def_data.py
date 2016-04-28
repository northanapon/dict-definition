import codecs
import gcide.gcide_util as gcu
import wordnet.wordnet_util as wnu
from nltk.corpus import wordnet as wn

def filter_word(word, banned_words):
    if len(word) < 3 or word in banned_words:
        return False
    return True

def normalized_def2str(norm_def):
    a = [
        norm_def['word'],
        norm_def['pos'],
        norm_def['source'],
        norm_def['def'].lower()
    ]
    return u'\t'.join(a)

word_filepath = 'data/norvig_ngram/count_1w.txt'
stopword_filepath = 'data/wn_stop_words.txt'
funcword_filepath = 'data/function_words.txt'
gcide_dir = 'output/gcide-entries/'
output_filepath = 'output/top10kwords_2defs.tsv'

gcide_index = gcu.index_gcide(gcide_dir)
words = []
with codecs.open(word_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.append(line.split('\t')[0])

banned_words = set()
with open(stopword_filepath, 'r') as ifp:
    for line in ifp:
        banned_words.add(line.strip().lower())
with open(funcword_filepath, 'r') as ifp:
    for line in ifp:
        banned_words.add(line.strip().lower())

ofp = codecs.open(output_filepath, 'w', 'utf-8')
count = 0
for word in words:
    if not filter_word(word, banned_words):
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
        ofp.write(normalized_def2str(sense))
        ofp.write('\n')
    for sense in gc_senses:
        ofp.write(normalized_def2str(sense))
        ofp.write('\n')
    count = count + 1
    if count >= 10000:
        break
ofp.close()
