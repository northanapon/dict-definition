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
