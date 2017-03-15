from neobunch import Bunch


class WN18Parser(object):

    def __init__(self, opt):
        self.opt = opt

    def parse_entity(self, e):
        parts = e[2:].split('_')
        return Bunch(
            word=' '.join(parts[0:-2]),
            pos=parts[-2],
            sense_id=parts[-1])

    def parse_line(self, line):
        parts = line.strip().split('\t')
        output = Bunch(self.parse_entity(parts[1]),
                       wn_id=parts[0],
                       wn_key=parts[1],
                       definition=parts[-1])
        return output

    def to_list(self, entry,
                order_keys=['word', 'pos', 'sense_id',
                            'wn_id', 'definition']):

        output = [entry[k] for k in order_keys]
        return output

    def preprocess(self, ifp, ofp):
        for line in ifp:
            entry = self.parse_line(line)
            if self.opt.only_first_sense and entry.sense_id != '1':
                continue
            ofp.write(u'{}\n'.format(u'\t'.join(self.to_list(entry))))
