import random
import struct
import match_runtime as compiler
from project import ROOT, configuration, now, read_json, sha256, write_json
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR

ADDRESS = 0x021D8D48
ARENA = 0x03002000
STOP = 0x0301E000
SOURCE = 'src/runtime/ov007-enable01/native_ov007_021d8d48.c'
SOURCE_HASH = '7218a55ae73be8b0f78875964f84995b758346791614280c52e18cac0f129aba'
MASKS = [0, 65535, *(1 << index for index in range(16))]


def execute(code, mask, seed):
    rng = random.Random(20261027007 + seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x200000)
    machine.mem_map(0x03000000, 0x20000)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(0x021DA9E8, struct.pack('<I', ARENA))
    before = rng.randbytes(0x1000)
    machine.mem_write(ARENA, before)
    machine.mem_write(0x0301F000, rng.randbytes(0x1000))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    registers = [rng.getrandbits(32) for unused in compiler.REGISTERS]
    registers[-2:] = [0x0301FFF0, STOP]
    for register, value in zip(compiler.REGISTERS, registers):
        machine.reg_write(register, value)
    calls, writes, visited = [], [], set()
    def observe(uc, address, size, data):
        if ADDRESS <= address < ADDRESS + 108:
            visited.add(address)
            return
        args = [uc.reg_read(register) for register in compiler.REGISTERS[:4]]
        index = len(calls) // 2
        if address == 0x021D873C:
            if len(calls) % 2 or args[0] != index or not 0 <= index < 16:
                raise ValueError('Unexpected predicate call')
            result = (mask >> index) & 1
        elif address == 0x02048A44:
            if len(calls) % 2 != 1 or args[:2] != [ARENA + index * 144 + 8, 1]:
                raise ValueError('Unexpected object callback call')
            result = (0xA5C00000 + index * 257 + seed) & 0xFFFFFFFF
        else:
            raise ValueError('Execution escaped explicit caller and synthetic contracts')
        calls.append([address, args])
        for number, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (result ^ ((number + 1) * 0x7654321)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, (len(calls) & 15) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data: writes.append([address, size, value]))
    machine.emu_start(ADDRESS, STOP, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or len(calls) != 32:
        raise ValueError('Caller did not return after all sixteen records')
    expected = bytearray(before)
    for index in range(16):
        offset = index * 144 + 124
        prior = struct.unpack_from('<I', expected, offset)[0]
        value = prior | 2 if mask >> index & 1 else prior & ~2
        struct.pack_into('<I', expected, offset, value)
    after = bytes(machine.mem_read(ARENA, len(expected)))
    actual = [machine.reg_read(register) for register in compiler.REGISTERS]
    if after != expected or actual[4:12] != registers[4:12] or machine.reg_read(UC_ARM_REG_SP) != registers[-2]:
        raise ValueError('Independent record-bit or preserved-register model differs')
    if actual[0] != (0xA5C00000 + 15 * 257 + seed) & 0xFFFFFFFF:
        raise ValueError('Final callback result differs')
    return {'registers': actual, 'flags': machine.reg_read(UC_ARM_REG_CPSR), 'memorySha256': compiler.sha(after), 'stackSha256': compiler.sha(bytes(machine.mem_read(0x0301F000, 0x1000))), 'writes': writes, 'calls': calls, 'visited': sorted(visited)}


def main():
    source = ROOT / SOURCE
    if sha256(source) != SOURCE_HASH:
        raise ValueError('Frozen source changed')
    binary = ROOT / 'extract/arm9_overlays/ov007.bin'
    module = next(item for item in read_json(ROOT / 'provenance/seed-manifest.json')['modules'] if item['name'] == 'ov007')
    if sha256(binary) != module['sha256']:
        raise ValueError('Overlay input identity changed')
    unused, found = compiler.compare(source, 'ov007', 2, 'off', True)
    entry, rebuilt = found['native_ov007_021d8d48']
    native = binary.read_bytes()[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 112]
    bindings = {}
    for relocation in entry['relocations']:
        name = relocation['symbol']
        function = name.startswith('native_fn_')
        bindings[name] = {'processor': 'arm9', 'module': 'ov007' if '_ov007_' in name else 'main', 'address': relocation['target'], 'mode': 'arm' if function else 'data', 'kind': 'function' if function else 'data'}
    from link_runtime_unit import validate
    proof = validate(entry, bindings)
    hashes, visited = [], set()
    for mask in MASKS:
        for seed in range(4):
            original = execute(native, mask, seed)
            compiled = execute(rebuilt, mask, seed)
            if original != compiled:
                raise ValueError('Native and reconstructed caller state differs')
            visited.update(original['visited'])
            hashes.append(compiler.sha(__import__('json').dumps(original, sort_keys=True).encode()))
    entry['oracle'] = {'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True, 'instructionLimit': 2000, 'stateSha256': hashes, 'nativeInstructionCoverage': len(visited), 'externalCalleesExecutedNatively': False, 'model': 'Sixteen144-byte records set or clear bit1 at offset124 under an explicit predicate contract, followed by callback(record+8,1)', 'limitations': ['Synthetic predicate and callback contracts characterize caller behavior only; game field meanings and actual callees remain separate.']}
    entry['sourceHypothesis'] = 'Equivalent if/else arm order preserves the native conditional instruction layout'
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'], 'module': 'ov007', 'moduleInputSha256': sha256(binary), 'matches': [entry], 'nativeSymbols': {item['symbol']: item['target'] for item in entry['relocations']}, 'nativeSymbolEntries': bindings, 'isolatedRealMwCallerLink': proof, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    write_json(ROOT / 'evidence/matches/ov007-enable01.json', report)
    print({'functions': 1, 'bytes': 112, 'oracleCases': len(hashes), 'oracleCalls': len(hashes) * 2})


if __name__ == '__main__':
    main()
