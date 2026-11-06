import copy
import hashlib
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify
from link_runtime_unit import verify_binding

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/tenth/abi-inputs.json'
INPUT_SHA = '11d0f740bdb222c421947ff826e0ad6aad7081726f6b5b7c3c0b47053792824a'
EXPECTED = {0x020379c4: (40, {12: 0xe1a04002}), 0x0203b8dc: (48, {32: 0xe1a01002}), 0x0203a0c4: (272, {248: 0xe3550004, 252: 0xe2877f5d})}


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Frozen read-only live-R2/neighbor-stride contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen original ABI inventory/image changed')
    return value


def validate(witness, image, inventory):
    if tuple(witness.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'arm', 'function'):
        raise ValueError('Read-only ABI function namespace/kind/mode differs')
    target = int(witness['address'], 0)
    if target not in EXPECTED:
        raise ValueError('Unqualified read-only ABI function')
    size, words = EXPECTED[target]
    if witness['bytes'] != size or witness['instructionWords'] != {str(k): v for k, v in words.items()}:
        raise ValueError('Measured live-word/loop/stride witness differs')
    record = 'func_%08x kind:function(arm,size=0x%x) addr:0x%08x' % (target, size, target)
    if witness['originalInventoryRecord'] != record or record not in inventory.splitlines():
        raise ValueError('Exact original ABI function inventory missing')
    start = target - 0x02000000
    if hashlib.sha256(image[start:start + size]).hexdigest() != witness['targetSha256']:
        raise ValueError('Complete actual original ABI function changed')
    if any(struct.unpack_from('<I', image, start + offset)[0] != word for offset, word in words.items()):
        raise ValueError('Actual original argument-consumption/neighbor-loop words differ')
    if not witness['readOnlyInspection'] or witness['nativeExecution'] != 0 or witness['sourceCredit'] != 0:
        raise ValueError('Read-only ABI observation cannot gain execution/source credit')
    verify_binding('native_fn_%08x' % target, witness)
    return witness


def verify_original(row, bindings):
    result = branch_verify(row, bindings)
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    if {int(w['address'], 0) for w in value['witnesses']} != set(EXPECTED):
        raise ValueError('Read-only ABI witness identity set differs')
    return dict(result, liveArgumentAndStrideWitnesses=[validate(w, image, inventory) for w in value['witnesses']],
                abiQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA), originalCalleeExecution=0, sourceCredit=0)


def negative_controls():
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    checks = []
    for witness in value['witnesses']:
        for label, key, wrong in [('wrong-CPU', 'processor', 'arm7'), ('wrong-mode', 'mode', 'thumb'), ('wrong-module', 'module', 'ov000'),
                                  ('wrong-extent', 'bytes', witness['bytes'] - 4), ('wrong-words', 'instructionWords', {}),
                                  ('invented-native-execution', 'nativeExecution', 1), ('invented-source-credit', 'sourceCredit', 4)]:
            bad = copy.deepcopy(witness)
            bad[key] = wrong
            try:
                validate(bad, image, inventory)
            except ValueError as error:
                checks.append(dict(address=witness['address'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid read-only ABI observation accepted')
        changed = bytearray(image)
        changed[int(witness['address'], 0) - 0x02000000] ^= 1
        for label, raw, records in [('changed-actual-code', bytes(changed), inventory),
                                     ('missing-original-function', image, inventory.replace(witness['originalInventoryRecord'], ''))]:
            try:
                validate(witness, raw, records)
            except ValueError as error:
                checks.append(dict(address=witness['address'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed read-only ABI original evidence accepted')
    return dict(status='passed', negativeCases=checks, nativeCalleeExecution=0, sourceCredit=0)
