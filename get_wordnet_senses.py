import os
import argparse

from dictdef import reader


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(wndb_path, output_path):
    get, i, _s, _n = reader.wordnet_db_reader(wndb_path)
    # lemma_list = tuple(i.keys())
    with open(output_path, 'w') as ofp:
        for lemma in i.keys():
            entries = get(lemma)
            for entry in entries:
                str_entry = '\t'.join((str(item) for item in entry[:-1]))
                ofp.write(f'{str_entry}\t{entry.definition}\n')


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Preprocess data from WordNet database")
    aparser.add_argument('wndb_path', type=str, help='WordNet database path')
    aparser.add_argument('output_path', type=str, help='output path')

    opt = aparser.parse_args()
    ensure_dir(os.path.dirname(opt.output_path))
    main(opt.wndb_path, opt.output_path)
