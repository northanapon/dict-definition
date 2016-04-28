import codecs
from nltk.tokenize import wordpunct_tokenize as tokenize

data_filepath = 'output/top10kwords_2defs.tsv'

def num_words_with_freq(freq, n):
    c = 0
    for w in freq:
        if freq[w] == n:
            c = c + 1
    return c

defined_words = set()
freq = {}
total_tokens = 0
total_defs = 0
with codecs.open(data_filepath, 'r', 'utf-8') as ifp:
    for line in ifp:
        total_defs = total_defs + 1
        line = line.strip()
        parts = line.split('\t')
        if parts[0] not in freq:
            freq[parts[0]] = 0
        freq[parts[0]] = freq[parts[0]] + 1
        defined_words.add(parts[0])
        for t in tokenize(parts[3]):
            if t not in freq:
                freq[t] = 0
            freq[t] = freq[t] + 1
            total_tokens = total_tokens + 1

print('#word being defined: ' + str(len(defined_words)))
print('#definition: ' + str(total_defs))
print('#tokens: ' + str(total_tokens))
print('vocab size: ' + str(len(freq)))
print('rare word frequency: ')
print(' - 1: ' + str(num_words_with_freq(freq, 1)))
print(' - 2: ' + str(num_words_with_freq(freq, 2)))
print(' - 3: ' + str(num_words_with_freq(freq, 3)))
print(' - 4: ' + str(num_words_with_freq(freq, 4)))
print(' - 5: ' + str(num_words_with_freq(freq, 5)))
