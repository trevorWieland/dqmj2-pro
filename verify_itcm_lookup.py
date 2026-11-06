import json
import random
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control43/native_itcm_01ffa8f0.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffa8f0.json'
ADDRESS = 0x01FFA8F0
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    selectors = [((i * 17 + vector * 3) & 255) - 128 for i in range(8)]
    results = [((i * 31 + vector * 7) & 255) - 128 for i in range(8)]
    if vector % 13 == 0:
        selectors = [-128] * 8
    chosen = vector % 10
    value = selectors[chosen] if chosen < 8 else [-129, 128][chosen - 8]
    match = next((index for index, selector in enumerate(selectors) if selector == value), None)
    expected = list(range(8)) if match is None else list(range(match + 1)) + [match]
    for index in range(8):
        pointer = 0x03002000 + index * 0x200
        engine.mem_write(pointer + 0x165, bytes([selectors[index] & 255]))
        engine.mem_write(pointer + 0x16e, bytes([results[index] & 255]))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[0], registers[-2], registers[-1] = value & 0xFFFFFFFF, 0x0301FFF0, 0x05000000
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        index = uc.reg_read(matcher.REGISTERS[0])
        if address != 0x01FFB4EC or len(calls) >= len(expected) or index != expected[len(calls)]:
            raise ValueError('Signed lookup selected a different record or call order')
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append(index)
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], 0x03002000 + index * 0x200)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=1000)
    result = 0 if match is None else results[match] & 0xFFFFFFFF
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or calls != expected or engine.reg_read(matcher.REGISTERS[0]) != result:
        raise ValueError('Signed lookup did not return the first matching signed record value')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Lookup C compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen signed lookup C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Lookup C stopped matching the full native function')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(80):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled signed lookup effects differ')
        external += len(expected['calls']) * 2
        cases.append({'vector': vector, 'indices': expected['calls'], 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': 80, 'nativeAndRecompiledCalls': 160, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'independentFirstMatchAssertions': True, 'records': cases,
                       'limitations': ['The external record accessor uses a synthetic index-to-pointer contract; its native body does not execute or gain credit',
                                       'Signed record fields, all eight search positions, absent values, duplicate selectors and signed return promotion are checked',
                                       'Registers R0-R12/SP/LR,CPSR,ordered writes,call order and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 80, 'nativeAndRecompiledCalls': 160, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
