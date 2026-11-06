import json
from functools import lru_cache
from wave20261102_host_arm7_seventh_index import layout, candidates, accepted_spec
import wave20261102_host_arm7_seventh_real_link as real
from project import ROOT, sha256


@lru_cache(maxsize=1)
def known_entries():
    runtime = layout()
    modules = {m['id']: m for m in runtime['modules']}
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    result = {(r['processor'], r['address']): r for r in candidates()}
    for row in inventory['functions']:
        address = int(row['address'], 0)
        if row['mode'] not in ['arm', 'thumb'] or not row['ranges']:
            continue
        if not any(int(a, 0) <= address < int(b, 0) for a, b in row['ranges']):
            continue
        module = modules[row['module']]
        result.setdefault(('arm7', address), dict(program='', processor='arm7', module=module['id'],
            mode=row['mode'], address=address, ranges=row['ranges'], inputModuleSha256=module['sha256']))
    return result


def validate(entry, directory):
    if entry.get('program') or entry['processor'] != 'arm7':
        raise ValueError('Source/link packet is not the host ARM7 namespace')
    index = known_entries()
    for row in entry['relocations']:
        if row['targetMode'] not in ['arm', 'thumb']:
            continue
        target = index.get(('arm7', int(row['target'], 0) & ~1))
        if target is None or target['mode'] != row['targetMode']:
            raise ValueError('Original target lacks an existing same-mode host ARM7 entry')
    old = real.canonical
    real.canonical = lambda: index
    try:
        proof = real.validate(entry, directory)
    finally:
        real.canonical = old
    proof.update(hostArm7Namespace=True, originalInventorySha256=sha256(ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'),
        canonicalInventoryUnchanged=True, calleeSourceByteCredit=0, calleeFunctionCredit=0)
    return proof
