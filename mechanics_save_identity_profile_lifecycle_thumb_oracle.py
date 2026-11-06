import hashlib
import json
import random
import re
import struct
import time
import zlib

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
INPUT = BASE + 0x40
STOP = 0x027ff800
MULTIPLIER = 0x5d588b656c078965
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096cc0, 0x02096cd8, 0x02096ce8, 0x02096da4, 0x02096cf8}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/mechanics-save-identity-core-thumb.json', 'evidence/matches/mechanics-save-identity-values-thumb.json', 'evidence/matches/mechanics-save-identity-profile-storage-thumb.json')
    extra = {0x02096db4, 0x02096c6c, 0x02096c90, 0x020971bc, 0x020972c0, 0x020972a8}
    result = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for path in paths:
        report = json.loads((root / path).read_text(encoding='utf-8'))
        for entry in report['matches']:
            address = int(entry['address'], 0)
            if address not in wanted | extra:
                continue
            for field in ('source', 'object'):
                if sha((root / entry[field]).read_bytes()) != entry[field + 'Sha256']:
                    raise AssertionError(('Profile dependency source/object differs', entry['name']))
            row = dict(entry)
            if 'isolatedCallerBinary' not in row:
                bindings = {}
                for relocation in row['relocations']:
                    target = int(relocation['target'], 0) & ~1
                    match = re.search(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + r'$', config, re.M)
                    if not match:
                        raise AssertionError(('Profile dependency target missing', target))
                    bindings[relocation['symbol']] = {'address': hex(target), 'mode': match[1], 'module': 'main', 'processor': 'arm9', 'kind': 'function'}
                row.update(freeze_link(validate_link(row, bindings)))
            binary = (root / row['isolatedCallerBinary']).read_bytes()
            if sha(binary) != row['isolatedCallerBinarySha256'] or binary != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError(('Profile dependency actual linked bytes differ', row['name']))
            result.append((row, binary))
    if {int(row['address'], 0) for row, code in result} != wanted | extra:
        raise AssertionError('Profile dependency batch incomplete')
    return result


def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]

def put(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xffffffff)

def seed_identity(data, offset, words, context):
    seed = 0
    for value in words:
        seed ^= value
    first, second = context[:2] if context[0] or context[1] else context[2:]
    if second <= 0x7ff:
        put(data, offset, (word(data, offset) & ~0x7ff) | second)
    put(data, offset + 4, first)
    put(data, offset + 8, ((seed * MULTIPLIER) >> 32) & 0xffffffff)
    put(data, offset, (word(data, offset) & ~0x1800) | 0x800)

def model(name, data, words, context, key):
    offset = 0x40
    result = None
    present = bool(context[0] or context[1])
    if name == 'saved_sdk_context_snapshot':
        struct.pack_into('<IIIII', data, offset, *context, int(present))
    elif name == 'saved_identity_seed_initialize':
        seed_identity(data, offset, words, context)
    elif name == 'saved_profile_initialize':
        data[offset:offset + 64] = bytes(64)
        put(data, offset, 64)
        put(data, offset + 36, key)
        seed_identity(data, offset + 4, words, context)
        put(data, offset + 60, zlib.crc32(data[offset:offset + 60]))
        put(data, offset + 32, 1)
    elif name == 'saved_identity_context_equal':
        first, second = context[:2] if present else context[2:]
        result = int(word(data, offset + 4) == first and (word(data, offset) & 0x7ff) == second)
    elif name == 'saved_profile_context_equal':
        if ((word(data, offset + 16) >> 11) & 3) == 0:
            result = 1
        elif not present:
            result = 0
        else:
            result = int(word(data, offset + 20) == context[0] and (word(data, offset + 16) & 0x7ff) == context[1])
    else:
        raise AssertionError(name)
    return result

def validate(arm, save, matches, root):
    from match_mechanics_save_identity_profile_lifecycle_thumb import SPECS
    if set(matches) != set(SPECS):
        raise AssertionError('Complete profile lifecycle source batch is required')
    reused = dependencies(root, arm)
    controls = {'words': (), 'context': (), 'calls': [], 'trace': None, 'flags': 0}
    def provider(machine, address, size, user):
        output = machine.reg_read(UC_ARM_REG_R0)
        values = controls['words'] if address == 0x02008360 else controls['context']
        machine.mem_write(output, struct.pack('<' + 'I' * len(values), *values))
        controls['calls'].append(address)
        for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12), (0x13579bdf, 0x2468ace0, 0xffffffff, 0, 0x12345678)):
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_CPSR, (machine.reg_read(UC_ARM_REG_CPSR) & 0x0fffffff) | (controls['flags'] << 28))
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
    def instruction(machine, address, size, user):
        if controls['trace'] is not None:
            controls['trace'].append({'address': hex(address), 'r0': hex(machine.reg_read(UC_ARM_REG_R0)), 'r1': hex(machine.reg_read(UC_ARM_REG_R1)), 'r2': hex(machine.reg_read(UC_ARM_REG_R2)), 'carry': int(bool(machine.reg_read(UC_ARM_REG_CPSR) & (1 << 29)))})
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Profile lifecycle actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        for address in (0x02008360, 0x020a4660):
            machine.hook_add(UC_HOOK_CODE, provider, user_data=10, begin=address, end=address)
        for address in (0x02097106, 0x02097108, 0x0209710a, 0x0209710c):
            machine.hook_add(UC_HOOK_CODE, instruction, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(2026102783)
    inverse = pow(MULTIPLIER & 0xffffffff, -1, 1 << 32)
    carry_seed = (-inverse) & 0xffffffff
    seeds = (0, 1, 2, 0x7fffffff, 0x80000000, 0xffffffff, carry_seed, (carry_seed - 1) & 0xffffffff, (carry_seed + 1) & 0xffffffff)
    contexts = ((0, 0, 0, 0), (0, 0, 0x12345678, 0x7ff), (0x12345678, 0x7ff, 0, 0), (0, 1, 0xffffffff, 0xffffffff), (1, 0, 2, 3), (0xffffffff, 0xffffffff, 0x7fffffff, 0x80000000))
    fixtures = []
    for seed in seeds:
        for context in contexts:
            for kind in range(4):
                initial = bytearray(rng.randbytes(0x1000))
                put(initial, 0x50, (word(initial, 0x50) & ~0x1800) | (kind << 11))
                fixtures.append((bytes(initial), (0, 0, 0, 0, 0, 0, 0, seed), context, rng.getrandbits(32)))
    for index in range(128):
        context = tuple(rng.getrandbits(32) for part in range(4))
        if index & 1:
            context = (context[0], context[1] & 0x7ff, context[2], context[3] & 0x7ff)
        if index % 4 == 0:
            context = (0, 0, context[2], context[3])
        initial = bytearray(rng.randbytes(0x1000))
        chosen = context[:2] if context[0] or context[1] else context[2:]
        for offset in (0x40, 0x50):
            put(initial, offset, (word(initial, offset) & ~0x7ff) | (chosen[1] & 0x7ff))
            put(initial, offset + 4, chosen[0] ^ (1 if index % 8 == 0 else 0))
        fixtures.append((bytes(initial), tuple(rng.getrandbits(32) for part in range(8)), context, rng.getrandbits(32)))
    cases = calls = 0
    carry_cases = 0
    carry_traces = []
    for initial, words, context, key in fixtures:
        for name in SPECS:
            current = bytearray(initial)
            result = model(name, current, words, context, key)
            incoming = [rng.getrandbits(32) for register in SAVED]
            stack = rng.randbytes(0x10000)
            guard = rng.randbytes(0x1000)
            expected_calls = [] if name == 'saved_profile_context_equal' and ((word(initial, 0x50) >> 11) & 3) == 0 else [0x020a4660]
            if name in ('saved_identity_seed_initialize', 'saved_profile_initialize'):
                expected_calls.insert(0, 0x02008360)
            is_carry = words[-1] == carry_seed and not any(words[:-1]) and name in ('saved_identity_seed_initialize', 'saved_profile_initialize')
            controls.update({'words': words, 'context': context, 'flags': cases & 15})
            traces = []
            row, code = matches[name]
            for machine in machines:
                controls['calls'] = []
                controls['trace'] = [] if is_carry else None
                machine.mem_write(BASE, initial)
                machine.mem_write(0x021d0000, guard)
                machine.mem_write(0x027f0000, stack)
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_R0, INPUT)
                machine.reg_write(UC_ARM_REG_R1, key)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
                began = time.monotonic()
                machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                    raise AssertionError(('Profile lifecycle bounded return/ABI', name, words, context))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Profile lifecycle independent result', name, result, machine.reg_read(UC_ARM_REG_R0)))
                actual = bytes(machine.mem_read(BASE, 0x1000))
                if actual != current or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                    differing = [(index, left, right) for index, (left, right) in enumerate(zip(actual, current)) if left != right][:8]
                    raise AssertionError(('Profile lifecycle independent RAM/guard', name, words, context, differing))
                if controls['calls'] != expected_calls:
                    raise AssertionError(('Profile lifecycle bounded provider calls', name, controls['calls'], expected_calls))
                if is_carry:
                    traces.append(list(controls['trace']))
                calls += 1
            if words[-1] == carry_seed and not any(words[:-1]) and name in ('saved_identity_seed_initialize', 'saved_profile_initialize'):
                if traces[0] != traces[1] or len(traces[0]) != 4:
                    raise AssertionError('Native/source carry instruction states differ')
                trace = traces[0]
                high = ((carry_seed * MULTIPLIER) >> 32) & 0xffffffff
                pointer = INPUT if name == 'saved_identity_seed_initialize' else INPUT + 4
                if int(trace[0]['r0'], 0) != 0xffffffff or int(trace[0]['r1'], 0) != high or int(trace[1]['r2'], 0) != 0 or trace[2]['carry'] != 0 or int(trace[2]['r0'], 0) != pointer or int(trace[3]['r1'], 0) != high:
                    raise AssertionError(('Target compiler carry-loss instruction model differs', trace))
                if not any(row['name'] == name for row in carry_traces):
                    carry_traces.append({'name': name, 'seed': hex(carry_seed), 'sourceExpressionHigh': hex((high + 1) & 0xffffffff), 'nativeAndRecompiledHigh': hex(high), 'instructionStatesBeforeExecution': trace})
                carry_cases += 1
            cases += 1
    protocols = 0
    from mechanics_save_identity_profile_storage_thumb_oracle import model as storage_model
    storage = {row['name']: (row, code) for row, code in reused if row['name'].startswith('saved_profile_')}
    for initial, words, context, key in fixtures[:64]:
        current = bytearray(initial)
        guard = rng.randbytes(0x1000)
        controls.update({'words': words, 'context': context, 'flags': 15, 'trace': None})
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x021d0000, guard)
        sequence = ('saved_profile_initialize', 'saved_profile_checksum_valid', 'saved_profile_dirty', 'saved_profile_checksum_refresh', 'saved_profile_checksum_valid', 'saved_profile_context_equal')
        for name in sequence:
            result = model(name, current, words, context, key) if name in SPECS else storage_model(name, current, (INPUT,))
            row, code = matches[name] if name in matches else storage[name]
            incoming = [rng.getrandbits(32) for register in SAVED]
            for machine in machines:
                machine.mem_write(0x027f0000, rng.randbytes(0x10000))
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_R0, INPUT)
                machine.reg_write(UC_ARM_REG_R1, key)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
                began = time.monotonic()
                machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                    raise AssertionError(('Profile lifecycle protocol bound/ABI', name))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Profile lifecycle protocol result', name))
                if bytes(machine.mem_read(BASE, 0x1000)) != current or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                    raise AssertionError(('Profile lifecycle protocol RAM/guard', name))
                calls += 1
            cases += 1
        protocols += 1
    flag_probes = []
    controls['trace'] = None
    for carry in (0, 1):
        high = ((carry_seed * MULTIPLIER) >> 32) & 0xffffffff
        states = []
        for machine in machines:
            for register, value in ((UC_ARM_REG_R0, 0xffffffff), (UC_ARM_REG_R1, high), (UC_ARM_REG_R2, 0xffffffff), (UC_ARM_REG_R5, INPUT)):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_CPSR, (machine.reg_read(UC_ARM_REG_CPSR) & 0x0fffffff) | (carry << 29))
            machine.emu_start(0x02097107, 0x0209710c, count=3)
            state = (machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_R0), machine.reg_read(UC_ARM_REG_R1), machine.reg_read(UC_ARM_REG_R2), int(bool(machine.reg_read(UC_ARM_REG_CPSR) & (1 << 29))))
            if state != (0x0209710c, INPUT, high, 0, 0):
                raise AssertionError(('Isolated emitted ADD/ADC instruction-state probe', carry, state))
            states.append(state)
        flag_probes.append({'incomingCarry': carry, 'endPc': hex(states[0][0]), 'pointerArgument': hex(states[0][1]), 'highResult': hex(states[0][2]), 'outgoingCarry': states[0][4], 'nativeAndRecompiledEqual': states[0] == states[1]})
    malformed = []
    controls.update({'words': (0,) * 8, 'context': (0,) * 4, 'flags': 0, 'trace': None})
    for name in ('saved_identity_seed_initialize', 'saved_sdk_context_snapshot', 'saved_profile_context_equal'):
        initial = rng.randbytes(0x1000)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        outcomes = []
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, 0)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | 1)
            began = time.monotonic()
            try:
                machine.emu_start(SPECS[name][0] | 1, STOP, count=1000000)
            except UcError as error:
                if time.monotonic() - began > 2:
                    raise AssertionError('Lifecycle malformed fault exceeded bound')
                outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
            else:
                raise AssertionError('Lifecycle malformed pointer unexpectedly returned')
            calls += 1
        expected_pc = {'saved_identity_seed_initialize': 0x02096c7c, 'saved_sdk_context_snapshot': 0x020a55fa, 'saved_profile_context_equal': 0x02096ce8}[name]
        if outcomes[0][1] != expected_pc:
            raise AssertionError(('Lifecycle malformed fault location differs', name))
        if outcomes[0] != outcomes[1] or outcomes[0][4] != initial:
            raise AssertionError(('Lifecycle malformed partial state differs', name))
        malformed.append({'name': name, 'argument': 0, 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
        cases += 1
    retained = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for address, mode in ((0x02026124, 'arm'), (0x02008d78, 'arm'), (0x02019adc, 'arm'), (0x02019ba8, 'arm')):
        match = re.search(r'kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('Lifecycle retained dependency missing', address))
        size = int(match[1], 0)
        retained.append({'address': hex(address), 'mode': mode, 'module': 'main', 'processor': 'arm9', 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    providers = []
    for address, mode in ((0x02008360, 'arm'), (0x020a4660, 'thumb')):
        match = re.search(r'kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('Lifecycle provider native span missing', address))
        size = int(match[1], 0)
        providers.append({'address': hex(address), 'mode': mode, 'module': 'main', 'processor': 'arm9', 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'nativeInstructionsExecuted': False, 'functionCredit': 0})
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentPythonZlibAndIntegerStateModels': True, 'multiplicationLowWordFFFFFFFFCarryCases': carry_cases, 'connectedInitializationRefreshProtocols': protocols, 'isolatedThreeInstructionFlagProbes': flag_probes, 'flagProbeNativeAndRecompiledRuns': 4, 'flagProbeInstructionRangeSha256': sha(arm[0x97106:0x9710c]), 'malformedPointerCases': malformed, 'retainedNativeEntries': retained, 'providerNativeEntries': providers, 'targetCompilerCarryLossRequiredRegression': carry_traces, 'platformStubs': {'main:arm:0x02008360': 'Writes exactly eight controlled u32 seed words, preserving the native caller algorithm while replacing hardware entropy/timing.', 'main:thumb:0x020A4660': 'Writes exactly four controlled u32 context words; the recovered62-byte context snapshot computes presence itself. Both providers clobber caller-saved registers and flags, return to the real LR and are counted per call.'}, 'reusedAcceptedSources': [row for row, code in reused], 'observations': ['Eight hardware seed words reduce by prefix XOR. The matched C source multiplies the last prefix by5D588B656C078965 and adds1, but emitted Thumb code clears carry during pointer argument preparation before ADC; observed identity word2 equals the product high32 bits even when its low word isFFFFFFFF.', 'The context snapshot copies four raw words and marks presence only when its first64 bits are nonzero.', 'Identity initialization chooses the first context pair when present, otherwise the second; checked low11-bit login-field writes can reject a high context word above7FF while still replacing word1.', 'Profile initialization clears64 bytes, writes size64/key+36, initializes the first identity, computes checksum over60 bytes and then marks dirty.', 'Context equality compares the raw login43-bit value to the selected64-bit context pair; profile comparison accepts kind0 without reading context and otherwise requires a present matching primary pair.'], 'limitations': ['Hardware seed collection and context acquisition are explicit controlled providers; entropy quality, clocks, network state and authentic platform bootstrap remain unresolved.', 'The64-bit multiplier, CRC32 and SDK fill remain native implementations.', 'Exact target C compilation does not imply portable C arithmetic: the required seed carry-loss regressions separately record source-expression and emitted-instruction expectations.', 'Raw constructor/context behavior does not establish complete profile legality, online identity semantics or new save-byte meanings.']}
