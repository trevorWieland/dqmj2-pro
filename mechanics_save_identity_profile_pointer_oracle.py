import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(arm, save, matches, root):
    document = json.loads((root / 'evidence/matches/mechanics-save-pointer-controls.json').read_text(encoding='utf-8'))
    row = next(row for row in document['matches'] if row['address'] == '0x2063e98')
    if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
        raise AssertionError('Identity profile base source/object identity differs')
    with (root / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
        code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
    for relocation in row['relocations']:
        if relocation['type'] != 2:
            raise AssertionError('Identity profile base relocation differs')
        struct.pack_into('<I', code, relocation['offset'], int(relocation['target'], 16) + relocation['addend'])
    if code != arm[0x63e98:0x63ea4]:
        raise AssertionError('Identity profile base native span differs')
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            machine.mem_write(0x02063e98, bytes(code))
            for match, compiled in matches.values():
                machine.mem_write(int(match['address'], 16), compiled)
        machines.append(machine)
    rng = random.Random(202610279)
    calls = 0
    for pattern in range(4):
        memory = bytes([0]) * 0x1000 if pattern == 0 else bytes([255]) * 0x1000 if pattern == 1 else rng.randbytes(0x1000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            machine.mem_write(0x021bb000, memory)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(0x020685b0, STOP, count=1000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                raise AssertionError('Identity profile pointer bounded return/ABI differs')
            if machine.reg_read(UC_ARM_REG_R0) != 0x021bb278 or bytes(machine.mem_read(0x021bb000, 0x1000)) != memory:
                raise AssertionError('Identity profile pointer/guard differs')
            calls += 1
    return {'engine': 'Unicorn', 'cases': 4, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'platformStubs': {}, 'retainedNative': [], 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')}], 'observations': ['The ARM profile getter tail-calls the accepted section3-base getter and returns0x021BB278 without RAM effects.'], 'limitations': ['The raw profile pointer establishes no complete identity/profile format or semantic partition meanings.']}
