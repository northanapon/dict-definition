import argparse
import codecs
from definition.readers.wn18 import WN18Parser
from definition.readers.wordnet import WordNetParser
from definition.words import word_sampler


def get_parser(name, opt):
    if name == 'wn18':
        return WN18Parser(opt)
    if name == 'wordnet':
        return WordNetParser(opt)


def main(opt):
    parser = get_parser(opt.data_name, opt)
    with codecs.open(opt.input_filepath, 'r', 'utf-8') as ifp:
        with codecs.open(opt.output_filepath, 'w', 'utf-8') as ofp:
            parser.preprocess(ifp, ofp)


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="Preprocess data from a corpus")
    aparser.add_argument(
        'input_filepath', type=str,
        help='input file path')
    aparser.add_argument(
        'output_filepath', type=str,
        help='output file path')
    aparser.add_argument(
        'data_name', choices=['wn18', 'wordnet'],
        help='type of the corpus')
    aparser.add_argument(
        '--only_first_sense', dest='only_first_sense', action='store_true')
    opt = aparser.parse_args()
    main(opt)
