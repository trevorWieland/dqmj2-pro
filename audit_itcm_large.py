import json
import re
import struct
from collections import deque
from pathlib import Path
import match_lowlevel as common
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG, ARM_REG_PC, ARM_REG_LR, ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_INS_CMP

ROOT = Path(__file__).resolve().parent
TARGETS = [0x01FFCD84, 0x01FF97E0, 0x01FFC890, 0x01FFBBCC]
BASE = 0x01FF8000
PIN = '69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb'


def merged(addresses):
    result = []
    for address in sorted(addresses):
        if result and result[-1][1] == address:
            result[-1][1] += 4
        else:
            result.append([address, address + 4])
    return [{'start': hex(first), 'end': hex(last), 'bytes': last - first} for first, last in result]


def analyze(binary, start, size, entries):
    end = start + size
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    def instruction(address):
        if address % 4 or not start <= address <= end - 4:
            return None
        return next(decoder.disasm(binary[address - BASE:address - BASE + 4], address), None)
    pending = deque([start])
    visited, pools, switches, calls, edges, unresolved = set(), {}, [], [], [], []
    def edge(source, destination, kind):
        edges.append({'from': hex(source), 'to': hex(destination), 'kind': kind})
        if start <= destination < end:
            pending.append(destination)
        else:
            unresolved.append({'address': hex(source), 'target': hex(destination), 'kind': kind,
                               'knownConfiguredEntry': destination in entries})
    while pending:
        address = pending.popleft()
        if address in visited:
            continue
        current = instruction(address)
        if current is None:
            unresolved.append({'address': hex(address), 'kind': 'undecoded-or-unaligned-target'})
            continue
        visited.add(address)
        value = struct.unpack_from('<I', binary, address - BASE)[0]
        conditional = value >> 28 not in (14, 15)
        for operand in current.operands:
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC and not operand.mem.index:
                target = address + 8 + operand.mem.disp
                width = 8 if current.mnemonic.startswith('ldrd') else 4
                for slot in range(target, target + width, 4):
                    if start <= slot <= end - 4 and slot % 4 == 0:
                        pools.setdefault(slot, set()).add(address)
        if current.id in (ARM_INS_BL, ARM_INS_BLX):
            target = current.operands[0].imm & 0xffffffff if current.operands and current.operands[0].type == ARM_OP_IMM else None
            calls.append({'address': hex(address), 'target': hex(target) if target is not None else None,
                          'kind': current.mnemonic, 'internal': target is not None and start <= (target & ~1) < end})
            if target is not None and start <= target < end:
                pending.append(target)
            edge(address, address + 4, 'call-return')
            continue
        if current.id == ARM_INS_B:
            if current.operands and current.operands[0].type == ARM_OP_IMM:
                edge(address, current.operands[0].imm & 0xffffffff, 'branch')
            else:
                unresolved.append({'address': hex(address), 'kind': 'non-immediate-branch'})
            if conditional:
                edge(address, address + 4, 'conditional-fallthrough')
            continue
        if current.id == ARM_INS_BX:
            if current.operands[0].type != ARM_OP_REG or current.operands[0].reg != ARM_REG_LR:
                unresolved.append({'address': hex(address), 'kind': 'indirect-tail-transfer', 'operand': current.op_str})
            if conditional:
                edge(address, address + 4, 'conditional-fallthrough')
            continue
        writes_pc = ARM_REG_PC in current.regs_access()[1]
        if writes_pc and current.mnemonic.startswith('add') and len(current.operands) == 3 and current.operands[0].reg == ARM_REG_PC and current.operands[1].reg == ARM_REG_PC:
            selector = current.operands[2]
            maximum = None
            for prior_address in range(address - 4, max(start - 4, address - 36), -4):
                prior = instruction(prior_address)
                if prior is None:
                    break
                if prior.id == ARM_INS_CMP and len(prior.operands) == 2 and prior.operands[0].type == ARM_OP_REG and prior.operands[0].reg == selector.reg and prior.operands[1].type == ARM_OP_IMM:
                    maximum = prior.operands[1].imm
                    break
                if prior.update_flags:
                    break
            table = address + 8
            targets = [instruction(table + index * 4) for index in range(maximum + 1)] if maximum is not None and 0 <= maximum <= 256 else []
            if selector.type == ARM_OP_REG and selector.shift.value == 2 and targets and all(item is not None and item.id == ARM_INS_B for item in targets):
                switches.append({'address': hex(address), 'table': hex(table), 'maximum': maximum,
                                 'bytes': len(targets) * 4, 'tableKind': 'ARM-branch-instructions'})
                for item in targets:
                    edge(address, item.address, 'bounded-switch-entry')
                if conditional:
                    edge(address, address + 4, 'switch-default')
                continue
            unresolved.append({'address': hex(address), 'kind': 'unresolved-pc-add-switch', 'operand': current.op_str})
            if conditional:
                edge(address, address + 4, 'conditional-fallthrough')
            continue
        if writes_pc:
            returns = current.mnemonic.startswith(('pop', 'ldm')) or current.mnemonic.startswith('mov') and current.operands[-1].type == ARM_OP_REG and current.operands[-1].reg == ARM_REG_LR
            if not returns:
                unresolved.append({'address': hex(address), 'kind': 'other-pc-write', 'instruction': current.mnemonic + ' ' + current.op_str})
            if conditional:
                edge(address, address + 4, 'conditional-fallthrough')
            continue
        if address + 4 < end:
            edge(address, address + 4, 'fallthrough')
        else:
            unresolved.append({'address': hex(address), 'kind': 'falls-through-configured-end'})
    data = set(pools)
    words = set(range(start, end, 4))
    unknown = words - visited - data
    collisions = sorted(visited & data)
    literals = []
    for address, consumers in sorted(pools.items()):
        value = struct.unpack_from('<I', binary, address - BASE)[0]
        literals.append({'address': hex(address), 'value': hex(value), 'consumers': [hex(item) for item in sorted(consumers)],
                         'interiorPointerCandidate': start <= (value & ~1) < end})
    payload = binary[start - BASE:end - BASE]
    return {'module': 'itcm', 'processor': 'arm9', 'mode': 'arm', 'address': hex(start), 'bytes': size,
            'end': hex(end), 'sha256': common.sha(payload), 'configuredInteriorEntries': [hex(value) for value in sorted(entries) if start < value < end],
            'reachableInstructionBytes': len(visited) * 4, 'referencedLiteralBytes': len(data) * 4, 'unclassifiedBytes': len(unknown) * 4,
            'reachableRanges': merged(visited), 'referencedLiteralRanges': merged(data), 'unclassifiedRanges': merged(unknown),
            'codeLiteralCollisions': [hex(value) for value in collisions], 'switches': switches, 'calls': calls, 'literals': literals,
            'unresolvedTransfers': unresolved, 'trailingWord': hex(struct.unpack_from('<I', payload, len(payload) - 4)[0]),
            'cfgComplete': not unresolved and not collisions and not unknown,
            'boundaryEvidence': 'Pinned dsd configured extent checked against bounded native ARM entry reachability, direct branches, returns and validated branch-table switches',
            'ordinaryFunctionCredit': 0, 'sourceReconstructionComplete': False}


def main():
    binary_path = ROOT / 'extract/arm9/itcm.bin'
    binary = binary_path.read_bytes()
    if common.sha(binary) != PIN:
        raise ValueError('Native ITCM input module changed')
    config = ROOT / 'config/arm9/itcm/symbols.txt'
    functions = {int(address, 0): int(size, 0) for size, address in re.findall(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', config.read_text())}
    records = [analyze(binary, address, functions[address], set(functions)) for address in TARGETS]
    report = {'schemaVersion': 1, 'romSha256': common.sha((ROOT / 'inputs/game.nds').read_bytes()), 'module': 'itcm', 'processor': 'arm9',
              'binary': binary_path.relative_to(ROOT).as_posix(), 'inputModuleSha256': PIN,
              'configuration': config.relative_to(ROOT).as_posix(), 'configurationSha256': common.sha(config.read_bytes()),
              'functions': records, 'sourceReconstructionComplete': False,
              'limitations': ['Native reachability establishes measured control/data evidence, not recovered source or new function credit',
                              'Unreached words and unresolved indirect transfers remain explicit; executable-looking data does not create entries',
                              'Configured extents remain hypotheses wherever reachability or literals conflict, and original inputs/configurations are not mutated']}
    output = ROOT / 'evidence/itcm/large-boundaries.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    for record in records:
        print({key: record[key] for key in ('address', 'bytes', 'reachableInstructionBytes', 'referencedLiteralBytes', 'unclassifiedBytes', 'cfgComplete')})


if __name__ == '__main__':
    main()
