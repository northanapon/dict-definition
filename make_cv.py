import os
import argparse
from functools import partial
from collections import defaultdict
from dictdef.dataset import cv_by_lemma


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_file(filepath, word_list, data):
    with open(filepath, mode='w')as ofp:
        for word in word_list:
            for line in data[word]:
                ofp.write(line)


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Split words in a TSV definition file into k-fold CV.")
    aparser.add_argument(
        'input_filepath', type=str, help='input file path')
    aparser.add_argument(
        'output_dir', type=str, help='output directory')
    aparser.add_argument('k', type=int, help="k fold")

    opt = aparser.parse_args()

    ensure_dir(opt.output_dir)
    dpath = partial(os.path.join, opt.output_dir)
    data = defaultdict(list)
    with open(opt.input_filepath) as lines:
        for line in lines:
            word = line.split('\t')[0]
            data[word].append(line)
    CVs = cv_by_lemma(list(data.keys()), k=opt.k)
    for i, (train, valid) in enumerate(CVs):
        ensure_dir(dpath(f'cv{i}'))
        write_to_file(dpath(f'cv{i}/train.txt'), train, data)
        write_to_file(dpath(f'cv{i}/valid.txt'), valid, data)
