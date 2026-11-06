import copy
import json
from functools import lru_cache
from pathlib import Path
from project import ROOT, sha256, write_json
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wl/helper-inputs.json'
INPUT_SHA = '234ac66c23c9eec7fcdd752c5c62a1f1a61d2ed8cb09a229dded39aacc3ee358'
HELPER_NAMES = {'_s32_div_f', '_ll_udiv'}


def validate(case, inventory, raw):
    if (case['program'], case['processor'], case['module'], case['callerMode'], case['targetMode']) != (
            utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-wram', 'arm', 'arm'):
        raise ValueError('Helper namespace or mode differs')
    address, target = int(case['caller'], 0), int(case['target'], 0)
    native = raw[address - case['base']:address - case['base'] + case['bytes']]
    if len(native) != case['bytes'] or utility_runtime.sha(native) != case['callerSha256']:
        raise ValueError('Original complete caller differs')
    row = next((e for e in inventory['functions'] if int(e['address'], 0) == target), None)
    if row is None or (row['module'], row['processor'], row['mode']) != (case['module'], 'arm7', 'arm'):
        raise ValueError('Compiler helper lacks original same-program ARM entry')
    if [(r['start'], r['endExclusive']) for r in case['targetInventoryRanges']] != [tuple(r) for r in row['ranges']]:
        raise ValueError('Original helper body ranges changed')
    for part in case['targetInventoryRanges']:
        a, z = int(part['start'], 0) - case['base'], int(part['endExclusive'], 0) - case['base']
        if not 0 <= a < z <= len(raw) or utility_runtime.sha(raw[a:z]) != part['sha256']:
            raise ValueError('Original helper body fragment changed')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    for branch in case['originalBranches']:
        offset = branch['offset']
        body = native[offset:offset + 4]
        instruction = next(decoder.disasm(body, address + offset), None)
        if (body.hex() != branch['bytesHex'] or instruction is None or instruction.mnemonic != 'bl' or
                len(instruction.operands) != 1 or instruction.operands[0].type != ARM_OP_IMM or
                instruction.operands[0].imm != target):
            raise ValueError('Original helper BL target, mode or encoded instruction differs')
    return dict(case, canonicalInventoryUnchanged=True, originalCompilerObjectRewrite=False,
                calleeFunctionCredit=0, actualCallerExecutions=0, actualCalleeExecutions=0)


@lru_cache(maxsize=1)
def qualified():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Frozen helper qualification manifest changed')
    value = json.loads(INPUT.read_text())
    if sha256(ROOT / value['inventory']) != value['inventorySha256']:
        raise ValueError('Original ARM7 inventory changed')
    inventory = json.loads((ROOT / value['inventory']).read_text())
    if (inventory['program'], inventory['processor']) != (utility_runtime.PROGRAM, 'arm7'):
        raise ValueError('Original inventory namespace changed')
    result = []
    for case in value['cases']:
        if sha256(ROOT / case['binary']) != case['inputModuleSha256']:
            raise ValueError('Original ARM7 image changed')
        result.append(validate(case, inventory, (ROOT / case['binary']).read_bytes()))
    return result


def helper_target(name, spec):
    case = next((r for r in qualified() if r['compilerHelperName'] == name and int(r['caller'], 0) == spec['address']), None)
    if case is None or (spec['program'], spec['processor'], spec['module'], spec['mode'], spec['bytes'], spec['inputModuleSha256']) != (
            case['program'], case['processor'], case['module'], case['callerMode'], case['bytes'], case['inputModuleSha256']):
        raise ValueError('Compiler helper is outside its frozen caller contract')
    return int(case['target'], 0)


def validate_relocations(row):
    for case in qualified():
        if int(row['address'], 0) != int(case['caller'], 0):
            continue
        actual = [r for r in row['relocations'] if r['symbol'] == case['compilerHelperName']]
        if sorted(r['offset'] for r in actual) != sorted(r['offset'] for r in case['originalBranches']):
            raise ValueError('Compiler helper relocation sites differ from original calls')
        if any((r['type'], r['targetMode'], int(r['target'], 0), r['addend']) != (1, 'arm', int(case['target'], 0), -8) for r in actual):
            raise ValueError('Compiler helper relocation type, addend or mode differs')


def main():
    cases = qualified()
    value = json.loads(INPUT.read_text())
    inventory = json.loads((ROOT / value['inventory']).read_text())
    controls = []
    for original in value['cases']:
        raw = (ROOT / original['binary']).read_bytes()
        for field, wrong in [('program', ''), ('processor', 'arm9'), ('targetMode', 'thumb'), ('target', hex(int(original['target'], 0) + 4))]:
            case = copy.deepcopy(original)
            case[field] = wrong
            try:
                validate(case, inventory, raw)
            except ValueError:
                controls.append(dict(caller=original['caller'], field=field, rejected=True))
            else:
                raise ValueError('Invalid helper qualification accepted')
    output = INPUT.with_name('helper-qualification.json')
    write_json(output, dict(status='passed', inputSha256=INPUT_SHA, cases=cases, controls=controls,
                           sourceCredit=0, callerExecutionCredit=0, calleeExecutionCredit=0))
    print(dict(cases=len(cases), originalBranchSites=sum(len(r['originalBranches']) for r in cases), controls=len(controls)))


if __name__ == '__main__':
    main()
