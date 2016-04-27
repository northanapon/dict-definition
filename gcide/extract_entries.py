from xml.etree import ElementTree
from entry_parser import *
import json
import codecs
import os

gcide_dir = '../data/gcide/new-entries/'
gcide_output_dir = '../output/gcide-entries'
# gcide_output_index

target = [chr(i) for i in range(97, 123)]


for c in target:
    gcide_filepath = os.path.join(gcide_dir, 'gcide_'+c+'-entries.xml')
    gcide_output_path = os.path.join(gcide_output_dir, 'gcide_'+c+'-entries.jsonl')
    n_entries = ElementTree.parse(gcide_filepath).getroot()
    ln_entry = n_entries.findall('entry')
    with codecs.open(gcide_output_path, 'w', 'utf-8') as of:
        for n_entry in ln_entry:
            if not is_from_webster(n_entry) or is_phrase(n_entry):
                continue
            entry = parse_entry(n_entry)
            if 'senses' not in entry:
                continue
            json.dump(entry, of)
            of.write('\n')
