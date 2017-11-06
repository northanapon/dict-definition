import os
import argparse

from dictdef import dataset

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Run CoreNLP tokenizer on a TSV definition file")
    aparser.add_argument(
        'input_filepath', type=str, help='input file path')
    aparser.add_argument(
        'target_words', type=str, help='file path to a list of target words')
    aparser.add_argument(
        'output_filepath', type=str, help='output file path')
    aparser.add_argument(
        '--ban_words', type=str, default=None,
        help='file path to a list of banned words')

    opt = aparser.parse_args()

    ban_words = set()
    if opt.ban_words is not None:
        with open(opt.ban_words) as lines:
            for line in lines:
                word = line.split('\t')[0].strip()
                ban_words.add(word)
                ban_words.add(word.lower())
    target_words = set()
    with open(opt.target_words) as lines:
        for line in lines:
            word = line.split('\t')[0].strip()
            target_words.add(word)
    with open(opt.input_filepath) as lines, open(opt.output_filepath, 'w') as ofp:
        for line in lines:
            word = line.split('\t')[0].strip()
            if word in ban_words or word not in target_words:
                continue
            ofp.write(line)
