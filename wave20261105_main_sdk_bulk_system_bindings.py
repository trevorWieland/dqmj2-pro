import re
import struct
from project import ROOT, sha256
from link_runtime_unit import verify_binding
from wave20261105_main_sdk_bulk_bindings import verify as verify_plain


def verify(row, bindings, provenance):
    plain = dict(row, relocations=[rel for rel in row['relocations'] if rel['type'] != 2 or not rel['addend']])
    proof = verify_plain(plain, bindings)
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    path = ROOT / 'config/arm9/relocs.txt'
    text = path.read_text()
    assert sha256(path) == proof['originalRelocationsSha256']
    for relocation in row['relocations']:
        if relocation['type'] != 2 or not relocation['addend']:
            continue
        name = relocation['symbol']
        binding = bindings[name]
        if binding.get('program') or (binding['processor'], binding['module'], binding['mode'], binding['kind']) != ('arm9', 'main', 'data', 'data'):
            raise ValueError('SDK common-bank load changed its original data namespace')
        base = int(binding['address'], 0)
        if base != int(relocation['target'], 0):
            raise ValueError('SDK common-bank relocation and configured data base differ')
        layout = next((layout for layout in provenance['typedStorageLayouts'] if int(layout['nativeBase'], 0) == base), None)
        if layout is None:
            raise ValueError('SDK absolute addend has no typed original storage-bank context')
        extent = max(member['offset'] + member['bytes'] for member in layout['members'])
        if not 0 <= relocation['addend'] < extent:
            raise ValueError('SDK absolute addend escaped the declared storage bank')
        target = base + relocation['addend']
        site = int(row['address'], 0) + relocation['offset']
        match = re.search(r'(?m)^from:0x' + format(site, '08x') + r' kind:load to:0x' + format(target, '08x') + r' module:main\s*$', text)
        if match is None or struct.unpack_from('<I', image, site - 0x02000000)[0] != target:
            raise ValueError('SDK typed base-plus-addend load differs from its exact original resolved load')
        verify_binding(name, binding)
        proof['witnesses'].append(dict(site=hex(site), symbol=name, binding=binding, originalRecord=match[0].strip(),
            typedStorageBase=hex(base), typedStorageExtent=extent, unchangedObjectAddend=relocation['addend'], originalResolvedAddress=hex(target), originalStorageSourceCredit=0))
    return proof
