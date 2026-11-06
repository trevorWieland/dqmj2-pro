import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put
from mechanics_save_section3_oracle import dependencies, sha

SECTION = 0x021bb278
RECORD76 = 0x021bb5b8
RECORD12 = 0x021bc8b8
SCRATCH = 0x021bcbc0
INPUT = 0x02500100
STOP = 0x027ff800

def scratch_dependency(root, arm):
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            if int(row['address'], 16) != 0x02063ec8 or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Scratch pointer dependency hash differs')
            with (root / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            for relocation in row.get('relocations', []):
                if relocation['type'] != 2:
                    raise AssertionError('Unexpected scratch pointer relocation')
                struct.pack_into('<I', code, relocation['offset'], int(relocation['target'], 16) + relocation['addend'])
            if code != arm[0x63ec8:0x63ec8 + row['bytes']]:
                raise AssertionError('Scratch pointer dependency bytes differ')
            return {0x02063ec8: (row, bytes(code))}
    return {}

def expected(memory, name, first, second):
    if name == 'saved_section3_pair_reconcile':
        if not 0 <= first < 64 or not 0 <= second < 64:
            return 0
        first_values, second_values = RECORD12 + first * 12, RECORD12 + second * 12
        first_sum = sum(struct.unpack('<III', read(memory, first_values, 12))) & 0xffffffff
        second_sum = sum(struct.unpack('<III', read(memory, second_values, 12))) & 0xffffffff
        if first_sum == second_sum:
            return 0
        source, destination = (first, second) if first_sum > second_sum else (second, first)
        write(memory, RECORD76 + destination * 76, read(memory, RECORD76 + source * 76, 76))
        write(memory, RECORD12 + destination * 12, read(memory, RECORD12 + source * 12, 12))
        return 1
    if name == 'saved_section3_scratch_read':
        write(memory, first, read(memory, SCRATCH, 76))
        return 1
    if name == 'saved_section3_scratch_date_pointer':
        return SCRATCH + 60
    if name == 'saved_section3_scratch_date_write':
        write(memory, SCRATCH + 60, read(memory, first, 16))
        return None
    raise AssertionError(('Unknown section3 compare function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    reused.update(scratch_dependency(root, arm))
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    values = [(0, 0, 0), (1, 0, 0), (0xffffffff, 0, 0), (0xffffffff, 1, 0), (0xffffffff, 0xffffffff, 0xffffffff), (0x80000000, 0x80000000, 1), (0, 0xffffffff, 1)]
    indices = [-1, 0, 1, 31, 63, 64]
    pairs = [(first, second, left, right) for first in indices for second in indices for left in values for right in values]
    pairs += [(rng.randrange(64), rng.randrange(64), tuple(rng.getrandbits(32) for _ in range(3)), tuple(rng.getrandbits(32) for _ in range(3))) for _ in range(256)]
    vectors = [('saved_section3_pair_reconcile', first, second, left, right) for first, second, left, right in pairs]
    for name in ('saved_section3_scratch_read', 'saved_section3_scratch_date_pointer', 'saved_section3_scratch_date_write'):
        vectors += [(name, first, 0, None, None) for first in ([INPUT, SCRATCH] if name.endswith('_read') else [INPUT, SCRATCH + 60] if name.endswith('_write') else [0]) for _ in range(64)]
    cases = 0
    calls = 0
    for bank in (0, 0x7100):
        for name, first, second, left, right in vectors:
            if name not in matches:
                continue
            original = {0x021b9000: bytearray(rng.randbytes(0xb000)), 0x02500000: bytearray(rng.randbytes(0x3000))}
            write(original, SECTION, save[bank + 0x3a9c:bank + 0x5d40])
            if name == 'saved_section3_pair_reconcile':
                if 0 <= first < 64:
                    write(original, RECORD12 + first * 12, struct.pack('<III', *left))
                    write(original, RECORD76 + first * 76, rng.randbytes(76))
                if 0 <= second < 64:
                    write(original, RECORD12 + second * 12, struct.pack('<III', *right))
                    write(original, RECORD76 + second * 76, rng.randbytes(76))
            memory = {address: bytearray(data) for address, data in original.items()}
            result = expected(memory, name, first, second)
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
                machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Section3 comparison bounds', name, bank, first, second))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Section3 comparison result differs', name, first, second, left, right))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Section3 paired record/scratch/input/guard RAM differs', name, bank, first, second, left, right))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedWholeSectionAndGuardRam': True, 'platformStubs': {}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Two valid indices select corresponding12-byte and76-byte records.', 'The three12-byte words are summed with32-bit wrap, then promoted for unsigned comparison; overflow cases are covered explicitly.', 'Larger wrapped sum copies both paired records over the lower-sum pair and returns1; equal sums and invalid indices preserve state and return0.', 'Same-index requests return0; the operation does not infer chronological or ownership preference.', 'The section3 scratch record is76 bytes at offset0x1948, with its final16-byte slice at offset0x1984.'], 'limitations': ['All callees execute; no platform or gameplay provider is substituted.', 'The numerical comparison does not establish what the12-byte words measure or what the paired record represents.', 'No new semantic partition classification is assigned to section3.', 'Only equal or disjoint copy buffers are used; unsupported overlap contracts remain unclaimed.']}
