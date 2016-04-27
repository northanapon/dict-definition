import codecs
from random import shuffle
import argparse

import argparse
import sys
aparser = argparse.ArgumentParser(
    description="Sample words unigram count file")
aparser.add_argument(
    '--inputFilePath', metavar='i', type=str,
    default='../data/norvig_ngram/count_1w.txt',
    help='input file path (see ../data/README.md)')
aparser.add_argument(
    '--numGroups', metavar='G', type=int, default=5,
    help='number of groups to split data into')
aparser.add_argument(
    '--groupSize', metavar='S', type=int, default=1000,
    help='number of words for each group')
aparser.add_argument(
    '--groupSamples', metavar='D', type=int, default=20,
    help='number of samples (words) for each group')
aparser.add_argument(
    '--outputFilePath', metavar='O', type=str,
    default='../output/sample_words.txt',
    help='output file path')
opt = aparser.parse_args(sys.argv[1:])

input_filepath = opt.inputFilePath
output_filepath = opt.outputFilePath
n_group = opt.numGroups
group_size = opt.groupSize
group_samplig_size = opt.groupSamples

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
