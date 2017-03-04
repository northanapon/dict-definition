import pickle
import os
import codecs

data_dir = 'data/hillf_tacl_2016/train'
emb_fp = 'D_cbow_pdw_8B.pkl'
output_filepath = 'output/hillf_tacl_2016_embs.txt'

print('Loading data...')
ifp = open(os.path.join(data_dir, emb_fp))
emb = pickle.load(ifp)
ifp.close()
print('Emb size: ' + str(len(emb)) + ', ' + str(len(emb['a'])))
print('Processing data... (this will take a minute)')
ofp = codecs.open(output_filepath, 'w', 'utf-8')

for k in emb:
    ofp.write(unicode(k, 'utf-8'))
    ofp.write(' ')
    ofp.write(' '.join([str(x) for x in emb[k]]))
    ofp.write('\n')

ofp.close()
