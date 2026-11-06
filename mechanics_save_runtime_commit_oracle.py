import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_record_update_oracle import lookup

RECORDS = 0x021bd674
RUNTIME = 0x021c0ef4
PARTY = RUNTIME + 32
ENEMY = PARTY + 1584
RESERVE = ENEMY + 1584
FOURTH = RESERVE + 1584
RAW153 = 0x021bd66f
GOLD = 0x021bd538
MODE = 0x020f69e8
STOP = 0x027ff800
SAVED_REGISTERS = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x020443ec, 0x02062a10, 0x02062b1c, 0x02063f88}
    result = {}
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if row.get('module') not in ('main', 'arm9') or address not in wanted:
                continue
            if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Runtime commit source dependency identity differs')
            with (root / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            for relocation in row.get('relocations', []):
                at = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                previous = struct.unpack_from('<I', code, at)[0]
                value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
                struct.pack_into('<I', code, at, value & 0xffffffff)
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Runtime commit source dependency bytes differ')
            result[address] = (row, bytes(code))
    if set(result) != wanted:
        raise AssertionError(('Runtime commit source dependency absent', sorted(wanted - set(result))))
    return result

def expected(memory, name, arguments, mode):
    if name == 'saved_runtime_rawb3_set':
        for index, value in enumerate(arguments):
            write(memory, ENEMY + index * 528 + 179, bytes([(value if mode == 0 else 0) & 255]))
    elif name == 'saved_runtime_fourth_markers':
        if mode in (0, 4, 7, 8):
            write(memory, FOURTH, bytes(1584))
            for index in range(3):
                write(memory, FOURTH + index * 528 + 46, b'\xff\xff')
        elif mode not in (5, 6):
            for index, value in enumerate(arguments):
                write(memory, FOURTH + index * 528 + 46, struct.pack('<H', value & 65535))
    elif name == 'saved_runtime_blocks_commit':
        for group in (PARTY, RESERVE):
            for index in range(3):
                view = group + index * 528
                record = lookup(memory, u32(memory, view + 4))
                if record:
                    write(memory, record + 32, read(memory, view + 284, 32))
        put(memory, GOLD, u32(memory, RUNTIME))
        write(memory, RAW153, b'\0')
    elif name == 'saved_runtime_gold_get':
        return u32(memory, RUNTIME)
    elif name == 'saved_runtime_gold_exchange':
        previous = u32(memory, RUNTIME)
        put(memory, RUNTIME, arguments[0])
        return previous
    else:
        raise AssertionError('Unexpected runtime commit function')
    return None

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = []
    arguments = ((0, 1, 255), (-1, 256, -257), (-32768, 32767, 65535), (-0x80000000, 0x7fffffff, 65536))
    for name in matches:
        if name in ('saved_runtime_rawb3_set', 'saved_runtime_fourth_markers'):
            vectors.extend((name, args, mode, 'distinct', 0) for mode in range(256) for args in arguments)
        else:
            vectors.extend((name, (value, 0, 0), 0, label, bank) for label in ('distinct', 'duplicate-record-ids', 'duplicate-runtime-ids', 'missing-ids', 'zero-ids', 'mixed-ids') for bank in (0, 0x7100) for value in (0, 1, 9999999, 10000000, 0x80000000, 0xffffffff))
    cases = calls = 0
    for name, args, mode, label, bank in vectors:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0xa000))}
        write(original, 0x021bd51c, save[bank + 0x90:bank + 0x3a68])
        write(original, MODE, bytes([mode]))
        for index in range(100):
            data = bytearray(rng.randbytes(132))
            identity = 1 if label == 'duplicate-record-ids' and index < 3 else index + 1
            struct.pack_into('<I', data, 20, identity)
            write(original, RECORDS + index * 132, bytes(data))
        identities = [1, 2, 3, 4, 5, 6] if label in ('distinct', 'duplicate-record-ids') else [1] * 6 if label == 'duplicate-runtime-ids' else [0xffffffff] * 6 if label == 'missing-ids' else [0] * 6 if label == 'zero-ids' else [1, 0, 0xffffffff, 3, 1, 2]
        for ordinal, (group, index) in enumerate((group, index) for group in (PARTY, RESERVE) for index in range(3)):
            view = group + index * 528
            put(original, view + 4, identities[ordinal])
            write(original, view + 284, bytes([(ordinal + 1) * 31 & 255]) * 32)
        put(original, RUNTIME, (args[0] ^ 0xa5a55a5a) & 0xffffffff if name == 'saved_runtime_gold_exchange' else args[0] & 0xffffffff)
        write(original, RAW153, b'\xa5')
        memory = {address: bytearray(data) for address, data in original.items()}
        result = expected(memory, name, args, mode)
        incoming = [rng.getrandbits(32) for register in SAVED_REGISTERS]
        stack = rng.randbytes(0x10000)
        row, code = matches[name]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED_REGISTERS, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), args):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=500000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                raise AssertionError(('Runtime commit bounds/stack', name, mode, label))
            if [machine.reg_read(register) for register in SAVED_REGISTERS] != incoming:
                raise AssertionError(('Runtime commit callee-saved ABI', name, mode, label))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Runtime snapshot return', name, args, result))
            for address, data in memory.items():
                if bytes(machine.mem_read(address, len(data))) != data:
                    raise AssertionError(('Runtime commit saved/view/purse/raw153/guard RAM', name, mode, label, args))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 500000, 'elapsedSecondsLimit': 2, 'returnPcAndStackVerified': True, 'calleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentExpectedSavedBlocksPurseFlagsAndRuntimeModes': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008c58', 'bytes': 76, 'sha256': sha(arm[0x8c58:0x8ca4]), 'role': 'SDK bulk word fill'}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Writeback looks up three party view IDs, then three reserve view IDs, and copies each found32-byte block into saved record+0x20; repeated IDs are sequential last-writer-wins with the last reserve slot last.', 'Missing/zero IDs skip block writes but do not skip the unconditional saved-purse copy or reset of raw saved byte+0x153 at bank0x1E3.', 'Runtime snapshot exchange preserves all32 bits and returns the previous word; no cap is imposed by these bodies.', 'The raw view byte+0xB3 is set from truncated arguments only in mode0 and cleared in every other mode.', 'The fourth-view dispatcher clears/marks three views in modes0/4/7/8, preserves them in modes5/6, and stores truncated species markers for all other mode bytes including9..255.', 'Every mode byte, signed/unsigned value boundaries, both copied banks, duplicate record IDs, repeated runtime IDs and absent references are exercised.'], 'limitations': ['The76-byte SDK bulk fill remains native ARM; no gameplay or platform provider is substituted.', 'The32-byte block includes more than the16-byte stat array; field purpose, legal quantities and raw byte153 meaning remain unresolved.', 'Default fourth-view behavior on out-of-range modes is a native byte observation rather than a valid scene-mode claim.', 'No new semantic partition bytes or original save/game data are changed.']}
