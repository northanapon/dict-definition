import argparse
from dictdef.dataset import corenlp_tokenize


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Run CoreNLP tokenizer on a TSV definition file")
    aparser.add_argument(
        'input_filepath', type=str, help='input file path')
    aparser.add_argument(
        'output_filepath', type=str, help='output file path')
    aparser.add_argument(
        'corenlp_postagger_path', type=str,
        help="path to stanford-postagger.jar or stanford-corenlp-<version>.jar")

    opt = aparser.parse_args()

    entries = []
    definitions = []
    with open(opt.input_filepath) as ifp:
        for line in ifp:
            parts = line.strip().split('\t')
            entries.append('\t'.join(parts[:-1]))
            definition = parts[-1].replace('-', ' - ')
            definitions.append(definition)
    definitions = corenlp_tokenize(definitions, opt.corenlp_postagger_path)
    with open(opt.output_filepath, 'w') as ofp:
        for entry, definition in zip(entries, definitions):
            definition = definition.strip()
            ofp.write(f'{entry}\t{definition}\n')
