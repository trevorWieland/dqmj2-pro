import hashlib
import re
from project import ROOT
from link_runtime_unit import verify_binding
from wave20261105_main_sdk_bulk_system_bindings import verify as verify_storage
from wave20261104_main_tail_bindings import native_relocations


def verify(row, bindings, provenance):
    normal = dict(row, relocations=[rel for rel in row['relocations'] if not rel['symbol'].startswith('_')])
    proof = verify_storage(normal, bindings, provenance)
    for relocation in row['relocations']:
        if not relocation['symbol'].startswith('_'):
            continue
        name = relocation['symbol']
        binding = bindings[name]
        site = int(row['address'], 0) + relocation['offset']
        expected = (0x0201A670, 0x0201ADA0, '_ll_udiv', 0x020260DC)
        if (int(row['address'], 0), site, name, int(binding['address'], 0)) != expected:
            raise ValueError('Formatter compiler helper lost its exact original caller/entry/name witness')
        if relocation['type'] not in [1, 28, 29] or (binding['processor'], binding['module'], binding['mode'], binding['kind']) != ('arm9', 'main', 'arm', 'function') or binding.get('program'):
            raise ValueError('Formatter compiler helper namespace or relocation mode changed')
        original = native_relocations().get(site)
        if original is None or original['module'] != 'main' or int(original['address'], 0) != 0x020260DC or int(relocation['target'], 0) != 0x020260DC:
            raise ValueError('Formatter compiler helper differs from the original branch record')
        verify_binding(name, binding)
        symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
        match = re.search(r'(?m)^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x020260dc$', symbols)
        assert match is not None
        count = int(match[1], 0)
        body = (ROOT / 'extract/arm9/arm9.bin').read_bytes()[0x260dc:0x260dc + count]
        proof['witnesses'].append(dict(site=hex(site), symbol=name, binding=binding, originalRecord=original['record'], nativeConfiguredBytes=count,
            nativeConfiguredSha256=hashlib.sha256(body).hexdigest(), originalCompilerHelperName='_ll_udiv', helperOrCalleeSourceCredit=0))
    return proof
