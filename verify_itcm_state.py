import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control44/native_itcm_01ffb060.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffb060.json'
ADDRESS = 0x01FFB060
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x200000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    value = [0, 1, 2, 0x7fffffff, 0x80000000, 0xffffffff][vector % 6]
    handle = 0 if vector % 3 == 0 else rng.getrandbits(32) | 1
    changed = rng.getrandbits(32)
    target = 0x03004000
    original = [0, 2, 0xffffffff, rng.getrandbits(32)][vector % 4]
    engine.mem_write(0x01FFF97C, struct.pack('<I', handle))
    engine.mem_write(0x021CEBE0, rng.randbytes(32))
    engine.mem_write(target + 0x7c, struct.pack('<I', original))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[0], registers[-2], registers[-1] = value, 0x0301FFF0, 0x05000000
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        expected = [(0x0205FA4C, [0x01FFF960, value]), (0x0205F98C, [changed, 0])]
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if not handle or len(calls) >= 2 or (address, arguments[:2]) != expected[len(calls)]:
            raise ValueError('State update did not forward the explicit context/value or reload the changed handle')
        if address == 0x0205FA4C:
            uc.mem_write(0x01FFF97C, struct.pack('<I', changed))
            writes.append([0x01FFF97C, 4, changed])
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], target if address == 0x0205F98C else rng.getrandbits(32))
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=1000)
    updated = struct.unpack('<I', bytes(engine.mem_read(target + 0x7c, 4)))[0]
    flag = bytes(engine.mem_read(0x021CEBE4, 1))[0]
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != (2 if handle else 0):
        raise ValueError('State update did not return with the required external call count')
    if flag != (2 if value == 1 else 0) or updated != (original & ~2 if handle else original):
        raise ValueError('State byte or target flag clear differs from the independent expected effects')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('State C compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen state update C changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('State C stopped matching the complete native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(48):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled state effects differ')
        external += len(expected['calls']) * 2
        cases.append({'vector': vector, 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': 48, 'nativeAndRecompiledCalls': 96, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'independentStateAndReloadAssertions': True, 'records': cases,
                       'limitations': ['Two external functions use explicit synthetic context/handle/result contracts; native callees do not execute or gain credit',
                                       'The first callee changes the global handle, requiring a real reload before the second call',
                                       'Void-source return has no semantic value; all registers/CPSR,ordered writes,call arguments and initialized memory are still compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 48, 'nativeAndRecompiledCalls': 96, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
