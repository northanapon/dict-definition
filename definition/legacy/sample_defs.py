import codecs
from random import shuffle

input_filepath = 'output/common_words_defs.tsv'
gcide_out_path = 'output/sample_gcide_defs.tsv'
wn_out_path = 'output/sample_wn_defs.tsv'
num_samples = 100
d_index = {}

with codecs.open(input_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        line = line.strip()
        parts = line.split('\t')
        if parts[0] not in d_index:
            d_index[parts[0]] = []
        d_index[parts[0]].append(parts)

word_list = list(d_index.keys())
shuffle(word_list)
gofp = codecs.open(gcide_out_path, 'w', 'utf-8')
wofp = codecs.open(wn_out_path, 'w', 'utf-8')

for i in range(num_samples):
    word = word_list[i]
    for d in d_index[word]:
        ofp = None
        if d[2] == 'gcide':
            ofp = gofp
        if d[2] == 'wordnet':
            ofp = wofp
        ofp.write(u'\t'.join(d))
        ofp.write('\n')

gofp.close()
wofp.close()
