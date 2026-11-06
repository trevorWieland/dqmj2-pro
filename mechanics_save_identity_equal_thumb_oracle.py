import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
FIRST = BASE + 0x40
SECOND = BASE + 0x80
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
HELPERS = (0x02096cf8, 0x02096cbc, 0x02096ca8, 0x02096c90, 0x02096cac)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096cf8, 0x02096ce8, 0x02096ca8, 0x02096cbc}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/mechanics-save-identity-values-thumb.json')
    extra = {0x02096c90, 0x02096cac}
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


def expected(first, second):
    left, right = (first[0] >> 11) & 3, (second[0] >> 11) & 3
    calls = {address: 0 for address in HELPERS}
    calls[0x02096cf8] = 2
    if left != right or left == 0:
        return 0, calls
    if left == 3:
        calls[0x02096cbc] = 2
        return int(first[1] == second[1]), calls
    if left == 2:
        calls[0x02096cac] = 2
        return int(first[1:] == second[1:]), calls
    calls[0x02096c90] = 2
    if (first[0] & 0x7ff) != (second[0] & 0x7ff) or first[1] != second[1]:
        return 0, calls
    calls[0x02096ca8] = 2
    return int(first[2] == second[2]), calls

def validate(arm, save, matches, root):
    if set(matches) != {'saved_identity_equal'}:
        raise AssertionError('Complete identity equality source batch is required')
    reused = dependencies(root, arm)
    seen = {address: 0 for address in HELPERS}
    def entry(machine, address, size, user):
        seen[address] += 1
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Identity equality actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        for address in seen:
            machine.hook_add(UC_HOOK_CODE, entry, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(2026102788)
    vectors = []
    baselines = []
    for kind in range(4):
        for flags in (0, 0x7ff, 0x8000, 0xffffffff, *(rng.getrandbits(32) for index in range(8))):
            first = ((flags & ~0x1800) | (kind << 11), rng.getrandbits(32), rng.getrandbits(32))
            baselines.append(first)
            vectors.append((first, first))
            for bit in range(96):
                second = list(first)
                second[bit // 32] ^= 1 << (bit % 32)
                vectors.append((first, tuple(second)))
    for left in range(4):
        for right in range(4):
            for flags in (0, 0x7ff, 0xffffffff):
                for low in (0, 1, 2, 0x7ff, 0xffff, 0x7fffffff, 0x80000000, 0xffffffff, 0x12345678):
                    for high in (0, 1, 0xffffffff):
                        first = ((flags & ~0x1800) | (left << 11), low, high)
                        second = ((flags & ~0x1800) | (right << 11), low, high)
                        vectors.append((first, second))
    fixtures = []
    for first, second in vectors:
        initial = bytearray(rng.randbytes(0x1000))
        struct.pack_into('<III', initial, 0x40, *first)
        struct.pack_into('<III', initial, 0x80, *second)
        fixtures.append((bytes(initial), FIRST, SECOND))
    for first in baselines:
        for offset in (0x40, 0x44, 0x48):
            initial = bytearray(rng.randbytes(0x1000))
            struct.pack_into('<III', initial, 0x40, *first)
            fixtures.append((bytes(initial), FIRST, BASE + offset))
    cases = calls = 0
    helper_counts = {address: 0 for address in HELPERS}
    for initial, first_pointer, second_pointer in fixtures:
        first = struct.unpack_from('<III', initial, first_pointer - BASE)
        second = struct.unpack_from('<III', initial, second_pointer - BASE)
        result, expected_calls = expected(first, second)
        guard = rng.randbytes(0x1000)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            for address in seen:
                seen[address] = 0
            machine.mem_write(BASE, initial)
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, first_pointer)
            machine.reg_write(UC_ARM_REG_R1, second_pointer)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(0x020973d9, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('Identity equality bounded return/ABI', first, second))
            if machine.reg_read(UC_ARM_REG_R0) != result or seen != expected_calls:
                raise AssertionError(('Identity equality independent result/field short-circuit', first, second, result, seen, expected_calls))
            if bytes(machine.mem_read(BASE, 0x1000)) != initial or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                raise AssertionError('Identity equality complete input/global guards differ')
            for address, count in seen.items():
                helper_counts[address] += count
            calls += 1
        cases += 1
    malformed = []
    for first_pointer, second_pointer in ((0, SECOND), (FIRST, 0), (0, 0)):
        initial = rng.randbytes(0x1000)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        outcomes = []
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, first_pointer)
            machine.reg_write(UC_ARM_REG_R1, second_pointer)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | 1)
            began = time.monotonic()
            try:
                machine.emu_start(0x020973d9, STOP, count=1000000)
            except UcError as error:
                if time.monotonic() - began > 2:
                    raise AssertionError('Identity equality malformed fault exceeded bound')
                outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
            else:
                raise AssertionError('Identity equality null pointer unexpectedly returned')
            calls += 1
        if outcomes[0] != outcomes[1] or outcomes[0][1] != 0x02096ce8 or outcomes[0][4] != initial:
            raise AssertionError('Identity equality malformed partial state/fault location differs')
        malformed.append({'arguments': [hex(first_pointer), hex(second_pointer)], 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentRawKindAndWordModels': True, 'verifiedHelperEntryCountsAcrossNativeAndRecompiled': {hex(address): count for address, count in helper_counts.items()}, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in reused], 'retainedNativeEntries': [], 'malformedPointerCases': malformed, 'observations': ['Different raw kinds always compare unequal; raw kind0 compares unequal even for the same pointer and identical zero-filled records.', 'Raw kind3 compares only word1, kind2 compares words1/2, and kind1 compares word1 plus low11 bits of word0 plus word2.', 'Unrelated word0 flags are ignored after kind agreement; every bit in all three words is independently mutated across four kind classes.', 'Kind1 skips word2 readers when the43-bit login comparison already differs; getter entry counts verify that short circuit.', 'Both argument pointers are always consumed by kind readers; null first/second/both pointers fault in the declared flag getter without arena changes.'], 'limitations': ['This seven-body C closure covers equality and six declared getters without native callees, but does not establish legal identity kinds, authentication or online equivalence.', 'Same/overlapping read-only buffers are bounded native/source probes, not ownership or valid profile-layout claims.', 'The SP1p6 compiler is independently archive/member/smoke validated and pinned only for this function; earlier sources and their compiler selections remain unchanged.', 'No original input or semantic save partition changes are made.']}
