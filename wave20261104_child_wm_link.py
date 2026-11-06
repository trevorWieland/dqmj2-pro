import json
import struct
import utility_code
import utility_runtime
import wave20261104_child_wm_real_link as legacy
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_OP_IMM
from wave20261104_child_wm_prepare import ROOT
from project import sha256


def qualify(entry):
    canonical = dict(legacy.canonical())
    layout, files = utility_runtime.derive()
    modules = {m['id']: m for m in layout['modules']}
    caller_module = modules[entry['module']]
    raw = bytes(files[ROOT / caller_module['binary']])
    caller_address, base = int(entry['address'], 0), int(caller_module['base'], 0)
    native = raw[caller_address - base:caller_address - base + entry['bytes']]
    if (entry['program'] != utility_runtime.PROGRAM or caller_module['processor'] != entry['processor'] or
        len(native) != entry['bytes'] or utility_runtime.sha(native) != entry['targetSha256']):
        raise ValueError('Native caller CPU/program/span identity differs')
    inventory_path = ROOT / ('evidence/utility/ghidra-' + entry['processor'] + '.json')
    inventory = json.loads(inventory_path.read_text())
    if inventory.get('program') != entry['program'] or inventory.get('processor') != entry['processor']:
        raise ValueError('Measured callee inventory has a different CPU/program')
    entries = {int(f['address'], 0): f for f in inventory['functions']}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if entry['mode'] == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    qualifications = []
    for rel in entry['relocations']:
        if rel['targetMode'] not in ('arm', 'thumb'):
            continue
        target = int(rel['target'], 0) & ~1
        key = (entry['processor'], target)
        if key in canonical:
            continue
        function = entries.get(target)
        if function is None or function['mode'] != rel['targetMode'] or function['module'] not in modules:
            raise ValueError('Additional callee lacks measured same-program CPU/mode entry')
        module = modules[function['module']]
        block = next((b for b in inventory['memoryBlocks'] if b['name'] == module['id']), None)
        if block is None or block.get('sha256') != module['sha256'] or not function['ranges'] or int(function['ranges'][0][0], 0) != target:
            raise ValueError('Measured callee entry/boundary input is stale')
        if module['processor'] != entry['processor'] or target % (2 if function['mode'] == 'thumb' else 4):
            raise ValueError('Additional callee identity crosses CPU or alignment')
        body = bytes(files[ROOT / module['binary']])
        at = rel['offset']
        if rel['type'] == 2:
            actual = int.from_bytes(native[at:at + 4], 'little')
            expected = ((target | int(function['mode'] == 'thumb')) + rel.get('addend', 0)) & 0xffffffff
            if actual != expected:
                raise ValueError('Additional callee pointer/tag is not the original literal')
            reference = dict(kind='original-function-pointer-literal', offset=at, value=hex(actual))
        else:
            instruction = next(decoder.disasm(native[at:at + 4], caller_address + at), None)
            if instruction is None or not instruction.operands or instruction.operands[0].type != ARM_OP_IMM or not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)):
                raise ValueError('Additional callee lacks original direct branch')
            mode = ('arm' if entry['mode'] == 'thumb' else 'thumb') if instruction.mnemonic.startswith('blx') else entry['mode']
            if instruction.operands[0].imm & ~1 != target or mode != function['mode']:
                raise ValueError('Additional callee mode/target differs from original branch')
            reference = dict(kind='original-direct-branch', offset=at, address=hex(instruction.address),
                mnemonic=instruction.mnemonic, operands=instruction.op_str, bytesHex=instruction.bytes.hex())
        ranges = []
        for first, end in function['ranges']:
            first, end = int(first, 0), int(end, 0)
            start = first - int(module['base'], 0)
            if not 0 <= start < start + end - first <= len(body):
                raise ValueError('Additional callee analysis range escapes measured module')
            ranges.append(dict(start=hex(first), endExclusive=hex(end), sha256=utility_runtime.sha(body[start:start + end - first])))
        canonical[key] = dict(processor=entry['processor'], program=entry['program'], module=function['module'],
                              address=target, mode=function['mode'])
        qualifications.append(dict(name=rel['symbol'], targetAddress=hex(target), mode=function['mode'],
            program=entry['program'], processor=entry['processor'], module=function['module'],
            inputModuleSha256=module['sha256'], callerNativeSpanSha256=entry['targetSha256'],
            callerReference=reference, inventory=inventory_path.relative_to(ROOT).as_posix(),
            inventorySha256=sha256(inventory_path), ghidraBodyRanges=ranges,
            entryPrefixHex=body[target - int(module['base'], 0):target - int(module['base'], 0) + 16].hex(),
            fullCalleeBoundaryProved=False, calleeFunctionCredit=0, calleeSourceBytes=0,
            boundaryEvidence='Existing measured Ghidra entry and explicit original branch/pointer; discontiguous body ranges retained as provisional, no reconstructed callee extent claimed'))
    return canonical, qualifications


def validate(entry, directory):
    canonical, qualifications = qualify(entry)
    original_lookup = legacy.canonical
    legacy.canonical = lambda: canonical
    try:
        proof = legacy.validate(entry, directory)
    finally:
        legacy.canonical = original_lookup
    proof.update(qualifiedAdditionalCalleeBindings=qualifications, canonicalInventoryUnchanged=True,
                 additionalCalleeFunctionCredit=0, additionalCalleeSourceByteCredit=0)
    return proof
