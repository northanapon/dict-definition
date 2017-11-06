import re
import random
from collections import defaultdict

from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import StanfordTokenizer


def lemmatize_all(
        w, wnl=WordNetLemmatizer(), pos_to_try=(wn.NOUN, wn.VERB, wn.ADJ, wn.ADV)):
    return tuple((wnl.lemmatize(w, pos=pos), pos) for pos in pos_to_try)


def lemmatize(
        w, wnl=WordNetLemmatizer(), pos='n', try_all_pos_tags=False,
        pos_to_try=(wn.NOUN, wn.VERB, wn.ADJ, wn.ADV)):
    if try_all_pos_tags:
        for pos in pos_to_try:
            lemma = wnl.lemmatize(w, pos=pos)
            if w != lemma:
                return lemma
        return lemma
    else:
        return wnl.lemmatize(w, pos=pos)


def remove_words_with_regex(word_list, regex=r"[^a-zA-Z]+"):
    new_words = []
    p = re.compile(regex)
    for word in word_list:
        if p.search(word) is not None:
            continue
        new_words.append(word)
    return new_words


def remove_banned_words(word_list, banned_words, lower=False):
    if lower:
        bwset = set()
        for word in banned_words:
            bwset.add(word.lower())
    else:
        bwset = set(banned_words)
    words = []
    for w in word_list:
        if lower:
            w = w.lower()
        if w not in bwset:
            words.append(w)
    return words


def split_by_lemma(word_list, train_frac=0.95):
    _frac = 1.0 - train_frac
    val_frac = test_frac = _frac / 2
    lemma_words = defaultdict(list)
    for w in word_list:
        lemma = lemmatize(w, try_all_pos_tags=False)
        lemma_words[lemma].append(w)
    lemmas = lemma_words.keys()
    n_valid = int(len(lemmas) * val_frac)
    n_test = int(len(lemmas) * test_frac)
    shuffled = list(lemmas)
    random.shuffle(shuffled)
    valid_lemmas = shuffled[0:n_valid]
    test_lemmas = shuffled[n_valid:n_valid+n_test]
    train_lemmas = shuffled[n_valid+n_test:]

    def map_lemmas_to_words(lemmas):
        words = []
        for lemma in lemmas:
            words.extend(lemma_words[lemma])
        return words

    train_words = map_lemmas_to_words(train_lemmas)
    valid_words = map_lemmas_to_words(valid_lemmas)
    test_words = map_lemmas_to_words(test_lemmas)
    return (train_words, valid_words, test_words)


def clean_definition(
        word, definition,
        _delimiter=re.compile(r'[;:]'), _removed=re.compile(r'\([^\)]+\)')):
    _d = definition
    # take only first definition `:` or `;`
    m = _delimiter.search(definition)
    if m is not None:
        definition = definition[0:m.start()]
    # remove domain specifiers or comments
    while True:
        m = _removed.match(definition)
        if m is not None:
            definition = '{} {}'.format(definition[0:m.start()].strip(),
                                        definition[m.end():].strip())
        else:
            break
    tokens = definition.strip().split()
    if len(tokens) == 0:
        return ""
    # e.g. at the end
    if tokens[-1] == "e.g.":
        tokens = tokens[:-1]
    # remove self reference
    word_lemmas = set((p[0] for p in lemmatize_all(word)))
    tokens_lemmas = set()
    for token in tokens:
        tokens_lemmas = tokens_lemmas.union(
            set([p[0] for p in lemmatize_all(token)]))
    if len(word_lemmas.intersection(tokens_lemmas)) > 0:
        return ""
    definition = ' '.join(tokens)
    return definition


def corenlp_tokenize(text_list, path_to_jar):
    tokenizer = StanfordTokenizer(
        path_to_jar=path_to_jar, options={
            'ptb3Escaping': 'false', 'tokenizePerLine': 'true',
            'tokenizeNLs': 'true', 'americanize': 'true'})
    text = '\n'.join(text_list)
    tokens = tokenizer.tokenize(text)
    text = ' '.join(tokens)
    text_list = text.split('*NL*')
    return text_list
