# dict-definition
Preprocessing scripts to read definitions and other information from dictionaries. This repository accompanies AAAI2017 paper: "Definition Modeling: Learning to define word embeddings in natural language". For data used in the paper, please visit [torch-defseq](https://github.com/NorThanapon/torch-defseq).

## Dependencies
- Python 3.6
- [nltk](http://www.nltk.org/) >= 3.1
- [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) (for tokenization)

## TODO
- [x] WordNet databae parser
- [x] CoreNLP tokenizer
- [ ] GCIDE parser
- [ ] Wordnik API reader
- [ ] Oxford API reader

## Where to get data

### Datasets
- [GCIDE](http://gcide.gnu.org.ua/), GNU Collaborative International Dictionary of English, contains entries mostly from Webster. This project use a pre-processed version of the original release which can be found [here](http://rali.iro.umontreal.ca/GCIDE/).
- [WordNet](https://wordnet.princeton.edu/) contains about 150,000 words and phrases. This project uses [NLTK](http://www.nltk.org/) to read data from WordNet.
- [HillF_TACL2016](http://arxiv.org/abs/1504.00548) provides more than 800k definitions from WordNik API along with word embeddings. Unfortunately, [the link](http://www.cl.cam.ac.uk/~fh295/) to the data is not present.

### APIs
- [Wordnik](https://www.wordnik.com/) provides an API to get word definitions and other information from *multiple* dictionaries. You will need an API Key to access (see [Developer site](http://developer.wordnik.com/)).
- [Oxford Dictionaries](https://developer.oxforddictionaries.com/) provides various API including definition query from Oxford dictionaries. The definitions quality are exceptionally high (resembled defintions from Google search), but the number of queries is limited for a free user.
