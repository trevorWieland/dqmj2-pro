from collections import deque
import match_lowlevel
import utility_abi
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_INT
from capstone.arm import ARM_OP_IMM, ARM_OP_REG, ARM_OP_MEM
import capstone.arm as arm

REGISTERS = {f'r{index}': 1 << index for index in range(4)}


def predicate(condition, flags):
    n, z, c, v = bool(flags & 8), bool(flags & 4), bool(flags & 2), bool(flags & 1)
    values = {0: True, 1: z, 2: not z, 3: c, 4: not c, 5: n, 6: not n, 7: v, 8: not v,
        9: c and not z, 10: not c or z, 11: n == v, 12: n != v, 13: not z and n == v, 14: z or n != v, 15: True}
    if condition not in values:
        raise ValueError('Unknown ARM condition code')
    return values[condition]


def register_names(instruction, values):
    return {instruction.reg_name(value) for value in values}


def access_names(instruction):
    reads, writes = instruction.regs_access()
    read_names, write_names = register_names(instruction, reads), register_names(instruction, writes)
    operands, mnemonic = instruction.operands, instruction.mnemonic
    if mnemonic.startswith(('stm', 'push')):
        registers = [instruction.reg_name(value.reg) for value in operands if value.type == ARM_OP_REG]
        listed = registers if mnemonic.startswith('push') else registers[1:]
        read_names.update(listed)
        write_names.difference_update(listed)
        base = 'sp' if mnemonic.startswith('push') else registers[0]
        read_names.add(base)
        if instruction.writeback or mnemonic.startswith('push'):
            write_names.add(base)
    elif mnemonic.startswith(('ldm', 'pop')):
        registers = [instruction.reg_name(value.reg) for value in operands if value.type == ARM_OP_REG]
        listed = registers if mnemonic.startswith('pop') else registers[1:]
        read_names.difference_update(listed)
        write_names.update(listed)
        base = 'sp' if mnemonic.startswith('pop') else registers[0]
        read_names.add(base)
        if instruction.writeback or mnemonic.startswith('pop'):
            write_names.add(base)
    elif mnemonic.startswith('str') and operands and operands[0].type == ARM_OP_REG:
        read_names.add(instruction.reg_name(operands[0].reg))
    for operand in operands:
        if operand.type == ARM_OP_MEM:
            if operand.mem.base:
                read_names.add(instruction.reg_name(operand.mem.base))
                if instruction.writeback:
                    write_names.add(instruction.reg_name(operand.mem.base))
            if operand.mem.index:
                read_names.add(instruction.reg_name(operand.mem.index))
    return read_names, write_names


def condition_flags(condition):
    return {0: 0, 1: 4, 2: 4, 3: 2, 4: 2, 5: 8, 6: 8, 7: 1, 8: 1,
        9: 6, 10: 6, 11: 9, 12: 9, 13: 13, 14: 13, 15: 0}[condition]


def flag_update(instruction, mode):
    full = {getattr(arm, 'ARM_INS_' + name) for name in ('CMP', 'CMN', 'ADD', 'ADC', 'SUB', 'SBC', 'RSB', 'RSC')}
    if instruction.id in full:
        return 15, 15
    logical = {getattr(arm, 'ARM_INS_' + name) for name in ('AND', 'ORR', 'EOR', 'BIC', 'MOV', 'MVN', 'TST', 'TEQ')}
    shifts = {getattr(arm, 'ARM_INS_' + name) for name in ('LSL', 'LSR', 'ASR', 'ROR', 'RRX')}
    if instruction.id in logical | shifts:
        may, must = 12, 12
        if instruction.id in shifts:
            may |= 2
            if instruction.id == arm.ARM_INS_RRX or instruction.operands[-1].type == ARM_OP_IMM and instruction.operands[-1].imm:
                must |= 2
        for operand in instruction.operands:
            if operand.shift.type:
                may |= 2
                if operand.shift.type in (arm.ARM_SFT_ASR, arm.ARM_SFT_LSL, arm.ARM_SFT_LSR, arm.ARM_SFT_ROR, arm.ARM_SFT_RRX) and (operand.shift.value or operand.shift.type == arm.ARM_SFT_RRX):
                    must |= 2
        if mode == 'arm' and instruction.size == 4:
            encoded = int.from_bytes(instruction.bytes, 'little')
            if encoded & (1 << 25) and (encoded >> 8) & 15:
                may |= 2
                must |= 2
        return may, must
    return 15, 12 if instruction.mnemonic.startswith(('mul', 'mla', 'umull', 'smull', 'umlal', 'smlal')) else 0


def conventional_return(instruction):
    operands = instruction.operands
    read_names, written = access_names(instruction)
    if instruction.mnemonic.startswith('bx') and operands and operands[0].type == ARM_OP_REG:
        return instruction.reg_name(operands[0].reg) == 'lr'
    if instruction.mnemonic.startswith('pop') or instruction.mnemonic.startswith('ldm') and instruction.op_str.startswith('sp!'):
        return 'pc' in written
    if instruction.mnemonic.startswith('mov') and len(operands) == 2 and all(value.type == ARM_OP_REG for value in operands):
        return instruction.reg_name(operands[0].reg) == 'pc' and instruction.reg_name(operands[1].reg) == 'lr'
    return False


def analyze(spec, callee_inputs=None, callee_outputs=None, return_live_mask=1, state_limit=100000):
    callee_inputs, callee_outputs = callee_inputs or {}, callee_outputs or {}
    instructions = {instruction.address: instruction for instruction in spec['instructions']}
    if spec['address'] not in instructions:
        raise ValueError('Explicit native entry has no decoded instruction')
    incoming, pending = {}, deque()
    needed, direct, return_passthrough, return_defined = 0, 0, 0, 15
    observations, unsafe, unknown_calls = set(), set(), set()
    returns, visits = set(), 0
    def enqueue(pc, flags, entry_flags, call_flags, defined):
        if pc not in instructions:
            unsafe.add('unresolved-flow-to-' + hex(pc))
            return
        key = pc, flags, entry_flags, call_flags
        merged = incoming[key] & defined if key in incoming else defined
        if key not in incoming or merged != incoming[key]:
            incoming[key] = merged
            pending.append(key)
    for flags in range(16):
        enqueue(spec['address'], flags, 15, 0, 0)
    while pending:
        key = pending.popleft()
        pc, flags, entry_flags, call_flags = key
        defined = incoming[key]
        instruction = instructions[pc]
        visits += 1
        if visits > state_limit:
            unsafe.add('state-budget-exhausted')
            break
        following = pc + instruction.size
        condition = instruction.cc
        conditional = condition not in (0, 15)
        flag_reads = condition_flags(condition)
        if entry_flags & flag_reads:
            observations.add(('entry-CPSR-read', pc, entry_flags & flag_reads))
        if call_flags & flag_reads:
            observations.add(('unqualified-call-CPSR-read', pc, call_flags & flag_reads))
        if not predicate(condition, flags):
            enqueue(following, flags, entry_flags, call_flags, defined)
            continue
        read_names, write_names = access_names(instruction)
        if instruction.mnemonic.startswith('mrs'):
            observations.add(('explicit-machine-state-read', pc, 15))
        carry = instruction.id in {getattr(arm, 'ARM_INS_' + name) for name in ('ADC', 'SBC', 'RSC', 'RRX')} or any(operand.shift.type == arm.ARM_SFT_RRX for operand in instruction.operands)
        if carry or 'cpsr' in read_names and not conditional and not instruction.mnemonic.startswith('mrs'):
            explicit_mask = 2 if carry else 15
            if entry_flags & explicit_mask:
                observations.add(('entry-CPSR-operand', pc, entry_flags & explicit_mask))
            if call_flags & explicit_mask:
                observations.add(('unqualified-call-CPSR-operand', pc, call_flags & explicit_mask))
        read_mask = sum(REGISTERS[name] for name in read_names & REGISTERS.keys())
        direct |= read_mask & ~defined
        needed |= read_mask & ~defined
        call = instruction.group(CS_GRP_CALL)
        immediate = instruction.operands[0].imm & ~1 if instruction.operands and instruction.operands[0].type == ARM_OP_IMM else None
        if call:
            mask = callee_inputs.get(immediate, 15)
            if immediate not in callee_inputs:
                unknown_calls.add(hex(immediate) if immediate is not None else 'indirect')
            needed |= mask & ~defined
            defined |= callee_outputs.get(immediate, 0)
            for next_flags in range(16):
                enqueue(following, next_flags, 0, 15, defined)
            continue
        if instruction.group(CS_GRP_INT):
            needed |= 15 & ~defined
            unsafe.add('unqualified-software-interrupt')
            for next_flags in range(16):
                enqueue(following, next_flags, 0, 15, defined)
            continue
        defined |= sum(REGISTERS[name] for name in write_names & REGISTERS.keys())
        if conventional_return(instruction):
            returns.add(pc)
            return_passthrough |= 15 & ~defined
            return_defined &= defined
            needed |= return_live_mask & ~defined
            continue
        if instruction.group(CS_GRP_JUMP) or 'pc' in write_names:
            if immediate in instructions:
                enqueue(immediate, flags, entry_flags, call_flags, defined)
            elif immediate in callee_inputs:
                needed |= callee_inputs[immediate] & ~defined
                exits_defined = defined | callee_outputs.get(immediate, 0)
                return_passthrough |= 15 & ~exits_defined
                return_defined &= exits_defined
                needed |= return_live_mask & ~exits_defined
                returns.add(pc)
            else:
                unsafe.add('unqualified-indirect-or-outside-branch')
            continue
        if instruction.update_flags or 'cpsr' in write_names or instruction.mnemonic.startswith('msr'):
            may, must = flag_update(instruction, spec['mode'])
            if instruction.mnemonic.startswith('msr'):
                observations.add(('explicit-machine-state-write', pc, 15))
            for next_flags in range(16):
                if not (next_flags ^ flags) & (15 & ~may):
                    enqueue(following, next_flags, entry_flags & ~must, call_flags & ~must, defined)
        else:
            enqueue(following, flags, entry_flags, call_flags, defined)
    if not returns:
        unsafe.add('no-qualified-return-path')
        return_defined = 0
    if unsafe:
        needed, return_defined = 15, 0
    stack_words, stack_evidence = utility_abi.incoming_stack_words(spec)
    unknown_stack = False
    for instruction in spec['instructions']:
        read_registers, written_registers = instruction.regs_access()
        names = register_names(instruction, written_registers)
        if any(operand.type == ARM_OP_MEM and instruction.reg_name(operand.mem.base) == 'sp' and operand.mem.index for operand in instruction.operands):
            unknown_stack = True
        if 'sp' in names:
            saved = instruction.mnemonic.startswith(('push', 'pop')) or instruction.mnemonic.startswith(('stm', 'ldm')) and instruction.op_str.startswith('sp!')
            immediate_adjustment = instruction.id in (arm.ARM_INS_ADD, arm.ARM_INS_SUB) and instruction.operands[-1].type == ARM_OP_IMM and (
                len(instruction.operands) == 2 or len(instruction.operands) == 3 and instruction.operands[1].type == ARM_OP_REG and instruction.reg_name(instruction.operands[1].reg) == 'sp')
            if instruction.cc not in (0, 15) or not (saved or immediate_adjustment):
                unknown_stack = True
    return {'address': hex(spec['address']), 'mode': spec['mode'], 'directRegisterReadLiveInMask': direct, 'registerInputMask': needed,
        'definitelyWrittenOnEveryReturnMask': return_defined, 'mayPassOriginalRegisterThroughReturnMask': return_passthrough,
        'returnProjectionMask': return_live_mask, 'argumentCountHypothesis': max(needed.bit_length(), 4 + stack_words if stack_words else 0),
        'incomingStackWords': stack_words, 'stackEvidence': stack_evidence, 'predicateStates': len(incoming), 'workItems': visits,
        'returnInstructionAddresses': [hex(pc) for pc in sorted(returns)], 'unqualifiedCalleeTargets': sorted(unknown_calls),
        'flagContractQuestions': [{'kind': kind, 'pc': hex(pc), 'flagMask': mask} for kind, pc, mask in sorted(observations)], 'unsupported': sorted(unsafe),
        'unknownStackTransformationOrIndexedRead': unknown_stack, 'prototypeHintUsable': not unsafe and not observations and not unknown_stack and not unknown_calls,
        'allFlagStatesEnumerated': True, 'conditionFactsCrossCallsOrCpsrWriters': False,
        'argumentAndReturnTypesUnproved': True, 'ordinarySourceCredit': 0}


def argument_hints(specs, iterations=16):
    inputs = {spec['address']: 15 for spec in specs}
    outputs = {spec['address']: 0 for spec in specs}
    reports, rounds, converged = {}, 0, False
    for rounds in range(1, iterations + 1):
        reports = {spec['address']: analyze(spec, inputs, outputs) for spec in specs}
        next_inputs = {address: inputs[address] & report['registerInputMask'] for address, report in reports.items()}
        next_outputs = {address: outputs[address] | report['definitelyWrittenOnEveryReturnMask'] for address, report in reports.items()}
        if next_inputs == inputs and next_outputs == outputs:
            converged = True
            break
        inputs, outputs = next_inputs, next_outputs
    counts = {address: max(inputs[address].bit_length(), 4 + report['incomingStackWords'] if report['incomingStackWords'] else 0)
        for address, report in reports.items()}
    return counts, reports, {'iterations': rounds, 'converged': converged,
        'sourceCredit': 0, 'conservativeRegisterDependencyHypothesesOnly': True, 'registerScope': ['r0', 'r1', 'r2', 'r3'], 'nonstandardLanguageCallingConventionsRecovered': False,
        'limitations': ['R0 return projection is an explicit conservative hypothesis, not a recovered original language signature',
            'Stack words reuse the existing bounded stack scan; unknown stack transformations and opaque callees require independent qualification',
            'A register preserved across a call is not assumed newly defined without a proven callee output summary']}
