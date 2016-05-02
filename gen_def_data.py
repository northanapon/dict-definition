import codecs
import gcide.gcide_util as gcu
import wordnet.wordnet_util as wnu
from nltk.corpus import wordnet as wn

def filter_word(word, banned_words, w2v_vocab):
    if (len(word) < 3
        or word in banned_words
        or word not in w2v_vocab):
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
gsl_word_filepath = 'data/gsl_words.txt'
stopword_filepath = 'data/wn_stop_words.txt'
funcword_filepath = 'data/function_words.txt'
w2vvocab_filepath = 'data/w2v_vocab.txt'
gcide_dir = 'output/gcide-entries/'
output_filepath = 'output/common_words_defs.tsv'

gcide_index = gcu.index_gcide(gcide_dir)
words = set()
banned_words = set()
w2v_vocab = set()

with codecs.open(word_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.add(line.split('\t')[0])
with codecs.open(gsl_word_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.add(line.split('\t')[0].lower())


with open(stopword_filepath, 'r') as ifp:
    for line in ifp:
        banned_words.add(line.strip().lower())
with open(funcword_filepath, 'r') as ifp:
    for line in ifp:
        banned_words.add(line.strip().lower())
with codecs.open(w2vvocab_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        parts = line.strip().split('\t')
        # XXX: There are empty words. Is it a bug?
        if len(parts) <= 1:
            continue
        word = parts[1]
        if '_' in word:
            continue
        w2v_vocab.add(word)

ofp = codecs.open(output_filepath, 'w', 'utf-8')
count = 0
num_words = 0
print('total words: ' + str(len(words)))
for word in words:
    num_words = num_words + 1
    if not filter_word(word, banned_words, w2v_vocab):
        continue
    wn_senses = wn.synsets(word)
    wn_senses = wnu.remove_person_name(wn_senses)
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
    wn_senses = wnu.split_and_clean_norm_entries(wn_senses)
    gc_senses = gcu.filter_entries(gc_senses)
    gc_senses = gcu.topk_senses(gc_senses, 2)
    gc_senses = gcu.normalize_entries(gc_senses)
    gc_senses = gcu.split_and_clean_norm_entries(gc_senses)
    if len(wn_senses) == 0 or len(gc_senses) == 0:
        continue
    for sense in wn_senses:
        ofp.write(normalized_def2str(sense))
        ofp.write('\n')
    for sense in gc_senses:
        ofp.write(normalized_def2str(sense))
        ofp.write('\n')
    count = count + 1
    if count % 1000 == 0:
        print(str(count) + '/' + str(num_words))
    if count >= 50000:
        break
ofp.close()
