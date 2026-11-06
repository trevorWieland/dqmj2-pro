import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x01FFC198
SOURCE = ROOT / 'src/itcm/control40/native_itcm_01ffc198.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffc198.json'
VALUES = [-2147483648, -101, -10, -9, -1, 0, 1, 9, 10, 101, 2147483647]
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, value, initialized, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    status, other = 0x03002000, 0x03004000
    other_value = [-2147483648, 0, 2147483647, -77][vector % 4]
    engine.mem_write(other, struct.pack('<i', other_value))
    old_handles = [0x12340000 | vector, 0xA5A50000 | (vector + 7)]
    new_handles = [0xEF120000 | (vector + 31), 0xCF560000 | (vector + 63)]
    engine.mem_write(0x01FFFAB8, struct.pack('<II', *old_handles))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
    for register, contents in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, contents)
    expected = [(0x01FFBB38, []), (0x02067DD4, []), (0x01FFBB38, []), (0x020894C8, []), (0x01FFBB38, []), (0x020271C8, [])]
    labels = [0x020E2C98, 0x020E2CA4] if initialized else [0x020E2C80, 0x020E2C8C]
    for index, pointer in enumerate((0x01FFFAAC, 0x01FFFAA8)):
        expected.append((0x020BA598, [old_handles[index] & 255 if initialized else 0, labels[index], pointer]))
    if not initialized:
        expected.append((0x020271D8, []))
    expected.append((0x020BA7C4, [2, 0x01FFBFBC, 0x01FFBFFC, 0x01FFC194]))
    writes, calls, visited = [], [], set()
    ui_calls = 0
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, contents, user: writes.append([address, size, contents & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        nonlocal ui_calls
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        index = len(calls)
        if index >= len(expected) or address != expected[index][0]:
            raise ValueError('Status protocol called an unexpected function/order')
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if arguments[:len(expected[index][1])] != expected[index][1]:
            raise ValueError({'stage': index, 'actual': arguments, 'expected': expected[index][1]})
        stack = bytes(uc.mem_read(uc.reg_read(matcher.REGISTERS[-2]), 8))
        if address == 0x020BA7C4 and struct.unpack('<II', stack) != (0x01FFC184, 0x2710):
            raise ValueError('Six-argument callback registration lost its two stack arguments')
        if address == 0x01FFBB38:
            result = status
        elif address == 0x02067DD4:
            result = value & 0xFFFFFFFF
        elif address == 0x020894C8:
            result = other
        elif address == 0x020271C8:
            result = 7 if initialized else 0
        elif address == 0x020BA598:
            result = new_handles[ui_calls]
            ui_calls += 1
        elif address == 0x020BA7C4:
            result = 0x93000000 | vector
        else:
            result = rng.getrandbits(32)
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'stage': index, 'address': hex(address), 'arguments': arguments, 'stack': stack.hex()})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Status protocol failed to complete and return')
    quotient = abs(value) // 10 * (-1 if value < 0 else 1)
    required = {status: value & 0xFFFFFFFF, status + 4: 0, 0x01FFFAAC: other_value & 0xFFFFFFFF,
                0x01FFFAA8: quotient & 0xFFFFFFFF, 0x01FFFAB8: old_handles[0] if initialized else new_handles[0],
                0x01FFFABC: old_handles[1] if initialized else new_handles[1]}
    if any(struct.unpack('<I', bytes(engine.mem_read(address, 4)))[0] != contents for address, contents in required.items()):
        raise ValueError('Independent signed division/status/handle state assertion failed')
    if engine.reg_read(matcher.REGISTERS[0]) != 0x93000000 | vector:
        raise ValueError('Final callback-registration result was not returned')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Status compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = next(entry for entry in report['matches'] if int(entry['address'], 0) == ADDRESS)
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen status C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Status C stopped matching its complete native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases, calls = [], 0
    for value in VALUES:
        for initialized in (False, True):
            for irq in range(2):
                vector = len(cases)
                expected, actual = execute(native, value, initialized, vector), execute(compiled, value, initialized, vector)
                if expected != actual:
                    raise ValueError('Native and compiled status protocol differ')
                calls += len(expected['calls']) * 2
                cases.append({'vector': vector, 'signedInput': value, 'initialized': initialized,
                              'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': calls, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'instructionLimit': 2000, 'independentSignedQuotientAndStateAssertions': True, 'records': cases,
                       'limitations': ['External pointer/value/initialization/display/task-registration APIs use deterministic synthetic contracts; their native bodies and callback scheduler are not executed',
                                       'Signed32 extrema,negative/positive division truncation,initialization/update paths,handle-byte extraction and six-argument callback registration are checked',
                                       'All register/CPSR,ordered write,call argument,stack and initialized memory states are compared; no callee gains source credit']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': calls})


if __name__ == '__main__':
    main()
