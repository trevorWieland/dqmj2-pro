import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

BASE = 0x021c0ef4
GROUPS = tuple(BASE + 32 + index * 1584 for index in range(4))
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def find(memory, group, identity):
    for ordinal in ((1, 3) if group & 1 else (0, 2)):
        for index in range(3):
            address = GROUPS[ordinal] + index * 528
            if struct.unpack_from('<I', memory, address - BASE + 4)[0] == identity:
                return address
    return 0

def validate(arm, save, matches, root):
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in matches.values():
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(202610272)
    modes = (0, 1, 2, 3, 4, 5, 6, 7, 127, 128, 255, 256, -1, -2, -2147483648, 2147483647)
    vectors = [(mode, index, target, label) for mode in modes for index in range(3) for target in (*range(13), 0xffffffff) for label in ('distinct', 'all-zero', 'all-duplicate', 'pair-duplicate', 'sparse')]
    vectors.extend((mode, mode % 3, (mode % 12) + 1, 'distinct') for mode in range(256))
    cases = calls = 0
    for mode, index, target, label in vectors:
        original = bytearray(rng.randbytes(0x2000))
        for ordinal in range(12):
            identity = ordinal + 1 if label == 'distinct' else 0 if label == 'all-zero' else 1 if label == 'all-duplicate' else ordinal // 2 + 1 if label == 'pair-duplicate' else ordinal + 1 if ordinal % 3 == 0 else 0
            address = GROUPS[ordinal // 3] + (ordinal % 3) * 528
            struct.pack_into('<I', original, address - BASE + 4, identity)
        pointer = find(original, mode, target)
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        for name in ('saved_runtime_view_find', 'saved_runtime_view_swap'):
            memory = bytearray(original)
            if name == 'saved_runtime_view_find':
                arguments = (mode, target, rng.getrandbits(32))
                result = pointer
            else:
                arguments = (mode, index, target)
                selected = GROUPS[0 if mode == 0 else 2 if mode == 2 else 1 if mode == 1 else 3] + index * 528
                if pointer:
                    first = bytes(memory[selected - BASE:selected - BASE + 528])
                    second = bytes(memory[pointer - BASE:pointer - BASE + 528])
                    memory[selected - BASE:selected - BASE + 528] = second
                    memory[pointer - BASE:pointer - BASE + 528] = first
                result = int(bool(pointer))
            row, code = matches[name]
            for machine in machines:
                machine.mem_write(BASE - 0x100, b'\x6e' * 0x100 + bytes(original) + b'\xc3' * 0x100)
                machine.mem_write(0x027f0000, stack)
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                    machine.reg_write(register, value & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=50000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                    raise AssertionError(('Runtime view swap bounded return/ABI', name, mode, index, target, label))
                if machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Runtime view find/swap result', name, mode, index, target, label, result))
                if bytes(machine.mem_read(BASE - 0x100, 0x2200)) != b'\x6e' * 0x100 + bytes(memory) + b'\xc3' * 0x100:
                    raise AssertionError(('Runtime view find/swap complete state and guards', name, mode, index, target, label))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 50000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentComplete528ByteSwapAndPointerModel': True, 'platformStubs': {}, 'retainedNative': [{'module': 'main', 'mode': 'ARM', 'address': '0x02008e0c', 'bytes': 304, 'sha256': sha(arm[0x8e0c:0x8f3c]), 'role': 'SDK byte copy'}], 'observations': ['Lookup selects party then reserve when argument bit0 is clear, enemy then fourth when set; it returns the first identity match, including zero identities.', 'Swap selects party for group0, reserve for2, enemy for1 and fourth for every other argument; its lookup still uses only argument bit0.', 'A found source swaps every528 bytes through a stack temporary; self-swap preserves state, and an absent identity returns0 without writes.', 'All256 byte-valued group arguments, negative/large signed arguments, every valid selected slot, duplicates, zero IDs and missing identities are covered.'], 'limitations': ['The304-byte SDK byte-copy function remains native ARM, with no substituted provider.', 'Selected slot indices are limited to0..2; native unchecked pointer arithmetic does not prove larger indices are legal.', 'Working view/group names do not establish scene semantics or saved field meanings.']}
