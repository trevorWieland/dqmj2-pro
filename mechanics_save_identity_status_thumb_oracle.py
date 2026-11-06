import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
INPUT = BASE + 0x40
GLOBALS = 0x021d2000
STOP = 0x027ff800
CALLBACKS = (0x0209aadd, 0x0209aafd, 0x0209aae9, 0x0209ab0d)
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096cf8, 0x02096ce8, 0x02096da4, 0x020a9268}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/main-runtime09.json', 'evidence/matches/mechanics-save-identity-values-thumb.json')
    extra = {0x02096c6c, 0x02000b64}
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
                    if not match and (relocation['symbol'] != 'native_data_021d2374' or target != 0x021d2374 or relocation['type'] != 2):
                        raise AssertionError('Unqualified status dependency relocation target')
                    bindings[relocation['symbol']] = {'address': hex(target), 'mode': match[1] if match else 'data', 'module': 'main', 'processor': 'arm9', 'kind': 'function' if match else 'data'}
                row.update(freeze_link(validate_link(row, bindings)))
            binary = (root / row['isolatedCallerBinary']).read_bytes()
            if sha(binary) != row['isolatedCallerBinarySha256'] or binary != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError(('Profile dependency actual linked bytes differ', row['name']))
            result.append((row, binary))
    if {int(row['address'], 0) for row, code in result} != wanted | extra:
        raise AssertionError('Profile dependency batch incomplete')
    return result


def validate(arm, save, matches, root):
    from match_mechanics_save_identity_status_thumb import SPECS, GLOBALS as TARGETS
    if set(matches) != set(SPECS):
        raise AssertionError('Complete identity status source batch is required')
    reused = dependencies(root, arm)
    controls = {'query': 0, 'pending': 0, 'input': 0, 'calls': [], 'flags': 0}
    def provider(machine, address, size, user):
        argument = machine.reg_read(UC_ARM_REG_R0)
        controls['calls'].append((address, argument if address != 0x020a5628 else None))
        if address in (0x020a4e70, 0x020a5458) and argument != controls['input']:
            raise AssertionError('Status provider original input pointer differs')
        if argument and address == 0x020a4e70:
            old = struct.unpack('<I', bytes(machine.mem_read(argument, 4)))[0]
            machine.mem_write(argument, struct.pack('<I', old ^ 0xa5a55a5a))
        if argument and address == 0x020a5458:
            machine.mem_write(argument + 4, struct.pack('<I', 0x76543210))
        result = controls['query'] if address == 0x020a4e70 else controls['pending'] if address == 0x020a5628 else 0xbad0cafe
        for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12), (result, 0xffffffff, 0x13579bdf, 0x2468ace0, 0)):
            machine.reg_write(register, value & 0xffffffff)
        machine.reg_write(UC_ARM_REG_CPSR, (machine.reg_read(UC_ARM_REG_CPSR) & 0x0fffffff) | (controls['flags'] << 28))
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Status actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        for address in (0x020a4e70, 0x020a5628, 0x020a5458):
            machine.hook_add(UC_HOOK_CODE, provider, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(2026102785)
    words = (0, 1, 2, 3, 0x7ff, 0x800, 0x1800, 0x7fffffff, 0x80000000, 0xffffffff)
    vectors = [('saved_sdk_bootstrap_status', pointer, query, pending) for pointer in (0, INPUT, INPUT + 4) for query in words for pending in words]
    vectors += [('saved_sdk_bootstrap_status', INPUT, rng.getrandbits(32), rng.getrandbits(32)) for index in range(256)]
    vectors += [('saved_identity_mark_flag4', INPUT, (flags & ~0x1800) | (kind << 11), 0) for flags in (*words, *(rng.getrandbits(32) for index in range(256))) for kind in range(4)]
    cases = calls = 0
    for name, pointer, query, pending in vectors:
        initial = bytearray(rng.randbytes(0x1000))
        globals_initial = rng.randbytes(0x1000)
        if name == 'saved_identity_mark_flag4':
            struct.pack_into('<I', initial, 0x40, query)
        expected = bytearray(initial)
        globals_expected = bytearray(globals_initial)
        provider_calls = []
        if name == 'saved_sdk_bootstrap_status':
            provider_calls = [(0x020a4e70, pointer), (0x020a5628, None)]
            if pointer:
                offset = pointer - BASE
                old = struct.unpack_from('<I', expected, offset)[0]
                struct.pack_into('<I', expected, offset, old ^ 0xa5a55a5a)
                if pending:
                    struct.pack_into('<I', expected, offset + 4, 0x76543210)
            if pending:
                provider_calls.append((0x020a5458, pointer))
            result = (2 if pending else 3) if query & 0x80000000 else (1 if pending else 0)
            struct.pack_into('<IIII', globals_expected, 0x37c, *CALLBACKS)
        else:
            result = None
            if ((query >> 11) & 3) == 3:
                struct.pack_into('<I', expected, 0x40, query | (4 << 11))
        controls.update({'query': query, 'pending': pending, 'input': pointer, 'flags': cases & 15})
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        row, code = matches[name]
        for machine in machines:
            controls['calls'] = []
            machine.mem_write(BASE, bytes(initial))
            machine.mem_write(GLOBALS, globals_initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, pointer)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('Status bounded return/ABI', name, pointer, query, pending))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Status independent branch result', query, pending, result))
            if bytes(machine.mem_read(BASE, 0x1000)) != expected or bytes(machine.mem_read(GLOBALS, 0x1000)) != globals_expected:
                raise AssertionError(('Status complete input/global RAM model differs', name, query, pending))
            if controls['calls'] != provider_calls:
                raise AssertionError(('Status provider sequence/input differs', controls['calls'], provider_calls))
            calls += 1
        cases += 1
    malformed = []
    stack = rng.randbytes(0x10000)
    initial = rng.randbytes(0x1000)
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
            machine.emu_start(0x02096dd1, STOP, count=1000000)
        except UcError as error:
            if time.monotonic() - began > 2:
                raise AssertionError('Status malformed fault exceeded bound')
            outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
        else:
            raise AssertionError('Status null identity unexpectedly returned')
        calls += 1
    if outcomes[0] != outcomes[1] or outcomes[0][1] != 0x02096ce8 or outcomes[0][4] != initial:
        raise AssertionError('Status malformed partial state/fault location differs')
    malformed.append({'name': 'saved_identity_mark_flag4', 'argument': 0, 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
    cases += 1
    config = (root / 'config/arm9/symbols.txt').read_text()
    provider_entries = []
    for address in (0x020a4e70, 0x020a5628, 0x020a5458):
        match = re.search(r'kind:function\(thumb,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('Status native provider span missing', address))
        size = int(match[1], 0)
        provider_entries.append({'address': hex(address), 'mode': 'thumb', 'module': 'main', 'processor': 'arm9', 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'nativeInstructionsExecuted': False, 'functionCredit': 0})
    start = 0xbfc
    end = arm.index(0, start) + 1
    version = {'address': '0x02000bfc', 'bytes': end - start, 'sha256': sha(arm[start:end]), 'module': 'main', 'processor': 'arm9', 'kind': 'data', 'sourceCredit': 0}
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentBranchFlagAndWholeMemoryModels': True, 'platformStubs': {'main:thumb:0x020A4E70': 'Controlled signed32 query result; optionally XORs the input word to model a callee RAM effect.', 'main:thumb:0x020A5628': 'Controlled arbitrary zero/nonzero predicate result.', 'main:thumb:0x020A5458': 'Records the original input pointer and optionally writes input+4. All three providers clobber caller-saved registers/flags and return to real LR; their native implementations are not credited.'}, 'providerNativeEntries': provider_entries, 'reusedAcceptedSources': [row for row, code in reused], 'nativeVersionData': version, 'malformedPointerCases': malformed, 'observations': ['The status caller returns0/1 for nonnegative query and zero/nonzero pending, and3/2 for negative query and zero/nonzero pending; finalization runs exactly when pending is nonzero.', 'All paths register four qualified Thumb function pointers, writing021D237C/380/384/388 through the accepted native callback registrar body.', 'The flag helper sets only field flag4 at word0 bit13 when raw kind bits11..12 equal3; other kinds and all surrounding bytes remain unchanged.'], 'limitations': ['The query/pending/finalizer bodies are explicit providers; full SDK bootstrap, hardware state and actual initialization errors remain unresolved.', 'Callback addresses are verified typed function entries but callback implementations and invocation semantics receive no source credit here.', 'Provider-supported null bootstrap input is a caller contract probe, not a claim that the original SDK permits null input.', 'No decoded kind meaning, legal profile namespace, save partition promotion or original input modification is claimed.']}
