from wordnik_config import *
from wordnik import *
import time
import codecs

def early_reject(word, existing=None):
    if existing and word in existing:
        return True
    if ' ' in word:
        return True

def random_words(num=20, existing=None, _words=None, min_l=3, min_cc=5000):
    if existing:
        num = num * 2
    results = words_api.getRandomWords(
        limit=num,
        minLength=min_l,
        minCorpusCount=min_cc,
        excludePartOfSpeech='proper-noun')
    words = set()
    if _words:
        words = _words
    for result in results:
        word = result.word
        if early_reject(word, existing):
            continue
        words.add(word)
        if len(words) >= num:
            break
    if len(words) < num:
        return random_words(10, existing, words)
    else:
        return words

def reject(word_defs, max_defs, min_dicts):
    dicts = set()
    if len(word_defs) > max_defs:
        return True
    for d in word_defs:
        if not d.text or not d.sourceDictionary or not d.partOfSpeech:
            continue
        dicts.add(d.sourceDictionary)
    return len(dicts) < min_dicts

def get_definitions(words, max_defs=25, min_dicts=5):
    definitions = []
    good_words = []
    for word in words:
        word_defs = word_api.getDefinitions(word, sourceDictionaries='all')
        if not reject(word_defs, max_defs, min_dicts):
            definitions += word_defs
            good_words.append(word)
        time.sleep(WORDNIK_API_STALL_TIME)
    return definitions, good_words


if __name__ == '__main__':
    import argparse
    import sys
    aparser = argparse.ArgumentParser(
        description="Sample words and definitions from Wordnik API")
    aparser.add_argument(
        '--numSamples', metavar='S', type=int, default=100,
        help='number of samples (only guaranteed to S be min)')
    aparser.add_argument(
        '--minLength', metavar='L', type=int, default=3,
        help='mininum word length (#chars)')
    aparser.add_argument(
        '--minCorpusCount', metavar='C', type=int, default=5000,
        help='mininum frequency of a word in corpus')
    aparser.add_argument(
        '--maxDefs', metavar='D', type=int, default=25,
        help='remove words that has more than MD definitions')
    aparser.add_argument(
        '--minDicts', metavar='S', type=int, default=5,
        help='remove words appear in less than S dictionaries (5 is total)')
    aparser.add_argument(
        '--outputFilePath', metavar='O', type=str,
        default='../output/wordnik_sampled_defs.tsv',
        help='output file path')
    opt = aparser.parse_args(sys.argv[1:])
    # create client
    client = swagger.ApiClient(WORDNIK_API_KEY, WORDNIK_API_URL)
    word_api = WordApi.WordApi(client)
    words_api = WordsApi.WordsApi(client)
    # random words
    existing = set()
    words = []
    definitions = []

    while len(words) < opt.numSamples:
        rand_words = random_words(
            existing=existing, min_l=opt.minLength, min_cc=opt.minCorpusCount)
        existing = existing.union(rand_words)
        word_defs, words_in_def = get_definitions(
            rand_words,
            max_defs=opt.maxDefs,
            min_dicts=opt.minDicts)
        words += words_in_def
        definitions += word_defs
        print('num sampled words: ' + len(words))

    f = codecs.open(opt.outputFilePath, 'w', 'utf-8')
    for word_def in definitions:
        if not word_def.text or not word_def.sourceDictionary or not word_def.partOfSpeech:
            continue
        f.write(word_def.word)
        f.write('\t')
        f.write(word_def.sourceDictionary)
        f.write('\t')
        f.write(word_def.partOfSpeech)
        f.write('\t')
        f.write(word_def.text)
        f.write('\n')
    f.close()
