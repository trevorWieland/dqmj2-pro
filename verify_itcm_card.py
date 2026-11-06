import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x01FF8370
SOURCE = ROOT / 'src/itcm/control36/native_itcm_01ff8370.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ff8370.json'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def bus_word(address):
    return ((address * 2654435761) ^ 0xC37A5B19) & 0xFFFFFFFF


def execute(code, source, extent, destination, stalled, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x027F0000, 0x10000), (0x03000000, 0x20000),
              (0x04000000, 0x1000), (0x04100000, 0x1000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
        engine.mem_write(first, rng.randbytes(size))
    header = [0, 0xFFFFFFFF, 0x00123456, 0x07000000, 0x08888888][vector % 5]
    control = (header & ~0x07000000) | 0xA1000000
    engine.mem_write(0x027FFE60, struct.pack('<I', header))
    engine.mem_write(ADDRESS, code)
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[:3] = [source, destination, extent]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x13 | (0x80 if vector % 2 else 0))
    for register, value in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, value)
    state = {'started': False, 'initialBusyPolls': 2 if stalled else 0, 'word': 0,
             'stallDone': False, 'pageAddress': 0, 'starts': 0, 'dataReads': [], 'statusReads': []}
    writes, visited = [], set()
    def read(uc, access, address, size, value, user):
        if address == 0x040001A4:
            if not state['started']:
                status = 0x80000000 if state['initialBusyPolls'] else 0
                state['initialBusyPolls'] = max(0, state['initialBusyPolls'] - 1)
            elif state['word'] >= 128:
                raise ValueError('Driver polled an already drained synthetic page')
            elif stalled and state['word'] % 17 == 0 and not state['stallDone']:
                status = 0x80000000
                state['stallDone'] = True
            else:
                status = 0x00800000 | (0x80000000 if state['word'] < 127 else 0)
            state['statusReads'].append(status)
            uc.mem_write(address, struct.pack('<I', status))
        elif address == 0x04100010:
            if not state['started'] or state['word'] >= 128:
                raise ValueError('Synthetic page data read without an active command')
            location = (state['pageAddress'] + state['word'] * 4) & 0xFFFFFFFF
            uc.mem_write(address, struct.pack('<I', bus_word(location)))
            state['dataReads'].append(location)
            state['word'] += 1
            state['stallDone'] = False
    def write(uc, access, address, size, value, user):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
        if address == 0x040001A4:
            if state['started'] and state['word'] != 128:
                raise ValueError('Driver started a new page before draining the previous page')
            state.update(started=True, word=0, stallDone=False,
                         pageAddress=int.from_bytes(bytes(uc.mem_read(0x040001A9, 4)), 'big'), starts=state['starts'] + 1)
    def trace(uc, address, size, user):
        if not ADDRESS <= address < ADDRESS + len(code):
            raise ValueError('Controller fixture executed code outside the reconstructed leaf')
        visited.add(address)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, write)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=30000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise ValueError('Controller leaf did not return within the instruction bound')
    alignment = source & 0x1FF
    aligned = source - alignment
    pages = (alignment + extent + 511) // 512
    expected_mmio = [[0x040001A1, 1, 0x80]]
    expected_data, expected_ram = [], []
    for page in range(pages):
        page_address = (aligned + page * 512) & 0xFFFFFFFF
        command = [0xB7, page_address >> 24, page_address >> 16 & 255, page_address >> 8 & 255, page_address & 255, 0, 0, 0]
        expected_mmio.extend([0x040001A8 + index, 1, value] for index, value in enumerate(command))
        expected_mmio.append([0x040001A4, 4, control])
        for index in range(128):
            location = (page_address + index * 4) & 0xFFFFFFFF
            expected_data.append(location)
            relative = page * 512 + index * 4 - alignment
            if 0 <= relative < extent:
                expected_ram.append([destination + relative, 4, bus_word(location)])
    mmio = [write for write in writes if 0x04000000 <= write[0] < 0x04001000]
    ram = [write for write in writes if destination <= write[0] < destination + max(extent, 4)]
    expected_return = (aligned + pages * 512) & 0xFFFFFFFF
    if mmio != expected_mmio or ram != expected_ram or state['dataReads'] != expected_data or state['starts'] != pages:
        raise ValueError('Native/compiled effects failed independent page-command, FIFO-drain or RAM-store assertions')
    if engine.reg_read(matcher.REGISTERS[0]) != expected_return:
        raise ValueError('Native/compiled next-page return differs from the independent arithmetic model')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'controller': state, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != COMPILER_HASH:
        raise ValueError('Controller C compiler pin changed')
    previous = json.loads(REPORT.read_text())
    old = next(entry for entry in previous['matches'] if int(entry['address'], 0) == ADDRESS)
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen controller C source changed')
    flags = old['compilerFlags']
    records, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Controller C stopped matching its complete native span')
    entry, compiled = matches[old['name']]
    native = (ROOT / 'extract/arm9/itcm.bin').read_bytes()[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    vectors = [(source, extent, 0x03002000, stalled) for source in (0, 4, 508, 512, 0x123400, 0x1235FC)
               for extent in (0, 4, 8, 512, 516) for stalled in (False, True)]
    vectors.extend((508, 8, 0x027FFE60, stalled) for stalled in (False, True))
    cases = []
    for index, (source, extent, destination, stalled) in enumerate(vectors):
        expected = execute(native, source, extent, destination, stalled, index)
        actual = execute(compiled, source, extent, destination, stalled, index)
        if expected != actual:
            raise ValueError('Native and compiled controller states differ')
        cases.append({'sourceOffset': hex(source), 'byteExtent': extent, 'destination': hex(destination), 'busyAndReadyStalls': stalled,
                      'pages': expected['controller']['starts'], 'dataReads': len(expected['controller']['dataReads']),
                      'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'instructionLimit': 30000,
                       'nativeHelperCalls': 0, 'verifiedReturn': True, 'independentPageCommandAndFifoModel': True,
                       'configAliasingVectors': 2, 'records': cases,
                       'limitations': ['A deterministic synthetic controller supplies busy/ready states and FIFO words; physical cartridge responses, timing and bus arbitration are unmodeled',
                                       'Source offsets and output stores are word-aligned; zero extents,512-byte page crossings,discarded prefix words,controller stalls and destination aliasing of the cached control header are exercised',
                                       'Registers R0-R12/SP/LR,CPSR,all ordered writes,controller read sequence and initialized memory are compared; no other native function executes']}
    previous.update(matches=[entry], attempts=records, nativeSymbols={})
    REPORT.write_text(json.dumps(previous, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2})


if __name__ == '__main__':
    main()
