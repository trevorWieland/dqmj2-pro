import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x01FFB398
SOURCE = ROOT / 'src/itcm/control39/native_itcm_01ffb398.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffb398.json'
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for address, size in ranges:
        engine.mem_map(address, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
    for register, value in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, value)
    resource = 0x03008000 + vector * 4
    block = 0x0301FFDC
    zero = block - 4
    pointers = [0x03002000, 0x03004000, 0x03006000]
    sizes = [8 + vector * 4, 28 + vector * 8, 68 + vector * 12]
    expected = [(0x0203CC2C, [0x020DE770, 2]),
                (0x0204518C, [block, resource, 0]),
                (0x0204820C, [pointers[0], 0, sizes[0]]),
                (0x0204820C, [zero, 0, 2]),
                (0x0204518C, [block, resource, 1]),
                (0x02045490, [1, pointers[1], 0, sizes[1]]),
                (0x0204518C, [block, resource, 2]),
                (0x02045994, [1, pointers[2], 0, sizes[2]]),
                (0x0202A498, [2, resource]), (0x02048308, []),
                (0x02223C24, [1, sizes[1]]), (0x022239AC, []), (0x022159B8, [0x020DE784, 4])]
    writes, calls, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        index = len(calls)
        if index >= len(expected) or address != expected[index][0]:
            raise ValueError('Block protocol called a different function or order')
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if arguments[:len(expected[index][1])] != expected[index][1]:
            raise ValueError({'stage': index, 'actual': arguments, 'expected': expected[index][1]})
        if index == 3 and bytes(uc.mem_read(zero, 2)) != b'\0\0':
            raise ValueError('Caller did not initialize the separate halfword input')
        if address == 0x0204518C:
            section = arguments[2]
            for location, value in ((block, pointers[section]), (block + 4, sizes[section])):
                uc.mem_write(location, struct.pack('<I', value))
                writes.append([location, 4, value])
        returned = uc.reg_read(matcher.REGISTERS[-1])
        result = resource if index == 0 else (0x8AD00000 | vector) if index == 12 else rng.getrandbits(32)
        calls.append({'stage': index, 'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Block protocol did not return after its complete contract sequence')
    if engine.reg_read(matcher.REGISTERS[0]) != 0x8AD00000 | vector:
        raise ValueError('Caller did not propagate the final external return value')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'calls': calls, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Block C compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = next(entry for entry in report['matches'] if int(entry['address'], 0) == ADDRESS)
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen block-record C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Block-record C stopped matching its full native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    offset = ADDRESS - 0x01FF8000
    native = binary[offset:offset + entry['bytes']]
    cases = []
    for vector in range(24):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled block-record protocol effects differ')
        cases.append({'vector': vector, 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode()), 'calls': expected['calls']})
    entry['oracle'] = {'vectors': 24, 'nativeAndRecompiledCalls': 48, 'syntheticExternalCalls': 624, 'nativeCalleeCalls': 0,
                       'instructionLimit': 2000, 'verifiedReturn': True, 'independentContractAssertions': True, 'records': cases,
                       'limitations': ['External functions use explicit synthetic resource/pointer/size contracts; native helper bodies and graphics hardware are not executed',
                                       'All three output records are populated with distinct sizes, and the second size must survive the third record overwrite',
                                       'Registers R0-R12/SP/LR,CPSR,ordered writes,call arguments,stack and initialized memory are compared; no callee gets source credit']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 24, 'nativeAndRecompiledCalls': 48, 'syntheticExternalCalls': 624})


if __name__ == '__main__':
    main()
