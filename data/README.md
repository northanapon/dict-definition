# Obtaining data

## GCIDE Entries

1. Download the pre-processed file found [here](http://rali.iro.umontreal.ca/GCIDE/)
2. Unzip the file
3. Copy and paste `new-entries` in `gcide` under this directory

## Common Unigram List

From Peter Norvig's [Ngrams](http://norvig.com/ngrams/)

1. Download [unigram count](http://norvig.com/ngrams/count_1w.txt)
2. Place it in `norvig_ngram` under this directory

## HillF_TACL2016

1. Download [training data](http://www.cl.cam.ac.uk/~fh295/defgen_data.tgz)
2. Unzip the file
3. Rename the directory to `train`
4. Place it in `hillf_tacl_2016` under this directory
5. Do the same with [evaluation data](http://www.cl.cam.ac.uk/~fh295/Defgen_evals.tgz) and the directory name is `eval`

# Function words and Stop words
- [function_words.txt](https://github.com/NorThanapon/dict-definition/blob/master/data/function_words.txt) is compiled from [function word lists](http://www.sequencepublishing.com/academic.html) by Leah Gilner and Franc Morales
- [wn_stop_words.txt](https://github.com/NorThanapon/dict-definition/blob/master/data/wn_stop_words.txt) is adapted from Ted Pedersen's [WordNet Stop List](http://www.d.umn.edu/~tpederse/Group01/WordNet/wordnet-stoplist.html)

# Word2Vec Vocabulary
[w2v_vocab.txt.bz2](https://github.com/NorThanapon/dict-definition/blob/master/data/w2v_vocab.txt.bz2) is a mapping (index -> word) of the pre-trained word and phrase vectors available [here](https://code.google.com/archive/p/word2vec/). The file was generated using [gensim](https://github.com/piskvorky/gensim/).

You will need to unzip the file using [bzip2's tools](http://www.bzip.org/).

```bash
  bunzip2 -k w2v_vocab.txt.bz2
```
