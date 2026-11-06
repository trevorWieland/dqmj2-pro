import hashlib
import re
import struct
from project import ROOT, sha256
from link_runtime_unit import verify_binding
from wave20261104_main_tail_bindings import native_relocations, RELOCATIONS_SHA256

HELPERS = {'_s32_div_f': (0x02018E88, 0x02018E9C, 0x02026144)}


def verify(row, bindings):
    if row.get('program') or row['processor'] != 'arm9' or row['module'] != 'main' or row['mode'] != 'arm':
        raise ValueError('SDK caller left the original host ARM9 main namespace')
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    relocations = ROOT / 'config/arm9/relocs.txt'
    assert sha256(relocations) == RELOCATIONS_SHA256
    text = relocations.read_text()
    branch_records = native_relocations()
    witnesses = []
    for relocation in row['relocations']:
        name = relocation['symbol']
        binding = bindings[name]
        site = int(row['address'], 0) + relocation['offset']
        target = int(binding['address'], 0)
        if binding.get('program') or binding['processor'] != 'arm9' or target != int(relocation['target'], 0):
            raise ValueError('SDK import program/CPU/address changed')
        kind = relocation['type']
        if kind in (1, 28, 29):
            record = branch_records.get(site)
            if record is None or binding['module'] != record['module'] or target != int(record['address'], 0):
                raise ValueError('SDK branch has no exact original namespace witness')
            if binding['kind'] != 'function' or binding['mode'] != 'arm':
                raise ValueError('SDK branch changed its original ARM entry mode')
            witness = dict(site=hex(site), symbol=name, binding=binding, originalRecord=record['record'])
            if name.startswith('_'):
                if HELPERS.get(name) != (int(row['address'], 0), site, target):
                    raise ValueError('SDK compiler helper has no independently pinned original caller/entry')
                symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
                match = re.search(r'(?m)^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + format(target, '08x') + r'$', symbols)
                if match is None:
                    raise ValueError('Compiler helper full native extent is not configured')
                size = int(match[1], 0)
                body = image[target - 0x02000000:target - 0x02000000 + size]
                assert len(body) == size
                witness['compilerHelper'] = dict(originalCompilerRelocationSymbol=name, completeNativeBytes=size, completeNativeSha256=hashlib.sha256(body).hexdigest(), suppliedCalleeSourceOrExecutionCredit=0)
        elif kind == 2:
            if binding['module'] != 'main' or (binding['kind'], binding['mode']) not in [('data', 'data'), ('function', 'arm')]:
                raise ValueError('SDK absolute load changed its original typed main namespace')
            pattern = r'(?m)^from:0x' + format(site, '08x') + r' kind:load to:0x' + format(target, '08x') + r' module:main\s*$'
            match = re.search(pattern, text)
            if match is None:
                raise ValueError('SDK absolute load has no exact original module/entry witness')
            word = struct.unpack_from('<I', image, site - 0x02000000)[0]
            if word != (target + relocation['addend']) & 0xffffffff:
                raise ValueError('SDK absolute load addend/native word changed')
            witness = dict(site=hex(site), symbol=name, binding=binding, originalRecord=match[0].strip(), originalWord=hex(word), originalAddend=relocation['addend'])
        else:
            raise ValueError('Unqualified SDK relocation kind')
        verify_binding(name, binding)
        witnesses.append(witness)
    return dict(originalRelocationsPath='config/arm9/relocs.txt', originalRelocationsSha256=RELOCATIONS_SHA256, witnesses=witnesses, originalDataCalleeOrHelperSourceCredit=0, sameNumericOverlayAddressInsufficient=True)
