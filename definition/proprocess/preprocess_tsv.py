import os
from random import shuffle
import re
import argparse
import codecs
from nltk import word_tokenize
from neobunch import Bunch
from definition.words import word_sampler

_delimiter = re.compile(r'[;:]')
_removed = re.compile(r'\(.+\)')

def read_tsv(ifp):
    entries = {}
    for line in ifp:
        parts = line.strip().split('\t')
        word = parts[0]
        definition = clean_definition(parts[-1])
        if len(definition) == 0:
            continue
        others = '\t'.join(parts[1:-1])
        if word not in entries:
            entries[word] = []
        entries[word].append([definition, others])
    return entries

def split_words(words, valid=.1, test=.1):
    n_valid = int(len(words) * valid)
    n_test = int(len(words) * test)
    shuffled = list(words)
    shuffle(shuffled)
    valid_words = shuffled[0:n_valid]
    test_words = shuffled[n_valid:n_valid+n_test]
    train_words = shuffled[n_valid+n_test:]
    return (train_words, valid_words, test_words)

def clean_definition(definition):
    # take only first definition (: or ;)
    m = _delimiter.search(definition)
    if m is not None:
        definition = definition[0:m.start()]
    # remove domain specifiers or comments
    while True:
        m = _removed.search(definition)
        if m is not None:
            definition = '{} {}'.format(definition[0:m.start()].strip(),
                                        definition[m.end():].strip())
        else:
            break
    return definition.strip()

def replace_unk(entries, vocab):
    new_entries = {}
    for word in entries:
        if word not in vocab:
            continue
        definitions = []
        for definition, others in entries[word]:
            tokens = word_tokenize(definition)
            c = 0
            for i in range(len(tokens)):
                if tokens[i] not in vocab:
                    tokens[i] = "<unk>"
                    c += 1
            if c == len(tokens):
                continue
            definitions.append((u' '.join(tokens), others))
        if len(definitions) == 0:
            continue
        new_entries[word] = definitions
    return new_entries


def main(opt):
    with codecs.open(opt.input_filepath, mode='r', encoding='utf-8') as ifp:
        entries = read_tsv(ifp)
        words = entries.keys()
        if opt.remove_non_char_words:
            words = word_sampler.remove_words_with_chars(words)
        if opt.remove_function_words:
            function_words = word_sampler.load_wordset_from_files(
                [opt.function_words_path], lower=True)
            words = word_sampler.remove_banned_words(words, function_words,
                                                     lower=True)
        if opt.universe_vocab_path is not None:
            vocab = word_sampler.load_wordset_from_files(
                [opt.universe_vocab_path], lower=False)
            entries = replace_unk(entries, vocab)
            words = entries.keys()
        split_names = ['train.txt', 'valid.txt', 'test.txt']
        word_splits = split_words(words)
        for i, split in enumerate(word_splits):
            output_filepath = os.path.join(
                opt.output_dir,
                '{}_{}'.format(opt.output_prefix, split_names[i]))
            with codecs.open(output_filepath, 'w', encoding='utf-8') as ofp:
                for word in split:
                    for definitions in entries[word]:
                        ofp.write('{}\t{}\t{}\n'.format(
                            word, definitions[1], definitions[0]))

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Preprocess TSV data")
    aparser.add_argument(
        'input_filepath', type=str,
        help='input file path (see ../data/README.md)')
    aparser.add_argument(
        'output_dir', type=str,
        help='output directory')
    aparser.add_argument(
        '--output_prefix', type=str, default='',
        help='output filename prefix')
    aparser.add_argument(
        '--remove_function_words', dest='remove_function_words',
        action='store_true')
    aparser.add_argument(
        '--remove_non_char_words', dest='remove_non_char_words',
        action='store_true')
    aparser.add_argument(
        '--universe_vocab_path', default=None, type=str)
    aparser.add_argument(
        '--function_words_path', type=str,
        default="data/wordlist/function_words.txt")
    opt = aparser.parse_args()
    main(opt)
