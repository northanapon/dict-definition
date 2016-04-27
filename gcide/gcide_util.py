def index_gcide(gcide_dir):
    index = {}
    for fn in os.listdir(gcide_dir):
        fp = os.path.join(gcide_dir, fn)
        if not os.path.isfile(fp):
            continue
        with codecs.open(fp, 'r', 'utf-8') as ifp:
            for line in ifp:
                entry = json.loads(line)
                key = entry[u'key'].lower()
                if key not in index:
                    index[key] = []
                index[key].append(entry)
    return index

def write_gcide_defs(entries, ofp):
    total_write_out = 0
    for entry in entries:
        if u'pos' not in entry:
            continue
        count = 0
        for sense in entry[u'senses']:
            ofp.write(entry[u'key'].lower())
            ofp.write('\t')
            ofp.write('gcide\t')
            ofp.write(entry[u'pos'][0])
            ofp.write('\t')
            ofp.write(sense[u'def'])
            ofp.write('\n')
            count = count + 1
            total_write_out = total_write_out + 1
            if count > 1:
                break
    return total_write_out
