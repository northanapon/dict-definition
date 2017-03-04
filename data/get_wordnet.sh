#!/bin/bash

echo "Preprocessing..."
mkdir -p common_wordnet/preprocess
DATA_DIR="data/common_wordnet"
cd ..
python -m definition.proprocess.preprocess_rawdata "data/wordlist/common_words.v2.txt" "$DATA_DIR/preprocess/all.tsv" wordnet
python -m definition.proprocess.preprocess_rawdata "data/wordlist/common_words.v2.txt" "$DATA_DIR/preprocess/first_sense.tsv" wordnet --only_first_sense
