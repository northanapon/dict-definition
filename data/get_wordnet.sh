#!/bin/bash

echo "Preprocessing..."
mkdir -p wordnet/preprocess
DATA_DIR="data/wordnet"
cd ..
python -m definition.proprocess.preprocess_rawdata "data/wordlist/common_words.v3.txt" "$DATA_DIR/preprocess/all.tsv" wordnet
