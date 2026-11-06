import functools
import re
from project import ROOT, sha256
from link_runtime_unit import verify_binding
from wave20261104_main_tail_compiler import helper_binding

RELOCATIONS_SHA256 = '4467aa2f299dcfcd32dd3744cbf37bec9e545cb29fc77e0b41287465101adc9e'


@functools.cache
def native_relocations():
    path = ROOT / 'config/arm9/relocs.txt'
    if sha256(path) != RELOCATIONS_SHA256:
        raise ValueError('Pinned original main relocation inventory differs')
    result = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch) to:(0x[0-9a-f]+) module:(main|itcm|dtcm|overlay\((\d+)\))', line)
        if match:
            origin = int(match[1], 0)
            module = 'ov' + match[5].zfill(3) if match[5] is not None else match[4]
            row = dict(address=match[3], module=module, record=line)
            if origin in result and result[origin] != row:
                raise ValueError('Original relocation namespace is ambiguous')
            result[origin] = row
    return result


def verify_original(entry, bindings):
    if entry.get('processor') != 'arm9' or entry.get('program') or entry['module'] != 'main' or entry['mode'] != 'arm':
        raise ValueError('Caller crossed the measured main ARM9 namespace')
    original = native_relocations()
    witnesses = []
    for relocation in entry['relocations']:
        name = relocation['symbol']
        binding = bindings.get(name)
        origin = int(entry['address'], 0) + relocation['offset']
        measured = original.get(origin)
        if relocation['type'] not in (1, 28, 29) or measured is None:
            raise ValueError('Caller lacks a pinned original branch relocation record')
        if binding is None or binding.get('processor') != 'arm9' or binding.get('program'):
            raise ValueError('Caller import changed program or CPU')
        if binding.get('module') != measured['module'] or int(binding['address'], 0) != int(measured['address'], 0):
            raise ValueError('Caller import differs from its original relocation module/address')
        if binding.get('kind') != 'function' or binding.get('mode') != 'arm':
            raise ValueError('Caller import changed the measured ARM function mode')
        if int(relocation['target'], 0) != int(measured['address'], 0):
            raise ValueError('Caller generated target differs from its original branch record')
        verify_binding(name, binding)
        if name.startswith('_') and helper_binding(name) != binding:
            normalized = dict(binding, program=binding.get('program') or '')
            if helper_binding(name) != normalized:
                raise ValueError('Compiler helper changed its fixed qualified native identity')
        witnesses.append(dict(symbol=name, origin=hex(origin), module=measured['module'], address=measured['address'],
                              mode='arm', originalRelocationRecord=measured['record'], sourceOrCalleeCredit=0))
    return dict(originalRelocationsPath='config/arm9/relocs.txt', originalRelocationsSha256=RELOCATIONS_SHA256,
                sameNumericOverlayAddressInsufficient=True, witnesses=witnesses, sourceCredit=0)
