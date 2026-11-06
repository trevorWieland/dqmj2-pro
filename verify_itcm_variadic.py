import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control41/native_itcm_01ffc330.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffc330.json'
ADDRESS = 0x01FFC330
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    arguments = [rng.getrandbits(32) for _ in range(8)]
    arguments[vector % 8] = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][vector % 5]
    engine.mem_write(0x0301FFF0, struct.pack('<IIII', *arguments[4:]))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[:4] = arguments[:4]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
    for register, value in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, value)
    writes, calls, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        if address != 0x020BA848 or calls:
            raise ValueError('Variadic forwarder reached an unexpected external function')
        actual = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        stack = struct.unpack('<IIII', bytes(uc.mem_read(uc.reg_read(matcher.REGISTERS[-2]), 16)))
        if actual != [2, 0x01FFBFBC, 0x01FFC324, 0x01FFC194] or stack != (0x01FFC184, 0x2710, 0x0301FFE0, 1):
            raise ValueError('Eight-argument registration contract differs')
        forwarded = list(struct.unpack('<IIIIIIII', bytes(uc.mem_read(stack[2], 32))))
        if forwarded != arguments:
            raise ValueError('Compiler-homed register and caller-stack variadic words were not preserved in order')
        calls.append({'address': hex(address), 'arguments': actual, 'stackArguments': list(stack), 'forwardedWords': forwarded})
        returned = uc.reg_read(matcher.REGISTERS[-1])
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], 0xB1400000 | vector)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector % 2 else 0))
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != 1 or engine.reg_read(matcher.REGISTERS[0]) != 0xB1400000 | vector:
        raise ValueError('Variadic wrapper failed to return the registration result')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Variadic compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = next(entry for entry in report['matches'] if int(entry['address'], 0) == ADDRESS)
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen variadic C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Variadic C stopped matching its full native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    for vector in range(64):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled variadic frame effects differ')
        cases.append({'vector': vector, 'forwardedWords': expected['calls'][0]['forwardedWords'],
                      'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['abiEvidence'] = {'kind': 'variadic-register-home-forwarder', 'fixedSourceWords': 1, 'registerHomeWords': 4,
                            'forwardedPointerRelativeToEntrySp': -16, 'modeledForwardedWords': 8, 'historicalOriginalDeclarationProven': False}
    entry['oracle'] = {'vectors': 64, 'nativeAndRecompiledCalls': 128, 'syntheticExternalCalls': 128, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'instructionLimit': 2000, 'independentEightWordForwardingAssertions': True, 'records': cases,
                       'limitations': ['This is the pinned MW ARM variadic parameter-home ABI, not a claim of portable contiguous storage for unrelated C locals',
                                       'The external registration API is a deterministic synthetic contract; native callback scheduler and callback bodies do not execute or gain credit',
                                       'All register/CPSR,memory,writes,callback arguments and forwarded register/stack words are compared; more than eight input words and floating-point varargs are outside this fixture']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 64, 'nativeAndRecompiledCalls': 128})


if __name__ == '__main__':
    main()
