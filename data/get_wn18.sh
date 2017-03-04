#!/bin/bash

echo "[1/3] Downloading data..."
wget http://websail-fe.cs.northwestern.edu/downloads/dictdef/kge.tar.gz
echo "[2/3] Extracting files..."
tar -xf kge.tar.gz
rm kge.tar.gz
mkdir -p wn18/preprocess
mv KGE/WN18/definitions.txt wn18/
DATA_DIR="data/wn18/"
rm -r KGE
echo "[3/3] Preprocessing..."
cd ..
python -m definition.proprocess.preprocess_rawdata "$DATA_DIR/definitions.txt" "$DATA_DIR/preprocess/all.tsv" wn18
python -m definition.proprocess.preprocess_rawdata "$DATA_DIR/definitions.txt" "$DATA_DIR/preprocess/first_sense.tsv" wn18 --only_first_sense
