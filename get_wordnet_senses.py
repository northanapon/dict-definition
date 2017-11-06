import os
import argparse

from dictdef import reader
from dictdef import dataset


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(wndb_path, output_path, train_frac, skip_words=None, remove_non_char=False):
    get, i, _s, _n = reader.wordnet_db_reader(wndb_path)
    lemma_list = tuple(i.keys())
    if skip_words is not None:
        lemma_list = dataset.remove_banned_words(lemma_list, skip_words, lower=True)
    if remove_non_char:
        lemma_list = dataset.remove_words_with_regex(lemma_list)
    splits = dataset.split_by_lemma(lemma_list, train_frac=train_frac)
    for split, name in zip(splits, ('train', 'valid', 'test')):
        with open(os.path.join(output_path, f'{name}.txt'), 'w') as ofp:
            for lemma in split:
                entries = get(lemma)
                for entry in entries:
                    definition = dataset.clean_definition(
                        entry.surface, entry.definition)
                    str_entry = '\t'.join((str(item) for item in entry[:-1]))
                    ofp.write(f'{str_entry}\t{definition}\n')


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Preprocess data from WordNet database")
    aparser.add_argument('wndb_path', type=str, help='WordNet database path')
    aparser.add_argument('output_path', type=str, help='output path')
    aparser.add_argument(
        '--train_frac', type=float, default=0.95, help='fraction of lemmas in training')
    aparser.add_argument(
        '--skip_words', type=str, default=None,
        help='path to file listing words that will be ommited')
    aparser.add_argument(
        '--remove_non_char', action='store_true',
        help='remove words containing non-English characters')

    opt = aparser.parse_args()
    ensure_dir(opt.output_path)
    main(
        opt.wndb_path, opt.output_path, opt.train_frac, opt.skip_words,
        opt.remove_non_char)
