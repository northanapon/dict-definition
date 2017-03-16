#!/bin/bash

echo "Preprocessing..."
mkdir -p nltk_wordnet/preprocess
DATA_DIR="data/nltk_wordnet"
cd ..
python -m definition.proprocess.preprocess_rawdata "data/wordlist/common_words.v3.txt" "$DATA_DIR/preprocess/all.tsv" nltk_wordnet
python -m definition.proprocess.preprocess_rawdata "data/wordlist/common_words.v3.txt" "$DATA_DIR/preprocess/first_sense.tsv" nltk_wordnet --only_first_sense
