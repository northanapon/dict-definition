from neobunch import Bunch
from nltk.corpus import wordnet as wn
import re

class WordNetParser(object):

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
            freq+=lemma.count()
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
