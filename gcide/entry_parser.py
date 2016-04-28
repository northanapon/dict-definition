def parse_entry(n_entry):
    entry = {}
    entry['key'] = n_entry.attrib['key']
    entry['cs'] = parse_cs(n_entry.find('cs'))
    entry['pos'] = parse_pos(n_entry.find('pos'))
    entry['plural'] = parse_plu(n_entry.find('plu'))
    entry['vmorph'] = parse_vmorph(n_entry.find('vmorph'))
    entry['amorph'] = parse_amorph(n_entry.find('amorph'))
    entry['senses'] = _extract_definitions(n_entry)
    return remove_none(entry)

#####################
# Misc. Tags
#####################

def parse_cs(n_cs):
    if n_cs is None: return None
    cs = []
    col = None
    for elem in list(n_cs):
        if elem.tag == 'col':
            if col is not None:
                cs.append(col)
            col = {}
            col['phrase'] = [elem.text]
        if elem.tag == 'mcol':
            if col is not None:
                cs.append(col)
            col = {}
            col['phrase'] = []
            for col_ele in elem.findall('col'):
                col['phrase'].append(col_ele.text)
        if elem.tag == 'fld' and col is not None and 'field' not in col:
            col['field'] = parse_fld(elem)
        if elem.tag == 'cd' and col is not None:
            if 'def' not in col:
                col['def'] = []
            col['def'].append(get_all_text(elem))
    if col is not None:
        cs.append(col)
    if len(cs) == 0:
        return None
    return cs

def parse_pos(n_pos):
    if n_pos is None:
        return None
    return [t.strip() for t in n_pos.text.split('&')]

def parse_plu(n_plu):
    if n_plu is None:
        return None
    n_plw = n_plu.find('plw')
    if n_plw is None:
        return None
    return n_plw.text

def parse_fld(n_fld):
    if n_fld is None:
        return None
    return n_fld.text

#####################
# Morphology
#####################

def _parse_morph(n_morph, tag):
    if n_morph is None:
        return None
    morphs = []
    morph = None
    for elem in list(n_morph):
        if elem.tag == 'pos':
            if morph is not None:
                morphs.append(morph)
            morph = {}
            morph['pos'] = parse_pos(elem)
        if elem.tag == tag and morph is not None:
            if 'word' not in morph:
                morph['word'] = []
            morph['word'].append(elem.text)
    if morph is not None:
        morphs.append(morph)
    if len(morphs) == 0:
        return None
    return morphs

def parse_vmorph(n_vmorph):
    return _parse_morph(n_vmorph, 'conjf')

def parse_amorph(n_amorph):
    return _parse_morph(n_amorph, 'adjf')

#####################
# Definition
#####################

def _extract_definitions(n_entry):
    definitions = []
    d = None
    for elem in list(n_entry):
        if elem.tag == 'def':
            if d is None:
                d = {}
            if d is not None and 'def' in d:
                if len(d['def']) > 0:
                    definitions.append(d)
                d = {}
            d['def'], d['usage'] = parse_def(elem)
        if elem.tag == 'fld':
            if d is None:
                d = {}
            if d is not None and 'def' in d:
                if len(d['def']) > 0:
                    definitions.append(d)
                d = {}
            d['field'] = parse_fld(elem)
        if elem.tag == 'sn':
            if d is not None and 'def' in d and len(d['def']) > 0:
                definitions.append(d)
            d = None
            sn_defs = parse_sn(elem)
            if sn_defs is not None:
                definitions = definitions + sn_defs
    if d is not None:
        definitions.append(d)
    if len(definitions) == 0:
        return None
    return definitions

def parse_sn(n_sn):
    if n_sn.find('sd') is None:
        return _extract_definitions(n_sn)
    n_fld = n_sn.find('fld')
    field = parse_fld(n_fld)
    definitions = []
    for n_sd in n_sn.findall('sd'):
        if n_sd.find('def') is None:
            continue
        d = {}
        d['def'], d['usage'] = parse_def(n_sd.find('def'))
        d['field'] = field
        definitions.append(d)
    return definitions

def parse_def(n_def):
    start_paren_end = False
    optional_spn = False
    definition = [n_def.text]
    if n_def.text is None:
        definition = ['']
    examples = []
    for elem in list(n_def):
        if definition[-1][-1] == '(':
            start_paren_end = True
        if elem.tag == 'as':
            examples.append(get_all_text(elem))
        elif elem.tag == 'spn' and start_paren_end:
            optional_spn = True
            if definition[-1][-1] == '(':
                definition[-1] = definition[-1][:-2]
            if elem.tail[0] == ')':
                start_paren_end = False
                optional_spn = False
                elem.tail = elem.tail[1:]
        else:
            definition.append(elem.text or '')
        if not optional_spn:
            definition.append(elem.tail or '')
    if len(examples) == 0:
        examples = None
    return clean_text(''.join(definition)), examples

#####################
# Utilities
#####################

def is_from_webster(n_entry):
    head = n_entry.find('wordforms')
    if head is not None:
        if 'source' in head.attrib:
            return 'Webster' in head.attrib['source']
    head = n_entry.find('mhw')
    if head is not None:
        if 'source' in head.attrib:
            return 'Webster' in head.attrib['source']
    else:
        head = n_entry.findall('hw')
    for h in head:
        if 'source' in h.attrib and 'Webster' in h.attrib['source']:
            return True
    return False

def is_phrase(n_entry):
    return ' ' in n_entry.attrib['key']

def get_all_text(elem):
    text = ''.join(elem.itertext())
    text = text.replace('\n', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def clean_text(text):
    text = text.replace('\n', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
            for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj
