import copy
import json
from functools import lru_cache
from pathlib import Path
import utility_code
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_MEM, ARM_OP_IMM, ARM_OP_REG, ARM_REG_PC, ARM_REG_LR, ARM_INS_B, ARM_CC_AL
from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wl/callback'
INPUT = LANE / 'boundary-inputs.json'
INPUT_SHA = 'e1fada66187ba6e1233489d46c51ce2e52d93e9d5406f8ffab7bc7b0c59039ee'


def decoder():
    result = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    result.detail = True
    return result


def neighbour_end(function, raw, base):
    if len(function['ranges']) != 1 or function['mode'] != 'arm':
        raise ValueError('Original neighbour is not one existing ARM body')
    first, end = [int(a, 0) for a in function['ranges'][0]]
    if first != int(function['address'], 0):
        raise ValueError('Original neighbour has a different entry')
    instructions = list(decoder().disasm(raw[first - base:end - base], first))
    if sum(i.size for i in instructions) != end - first:
        raise ValueError('Original neighbour body is not completely decoded')
    for instruction in instructions:
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                target = instruction.address + 8 + operand.mem.disp
                if target % 4 or not first <= target <= base + len(raw) - 4:
                    raise ValueError('Original neighbour literal is outside its measured image')
                end = max(end, target + 4)
    return end


def validate_native(value, raw, wram, inventory):
    spec = value['spec']
    identity = (spec['program'], spec['processor'], spec['module'], spec['mode'])
    if identity != (utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-main', 'arm'):
        raise ValueError('Private entry namespace or ARM mode differs')
    address, base = int(spec['address'], 0), spec['base']
    end = address + spec['bytes']
    if address % 4 or spec['bytes'] != value['codeBytes'] + value['literalBytes']:
        raise ValueError('Private entry alignment or complete extent differs')
    native = raw[address - base:end - base]
    if len(native) != spec['bytes'] or utility_runtime.sha(native) != spec['targetSha256']:
        raise ValueError('Original complete callback body differs')
    entries = {int(f['address'], 0): f for f in inventory['functions'] if f['module'] == spec['module']}
    if address in entries:
        raise ValueError('Private recovery unexpectedly duplicates an original Ghidra entry')
    previous, following = int(value['previousEntry'], 0), int(value['nextOriginalEntry'], 0)
    if max(a for a in entries if a < address) != previous or min(a for a in entries if a > address) != following:
        raise ValueError('Private entry is not between the exact original neighbours')
    if entries[following]['mode'] != 'arm' or neighbour_end(entries[previous], raw, base) != address or end != following:
        raise ValueError('Private extent overlaps or fails to fill the independently bounded original gap')
    for function in entries.values():
        if any(int(a, 0) < end and address < int(z, 0) for a, z in function['ranges']):
            raise ValueError('Private entry overlaps an original Ghidra body')
    incoming = value['incoming']
    if (incoming['program'], incoming['processor'], incoming['module'], incoming['mode']) != (
            utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-wram', 'arm'):
        raise ValueError('Original incoming pointer namespace differs')
    caller, wram_base = int(incoming['address'], 0), 0x037f8000
    original_caller = wram[caller - wram_base:caller - wram_base + incoming['bytes']]
    if utility_runtime.sha(original_caller) != incoming['targetSha256']:
        raise ValueError('Original complete pointer-owning caller differs')
    pointer = int(incoming['pointer'], 0)
    if int.from_bytes(wram[pointer - wram_base:pointer - wram_base + 4], 'little') != address:
        raise ValueError('Original incoming callback pointer or ARM tag differs')
    for use in incoming['uses']:
        at = int(use['address'], 0)
        payload = wram[at - wram_base:at - wram_base + 8]
        if payload.hex() != use['load'] + use['store']:
            raise ValueError('Original callback pointer load/store witness differs')
        instructions = list(decoder().disasm(payload, at))
        load, store = instructions
        mem = load.operands[-1]
        if load.mnemonic != 'ldr' or mem.type != ARM_OP_MEM or mem.mem.base != ARM_REG_PC or at + 8 + mem.mem.disp != pointer:
            raise ValueError('Incoming witness does not read the original callback literal')
        if store.mnemonic != 'str' or load.operands[0].reg != store.operands[0].reg:
            raise ValueError('Incoming witness does not store the loaded callback pointer')
    code_end = address + value['codeBytes']
    instructions = list(decoder().disasm(native[:value['codeBytes']], address))
    by_address = {i.address: i for i in instructions}
    if sum(i.size for i in instructions) != value['codeBytes']:
        raise ValueError('Private callback code is not completely decoded')
    pending, reached, returns, edges, pools = [address], set(), [], [], {}
    while pending:
        at = pending.pop()
        if at in reached:
            continue
        if at not in by_address:
            raise ValueError('Original CFG enters a literal or an interior instruction')
        reached.add(at)
        instruction = by_address[at]
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                target = at + 8 + operand.mem.disp
                if target % 4 or not code_end <= target <= end - 4:
                    raise ValueError('Callback literal reference escapes its exact suffix')
                pools[target] = int.from_bytes(raw[target - base:target - base + 4], 'little')
        if instruction.mnemonic == 'bx' and instruction.operands[0].type == ARM_OP_REG and instruction.operands[0].reg == ARM_REG_LR:
            returns.append(at)
            successors = [] if instruction.cc == ARM_CC_AL else [at + 4]
        elif instruction.id == ARM_INS_B:
            if instruction.operands[0].type != ARM_OP_IMM:
                raise ValueError('Callback CFG branch is indirect')
            successors = [instruction.operands[0].imm]
            if instruction.cc != ARM_CC_AL:
                successors.append(at + 4)
        else:
            if ARM_REG_PC in instruction.regs_access()[1]:
                raise ValueError('Callback CFG contains an unqualified PC write')
            successors = [at + 4]
        for target in successors:
            if target not in by_address:
                raise ValueError('Callback CFG escapes the proven code range')
            edges.append([hex(at), hex(target)])
            pending.append(target)
    if reached != set(by_address) or returns != [code_end - 4] or set(pools) != {code_end, code_end + 4}:
        raise ValueError('Callback CFG or two-word literal suffix is incomplete')
    return dict(spec=spec, previousOriginalConfiguredEnd=hex(address), nextOriginalEntry=hex(end),
                reachableInstructionCount=len(reached), originalCfgEdges=edges, originalReturns=[hex(a) for a in returns],
                literalWords=[dict(address=hex(a), value=hex(v)) for a, v in sorted(pools.items())],
                incomingPointer=hex(pointer), originalIncomingLoadStorePairs=len(incoming['uses']),
                canonicalGhidraUnchanged=True, sourceCredit=0, actualNativeFunctionReturns=0)


def inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Frozen private boundary manifest changed')
    value = read_json(INPUT)
    pins = [value['inventory'], *value['images'], dict(path=value['source'], sha256=value['sourceSha256']),
            *value['sourceDependencies'], dict(path=value['compiler'], sha256=value['compilerSha256'])]
    for pin in pins:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen private boundary source, inventory, image or compiler changed')
    inventory = read_json(ROOT / value['inventory']['path'])
    if (inventory['program'], inventory['processor']) != (utility_runtime.PROGRAM, 'arm7'):
        raise ValueError('Original callback inventory namespace changed')
    raw, wram = [(ROOT / pin['path']).read_bytes() for pin in value['images']]
    return value, raw, wram, inventory


@lru_cache(maxsize=1)
def qualified():
    value, raw, wram, inventory = inputs()
    proof = validate_native(value, raw, wram, inventory)
    spec = dict(value['spec'], address=int(value['spec']['address'], 0), compilerPath=ROOT / value['compiler'], compilerProc='arm7tdmi')
    flags = value['compilerFlags']
    previous_work = utility_code.WORK
    utility_code.WORK = ROOT / 'work/wl1104cb/boundary-replay'
    try:
        row, code = utility_code.compile_compare(ROOT / value['source'], spec, flags[0][2:], flags[flags.index('-inline') + 1], 'speed' in flags)
    finally:
        utility_code.WORK = previous_work
    if code is None or row['compilerFlags'] != flags or row['relocations']:
        raise ValueError('Independent ordinary callback C no longer matches all116 original bytes without relocations')
    proof.update(independentSourceCompile=row, sourceOnlyCompilerInput=True, originalObjectsAreCompilerInputs=False,
                 privateEntryQualified=True, originalInventoryExtended=False, actualCallbackExecutions=0)
    write_json(LANE / 'private-native-entry.json', dict(schemaVersion=1, program=spec['program'], processor='arm7',
               entry=proof, initializedFunctionBytes=116, codeBytes=108, literalBytes=8, functionCredit=0, sourceCredit=0))
    return proof


def candidate():
    proof = qualified()
    spec = dict(proof['spec'], address=int(proof['spec']['address'], 0))
    raw = (ROOT / spec['binary']).read_bytes()
    address, base = spec['address'], spec['base']
    spec['instructions'] = list(decoder().disasm(raw[address - base:address - base + 108], address))
    spec['pools'] = {int(r['address'], 0): int(r['value'], 0) for r in proof['literalWords']}
    return spec


def mandatory_inputs():
    value = read_json(INPUT)
    return [dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA), value['inventory'], *value['images'],
            dict(path=value['source'], sha256=value['sourceSha256']), *value['sourceDependencies'],
            dict(path=value['compiler'], sha256=value['compilerSha256']), dict(path='project.json', sha256=sha256(ROOT / 'project.json'))]


def main():
    proof = qualified()
    original, raw, wram, inventory = inputs()
    controls = []
    variants = [('interior-address', 'address', hex(int(original['spec']['address'], 0) + 4)),
                ('later-interior-address', 'address', hex(int(original['spec']['address'], 0) + 100)),
                ('wrong-mode', 'mode', 'thumb'), ('wrong-cpu', 'processor', 'arm9'),
                ('wrong-program', 'program', ''), ('overlap-next-boundary', 'bytes', 120),
                ('truncate-boundary', 'bytes', 112)]
    for label, field, wrong in variants:
        value = copy.deepcopy(original)
        value['spec'][field] = wrong
        try:
            validate_native(value, raw, wram, inventory)
        except (ValueError, KeyError):
            controls.append(dict(name=label, rejected=True))
        else:
            raise ValueError('Invalid private boundary accepted: ' + label)
    changed = bytearray(raw)
    changed[int(original['spec']['address'], 0) - original['spec']['base']] ^= 1
    try:
        validate_native(original, bytes(changed), wram, inventory)
    except ValueError:
        controls.append(dict(name='changed-original-native-body', rejected=True))
    else:
        raise ValueError('Changed original callback body accepted')
    changed = bytearray(wram)
    changed[int(original['incoming']['pointer'], 0) - 0x037f8000] ^= 1
    try:
        validate_native(original, raw, bytes(changed), inventory)
    except ValueError:
        controls.append(dict(name='changed-original-incoming-pointer', rejected=True))
    else:
        raise ValueError('Changed original incoming pointer accepted')
    write_json(LANE / 'boundary-controls.json', dict(status='passed', controls=controls, proof=proof,
               sourceCredit=0, actualCallbackExecutions=0, originalGhidraChanged=False))
    print(dict(privateEntryQualified=True, originalCfgInstructions=proof['reachableInstructionCount'],
               originalIncomingPointerUses=proof['originalIncomingLoadStorePairs'], negativeControls=len(controls), executionCredit=0))


if __name__ == '__main__':
    main()
