from neobunch import Bunch
import os
from nltk.corpus import wordnet as wn
import re
from itertools import izip
from definition.words.word_sampler import lemmatize_all


class NLTKWordNetParser(object):

    def __init__(self, opt):
        self.opt = opt

    def to_list(self, entry,
                order_keys=['word', 'pos', 'sense_id',
                            'wn_id', 'proper_noun',
                            'lemma_freq', 'definition']):
        output = [u'{}'.format(entry[k]) for k in order_keys]
        return output

    def parse_synset_name(self, name):
        parts = name.split('.')
        return Bunch(pos=parts[-2],
                     sense_id=int(parts[-1]), wn_id=name)

    def get_entry(self, word, sense):
        synset = self.parse_synset_name(sense.name())
        synset.word = word
        synset.definition = sense.definition()
        synset.proper_noun = self.is_proper_noun(sense)
        freq = 0
        for lemma in sense.lemmas():
            freq += lemma.count()
        synset.lemma_freq = freq
        return synset

    def is_proper_noun(self, sense):
        cap = 0
        for lemma in sense.lemmas():
            if lemma.name() != lemma.name().lower():
                cap += 1
        return cap == len(sense.lemmas())

    def get_entries(self, word):
        entries = []
        query = word
        senses = wn.synsets(query)
        for sense in senses:
            entries.append(self.get_entry(word, sense))
        entries.sort(key=lambda x: x.lemma_freq, reverse=True)
        return entries

    def one_sense_per_pos(self, entries, pref=['v', 'a', 's', 'n', 'r']):
        new_entries = []
        for p in pref:
            for entry in entries:
                if entry.pos == p:
                    new_entries.append(entry)
                    break
        return new_entries

    def select_top_entry(self, entries):
        if len(entries) < 2:
            return entries
        if entries[0].lemma_freq > entries[1].lemma_freq:
            return [entries[0]]
        top_freq = entries[0].lemma_freq
        entries = filter(lambda e: e.lemma_freq == top_freq, entries)
        entries = self.one_sense_per_pos(entries)
        return [entries[0]]

    def remove_self_ref(self, word, entries):
        new_entries = []
        p = re.compile(r' ' + word + r'[ ,:;"\']')
        for entry in entries:
            if p.search(entry.definition) is None:
                new_entries.append(entry)
        return new_entries

    def preprocess(self, ifp, ofp):
        for line in ifp:
            word = line.strip()
            entries = self.get_entries(word)
            entries = self.remove_self_ref(word, entries)
            if self.opt.only_first_sense and len(entries) > 1:
                entries = self.select_top_entry(entries)
            for entry in entries:
                ofp.write(u'{}\n'.format(u'\t'.join(self.to_list(entry))))


class DBWordNetParser(object):
    def __init__(self, opt):
        self.opt = opt
        self.dir = opt.wndb_dir
        self.lexnames = DBWordNetParser.read_lexname(self.dir)
        self.idx = DBWordNetParser.read_index_files(self.dir)
        self.data = DBWordNetParser._read_data_files(self.dir, self.lexnames)
        self.sense_numbers = DBWordNetParser.read_sense_file(self.dir)

    _POS_FILE_MAP_ = {'n': 'noun', 'v': 'verb', 'a': 'adj', 'r': 'adv'}
    _SYNSET_TYPE_MAP_ = [None, 'n', 'v', 'a', 'r', 's']

    def to_list(self, word, entry, inflected=False):
        source = 'lemma'
        if inflected:
            source = 'inflection'
        output = [word, entry.lemma, entry.synset_type,
                  str(entry.sense_number), entry.pos, source, entry.gloss]
        return output

    def get_idx_entries(self, word, try_lemma=True):
        if word in self.idx:
            return self.idx[word], False
        if try_lemma:
            out_entries = []
            tagged_lemmas = lemmatize_all(word)
            for lemma, pos in tagged_lemmas:
                for e in self.idx.get(lemma, []):
                    if e.pos == pos and lemma != word:
                        out_entries.append(e)
            return out_entries, True

    def get_entries(self, idx_entries):
        out_entries = []
        for idx_entry in idx_entries:
            for synset_offset in idx_entry.synset_offsets:
                data_entry = self.data[synset_offset]
                sense_key = '{}-{}-{}'.format(
                    idx_entry.lemma, data_entry.synset_type, data_entry.offset)
                entry = Bunch(lemma=idx_entry.lemma,
                              pos=idx_entry.pos,
                              synset_type=data_entry.synset_type,
                              sense_number=self.sense_numbers[sense_key],
                              gloss=data_entry.gloss)
                out_entries.append(entry)
        return out_entries

    def preprocess(self, ifp, ofp):
        for line in ifp:
            word = line.strip()
            idx_entries, inflected = self.get_idx_entries(word)
            entries = self.get_entries(idx_entries)
            for entry in entries:
                ofp.write(u'{}\n'.format(
                    u'\t'.join(self.to_list(word, entry, inflected))))

    @staticmethod
    def read_lexname(wndb_path):
        lexnames = {}
        lexname_path = os.path.join(wndb_path, 'lexnames')
        with open(lexname_path) as ifp:
            for line in ifp:
                if line.startswith(' '):
                    continue
                part = line.strip().split('\t')
                lexnames[part[0]] = part[1]
        return lexnames

    @staticmethod
    def read_sense_file(wndb_path):
        sense_numbers = {}
        idx_sense_path = os.path.join(wndb_path, 'index.sense')
        with open(idx_sense_path) as ifp:
            for line in ifp:
                if line.startswith(' '):
                    continue
                part = line.strip().split(' ')
                lemma, key = part[0].split('%')
                synset_type = DBWordNetParser._SYNSET_TYPE_MAP_[int(key[0])]
                offset = part[1]
                number = int(part[2])
                sense_key = '{}-{}-{}'.format(lemma, synset_type, offset)
                sense_numbers[sense_key] = number
        return sense_numbers

    @staticmethod
    def read_index_files(wndb_path, pos_files=['noun', 'verb', 'adj', 'adv']):
        entries = {}
        for pos_file in pos_files:
            idx_path = os.path.join(wndb_path, 'index.' + pos_file)
            with open(idx_path) as ifp:
                for line in ifp:
                    if line.startswith(' '):
                        continue
                    part = line.strip().split()
                    _ap = 4+int(part[3])
                    lemma = part[0]
                    idx_entry = Bunch(
                        lemma=lemma,
                        pos=part[1],
                        pointers=part[4:_ap],
                        num_tagsenes=int(part[_ap + 1]),
                        synset_offsets=['{}-{}'.format(pos_file, _o)
                                        for _o in part[_ap + 2:]])
                    entries[lemma] = entries.get(lemma, [])
                    entries[lemma].append(idx_entry)
        return entries

    @staticmethod
    def _parse_pointers(tups):
        pointers = []
        for tup in tups:
            pointers.append(
                Bunch(pointer=tup[0], offset='{}-{}'.format(
                    DBWordNetParser._POS_FILE_MAP_[tup[2]], tup[1]),
                      source=tup[3][:2], target=tup[3][2:]))
        return pointers

    @staticmethod
    def _parse_words(tups):
        words = []
        for tup in tups:
            words.append(Bunch(word=tup[0], lex_id=tup[1]))
        return words

    @staticmethod
    def _chunklist(t, size=2):
        it = iter(t)
        return list(izip(*[it]*size))

    @staticmethod
    def _read_data_files(wndb_path, lexnames,
                         pos_files=['noun', 'verb', 'adj', 'adv']):
        data = {}
        for pos_file in pos_files:
            data_path = os.path.join(wndb_path, 'data.' + pos_file)
            with open(data_path) as ifp:
                for line in ifp:
                    if line.startswith(' '):
                        continue
                    part = line.strip().split()
                    _num_words = int(part[3], 16)
                    _num_pointers = int(part[4 + _num_words * 2])
                    _pp = 4 + _num_words*2 + 1
                    _gloss_p = part.index('|') + 1
                    data_entry = Bunch(
                        offset=part[0],
                        lexname=lexnames[part[1]],
                        synset_type=part[2],
                        words=DBWordNetParser._parse_words(
                            DBWordNetParser._chunklist(part[4:_pp - 1])),
                        pointers=DBWordNetParser._parse_pointers(
                            DBWordNetParser._chunklist(
                                part[_pp:_pp + _num_pointers * 4], 4)),
                        gloss=' '.join(part[_gloss_p:]))
                    data['{}-{}'.format(pos_file, part[0])] = data_entry
        return data


if __name__ == '__main__':
    opt = Bunch(wndb_dir='data/wndb')
    parser = DBWordNetParser(opt)
    idx_entries, inflected = parser.get_idx_entries('tests')
    for e in parser.get_entries(idx_entries):
        print(e)
