import re
import codecs
from numpy.random import choice
from nltk.stem import WordNetLemmatizer

def remove_words_with_chars(word_list, regex=r"[^a-zA-Z]+"):
    new_words = []
    p = re.compile(regex)
    for word in word_list:
        if p.search(word) is not None:
            continue
        new_words.append(word)
    return new_words

def remove_banned_words(word_list, banned_words, lower=False):
    bwset = set(banned_words)
    words = []
    for w in word_list:
        if lower:
            w = w.lower()
        if w not in bwset:
            words.append(w)
    return words

def intersect_words(a, bset, lower=False):
    new = []
    for w in a:
        if lower:
            w = w.lower()
        if w in bset:
            new.append(w)
    return new

def lemmatize(w, wnl=WordNetLemmatizer(), pos='n', try_all_pos_tags=False,
              pos_to_try=['n', 'v', 'a', 's', 'r']):
    if try_all_pos_tags:
        for pos in pos_to_try:
            lemma = wnl.lemmatize(w, pos=pos)
            if w != lemma:
                return lemma
        return lemma
    else:
        return wnl.lemmatize(w, pos=pos)

def sample_words(word_list, num_samples):
    idx = range(len(word_list))
    sampled_idx = choice(idx, size=num_samples, replace=False)
    return [word_list[i] for i in sample_idx]

def load_wordset_from_files(filepath_list, lower=False):
    wordset = set()
    for filepath in filepath_list:
        with codecs.open(filepath, mode='r', encoding='utf-8') as ifp:
            for line in ifp:
                w = line.strip()
                if lower:
                    w = w.lower()
                wordset.add(w)
    return wordset

if __name__ == '__main__':
    import os
    data_dir = 'data/wordlist'
    files = ['gsl_words.txt', 'oxford3k_us_news.txt',
             'ptb_vocab.txt', 'web1t_top_100k.txt']
    words = load_wordset_from_files([os.path.join(data_dir, f) for f in files],
                                    lower=True)
    new_words = set()
    for w in words:
        if len(w) > 1:
            new_words.add(w)
    words = new_words
    vocab = load_wordset_from_files(
        [os.path.join(data_dir, 'glove.42B.300d.vocab')], lower=True)
    words = intersect_words(words, vocab, lower=True)
    print('Number of words: {}'.format(len(words)))
    lemmas = set()
    output_path = os.path.join(data_dir, 'common_words.v3.txt')
    with codecs.open(output_path, 'w', 'utf-8') as ofp:
        for w in words:
            lemma = lemmatize(w, try_all_pos_tags=True)
            lemmas.add(lemma)
            ofp.write('{}\n'.format(w))
    print('Number of lemmas: {}'.format(len(lemmas)))
    output_path = os.path.join(data_dir, 'common_lemmas.v3.txt')
    with codecs.open(output_path, 'w', 'utf-8') as ofp:
        for lemma in lemmas:
            ofp.write('{}\n'.format(lemma))
