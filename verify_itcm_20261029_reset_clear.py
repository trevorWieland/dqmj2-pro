import json
import os
import random
import struct
import subprocess
import sys
from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR
)

REGS = [
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR
]
NAME = 'native_itcm_01ff82b4'
ADDRESS = 0x01FF82B4
SOURCE = 'src/itcm/20261029_reset/native_itcm_01ff82b4.s'
PROVENANCE = 'evidence/itcm/2026-10-29-reset-clear-provenance.json'
PROVENANCE_HASH = 'b944a9d1825b41074a63d263d33dcdfd4ea53f6394533a7d7a238f06e0787615'
ASSEMBLER = 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
ASSEMBLER_HASH = 'e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c'
ARENA = 0x03002000
STOP = 0x0301E000


def signed(value):
    return value if value < 0x80000000 else value - 0x100000000


def run(code, destination, count, seed, thumb, fault=False):
    rng = random.Random(0x202610290082B4 + seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x01FF8000, 0x8000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_write(ADDRESS, code)
    before = rng.randbytes(4096)
    engine.mem_write(ARENA, before)
    registers = [rng.getrandbits(32) for unused in REGS]
    registers[1:3] = [destination, count]
    registers[-2:] = [0x0301FF00, STOP | int(thumb)]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, value in zip(REGS, registers):
        engine.reg_write(register, value)
    visited, writes = set(), []
    def observe(uc, address, size, data):
        if not ADDRESS <= address < ADDRESS + 20:
            raise ValueError('Clear primitive escaped its five source instructions')
        visited.add(address)
    engine.hook_add(UC_HOOK_CODE, observe)
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data: writes.append([address, size, value]))
    error = None
    try:
        engine.emu_start(ADDRESS, STOP, count=4000)
    except UcError as caught:
        error = str(caught)
    returned = engine.reg_read(UC_ARM_REG_PC) == STOP
    if fault:
        if error is None or returned or bytes(engine.mem_read(ARENA, 4096)) != before:
            raise ValueError('Unmapped-write fixture unexpectedly returned or changed the valid arena')
    else:
        if error is not None or not returned:
            raise ValueError('Valid primitive fixture did not actually return')
        expected, expected_writes = bytearray(before), []
        end, cursor = (destination + count) & 0xFFFFFFFF, destination
        while signed(cursor) < signed(end):
            offset = cursor - ARENA
            if not 0 <= offset <= len(expected) - 4:
                raise ValueError('Independent fixture model exceeded its bounded arena')
            struct.pack_into('<I', expected, offset, registers[0])
            expected_writes.append([cursor, 4, registers[0]])
            cursor = (cursor + 4) & 0xFFFFFFFF
        final = registers[:]
        final[1], final[12] = cursor, end
        actual = [engine.reg_read(register) for register in REGS]
        difference = (cursor - end) & 0xFFFFFFFF
        flags = ((difference >> 31) << 31) | (int(difference == 0) << 30) | (int(cursor >= end) << 29)
        flags |= int(bool((cursor ^ end) & (cursor ^ difference) & 0x80000000)) << 28
        expected_cpsr = flags | 0x10 | (0x20 if thumb else 0)
        if actual != final or engine.reg_read(UC_ARM_REG_CPSR) != expected_cpsr:
            raise ValueError('Independent register or final subtraction-flag model differs')
        if bytes(engine.mem_read(ARENA, 4096)) != expected or writes != expected_writes:
            raise ValueError('Independent complete-arena or ordered word-store model differs')
    return {
        'registers': [engine.reg_read(register) for register in REGS],
        'pc': engine.reg_read(UC_ARM_REG_PC),
        'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
        'writes': writes,
        'arenaSha256': __import__('hashlib').sha256(bytes(engine.mem_read(ARENA, 4096))).hexdigest(),
        'error': error,
        'returned': returned,
        'visited': sorted(visited)
    }


def main():
    if sha256(ROOT / ASSEMBLER) != ASSEMBLER_HASH or sha256(ROOT / PROVENANCE) != PROVENANCE_HASH:
        raise ValueError('Pinned assembler or SDK provenance differs')
    binary = ROOT / 'extract/arm9/itcm.bin'
    if sha256(binary) != '69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb':
        raise ValueError('Measured ITCM input differs')
    work = ROOT / 'work/lowlevel-recovery/20261029-itcm/reset-clear-proof'
    work.mkdir(parents=True, exist_ok=True)
    source, output = ROOT / SOURCE, work / 'compiled.o'
    output.unlink(missing_ok=True)
    command = [str(ROOT / ASSEMBLER), '-proc', 'arm5TE', '-c', str(source), '-o', str(output)]
    process = subprocess.run(
        command, cwd=ROOT,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')),
        capture_output=True, text=True, timeout=60
    )
    if process.returncode:
        raise ValueError(process.stdout + process.stderr)
    digest = sha256(output)
    immutable = work / (digest + '.o')
    if immutable.exists() and immutable.read_bytes() != output.read_bytes():
        raise ValueError('Immutable assembled object differs')
    if not immutable.exists():
        immutable.write_bytes(output.read_bytes())
    with immutable.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name == NAME)
        section = elf.get_section(symbol['st_shndx'])
        code = section.data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
        if any(item['sh_type'] in ('SHT_REL', 'SHT_RELA') and item['sh_info'] == symbol['st_shndx'] and item.num_relocations() for item in elf.iter_sections()):
            raise ValueError('Self-contained primitive unexpectedly has unresolved relocations')
        section_index, section_offset = symbol['st_shndx'], symbol['st_value']
    native = binary.read_bytes()[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + 20]
    if len(code) != 20 or native != code:
        raise ValueError('Every assembled primitive byte must match native code')
    entry = {
        'name': NAME,
        'nativeAlias': 'func_01ff82b4',
        'module': 'itcm',
        'processor': 'arm9',
        'mode': 'arm',
        'address': hex(ADDRESS),
        'bytes': 20,
        'size': 20,
        'compiledBytes': 20,
        'matchingBytes': 20,
        'exactAfterDeclaredRelocation': True,
        'source': SOURCE,
        'sourceSha256': sha256(source),
        'object': immutable.relative_to(ROOT).as_posix(),
        'objectSha256': digest,
        'compiler': ASSEMBLER,
        'compilerSha256': ASSEMBLER_HASH,
        'assemblerSha256': ASSEMBLER_HASH,
        'compilerFlags': ['-proc', 'arm5TE', '-c'],
        'targetSha256': __import__('hashlib').sha256(native).hexdigest(),
        'outputSha256': __import__('hashlib').sha256(code).hexdigest(),
        'relocations': [],
        'sectionIndex': section_index,
        'sectionOffset': section_offset,
        'sourceLanguage': 'assembly',
        'ordinaryCBytes': 0,
        'justifiedAssemblyBytes': 20,
        'justifiedAssemblyRanges': [{'address': hex(ADDRESS), 'bytes': 20}],
        'assemblyJustification': {
            'kind': 'verified-original-sdk-inline-assembly',
            'originalSymbol': 'OSi_CpuClear32',
            'provenance': PROVENANCE,
            'provenanceSha256': PROVENANCE_HASH,
            'nativeInstructions': 5,
            'rawExecutableBytesStoredAsSource': False
        }
    }
    from link_runtime_unit import validate
    linked = validate(entry, {}, work / 'real-link')
    hashes, visited = [], set()
    counts = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63, 64, 127, 128, 255, 256, 1023, 1024]
    cases = [(ARENA + offset, count, False) for offset in [0, 4, 12, 64, 256] for count in counts]
    cases += [(value, 0, False) for value in [0, 0x7FFFFFFC, 0x80000000, 0xFFFFFFFC]]
    cases += [(0x7FFFFFFC, 4, False), (0, 4, True)]
    for index, (destination, count, fault) in enumerate(cases):
        for thumb in [False, True]:
            first = run(native, destination, count, index, thumb, fault)
            second = run(code, destination, count, index, thumb, fault)
            if first != second:
                raise ValueError('Native and fresh source machines differ')
            visited.update(first['visited'])
            hashes.append(__import__('hashlib').sha256(json.dumps(first, sort_keys=True).encode()).hexdigest())
    if visited != set(range(ADDRESS, ADDRESS + 20, 4)):
        raise ValueError('Fixtures did not cover all five native instructions')
    fault_cases = sum(int(fault) * 2 for unused, unused_count, fault in cases)
    entry['oracle'] = {
        'cases': len(hashes),
        'nativeAndRecompiledCalls': len(hashes) * 2,
        'validReturningCases': len(hashes) - fault_cases,
        'nativeAndRecompiledReturningExecutions': (len(hashes) - fault_cases) * 2,
        'pinnedFaultCases': fault_cases,
        'nativeAndRecompiledFaultExecutions': fault_cases * 2,
        'returnModes': ['arm', 'thumb'],
        'instructionLimit': 4000,
        'stateSha256': hashes,
        'nativeInstructionCoverage': len(visited),
        'nativeInstructions': 5,
        'externalCalleesExecuted': 0,
        'independentModel': (
            'Signed32-bit cursor/end comparison, four-byte little-endian stores and wrap, '
            'full arena, ordered writes, R0-R14, and final subtraction NZCV flags'
        ),
        'supportedReturnRequired': True,
        'limitations': [
            'Unmapped-write faults characterize the isolated memory map rather than physical Nintendo DS bus-abort behavior.',
            'Word-aligned RAM cases and byte-count tails characterize this primitive; no unaligned STM or complete reset/hardware timing behavior is claimed.'
        ]
    }
    report = {
        'schemaVersion': 1,
        'createdUtc': now(),
        'romSha256': configuration()['romSha256'],
        'module': 'itcm',
        'moduleInputSha256': sha256(binary),
        'matches': [entry],
        'nativeSymbols': {},
        'isolatedRealMwCallerLink': linked,
        'wholeModuleLinked': False,
        'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/itcm-20261029-reset-clear.json', report)
    print({'functions': 1, 'bytes': 20, 'ordinaryCBytes': 0, 'justifiedOriginalAssemblyBytes': 20, 'oracleCases': len(hashes), 'oracleCalls': len(hashes) * 2})


if __name__ == '__main__':
    main()
