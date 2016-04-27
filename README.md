# dict-definition
Preprocessing scripts to read definitions and other information from dictionaries

## Dependencies
- Python 2.7
- [nltk](http://www.nltk.org/) >= 3.1
- [wordnik](https://github.com/wordnik/wordnik-python) >= 2.1.3

## Obtaining data
- [Wordnik](https://www.wordnik.com/) provides an API to get word definitions and other information from *multiple* dictionaries. You will need an API Key to access (see [Developer site](http://developer.wordnik.com/)).
- [GCIDE](http://gcide.gnu.org.ua/), GNU Collaborative International Dictionary of English, contains entries mostly from Webster. This project use a pre-processed version of the original release which can be found [here](http://rali.iro.umontreal.ca/GCIDE/).
- [WordNet](https://wordnet.princeton.edu/) contains about 150,000 words and phrases. This project uses [NLTK](http://www.nltk.org/) to read data from WordNet.
