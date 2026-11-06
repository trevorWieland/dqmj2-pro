import hashlib
import json
import struct
from pathlib import Path
import match_lowlevel as common
import utility_code
import utility_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/utility-crossreuse04.json'
ADDRESS = 0x037FEDE8
GLOBAL = 0x03805C44
RETURN = 0x05000000
VALUES = [0, 1, 127, 65535, 0x7fffffff, 0x80000000, 0xffffffff, 0x12345678]
GLOBALS = [0, 1, 127, 32767, 32768, 65535, 0xffffffff, 0x12345678]
CURVES = list(range(-32, 161)) + [-0x80000000, -105, -41, -40, 0x7fffffff]


def signed(value):
    return (value + 0x80000000) % 0x100000000 - 0x80000000


def result(first, second, global_value):
    if second < 24:
        scale = global_value * (second + 40) + ((32767 - global_value) << 6)
    elif second <= 104:
        return first
    else:
        scale = -global_value * (second - 40) + ((global_value + 32767) << 6)
    return (signed(first * (scale & 0xffffffff)) >> 21) & 0xffffffff


def engine(code):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address in (0x037FE000, 0x03805000, 0x0301F000, RETURN):
        machine.mem_map(address, 0x1000)
    machine.mem_write(ADDRESS, code)
    writes = []
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    return machine, writes


def execute(machine, writes, first, second, global_value, vector):
    machine.mem_write(GLOBAL, struct.pack('<I', global_value))
    machine.reg_write(UC_ARM_REG_CPSR, ((vector & 15) << 28) | 0x30)
    registers = [((vector + 1) * 0x9e3779b1 + index * 0x6a09e667) & 0xffffffff for index in range(13)] + [0x0301FFF0, RETURN]
    registers[:2] = [first, second & 0xffffffff]
    for register, initial in zip(common.REGISTERS, registers):
        machine.reg_write(register, initial)
    writes.clear()
    machine.emu_start(ADDRESS | 1, RETURN, count=100)
    actual = [machine.reg_read(register) for register in common.REGISTERS]
    expected_writes = [[0x0301FFE8, 4, registers[4]], [0x0301FFEC, 4, RETURN]]
    if machine.reg_read(UC_ARM_REG_PC) != RETURN or actual[0] != result(first, second, global_value) or actual[4:] != registers[4:] or writes != expected_writes:
        raise ValueError('Piecewise fixed-point curve disagrees with independent modulo32/arithmetic-shift evaluation')
    if bytes(machine.mem_read(GLOBAL, 4)) != struct.pack('<I', global_value):
        raise ValueError('Curve unexpectedly changed its scalar global')
    return struct.pack('<16I', *actual, machine.reg_read(UC_ARM_REG_CPSR)) + bytes(machine.mem_read(0x0301FFE8, 8))


def main():
    report = json.loads(REPORT.read_text())
    if len(report['matches']) != 1:
        raise ValueError('Curve fixture requires its frozen one-function batch')
    old = report['matches'][0]
    if old['module'] != 'utility-child-arm7-wram' or old['processor'] != 'arm7' or old['mode'] != 'thumb' or int(old['address'], 0) != ADDRESS:
        raise ValueError('Curve module,CPU,mode or qualified address changed')
    provenance = old['sourceReuseProvenance']
    for path, digest in [(old['source'], old['sourceSha256']), (provenance['source'], provenance['sourceSha256'])]:
        if utility_runtime.sha((ROOT / path).read_bytes()) != digest:
            raise ValueError('Frozen curve C or source provenance changed')
    spec = utility_code.accepted_spec(old)
    flags = old['compilerFlags']
    entry, compiled = utility_code.compile_compare(ROOT / old['source'], dict(spec, compilerPath=ROOT / old['compiler']),
                                                   int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if compiled is None:
        raise ValueError('Curve C stopped matching the complete native Thumb function and data relocation')
    binary = (ROOT / spec['binary']).read_bytes()
    native = binary[ADDRESS - spec['base']:ADDRESS - spec['base'] + spec['bytes']]
    first_machine, first_writes = engine(native)
    second_machine, second_writes = engine(compiled)
    digest = hashlib.sha256()
    vectors = 0
    for curve in CURVES:
        for index, global_value in enumerate(GLOBALS):
            first = VALUES[(index + vectors // 8) % len(VALUES)]
            expected = execute(first_machine, first_writes, first, curve, global_value, vectors)
            actual = execute(second_machine, second_writes, first, curve, global_value, vectors)
            if expected != actual:
                raise ValueError('Native and compiled curve register/flag effects differ')
            digest.update(struct.pack('<IiI', first, curve, global_value) + expected)
            vectors += 1
    entry['sourceReuseProvenance'] = provenance
    entry['oracle'] = {'vectors': vectors, 'nativeAndRecompiledCalls': vectors * 2, 'nativeCalleeCalls': 0, 'verifiedReturn': True,
                       'independentPiecewiseModuloArithmetic': True, 'scalarGlobalAddress': hex(GLOBAL), 'dataMemoryWrites': 0, 'stackWritesPerCall': 2,
                       'stateSha256': digest.hexdigest(),
                       'limitations': ['Signed selector values -32 through160 plus signed extrema and negative crossover cases are checked against eight scalar-global states',
                                       'Unsigned arithmetic wraps modulo2^32 before pinned signed interpretation and arithmetic shift; no floating point approximation is used',
                                       'The scalar/global and parameter application meanings remain unknown; this fixture establishes measured arithmetic effects only',
                                       'All registers/CPSR,callee-saved state,return,two balanced stack-save writes and absence of data writes are checked; no native helper executes or receives credit']}
    report.update(matches=[entry])
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': vectors, 'nativeAndRecompiledCalls': vectors * 2, 'dataWrites': 0, 'stackWritesPerCall': 2})


if __name__ == '__main__':
    main()
