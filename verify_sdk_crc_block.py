import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time
import zlib

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from link_runtime_unit import relocation_rows
from mechanics_save_sdk_crc_oracle import table_bytes, bit_update
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

START = 0x020199e0
END = 0x02019bd4
BASE = 0x02500000
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
LINKER = 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_oracle(native, rebuilt, rows):
    machines = []
    executed = [set(), set()]
    for index, code in enumerate((native, rebuilt)):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(START, code)
        def observe(uc, address, size, data, index=index):
            if not START <= address < END:
                raise AssertionError(('CRC execution escaped complete source block', hex(address)))
            executed[index].add(address)
        machine.hook_add(UC_HOOK_CODE, observe)
        machines.append(machine)
    entries = {row['name']: row for row in rows}
    rng = random.Random(2026102793)
    cases = calls = protocols = 0
    def invoke(row, args, current, expected, result=None):
        nonlocal cases, calls
        stack = rng.randbytes(0x10000)
        saved = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            machine.mem_write(BASE, bytes(current))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, saved):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            begin = time.monotonic()
            machine.emu_start(int(row['address'], 0), STOP, count=1000000)
            if time.monotonic() - begin > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                raise AssertionError('CRC contiguous block bounded return failed')
            if [machine.reg_read(register) for register in SAVED] != saved or bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) != bool(cases & 1):
                raise AssertionError('CRC contiguous block saved registers/return mode differ')
            if bytes(machine.mem_read(BASE, len(current))) != bytes(expected):
                raise AssertionError(('CRC contiguous block arena differs', row['name']))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('CRC contiguous block independent result differs', row['name']))
            calls += 1
        cases += 1
    for bits, polynomial, wrapper in ((8, 7, 0x02019b58), (16, 0xa001, 0x02019b80), (32, 0xedb88320, 0x02019ba8)):
        width = bits // 8
        table_row = entries[f'saved_crc{bits}_table']
        update_row = entries[f'saved_crc{bits}_update']
        wrapper_row = next(row for row in rows if int(row['address'], 0) == wrapper)
        for length in (0, 1, 2, 3, 7, 8, 9, 31, 32, 55, 56, 63, 64, 65, 255, 256, 1024):
            for state in (0, 1, (1 << bits) - 1, rng.getrandbits(bits)):
                current = bytearray(rng.randbytes(0x4000))
                expected = bytearray(current)
                expected[0x100:0x100 + 256 * width] = table_bytes(bits, polynomial)
                invoke(table_row, (BASE + 0x100, polynomial), current, expected)
                current = expected
                current[0x800:0x800 + width] = state.to_bytes(width, 'little')
                consumed = 0
                for chunk in (min(13, length), length - min(13, length)):
                    expected = bytearray(current)
                    value = int.from_bytes(current[0x800:0x800 + width], 'little')
                    updated = bit_update(bits, polynomial, value, current[0x1000 + consumed:0x1000 + consumed + chunk])
                    expected[0x800:0x800 + width] = updated.to_bytes(width, 'little')
                    invoke(update_row, (BASE + 0x100, BASE + 0x800, BASE + 0x1000 + consumed, chunk), current, expected)
                    current = expected
                    consumed += chunk
                start = 0xffffffff if bits == 32 else 0
                result = bit_update(bits, polynomial, start, current[0x1000:0x1000 + length]) ^ start
                if bits == 32 and result != zlib.crc32(current[0x1000:0x1000 + length]):
                    raise AssertionError('CRC contiguous block bitwise/zlib models differ')
                invoke(wrapper_row, (BASE + 0x100, BASE + 0x1000, length), current, current, result)
                protocols += 1
    reached = {row['name']: [int(row['address'], 0) in values for values in executed] for row in rows}
    if not all(all(values) for values in reached.values()):
        raise AssertionError('CRC source block entry coverage incomplete')
    return {'cases': cases, 'nativeAndRecompiledCalls': calls, 'connectedProtocols': protocols, 'allNineEntriesReached': reached, 'instructionLimitPerCall': 1000000, 'secondsLimitPerCall': 2, 'outsideBlockInstructions': 0, 'nativeCodeOutsideBlockLoaded': False, 'stubs': {}, 'independentBitwiseAndZlibModels': True, 'wholeArenaCompared': True, 'returnPcSpSavedRegistersAndArmThumbReturnModeVerified': True}


def main():
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    rom_hash = sha((ROOT / 'inputs/game.nds').read_bytes())
    if rom_hash != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('CRC block pinned input namespace differs')
    if sha((ROOT / LINKER).read_bytes()) != LINKER_HASH:
        raise AssertionError('CRC block real MW linker pin differs')
    paths = ('evidence/matches/mechanics-save-sdk-crc.json', 'evidence/matches/main-runtime08.json')
    rows = []
    for path in paths:
        document = json.loads((ROOT / path).read_text(encoding='utf-8'))
        if document['romSha256'] != rom_hash:
            raise AssertionError('CRC block source report ROM differs')
        for entry in document['matches']:
            if entry.get('module') != 'main' or entry.get('program') or not START <= int(entry['address'], 0) < END:
                continue
            if entry['mode'].lower() != 'arm' or not entry['exactAfterDeclaredRelocation']:
                raise AssertionError('CRC block source proof mode/match differs')
            for field in ('source', 'object'):
                if sha((ROOT / entry[field]).read_bytes()) != entry[field + 'Sha256']:
                    raise AssertionError(('CRC block source/object differs', entry['name']))
            rows.append({**entry, 'sourceReport': path, 'sourceReportSha256': sha((ROOT / path).read_bytes())})
    rows.sort(key=lambda row: int(row['address'], 0))
    cursor = START
    for row in rows:
        if int(row['address'], 0) != cursor:
            raise AssertionError('CRC block contains a missing/overlapping source span')
        cursor += row['bytes']
    if len(rows) != 9 or cursor != END:
        raise AssertionError('CRC complete block requires all nine source functions')
    identity = sha(json.dumps([(row['name'], row['sourceSha256'], row['objectSha256']) for row in rows]).encode())
    directory = ROOT / 'work/mechanics-save/crc-block' / identity
    directory.mkdir(parents=True, exist_ok=True)
    objects = []
    relocation_evidence = []
    for index, row in enumerate(rows):
        target = directory / f'unit{index}.o'
        original = ROOT / row['object']
        with original.open('rb') as stream:
            split_symbol(ELFFile(stream), row['name'], target)
        before = relocation_rows(original, row['name'])
        if before != relocation_rows(target, row['name']):
            raise AssertionError('CRC block split changed source relocation format/type/addend/instruction')
        relocation_evidence.append({'name': row['name'], 'relocations': before, 'splitObject': str(target.relative_to(ROOT)), 'splitObjectSha256': sha(target.read_bytes())})
        objects.append(target)
    aliases = {'native_fn_02019a20': 'saved_crc8_update', 'native_fn_02019a9c': 'saved_crc16_update', 'native_fn_02019b1c': 'saved_crc32_update'}
    lcf = directory / 'block.lcf'
    sections = '\n'.join(f'{path.name}(.text)' for path in objects)
    assignments = '\n'.join(f'{name} = {target};' for name, target in aliases.items())
    lcf.write_text(f'MEMORY {{ CRC: ORIGIN = {START:#x} > crc.bin }}\nSECTIONS {{\n.crc: {{\n{sections}\n}} > CRC\n{assignments}\n}}\n')
    linked = directory / 'block.elf'
    command = [str(ROOT / LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', rows[0]['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode:
        raise AssertionError(('CRC complete source link failed', process.stdout, process.stderr))
    code = (directory / 'crc.bin').read_bytes()
    native = arm[START - 0x02000000:END - 0x02000000]
    if code != native:
        raise AssertionError(('CRC complete block bytes differ', len(code), sum(a == b for a, b in zip(code, native))))
    with linked.open('rb') as stream:
        symbols = {symbol.name: symbol for symbol in ELFFile(stream).get_section_by_name('.symtab').iter_symbols()}
        for row in rows:
            symbol = symbols[row['name']]
            if symbol['st_value'] != int(row['address'], 0) or symbol['st_size'] != row['bytes'] or symbol['st_info']['type'] != 'STT_FUNC':
                raise AssertionError('CRC complete block linked function range/type differs')
        for name, target in aliases.items():
            if symbols[name]['st_value'] != symbols[target]['st_value']:
                raise AssertionError('CRC wrapper source alias differs')
    oracle = run_oracle(native, code, rows)
    artifacts = {name: {'path': str((directory / name).relative_to(ROOT)), 'sha256': sha((directory / name).read_bytes())} for name in ('block.lcf', 'block.elf', 'crc.bin')}
    report = {'schemaVersion': 1, 'romSha256': rom_hash, 'arm9Sha256': sha(arm), 'module': 'main', 'processor': 'arm9', 'address': hex(START), 'end': hex(END), 'bytes': len(code), 'sourceFunctions': 9, 'matches': [], 'newFunctionCredit': 0, 'newSourceBytesCredit': 0, 'exactAfterRealMwLink': True, 'blockSha256': sha(code), 'linkerSha256': LINKER_HASH, 'sourceFunctionAliases': aliases, 'unchangedSourceRelocations': relocation_evidence, 'linkCommand': command, 'artifacts': artifacts, 'oracle': {**oracle, 'reusedAcceptedSources': rows}, 'oracleSource': Path(__file__).name, 'oracleSourceSha256': sha(Path(__file__).read_bytes()), 'limitations': ['This contiguous500-byte CRC block is wholly built from nine existing ordinary C functions; it adds no function or byte credit and does not establish an entire host-module or ROM build.', 'Legacy wrapper source declarations use unspecified arguments/u32 return for the update externs; linker aliases establish the measured target ABI while the ignored update return does not establish an authentic original prototype.', 'Bounded block protocols cover valid tables and buffers; the earlier CRC batch retains separate malformed/alias/high-polynomial evidence.', 'Retained native data or callee bodies are not build inputs to this block.']}
    (ROOT / 'evidence/matches/mechanics-save-sdk-crc-block.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'sourceFunctions': 9, 'exactBlockBytes': len(code), 'newFunctionCredit': 0, 'oracleCases': oracle['cases'], 'oracleCalls': oracle['nativeAndRecompiledCalls']}, indent=2))


if __name__ == '__main__':
    main()
