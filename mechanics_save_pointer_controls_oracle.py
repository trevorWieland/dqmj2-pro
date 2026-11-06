import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write
from verify_save_protocol import PARTS

CONTROL = 0x021c0e68
STOP = 0x027ff800
POINTERS = {'saved_raw_controls_pointer': CONTROL, 'saved_section3_base_pointer': 0x021bb278, 'saved_identity_array_pointer': 0x021bb2b8, 'saved_section3_word228c_pointer': 0x021bd504, 'saved_section3_word2290_pointer': 0x021bd508, 'saved_section3_buffer1994_pointer': 0x021bcc0c, 'saved_section3_buffer1a94_pointer': 0x021bcd0c, 'saved_section3_pair2284_pointer': 0x021bd4fc}
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

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
    rng = random.Random(202610278)
    vectors = [('saved_raw_controls_reset', bank, value, pattern) for bank in (0, 0x7100) for value in (0, 1, 9999, 65535) for pattern in range(4)]
    vectors += [(name, bank, 65535, pattern) for name in POINTERS for bank in (0, 0x7100) for pattern in (0, 3)]
    cases = calls = 0
    for name, bank, count, pattern in vectors:
        original = {0x021b9000: bytearray(rng.randbytes(0xa000))}
        for start, end, address in PARTS:
            write(original, address, save[bank + start:bank + end])
        data = bytes(16) if pattern == 0 else bytes([255]) * 16 if pattern == 1 else b'\x55\xaa' * 8 if pattern == 2 else rng.randbytes(16)
        write(original, CONTROL + 0x68, data)
        write(original, CONTROL + 0x64, struct.pack('<H', count))
        expected = {address: bytearray(value) for address, value in original.items()}
        if name == 'saved_raw_controls_reset':
            write(expected, CONTROL + 0x64, bytes(2))
            write(expected, CONTROL + 0x68, bytes([255]) * 16)
            result = None
        else:
            result = POINTERS[name]
        row, code = matches[name]
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        for machine in machines:
            for address, value in original.items():
                machine.mem_write(address, bytes(value))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, rng.getrandbits(32))
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=10000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                raise AssertionError(('Raw pointer/control bounded return/ABI', name, bank, count, pattern))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Raw section/control pointer result', name, result))
            for address, value in expected.items():
                if bytes(machine.mem_read(address, len(value))) != value:
                    raise AssertionError(('Raw section/control complete RAM guard', name, bank, count, pattern))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 10000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentPointerAnd18ByteResetModel': True, 'platformStubs': {}, 'retainedNative': [], 'reusedAcceptedSources': [], 'pointerAddresses': {name: hex(address) for name, address in POINTERS.items()}, 'observations': ['The reset writes0xFF into each of eight bytes at offsets0x68 and0x70 and clears only the halfword at0x64, preserving reserved bytes and all surrounding state.', 'The eight no-argument getters return qualified main-module saved/control pointers without changing RAM.', 'Both copied banks, zero/one/9999/65535 halfword states, zero/FF/alternating/random byte patterns and randomized incoming ABI state are covered.'], 'limitations': ['Pointer identities and raw reset effects establish no complete field purpose, selection bounds or semantic-partition promotion.', 'No native helper or platform provider is substituted, and original inputs remain unchanged.']}
