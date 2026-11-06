import hashlib
import struct
from project import ROOT, read_json, sha256


CLAIM = 'evidence/lanes/parallel-wave20261106/auth-http-parameter-context/data-claim.json'
CLAIM_SHA = '8933bdb5cb3a1c641523af9f085b353c4a2f99cfadd88dfbd7e5c3b5e64b6090'
DATA_SYMBOL = 'native_data_020deb2c'
URL_SYMBOL = 'native_data_020deb48'


def inspect(elf, name):
    assert elf.elfclass == 32 and elf.little_endian
    assert elf['e_machine'] == 'EM_ARM' and elf['e_type'] == 'ET_REL'
    assert sha256(ROOT / CLAIM) == CLAIM_SHA
    claim = read_json(ROOT / CLAIM)
    assert claim['functionCount'] == 0 and claim['sourceCredit'] == 0
    row = claim['claimedStorage'][0]
    assert len(claim['claimedStorage']) == 1
    assert (row['program'], row['processor'], row['module'], row['address'], row['bytes']) == ('', 'arm9', 'main', '0x20deb2c', 28)
    assert sha256(ROOT / row['semanticSource']) == row['semanticSourceSha256']
    semantic = read_json(ROOT / row['semanticSource'])
    assert semantic['pointerWidth'] == 4 and semantic['byteOrder'] == 'little'
    fields = semantic['fields']
    assert fields['url']['address'] == '0x20deb48'
    assert fields['url']['text'] == 'https://nas.test.nintendowifi.net/ac'
    assert fields['action'] == 'DWCHTTP_POST'
    assert (fields['len_recvbuf'], fields['alloc'], fields['free'], fields['ignoreca'], fields['timeout']) == (4096, None, None, False, 20000)
    assert type(fields['ignoreca']) is bool
    native = struct.pack('<7I', 0x20deb48, 0, 4096, 0, 0, 0, 20000)
    assert hashlib.sha256(native).hexdigest() == row['targetSha256']
    symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
    functions = [(i, s) for i, s in enumerate(symbols) if s.name == name]
    assert len(functions) == 1
    function_index, function = functions[0]
    assert function['st_info']['type'] == 'STT_FUNC' and function['st_size'] == 192
    assert function['st_value'] & ~1 == 0 and isinstance(function['st_shndx'], int)
    text_index = function['st_shndx']
    text = elf.get_section(text_index)
    assert text.name == '.text' and text['sh_type'] == 'SHT_PROGBITS'
    assert text['sh_flags'] == 6 and text['sh_size'] == 192 and text['sh_addralign'] == 4
    allocated = [(i, s) for i, s in enumerate(elf.iter_sections()) if s['sh_flags'] & 2]
    assert len(allocated) == 2
    data_sections = [(i, s) for i, s in allocated if i != text_index]
    assert len(data_sections) == 1
    data_index, data = data_sections[0]
    assert data.name == '.data' and data['sh_type'] == 'SHT_PROGBITS'
    assert data['sh_flags'] == 3 and data['sh_size'] == 28 and data['sh_addralign'] == 4
    assert data.data() == bytes(4) + native[4:]
    objects = [s for s in symbols if s['st_info']['type'] == 'STT_OBJECT' and isinstance(s['st_shndx'], int)
               and elf.get_section(s['st_shndx'])['sh_flags'] & 2]
    assert len(objects) == 1 and objects[0].name == DATA_SYMBOL
    assert objects[0]['st_shndx'] == data_index and objects[0]['st_size'] == 28 and objects[0]['st_value'] == 0
    text_relocations, data_relocations = [], []
    for section in elf.iter_sections():
        if section['sh_type'] not in ('SHT_REL', 'SHT_RELA'):
            continue
        if section['sh_info'] not in [text_index, data_index]:
            continue
        assert section['sh_type'] == 'SHT_RELA'
        target = text_relocations if section['sh_info'] == text_index else data_relocations
        for relocation in section.iter_relocations():
            target.append((relocation['r_offset'], relocation['r_info_type'], relocation['r_info_sym'], relocation['r_addend']))
    assert len(data_relocations) == 1
    offset, kind, index, addend = data_relocations[0]
    assert (offset, kind, symbols[index].name, addend) == (0, 2, URL_SYMBOL, 0)
    assert symbols[index]['st_shndx'] == 'SHN_UNDEF'
    assert text_relocations and all(0 <= r[0] <= 188 and r[1] in [1, 2, 10, 28, 29] for r in text_relocations)
    return symbols, text, text_index, data_index, text_relocations, function_index


def extract(elf, name, output):
    symbols, text, text_index, data_index, relocations, function_index = inspect(elf, name)
    raw_symbols = elf.get_section_by_name('.symtab').data()
    used = {r[2] for r in relocations} | {i for i, s in enumerate(symbols) if s['st_shndx'] == text_index}
    used.discard(0)
    entries, canonical = [], {}
    kinds = {'STT_NOTYPE': 0, 'STT_OBJECT': 1, 'STT_FUNC': 2, 'STT_SECTION': 3, 'STT_FILE': 4}
    binds = {'STB_LOCAL': 0, 'STB_GLOBAL': 1, 'STB_WEAK': 2}
    context_indices = set()
    for index in sorted(used):
        symbol = symbols[index]
        section = symbol['st_shndx']
        info = symbol['st_info']
        if section == text_index:
            record = (symbol.name, symbol['st_value'], symbol['st_size'], binds[info['bind']], kinds[info['type']], 1, raw_symbols[index * 16 + 13])
        elif section == data_index:
            assert symbol['st_value'] == 0
            assert (info['bind'], info['type'], symbol.name) in [('STB_LOCAL', 'STT_SECTION', '.data'), ('STB_GLOBAL', 'STT_OBJECT', DATA_SYMBOL)]
            assert raw_symbols[index * 16 + 13] == 0
            record = (DATA_SYMBOL, 0, 0, 1, 1, 0, 0)
            context_indices.add(index)
        else:
            assert section == 'SHN_UNDEF' and info['bind'] in ['STB_GLOBAL', 'STB_WEAK']
            record = (symbol.name, 0, 0, binds[info['bind']], kinds[info['type']], 0, raw_symbols[index * 16 + 13])
        key = ('context', DATA_SYMBOL) if index in context_indices else ('original', index)
        if key not in canonical:
            canonical[key] = len(entries)
            entries.append(dict(record=record, indices=[index]))
        else:
            entries[canonical[key]]['indices'].append(index)
    assert context_indices
    entries.sort(key=lambda r: r['record'][3] != 0)
    strings, symbol_bytes, indices = bytearray(b'\0'), bytearray(16), {0: 0}
    for position, item in enumerate(entries, 1):
        symbol_name, value, size, bind, kind, section, other = item['record']
        at = len(strings)
        strings.extend(symbol_name.encode() + b'\0')
        symbol_bytes.extend(struct.pack('<IIIBBH', at, value, size, bind << 4 | kind, other, section))
        for index in item['indices']:
            assert symbols[index]['st_other']['visibility'] == 'STV_DEFAULT'
            indices[index] = position
    first_global = 1 + sum(item['record'][3] == 0 for item in entries)
    relocation_bytes = b''.join(struct.pack('<IIi', offset, indices[index] << 8 | kind, addend)
                                for offset, kind, index, addend in relocations)
    names, offsets = bytearray(b'\0'), []
    for label in ['.text', '.rela.text', '.symtab', '.strtab', '.shstrtab']:
        offsets.append(len(names))
        names.extend(label.encode() + b'\0')
    sections = [(offsets[0], 1, 6, text.data(), 0, 0, text['sh_addralign'], text['sh_entsize']),
                (offsets[1], 4, 0, relocation_bytes, 3, 1, 4, 12),
                (offsets[2], 2, 0, bytes(symbol_bytes), 4, first_global, 4, 16),
                (offsets[3], 3, 0, bytes(strings), 0, 0, 1, 0),
                (offsets[4], 3, 0, bytes(names), 0, 0, 1, 0)]
    result, headers = bytearray(52), [(0,) * 10]
    for label, kind, flags, data, link, info, alignment, entry_size in sections:
        result.extend(bytes((-len(result)) % alignment))
        at = len(result)
        result.extend(data)
        headers.append((label, kind, flags, 0, at, len(data), link, info, alignment, entry_size))
    result.extend(bytes((-len(result)) % 4))
    section_table = len(result)
    result.extend(b''.join(struct.pack('<10I', *h) for h in headers))
    result[:16] = b'\x7fELF\x01\x01\x01' + bytes(9)
    struct.pack_into('<HHIIIIIHHHHHH', result, 16, 1, 40, 1, 0, 0, section_table, elf['e_flags'], 52, 0, 0, 40, 6, 5)
    output.write_bytes(result)
    return text.data(), [r[0] for r in relocations]
