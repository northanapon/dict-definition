import codecs
from random import shuffle

input_filepath = '../data/norvig_ngram/count_1w.txt'
output_filepath = '../output/sample_100_words.txt'
n_group = 5
group_size = 1000
group_samplig_size = 20

words = []
with codecs.open(input_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        words.append(line.split('\t')[0])

with codecs.open(output_filepath, 'w', 'utf-8') as ofp:
    for g in range(n_group):
        group = words[g*group_size:(g+1)*group_size]
        shuffle(group)
        for i in range(group_samplig_size):
            ofp.write(group[i])
            ofp.write('\n')
