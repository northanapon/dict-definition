import codecs
import pickle
import os
from progressbar import ProgressBar

data_dir = 'data/hillf_tacl_2016/train'
train_fp = 'Wordnik_Wiki_alldefs_train.pkl'
dict_fp = 'Wordnik_Wiki_dict_alldefs_train.pkl'
emb_fp = 'D_cbow_pdw_8B.pkl'
output_filepath = 'output/hillf_tacl_2016_defs.tsv'

print('Loading data...')
ifp = open(os.path.join(data_dir, train_fp))
targets = pickle.load(ifp)
definitions = pickle.load(ifp)
ifp.close()
ifp = open(os.path.join(data_dir, dict_fp))
w2i = pickle.load(ifp)
ifp.close()
i2w = {}
for k in w2i:
    i2w[w2i[k]] = k
ifp.close()
ifp = open(os.path.join(data_dir, emb_fp))
emb = pickle.load(ifp)
ifp.close()
print('Definitions: ' + str(len(definitions)))
print('Vocab size: ' + str(len(i2w)))
print('Emb size: ' + str(len(emb)) + ', ' + str(len(emb['a'])))

print('Processing data... (this will take very long time)')
ofp = codecs.open(output_filepath, 'w', 'utf-8')
prev_word = None
prev_temb = None
with ProgressBar(max_value=len(definitions)) as pb:
    for i in range(len(targets)):
        temb = targets[i]
        word = None
        if prev_temb is not None and (temb - prev_temb).sum() == 0:
            word = prev_word
        if word is None:
            for k in emb:
                if (emb[k] - temb).sum() == 0:
                    word = k
                    break
        if word is None:
            print('Line: ' + str(i) + ' missing')
            word = ''
        ofp.write(word)
        ofp.write('\tNA\tNA\t')
        tokens = []
        for idx in definitions[i]:
            tokens.append(i2w[idx])
        ofp.write(u' '.join(tokens))
        ofp.write('\n')
        prev_word = word
        prev_temb = temb
        pb.update(i)
ofp.close()
