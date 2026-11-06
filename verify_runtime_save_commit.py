import hashlib
import json
import random
import struct
import time

from project import ROOT, configuration, native_dependencies, verify_inputs, write_json

CONFIG = configuration()
native_dependencies(CONFIG)
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put
from mechanics_save_runtime_commit_oracle import expected, PARTY, RESERVE, RUNTIME, RECORDS, RAW153
from verify_save_protocol import PARTS, DATE, TIME, expected_summary, seal

STOP = 0x027ff800
BUFFER = 0x02500000
IO = 0x021c6bfc
ENTRIES = (0x02065210, 0x0207e564, 0x0207e690, 0x0207e6a0)
PROVIDERS = {0x0202a44c: 'allocate-tail', 0x0202a498: 'free', 0x0200f3e0: 'date', 0x0200f48c: 'time'}
RETAINED = {0x02008d78: 148, 0x02008e0c: 304}
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(arm, rom_hash):
    available = {}
    for batch in json.loads((ROOT / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        path = ROOT / batch['report']
        document = json.loads(path.read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            if row.get('module', 'main') in ('main', 'arm9') and row.get('exactAfterDeclaredRelocation', row.get('exactBytes', False)):
                available[int(row['address'], 16)] = (row, document, batch['report'])
    pending = list(ENTRIES)
    result = {}
    missing = set()
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    while pending:
        address = pending.pop()
        if address in result or address in PROVIDERS or address in RETAINED:
            continue
        if address not in available:
            missing.add(address)
            continue
        row, document, report = available[address]
        if document['romSha256'] != rom_hash:
            raise AssertionError('Runtime serialization ROM namespace differs')
        source = row.get('source') or document['source']
        source_hash = row.get('sourceSha256') or document['sourceSha256']
        if sha((ROOT / source).read_bytes()) != source_hash or sha((ROOT / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError(('Runtime serialization source/object identity differs', source))
        with (ROOT / row['object']).open('rb') as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
            code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
        for relocation in row.get('relocations', []):
            at = relocation['offset']
            target = int(relocation['target'], 16) + relocation['addend']
            previous = struct.unpack_from('<I', code, at)[0]
            if relocation['type'] == 2:
                value = target
            elif relocation['type'] in (1, 28, 29):
                value = (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
            else:
                raise AssertionError('Runtime serialization unsupported relocation')
            struct.pack_into('<I', code, at, value & 0xffffffff)
        size = row.get('bytes', row.get('size'))
        if code != arm[address - 0x02000000:address - 0x02000000 + size]:
            raise AssertionError(('Runtime serialization source span differs', row['name']))
        result[address] = {'name': row['name'], 'address': hex(address), 'bytes': size, 'source': source, 'sourceSha256': source_hash, 'object': row['object'], 'objectSha256': row['objectSha256'], 'report': report, 'code': bytes(code)}
        for instruction in decoder.disasm(code, address):
            if instruction.mnemonic in ('b', 'bl') and instruction.op_str.startswith('#0x'):
                target = int(instruction.op_str[1:], 16)
                if not address <= target < address + size:
                    pending.append(target)
    if missing:
        raise AssertionError(('Runtime serialization missing source dependencies', [hex(value) for value in sorted(missing)]))
    return result

def make_fixture(save, bank, label, value, rng):
    memory = {0x020edc00: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0xa000)), 0x021c6000: bytearray(rng.randbytes(0x1000)), BUFFER - 0x100: bytearray(rng.randbytes(0x9200))}
    for start, end, address in PARTS:
        write(memory, address, save[bank + start:bank + end])
    write(memory, BUFFER, bytes([0xa5]) * 0x7100)
    put(memory, 0x020edd04, 0x7100)
    for index in range(100):
        record = bytearray(rng.randbytes(132))
        struct.pack_into('<I', record, 20, 1 if label == 'duplicate-record-ids' and index < 3 else index + 1)
        struct.pack_into('<h', record, 24, index % 512)
        record[28] = (index % 3) * 5
        record[48] = (50, 75, 100)[index % 3]
        write(memory, RECORDS + index * 132, bytes(record))
    identities = [1, 2, 3, 4, 5, 6] if label in ('distinct', 'duplicate-record-ids') else [1] * 6 if label == 'duplicate-runtime-ids' else [0xffffffff] * 6 if label == 'missing-ids' else [0] * 6 if label == 'zero-ids' else [1, 0, 0xffffffff, 3, 1, 2]
    for ordinal, identity in enumerate(identities):
        view = (PARTY if ordinal < 3 else RESERVE) + (ordinal % 3) * 528
        put(memory, view + 4, identity)
        block = bytearray(rng.randbytes(32))
        block[16] = (50, 75, 100)[ordinal % 3]
        write(memory, view + 284, bytes(block))
    write(memory, 0x021bd540, struct.pack('<III', *identities[:3]))
    write(memory, 0x021bd54c, struct.pack('<III', *identities[3:]))
    put(memory, RUNTIME, value)
    write(memory, RAW153, b'\xa5')
    put(memory, RAW153 + 1, 0x12345678)
    write(memory, 0x021bb278 + 0x100, bytes([(bank >> 8) ^ 0x5a]))
    write(memory, 0x021b9ee8 + 0x100, bytes([(bank >> 8) ^ 0xa5]))
    return memory

def built_bank(memory):
    bank = bytearray(bytes([0xa5]) * 0x7100)
    struct.pack_into('<III', bank, 0, 0x5a4953, 0x10000, 0x70d0)
    bank[0xc:0x1c] = DATE
    bank[0x1c:0x28] = TIME
    for start, end, address in PARTS:
        bank[start:end] = read(memory, address, end - start)
    bank[0x28:0x88] = expected_summary(bank)
    return seal(bank)

def main():
    inputs = verify_inputs(CONFIG)
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('Runtime serialization ARM9 identity differs')
    save = CONFIG['save'].read_bytes()
    functions = dependencies(arm, inputs['rom']['sha256'])
    rng = random.Random(202610271)
    machines = []
    contexts = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for address, function in functions.items():
                machine.mem_write(address, function['code'])
        context = {'seen': set(), 'trace': []}
        def hook(uc, address, size, state):
            if address in functions or address in RETAINED:
                state['seen'].add(address)
            if address not in PROVIDERS:
                return
            args = [uc.reg_read(register) for register in REGS]
            role = PROVIDERS[address]
            state['trace'].append((role, args[:3] if role == 'allocate-tail' else args[:2] if role == 'free' else args[:1]))
            result = 0
            if role == 'allocate-tail':
                if args != [state['heap'] & 0xffffffff, 0x7100, 4, args[3]]:
                    raise AssertionError(('Runtime serialization allocator arguments', args, state['heap']))
                result = BUFFER if state['success'] else 0
            elif role == 'free':
                signed_heap = ((state['heap'] + 128) & 255) - 128
                if args[:2] != [signed_heap & 0xffffffff, BUFFER]:
                    raise AssertionError(('Runtime serialization free arguments', args, signed_heap))
            elif role in ('date', 'time'):
                if args[0] != BUFFER + (0xc if role == 'date' else 0x1c):
                    raise AssertionError('Runtime serialization clock destination differs')
                uc.mem_write(args[0], DATE if role == 'date' else TIME)
            for register, value in zip(REGS, (result, 0xdead0001, 0xdead0002, 0xdead0003)):
                uc.reg_write(register, value)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        machine.hook_add(UC_HOOK_CODE, hook, context)
        machines.append(machine)
        contexts.append(context)
    cases = calls = 0
    hashes = set()
    executed = set()
    for bank in (0, 0x7100):
        for label in ('distinct', 'duplicate-record-ids', 'duplicate-runtime-ids', 'missing-ids', 'zero-ids', 'mixed-ids'):
            for value in (0, 1, 9999999, 10000000, 0x80000000, 0xffffffff):
                for heap in (-257, -128, -1, 0, 127, 128, 255, 256):
                    for success in (False, True):
                        original = make_fixture(save, bank, label, value, rng)
                        memory = {address: bytearray(data) for address, data in original.items()}
                        expected(memory, 'saved_runtime_blocks_commit', (), 0)
                        serialized = built_bank(memory)
                        incoming = [rng.getrandbits(32) for register in SAVED]
                        stack = rng.randbytes(0x10000)
                        expected_trace = [('allocate-tail', [heap & 0xffffffff, 0x7100, 4])]
                        if success:
                            expected_trace += [('date', [BUFFER + 0xc]), ('time', [BUFFER + 0x1c])]
                        for machine, context in zip(machines, contexts):
                            context.update({'seen': set(), 'trace': [], 'heap': heap, 'success': success})
                            for address, data in original.items():
                                machine.mem_write(address, bytes(data))
                            machine.mem_write(0x027f0000, stack)
                            for register, datum in zip(SAVED, incoming):
                                machine.reg_write(register, datum)
                            model = {address: bytearray(data) for address, data in memory.items()}
                            for step, address in enumerate(ENTRIES if success else ENTRIES[:3]):
                                machine.reg_write(UC_ARM_REG_R0, heap & 0xffffffff)
                                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                                machine.reg_write(UC_ARM_REG_LR, STOP)
                                began = time.monotonic()
                                machine.emu_start(address, STOP, count=500000)
                                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                                    raise AssertionError(('Runtime serialization bounded return/ABI', step, label))
                                result = None
                                if step == 1:
                                    write(model, IO + 1, bytes([heap & 255]))
                                    put(model, IO + 8, BUFFER if success else 0)
                                    if success:
                                        write(model, BUFFER, serialized)
                                    result = 0x7100 if success else 0
                                elif step == 2:
                                    result = BUFFER if success else 0
                                elif step == 3:
                                    put(model, IO + 8, 0)
                                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                                    raise AssertionError(('Runtime serialization return value', step, label, result))
                                for start, data in model.items():
                                    actual = bytes(machine.mem_read(start, len(data)))
                                    if actual != data:
                                        mismatch = next(index for index, (a, b) in enumerate(zip(actual, data)) if a != b)
                                        raise AssertionError(('Runtime serialization RAM/bank/guard differs', step, label, bank, heap, success, hex(start + mismatch), actual[mismatch], data[mismatch]))
                                calls += 1
                            trace = expected_trace + ([('free', [(((heap + 128) & 255) - 128) & 0xffffffff, BUFFER])] if success else [])
                            if context['trace'] != trace:
                                raise AssertionError(('Runtime serialization platform sequence differs', context['trace'], trace))
                            required = {ENTRIES[0], ENTRIES[1], ENTRIES[2]}
                            if success:
                                required |= {ENTRIES[3], 0x0207db94, 0x0207da70, 0x0207daa0}
                            if not required <= context['seen']:
                                raise AssertionError('Runtime serialization required native/C entries absent')
                            executed.update(context['seen'])
                        if success:
                            hashes.add(sha(serialized))
                        cases += 1
    source = 'verify_runtime_save_commit.py'
    report = {'schemaVersion': 1, 'romSha256': inputs['rom']['sha256'], 'saveSha256': inputs['save']['sha256'], 'arm9Sha256': sha(arm), 'matches': [], 'oracleSource': source, 'oracleSourceSha256': sha((ROOT / source).read_bytes()), 'oracle': {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 500000, 'elapsedSecondsLimit': 2, 'verifiedReturnPcStackAndCalleeSavedR4ThroughR11': True, 'randomizedInitialStack': True, 'sourcePatchedFunctions': len(functions), 'executedSourceOrRetainedEntries': [hex(address) for address in sorted(executed)], 'distinctExpectedSerializedBankHashes': len(hashes), 'platformProviders': {hex(address): role for address, role in PROVIDERS.items()}, 'retainedNative': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in RETAINED.items()], 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values()], 'independentModels': [{'source': source, 'sha256': sha((ROOT / source).read_bytes())}, {'source': 'mechanics_save_runtime_commit_oracle.py', 'sha256': sha((ROOT / 'mechanics_save_runtime_commit_oracle.py').read_bytes())}, {'source': 'verify_save_protocol.py', 'sha256': sha((ROOT / 'verify_save_protocol.py').read_bytes())}]}, 'observations': ['Three party blocks followed by three reserve blocks write back by saved identity before serialization; duplicate identities preserve native last-writer order.', 'The serializer consumes four actual RAM sections, actual summary consumers, and both native/recompiled checksum bodies; expected complete bank bytes, untouched padding and surrounding guards agree.', 'Allocation failure preserves prior writeback, stores the truncated heap and null buffer pointer, and skips header, clock, summary and checksum effects.', 'Successful buffer free receives a sign-extended stored heap byte, invokes the free provider and clears the global buffer pointer.', 'Both captured banks seed isolated RAM fixtures; distinct, duplicate, absent, zero and mixed IDs and signed heap boundaries are covered.'], 'limitations': ['Allocator, free, date and time are bounded providers; the two SDK memory primitives remain original native ARM.', 'The produced bank exists only in a private mapped buffer; device persistence, atomicity, chronology and newest-bank selection are outside this proof.', 'Raw32-byte blocks, byte153 and surrounding fields gain no new semantic partition coverage.'], 'inputsUnchanged': verify_inputs(CONFIG) == inputs}
    write_json(ROOT / 'evidence/matches/mechanics-save-runtime-save-commit.json', report)
    print(json.dumps({'cases': cases, 'calls': calls, 'sourcePatchedFunctions': len(functions), 'distinctBanks': len(hashes)}))

if __name__ == '__main__':
    main()
