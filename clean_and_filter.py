import re
import os
import argparse

from dictdef import dataset


def contain_non_alpha_char(word, regex=re.compile(r'[^a-zA-Z_]+')):
    if regex.search(word) is not None:
        return True
    return False


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
    aparser.add_argument(
        '--remove_non_char', action='store_true',
        help='remove words containing non-English characters')
    aparser.add_argument(
        '--only_first_def', action='store_true',
        help='take only first part of the definition (split by ; or :)')
    aparser.add_argument(
        '--remove_paren_phrase', action='store_true',
        help='remove phrases in parenthesis from definitions')
    aparser.add_argument(
        '--remove_self_ref', action='store_true',
        help='remove direct self reference')
    aparser.add_argument(
        '--remove_lemma_ref', action='store_true',
        help='remove lemma self reference')

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
            parts = line.split('\t')
            word = parts[0].strip()
            definition = parts[-1].strip()
            if word in ban_words or word not in target_words:
                continue
            if opt.remove_non_char and contain_non_alpha_char(word):
                continue
            definition = dataset.clean_definition(
                word, definition, opt.only_first_def, opt.remove_paren_phrase,
                opt.remove_self_ref, opt.remove_lemma_ref)
            if len(definition) == 0:
                continue
            ofp.write('\t'.join(parts[:-1]))
            ofp.write(f'\t{definition}\n')
