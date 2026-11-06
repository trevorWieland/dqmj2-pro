import hashlib
import json
from pathlib import Path
import arm7_runtime
import match_runtime
import link_arm7_bulk_20261030 as linker
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC
from project import write_json

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT / 'evidence/attempts/arm7-seq-main-layout-20261030.json'
PRIOR_SHA = '22b69194749a7a6caa9fef28d38a6bb2d044065e48ea4a24dd17416f6ddf9884'
START, CODE_END, END = 0x037FFF54, 0x038000AC, 0x038000B4


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if digest(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Frozen original loader/gap evidence differs')
    prior = json.loads(PRIOR.read_text())
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    for name, raw in binaries.items():
        if digest(raw) != modules[name]['sha256']:
            raise ValueError('Measured ARM7 module differs during consumer audit')
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    if digest(inventory_path.read_bytes()) != prior['inventorySha256']:
        raise ValueError('Inventory changed before discontiguous consumer audit')
    inventory = json.loads(inventory_path.read_text())
    functions = inventory['functions']
    own = next(row for row in functions if row['module'] == 'arm7-wram' and int(row['address'], 0) == START)
    conflicts, outside_flows, data_reads = [], [], []
    for function in functions:
        mode, module_name = function.get('mode'), function['module']
        if mode not in ('arm', 'thumb'):
            continue
        raw, base = binaries[module_name], int(modules[module_name]['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            if function is not own and module_name == 'arm7-wram' and first < END and START < last:
                conflicts.append({'function': function['address'], 'mode': mode, 'overlap': [hex(max(first, START)), hex(min(last, END))]})
            for instruction in decoder.disasm(raw[first - base:last - base], first):
                if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands and instruction.operands[0].type == 2:
                    target = instruction.operands[0].imm & ~1
                    if START <= target < END and not (module_name == 'arm7-wram' and START <= instruction.address < CODE_END):
                        outside_flows.append({'module': module_name, 'function': function['address'], 'mode': mode,
                            'pc': hex(instruction.address), 'operation': instruction.mnemonic, 'target': hex(target),
                            'interiorOrPool': target != START})
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        pc_base = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        target = pc_base + operand.mem.disp
                        if START <= target < END:
                            data_reads.append({'module': module_name, 'function': function['address'], 'mode': mode,
                                'pc': hex(instruction.address), 'storage': hex(target),
                                'inProposedPool': CODE_END <= target <= END - 4, 'outsideProposedFunction': not START <= instruction.address < CODE_END})
    words = []
    for name, raw in binaries.items():
        base = int(modules[name]['base'], 0)
        for offset in range(0, len(raw) - 3, 4):
            value = int.from_bytes(raw[offset:offset + 4], 'little')
            if START <= (value & ~1) < END:
                words.append({'module': name, 'storage': hex(base + offset), 'word': hex(value),
                    'target': hex(value & ~1), 'taggedMode': 'thumb' if value & 1 else 'arm', 'interiorOrPool': (value & ~1) != START})
    raw, base = binaries['arm7-wram'], int(modules['arm7-wram']['base'], 0)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = {row.address: row for row in decoder.disasm(raw[START - base:CODE_END - base], START)}
    for pc, instruction in instructions.items():
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                target = pc + 8 + operand.mem.disp
                if START <= target < END and not any(row['module'] == 'arm7-wram' and int(row['pc'], 0) == pc and int(row['storage'], 0) == target for row in data_reads):
                    data_reads.append({'module': 'arm7-wram', 'function': hex(START), 'mode': 'arm', 'pc': hex(pc),
                        'storage': hex(target), 'inProposedPool': CODE_END <= target <= END - 4,
                        'outsideProposedFunction': False, 'newlyDecodedExcludedBlockReference': True})
    data_reads.sort(key=lambda row: (row['module'], int(row['pc'], 0), int(row['storage'], 0)))
    module_map, qualified = linker.namespace('')
    edges, calls, exits = {}, [], []
    for pc, instruction in instructions.items():
        successors = []
        if instruction.group(CS_GRP_CALL):
            if instruction.operands[0].type != 2:
                raise ValueError('Proposed sequence-main code has an unqualified indirect call')
            target = instruction.operands[0].imm & ~1
            if target not in qualified or qualified[target]['mode'] != 'arm':
                raise ValueError('Proposed sequence-main call lacks measured ARM7 ARM entry identity')
            calls.append({'pc': hex(pc), 'target': qualified[target], 'calleeSourceCredit': 0})
            successors = [pc + 4]
        elif instruction.group(CS_GRP_JUMP):
            if instruction.mnemonic == 'bx' and instruction.op_str == 'lr':
                exits.append(hex(pc))
            elif instruction.operands[0].type == 2:
                target = instruction.operands[0].imm
                if target not in instructions:
                    raise ValueError('Proposed sequence-main has a branch outside reconciled code')
                successors = [target] + ([pc + 4] if instruction.mnemonic != 'b' else [])
            else:
                raise ValueError('Proposed sequence-main has unresolved indirect control flow')
        else:
            successors = [pc + 4]
        if any(value not in instructions for value in successors):
            raise ValueError('Proposed ordinary instruction falls through into pool/outside span')
        edges[pc] = successors
    pending, reachable = [START], set()
    while pending:
        pc = pending.pop()
        if pc not in reachable:
            reachable.add(pc)
            pending.extend(edges[pc])
    roots = [row for row in functions if row['module'] == 'arm7-wram' and START < int(row['address'], 0) < END]
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'romSha256': prior['romSha256'], 'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'mode': 'arm',
        'loaderOwnershipProof': {'path': PRIOR.relative_to(ROOT).as_posix(), 'sha256': PRIOR_SHA},
        'inventorySha256': prior['inventorySha256'], 'candidate': prior['candidate'], 'configuredOverlapConflicts': conflicts,
        'additionalConfiguredRootsInsideCodeOrPool': roots, 'outsideImmediateFlows': outside_flows,
        'outsideInteriorOrPoolFlows': [row for row in outside_flows if row['interiorOrPool']],
        'knownPcRelativeReadsIntoProposedSpan': data_reads, 'alignedInitializedWordsReferencingProposedSpan': words,
        'rawInteriorOrPoolWords': [row for row in words if row['interiorOrPool']], 'qualifiedOriginalCalls': calls,
        'conservativeCfg': {'instructionWords': len(instructions), 'entryReachableWords': len(reachable),
            'allDecodedInstructionsEntryReachable': len(reachable) == len(instructions),
            'returnInstructionPcs': exits, 'edges': {hex(pc): [hex(target) for target in successors] for pc, successors in edges.items()},
            'excludedBlockDirectEntryPc': '0x37ffff0', 'excludedBlockConditionalFallthroughPc': '0x37ffffc'},
        'migrationApproved': False, 'sharedFilesEdited': False, 'sourceOrFunctionReturnCredit': 0,
        'limitations': ['All configured ARM/Thumb ranges plus initialized aligned words were audited under the original host ARM7 namespace',
            'CFG reachability permits both conditional outcomes and assumes qualified calls can return; it is not complete native feasibility proof',
            'No absence of opaque/computed producer, live-in or global dual-use consumer is claimed',
            'The discontiguous case is not submitted to the existing contiguous-merge helper']}
    destination = ROOT / 'evidence/attempts/arm7-seq-main-consumers-20261030-v2.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'conflicts': len(conflicts), 'outsideInteriorFlows': len(report['outsideInteriorOrPoolFlows']),
        'interiorWords': len(report['rawInteriorOrPoolWords']), 'reachableInstructions': len(reachable), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
