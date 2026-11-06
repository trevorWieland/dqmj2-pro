import json
import struct
from collections import deque
import utility_code
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_OP_IMM, ARM_OP_REG, ARM_OP_MEM
from utility_abi import argument_hints
from wave20261102_child_third_prepare import ROOT, LANE
from project import write_json, sha256


def inventories():
    layout, files = utility_runtime.derive()
    modules = {m['id']: m for m in layout['modules']}
    specs = {'arm9': {}, 'arm7': {}}
    for cpu in specs:
        path = ROOT / ('evidence/utility/ghidra-' + cpu + '.json')
        inventory = json.loads(path.read_text())
        for function in inventory['functions']:
            if function['mode'] not in ('arm', 'thumb') or function['module'] not in modules:
                continue
            module = modules[function['module']]
            base, address = int(module['base'], 0), int(function['address'], 0)
            binary = bytes(files[ROOT / module['binary']])
            decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if function['mode'] == 'thumb' else CS_MODE_ARM)
            decoder.detail = True
            instructions, ranges = [], []
            valid = True
            for first, end in function['ranges']:
                first, end = int(first, 0), int(end, 0)
                if not base <= first < end <= base + len(binary):
                    valid = False
                    break
                payload = binary[first - base:end - base]
                decoded = list(decoder.disasm(payload, first))
                if sum(i.size for i in decoded) != len(payload):
                    valid = False
                    break
                instructions.extend(decoded)
                ranges.append(dict(start=hex(first), endExclusive=hex(end), bytes=len(payload), sha256=utility_runtime.sha(payload)))
            if not valid or not instructions or instructions[0].address != address:
                continue
            specs[cpu][address] = dict(address=address, processor=cpu, program=utility_runtime.PROGRAM,
                module=function['module'], mode=function['mode'], instructions=instructions, ranges=ranges,
                inputModuleSha256=module['sha256'], inventory=path.relative_to(ROOT).as_posix(),
                binary=module['binary'], base=base,
                inventorySha256=sha256(path), fullFunctionBoundaryProved=False)
    return specs


def join(left, right):
    if left is None:
        return right
    sp = left[0] if left[0] == right[0] else None
    aliases = tuple(a if a == b else None for a, b in zip(left[1], right[1]))
    taint = left[3] | right[3]
    for index, (a, b) in enumerate(zip(left[1], right[1])):
        if a != b and (a is not None or b is not None):
            taint |= 1 << index
    guards = tuple((0x7ffe if left[2] & 1 << i else left[4][i]) &
                   (0x7ffe if right[2] & 1 << i else right[4][i]) for i in range(4))
    return sp, aliases, left[2] & right[2], taint, guards


def analyze(spec):
    instructions = {i.address: i for i in spec['instructions']}
    entry = spec['address']
    states = {entry: (0, (None,) * 13, 0, 0, (0,) * 4)}
    pending = deque([entry])
    def number(instruction, reg):
        name = instruction.reg_name(reg)
        return 12 if name == 'ip' else int(name[1:]) if name.startswith('r') and name[1:].isdigit() and int(name[1:]) <= 12 else None
    def transfer(instruction, state):
        sp, old, definitions, taint, old_guards = state
        guards = list(old_guards)
        aliases = list(old)
        operands = instruction.operands
        unconditional = instruction.cc in (0, 15)
        reads, writes = instruction.regs_access()
        for register in writes:
            index = number(instruction, register)
            if index is not None:
                aliases[index] = None
                taint &= ~(1 << index)
                if index < 4 and unconditional:
                    definitions |= 1 << index
                    guards[index] = 0
                elif index < 4:
                    guards[index] |= 1 << instruction.cc
                    inverse = ((instruction.cc - 1) ^ 1) + 1
                    if guards[index] & 1 << inverse:
                        definitions |= 1 << index
                        guards[index] = 0
        def value(operand):
            if operand.type != ARM_OP_REG:
                return None, False
            name = instruction.reg_name(operand.reg)
            if name == 'sp':
                return sp, sp is None
            index = number(instruction, operand.reg)
            return (old[index], bool(state[3] & 1 << index)) if index is not None else (None, False)
        name = instruction.mnemonic
        saved = name.startswith('push') or name.startswith('stmdb') and instruction.op_str.startswith('sp!')
        restored = name.startswith('pop') or name.startswith('ldm') and instruction.op_str.startswith('sp!')
        if saved or restored:
            count = sum(o.type == ARM_OP_REG for o in operands) - int(instruction.op_str.startswith('sp!'))
            sp = sp + count * 4 * (1 if restored else -1) if sp is not None and unconditional else None
        elif operands and operands[0].type == ARM_OP_REG:
            destination = instruction.reg_name(operands[0].reg)
            candidate, uncertain = None, False
            if name in ('mov', 'movs') and len(operands) == 2:
                candidate, uncertain = value(operands[1])
            elif name in ('add', 'adds', 'sub', 'subs'):
                source = operands[1] if len(operands) >= 3 else operands[0]
                immediate = operands[-1]
                origin, uncertain = value(source)
                if immediate.type == ARM_OP_IMM and origin is not None:
                    candidate = origin + immediate.imm * (-1 if name.startswith('sub') else 1)
            if destination == 'sp':
                sp = candidate if unconditional else None
            else:
                index = number(instruction, operands[0].reg)
                if index is not None and (candidate is not None or uncertain):
                    aliases[index] = candidate if unconditional else None
                    if uncertain or not unconditional:
                        taint |= 1 << index
        if instruction.group(CS_GRP_CALL):
            for index in range(4):
                aliases[index] = None
                taint &= ~(1 << index)
            if unconditional:
                definitions |= 15
        if instruction.update_flags or instruction.group(CS_GRP_CALL) or any(instruction.reg_name(r) == 'cpsr' for r in writes):
            guards = [0] * 4
        return sp, tuple(aliases), definitions, taint, tuple(guards)
    def successors(instruction):
        following = instruction.address + instruction.size
        if instruction.group(CS_GRP_CALL):
            return [following] if following in instructions else []
        if instruction.group(CS_GRP_JUMP):
            target = instruction.operands[0].imm & ~1 if instruction.operands and instruction.operands[0].type == ARM_OP_IMM else None
            result = [target] if target in instructions else []
            if instruction.cc not in (0, 15) and following in instructions:
                result.append(following)
            return result
        if instruction.mnemonic.startswith('pop') and any(instruction.reg_name(o.reg) == 'pc' for o in instruction.operands if o.type == ARM_OP_REG):
            return []
        if instruction.mnemonic.startswith('ldm') and 'pc' in instruction.op_str:
            return []
        return [following] if following in instructions else []
    iterations = 0
    while pending:
        address = pending.popleft()
        instruction = instructions[address]
        output = transfer(instruction, states[address])
        for target in successors(instruction):
            updated = join(states.get(target), output)
            if states.get(target) != updated:
                states[target] = updated
                pending.append(target)
        iterations += 1
        if iterations > 100000:
            raise ValueError('CFG/SP analysis did not converge')
    stack, unknown, local_mask, calls, returns, unknown_flow = [], [], 0, [], [], []
    for address, state in sorted(states.items()):
        instruction = instructions[address]
        sp, aliases, definitions, taint, guards = state
        effective_definitions = definitions
        if instruction.cc not in (0, 15):
            effective_definitions |= sum(1 << i for i in range(4) if guards[i] & 1 << instruction.cc)
        operands = instruction.operands
        reads, unused = instruction.regs_access()
        saved = instruction.mnemonic.startswith('push') or instruction.mnemonic.startswith('stmdb') and instruction.op_str.startswith('sp!')
        if not saved:
            for register in reads:
                index = number(instruction, register)
                if index is not None and index < 4 and not effective_definitions & 1 << index:
                    local_mask |= 1 << index
        if instruction.mnemonic.startswith('ldr'):
            for operand in operands:
                if operand.type != ARM_OP_MEM or operand.mem.index:
                    continue
                name = instruction.reg_name(operand.mem.base)
                index = number(instruction, operand.mem.base)
                origin = sp if name == 'sp' else aliases[index] if index is not None else None
                uncertain = name == 'sp' and sp is None or index is not None and taint & 1 << index
                if uncertain:
                    unknown.append(hex(address))
                if origin is not None and origin + operand.mem.disp >= 0:
                    offset = origin + operand.mem.disp
                    stack.append(dict(instruction=hex(address), entrySpOffset=offset, argumentSlot=4 + offset // 4))
        call = instruction.group(CS_GRP_CALL)
        branch = instruction.group(CS_GRP_JUMP) and operands and operands[0].type == ARM_OP_IMM and (operands[0].imm & ~1) not in instructions
        if call or branch:
            target = operands[0].imm & ~1 if operands and operands[0].type == ARM_OP_IMM else None
            calls.append((target, effective_definitions))
        if not successors(instruction):
            indirect = instruction.group(CS_GRP_JUMP) and not (operands and operands[0].type == ARM_OP_IMM)
            previous = instructions.get(address - 2)
            returned = instruction.mnemonic == 'bx' and operands and (
                instruction.reg_name(operands[0].reg) == 'lr' or previous is not None and previous.mnemonic == 'pop'
                and previous.op_str.strip('{}') == instruction.op_str)
            if indirect and not returned:
                unknown_flow.append(hex(address))
            else:
                returns.append(transfer(instruction, state)[0])
    ambiguous = [hex(a) for a, s in states.items() if s[0] is None]
    words = None if unknown or ambiguous or unknown_flow else max((e['argumentSlot'] - 3 for e in stack), default=0)
    return dict(localMask=local_mask, calls=calls, stackWords=words, stackReads=stack,
        unknownStackReads=unknown, unresolvedSpStates=ambiguous, returnSpDeltas=returns,
        unresolvedIndirectControlFlow=unknown_flow,
        reachableInstructions=len(states), totalInstructions=len(instructions))


def derive():
    specs = inventories()
    profiles, analyses = {}, {}
    for cpu, functions in specs.items():
        results = {address: analyze(spec) for address, spec in functions.items()}
        masks = {address: result['localMask'] for address, result in results.items()}
        for unused in range(32):
            updated = {address: result['localMask'] for address, result in results.items()}
            for address, result in results.items():
                for target, definitions in result['calls']:
                    updated[address] |= masks.get(target, 15) & ~definitions
            if updated == masks:
                break
            masks = updated
        unresolved = {a for a, r in results.items() if r['stackWords'] is None or
                      any(target is None and 15 & ~defined for target, defined in r['calls'])}
        for unused in range(32):
            more = {a for a, r in results.items() if any(target in unresolved and 15 & ~defined for target, defined in r['calls'])}
            if more <= unresolved:
                break
            unresolved |= more
        profiles[cpu] = {address: max(masks[address].bit_length(), 4 + result['stackWords'] if result['stackWords'] else 0)
                         for address, result in results.items() if address not in unresolved}
        for address, result in results.items():
            result['argumentContextUnresolved'] = address in unresolved
            result['minimumDirectRegisterWords'] = result['localMask'].bit_length()
        analyses[cpu] = results
    return specs, profiles, analyses


def controls():
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    decoder.detail = True
    multiple = list(decoder.disasm(bytes.fromhex('10b5002802d110bc08bc1847029810bc08bc1847'), 0x1000))
    ambiguous = list(decoder.disasm(bytes.fromhex('002800d081b000997047'), 0x2000))
    unreachable = list(decoder.disasm(bytes.fromhex('70473f98'), 0x3000))
    results = [analyze(dict(address=0x1000, instructions=multiple)),
               analyze(dict(address=0x2000, instructions=ambiguous)),
               analyze(dict(address=0x3000, instructions=unreachable))]
    if results[0]['stackWords'] != 1 or results[0]['returnSpDeltas'] != [0, 0]:
        raise ValueError('Multiple-return negative control failed')
    if results[1]['stackWords'] is not None or not results[1]['unresolvedSpStates']:
        raise ValueError('Unresolved-join negative control failed')
    if results[2]['stackWords'] != 0 or results[2]['reachableInstructions'] != 1:
        raise ValueError('Unreachable-read negative control failed')
    return dict(multipleReturns=results[0], unresolvedJoin=results[1], unreachableStackRead=results[2],
                sourceCredit=0, functionCredit=0, behavioralExecutionCredit=0)


def main():
    tested = controls()
    specs, profiles, analyses = derive()
    conditional = specs['arm9'][0x0200ab2c]
    modified = bytearray(b''.join(i.bytes for i in conditional['instructions']))
    load = next(i for i in conditional['instructions'] if i.mnemonic.startswith('ldrh'))
    offset = load.address - conditional['address']
    word = int.from_bytes(modified[offset:offset + 4], 'little')
    modified[offset:offset + 4] = ((word & 0x0fffffff) | (10 << 28)).to_bytes(4, 'little')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    inverted = analyze(dict(address=conditional['address'], instructions=list(decoder.disasm(bytes(modified), conditional['address']))))
    if profiles['arm9'].get(0x0200ab2c) != 3 or inverted['localMask'] != 15:
        raise ValueError('ARM predicated-definition negative control failed')
    tested['predicatedLoadStore'] = dict(nativeAddress='0x0200ab2c', baselineArgumentWords=3,
        invertedLoadRequiresFourthRegister=True, syntheticMutationOnly=True, sourceCredit=0)
    selected = {cpu: {hex(a): dict(argumentWords=profiles[cpu].get(a), **r,
        module=specs[cpu][a]['module'], mode=specs[cpu][a]['mode'],
        inputModuleSha256=specs[cpu][a]['inputModuleSha256'], ranges=specs[cpu][a]['ranges']) for a, r in rows.items()}
                for cpu, rows in analyses.items()}
    report = dict(schemaVersion=1, generator=__file__, generatorSha256=sha256(__file__),
        program=utility_runtime.PROGRAM, romSha256=utility_runtime.audit_regions.ROM_HASH,
        argumentProfiles={cpu: {hex(a): count for a, count in rows.items()} for cpu, rows in profiles.items()},
        analyses=selected, negativeControls=tested, sourceHypothesesOnly=True,
        canonicalInventoryChanged=False, sourceCredit=0, functionCredit=0,
        limitations=['CFG/SP and callee demands generate provisional source context; exact caller compilation/linking remains mandatory',
                    'Unresolved SP joins are retained and do not receive invented argument counts',
                    'Discontiguous native entries gain no reconstructed callee source or function credit'])
    write_json(LANE / 'cfg-abi-context.json', report)
    print({hex(a): profiles['arm9'].get(a) for a in [0x0200ba04, 0x0200e2c8]})


if __name__ == '__main__':
    main()
