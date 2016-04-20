from wordnik_config import *
from wordnik import *
import time
import codecs

def early_reject(word, existing=None):
    if existing and word in existing:
        return True
    if ' ' in word:
        return True

def random_words(num=20, existing=None, _words=None):
    if existing:
        num = num * 2
    results = words_api.getRandomWords(
        limit=num,
        minLength=3,
        minCorpusCount=5000,
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

def reject(word_defs):
    dicts = set()
    if len(word_defs) > 25:
        return True
    for d in word_defs:
        if not d.text or not d.sourceDictionary or not d.partOfSpeech:
            continue
        dicts.add(d.sourceDictionary)
    return len(dicts) < 5

def get_definitions(words):
    definitions = []
    good_words = []
    for word in words:
        word_defs = word_api.getDefinitions(word, sourceDictionaries='all')
        if not reject(word_defs):
            definitions += word_defs
            good_words.append(word)
        time.sleep(WORDNIK_API_STALL_TIME)
    return definitions, good_words


# create client
client = swagger.ApiClient(WORDNIK_API_KEY, WORDNIK_API_URL)
word_api = WordApi.WordApi(client)
words_api = WordsApi.WordsApi(client)
# random words
existing = set()
words = []
definitions = []

while len(words) < 100:
    rand_words = random_words(existing=existing)
    existing = existing.union(rand_words)
    word_defs, words_in_def = get_definitions(rand_words)
    words += words_in_def
    definitions += word_defs
    print(len(words))

f = codecs.open('../data/sample_definitions.tsv', 'w', 'utf-8')
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
