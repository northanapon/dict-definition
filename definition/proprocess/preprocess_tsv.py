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
        definition = clean_definition(word, parts[-1])
        if len(definition) == 0:
            continue
        others = '\t'.join(parts[1:-1])
        if word not in entries:
            entries[word] = []
        entries[word].append([definition, others])
    return entries


def map_lemmas_to_words(lemmas, lemma_words):
    words = []
    for lemma in lemmas:
        words.extend(lemma_words[lemma])
    return words


def split_words(words, valid=.1, test=.1):
    lemma_words = {}
    for w in words:
        lemma = word_sampler.lemmatize(w, try_all_pos_tags=False)
        if lemma not in lemma_words:
            lemma_words[lemma] = []
        lemma_words[lemma].append(w)
    lemmas = lemma_words.keys()
    n_valid = int(len(lemmas) * valid)
    n_test = int(len(lemmas) * test)
    shuffled = list(lemmas)
    shuffle(shuffled)
    valid_lemmas = shuffled[0:n_valid]
    test_lemmas = shuffled[n_valid:n_valid+n_test]
    train_lemmas = shuffled[n_valid+n_test:]
    train_words = map_lemmas_to_words(train_lemmas, lemma_words)
    valid_words = map_lemmas_to_words(valid_lemmas, lemma_words)
    test_words = map_lemmas_to_words(test_lemmas, lemma_words)
    return (train_words, valid_words, test_words)


def clean_definition(word, definition):
    # take only first definition `:` or `;`
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
    tokens = word_tokenize(definition)
    word_lemmas = set([p[0] for p in word_sampler.lemmatize_all(word)])
    tokens_lemmas = set()
    for token in tokens:
        tokens_lemmas = tokens_lemmas.union(
            set([p[0] for p in word_sampler.lemmatize_all(token)]))
    if len(word_lemmas.intersection(tokens_lemmas)) > 0:
        return ""
    definition = definition.strip()
    return definition


def replace_unk(entries, vocab, remove_unk, replace_unk):
    new_entries = {}
    for word in entries:
        if word not in vocab:
            continue
        definitions = []
        for definition, others in entries[word]:
            tokens = definition.split()
            c = 0
            for i in range(len(tokens)):
                if tokens[i] not in vocab:
                    if replace_unk:
                        tokens[i] = "<unk>"
                    c += 1
            if c == len(tokens):
                continue
            if remove_unk and c > 0:
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
            entries = replace_unk(
                entries, vocab, opt.remove_unk_defs, opt.replace_unk_words)
            words = entries.keys()
        split_names = ['train.txt', 'valid.txt', 'test.txt']
        word_splits = split_words(words)
        for i, split in enumerate(word_splits):
            output_filepath = os.path.join(
                opt.output_dir,
                '{}'.format(split_names[i]))
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
        '--remove_function_words', dest='remove_function_words',
        action='store_true')
    aparser.add_argument(
        '--remove_non_char_words', dest='remove_non_char_words',
        action='store_true')
    aparser.add_argument(
        '--replace_unk_words', dest='replace_unk_words',
        action='store_true')
    aparser.add_argument(
        '--remove_unk_defs', dest='remove_unk_defs',
        action='store_true')
    aparser.add_argument(
        '--remove_self_ref', dest='remove_self_ref',
        action='store_true')
    aparser.add_argument(
        '--universe_vocab_path', default=None, type=str)
    aparser.add_argument(
        '--function_words_path', type=str,
        default="data/wordlist/function_words.txt")
    opt = aparser.parse_args()
    main(opt)
