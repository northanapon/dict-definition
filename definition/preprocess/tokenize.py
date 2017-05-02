import argparse
from nltk.tokenize import StanfordTokenizer


aparser = argparse.ArgumentParser(
    description="Run CoreNLP tokenizer on a TSV definition file")
aparser.add_argument(
    'input_filepath', type=str, help='input file path')
aparser.add_argument(
    'output_filepath', type=str, help='output file path')
aparser.add_argument(
    'corenlp_postagger_path', type=str, help="path to stanford-postagger.jar")

opt = aparser.parse_args()
tokenizer = StanfordTokenizer(path_to_jar=opt.corenlp_postagger_path,
                              options={"ptb3Escaping": "false",
                                       "tokenizePerLine": "true",
                                       "tokenizeNLs": "true"})
entries = []
definitions = []
with open(opt.input_filepath) as ifp:
    for line in ifp:
        parts = line.strip().split('\t')
        entries.append(parts[:-1])
        definitions.append(parts[-1])
def_str = "\n".join(definitions)
tokens = tokenizer.tokenize(def_str)
def_str = " ".join(tokens)
definitions = def_str.split("*NL*")
with open(opt.output_filepath, 'w') as ofp:
    for entry, definition in zip(entries, definitions):
        ofp.write("{}\t{}\n".format('\t'.join(entry), definition.strip()))
