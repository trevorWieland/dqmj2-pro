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
REPORT = ROOT / 'evidence/matches/utility-crossreuse01.json'
ADDRESS = 0x020103C0
RETURN = 0x05000000
MMIO = 0x04000304


def engine(code):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address, size in [(0x02010000, 0x1000), (0x0301F000, 0x1000), (0x04000000, 0x1000), (RETURN, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(ADDRESS, code)
    writes = []
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    return machine, writes


def execute(machine, writes, value):
    machine.mem_write(MMIO, struct.pack('<H', value))
    machine.reg_write(UC_ARM_REG_CPSR, ((value & 15) << 28) | 0x30)
    registers = [((value + 1) * 0x9e3779b1 + index * 0x6a09e667) & 0xffffffff for index in range(13)] + [0x0301FFF0, RETURN]
    for register, initial in zip(common.REGISTERS, registers):
        machine.reg_write(register, initial)
    writes.clear()
    machine.emu_start(ADDRESS | 1, RETURN, count=100)
    result = [machine.reg_read(register) for register in common.REGISTERS]
    if machine.reg_read(UC_ARM_REG_PC) != RETURN or result[0] != value & 1 or result[4:] != registers[4:] or writes:
        raise ValueError('MMIO low-bit query changed state or returned a different Boolean')
    return struct.pack('<16I', *result, machine.reg_read(UC_ARM_REG_CPSR))


def main():
    report = json.loads(REPORT.read_text())
    if len(report['matches']) != 1:
        raise ValueError('Exhaustive MMIO fixture requires its frozen one-function batch')
    old = report['matches'][0]
    if old['module'] != 'utility-child-arm9-main' or old['processor'] != 'arm9' or old['mode'] != 'thumb' or int(old['address'], 0) != ADDRESS:
        raise ValueError('MMIO function identity or program-qualified mode changed')
    provenance = old['sourceReuseProvenance']
    for filename, digest in [(old['source'], old['sourceSha256']), (provenance['source'], provenance['sourceSha256'])]:
        if utility_runtime.sha((ROOT / filename).read_bytes()) != digest:
            raise ValueError('Frozen MMIO C or original C reuse provenance changed')
    spec = utility_code.accepted_spec(old)
    flags = old['compilerFlags']
    entry, compiled = utility_code.compile_compare(ROOT / old['source'], dict(spec, compilerPath=ROOT / old['compiler']),
                                                   int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if compiled is None:
        raise ValueError('MMIO C no longer matches the complete native Thumb span')
    binary = (ROOT / spec['binary']).read_bytes()
    native = binary[ADDRESS - spec['base']:ADDRESS - spec['base'] + spec['bytes']]
    first, first_writes = engine(native)
    second, second_writes = engine(compiled)
    digest = hashlib.sha256()
    for value in range(65536):
        expected, actual = execute(first, first_writes, value), execute(second, second_writes, value)
        if expected != actual:
            raise ValueError('Native and freshly recompiled MMIO query register/flag effects differ')
        digest.update(struct.pack('<H', value) + expected)
    entry['sourceReuseProvenance'] = provenance
    entry['oracle'] = {'vectors': 65536, 'nativeAndRecompiledCalls': 131072, 'nativeHelperCalls': 0, 'verifiedReturn': True,
                       'exhaustiveHalfwordDomain': True, 'inputAddress': hex(MMIO), 'inputWidth': 2,
                       'independentLowBitAssertion': True, 'emulatedMemoryWrites': 0, 'instructionLimitPerCall': 100,
                       'stateSha256': digest.hexdigest(),
                       'limitations': ['All 65536 synthetic halfword states are checked; physical MMIO side effects, timing and hardware ownership are not modeled',
                                       'Complete R0-R12/SP/LR,CPSR effects match; callee-saved state and absence of emulated writes are independently required',
                                       'The native instruction stream and fresh MW-generated C stream execute independently with identical reset state; no native helper or historical source declaration is claimed']}
    report.update(matches=[entry], nativeSymbols={}, nativeSymbolBindings=[])
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 65536, 'nativeAndRecompiledCalls': 131072, 'emulatedWrites': 0})


if __name__ == '__main__':
    main()
