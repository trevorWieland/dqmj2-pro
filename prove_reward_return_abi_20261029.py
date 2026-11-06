import bisect
import hashlib
import json
import random
import re
import struct
import sys
from pathlib import Path

import match_runtime
from link_runtime_unit import measured_module
from ov001_award_cases_20261029 import assets
from ov001_award_fixture_20261029 import functions
from project import ROOT, configuration, now, sha256, write_json
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, __version__ as unicorn_version
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

KIND, ABILITY, OUTPUT, ACTOR, DATA, ROSTER = 0x02300000, 0x02310000, 0x02320000, 0x02330000, 0x02331000, 0x021BD674
STOP, STACK = 0x07000000, 0x03010000
GETTERS = [0x02044A14, 0x02044A58, 0x02044A9C, 0x02044AE0, 0x02044B24, 0x02044B68]
OFFSETS = [0x47, 0x4B, 0x4F, 0x53, 0x57, 0x5B]


def signed(value):
    return (value + 0x80000000) % 0x100000000 - 0x80000000


def short(value):
    return (value + 0x8000) % 0x10000 - 0x8000


def divide(value, denominator):
    return abs(value) // denominator * (-1 if value < 0 else 1)


def scale(value, variant):
    return short(divide(signed(value * [1, 3, 2][variant]), [1, 2, 1][variant]))


def tier(level):
    return 0 if level <= 10 else 1 if level <= 40 else 2 if level <= 50 else 3


def execute(main, overlay, blobs, address, arguments, memory, patches, expected, seed):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(KIND, blobs['EnmyKindTbl.bin'][8:])
    machine.mem_write(ABILITY, blobs['AbilityTbl.bin'])
    machine.mem_write(0x020F69F0, struct.pack('<I', KIND))
    machine.mem_write(0x02238D58, struct.pack('<I', ABILITY))
    machine.mem_write(0x020F69E4, bytes(4))
    for location, payload in memory:
        machine.mem_write(location, payload)
    rng = random.Random(seed)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:len(arguments)] = [word & 0xFFFFFFFF for word in arguments]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    ram_expected = bytearray(machine.mem_read(0x02000000, 0x400000))
    for location, payload in patches:
        ram_expected[location - 0x02000000:location - 0x02000000 + len(payload)] = payload
    starts, ranges = functions()
    seen, cache = set(), {}
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Return ABI probe escaped qualified inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Return ABI probe entered incorrect native mode')
        seen.add(entry)

    def written(engine, access, destination, size, word, unused):
        if not (STACK <= destination < destination + size <= STACK + 0x10000 or any(start <= destination < destination + size <= start + len(payload) for start, payload in patches)):
            raise ValueError(('Return ABI probe wrote outside declared effects', hex(destination)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, word & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Return ABI probe did not actually return')
    actual = machine.reg_read(UC_ARM_REG_R0)
    if actual != expected & 0xFFFFFFFF:
        raise ValueError(('Independent return ABI model differs', hex(address), arguments, hex(actual), hex(expected & 0xFFFFFFFF)))
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Return ABI probe damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(ram_expected):
        raise ValueError('Return ABI native memory effects differ from independent model')
    return {'actualReturn': True, 'arguments': arguments, 'returnBits': hex(actual), 'signedReturn': signed(actual),
            **counts, 'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}


def growth(blobs, species, variant, level):
    kinds, ability = blobs['EnmyKindTbl.bin'][8:], blobs['AbilityTbl.bin']
    flags = struct.unpack_from('<H', kinds, species * 100 + 4)[0]
    size = ((flags >> 8) & 15) // 3
    numerator, denominator = (3, 2) if size == 1 else (2, 1) if size == 2 else (1, 1)
    base, parent = [], []
    for offset in OFFSETS:
        def entry(kind):
            curve = kinds[kind * 100 + offset + tier(level)]
            if curve >= 33:
                raise ValueError('Unsupported ability curve outside measured table')
            return ability[curve * 100 + level - 1]
        base.append(scale((numerator * entry(species) + denominator - 1) // denominator, variant))
        parent.append(divide(short(scale(entry(1), 0) + scale(entry(4), 1)) + 3, 4))
    return base, parent


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    main_metadata, main, main_config = measured_module('main')
    overlay_metadata, overlay, overlay_config = measured_module('ov001')
    blobs = assets()
    kinds = blobs['EnmyKindTbl.bin'][8:]
    facts = []
    seed = 202610304400
    for getter, offset in zip(GETTERS, OFFSETS):
        results = []
        for index in range(64):
            species = [0, 1, 4, 20, 33, 127, 255, 511][index % 8]
            level = [-1, 0, 1, 10, 11, 40, 41, 50, 51, 100][(index + index // 8) % 10]
            variant = [0, 1, 255, 0xFFFFFFFF][index // 4 % 4]
            expected = kinds[species * 100 + offset + tier(level)]
            results.append(execute(main, overlay, blobs, getter, [species, variant, level], [], [], expected, seed + index))
        facts.append({'module': 'main', 'address': hex(getter), 'returnRepresentation': 'R0 clean byte, zero-extended to32 bits',
                      'measuredRange': [min(int(row['returnBits'], 0) for row in results), max(int(row['returnBits'], 0) for row in results)],
                      'structuralRange': [0, 255], 'independentKindRowTierAndVariantCancellationModel': True, 'results': results})
    results = []
    for variant in range(3):
        for number in [-2147483648, -32769, -32768, -1, 0, 1, 127, 255, 32767, 32768, 2147483647]:
            results.append(execute(main, overlay, blobs, 0x021E404C, [variant, number], [], [], scale(number, variant), seed + len(results)))
    facts.append({'module': 'ov001', 'address': '0x021e404c', 'returnRepresentation': 'R0 signed16, sign-extended to32 bits',
                  'structuralRange': [-32768, 32767], 'independentWordMultiplySignedDivisionAndNarrowingModel': True, 'results': results})
    growth_results, wider = [], 0
    for species in [1, 4, 20, 33]:
        for level in [1, 10, 11, 40, 41, 50, 51, 100]:
            for variant in range(3):
                base, parent = growth(blobs, species, variant, level)
                before = [0, 32767, -32768, 20, -20, 32767 - base[5]]
                final = [short(short(old + first) + second) for old, first, second in zip(before, base, parent)]
                expected = short(before[5] + base[5]) + parent[5]
                record = bytearray(0x84)
                struct.pack_into('<IhB', record, 0x14, 5000, species, variant)
                struct.pack_into('<hh', record, 0x40, 1, 4)
                record[0x4C], record[0x4D] = 0, 1
                memory = [(ROSTER, bytes(100 * 0x84)), (ROSTER, bytes(record)), (OUTPUT, struct.pack('<6h', *before))]
                row = execute(main, overlay, blobs, 0x021E4120, [OUTPUT, 5000, level], memory,
                              [(OUTPUT, struct.pack('<6h', *final))], expected, seed + len(growth_results))
                row.update(species=species, level=level, variant=variant, initialStats=before,
                           baseGrowth=base, parentGrowth=parent, finalStats=final,
                           untruncatedFinalSum=expected, truncatedStoredValue=final[5])
                growth_results.append(row)
                wider += int(not -32768 <= expected <= 32767)
    if not wider:
        raise ValueError('No native full-width growth return distinguished from stored signed16')
    facts.append({'module': 'ov001', 'address': '0x021e4120', 'returnRepresentation': 'R0 full final signed32 sum; output stores low16 bits',
                  'fullWidthDistinguishingVectors': wider, 'independentSixStatGrowthAndNarrowingModel': True, 'results': growth_results})
    cap_results = []
    for points in [9998, 9999, 10000, 32767, -32768, -1]:
        for delta in [-32768, -1, 0, 1, 32767]:
            record, actor, data = bytearray(0x84), bytearray(0x440), bytearray(0xB0)
            struct.pack_into('<Ih', record, 0x14, 5000, 1)
            struct.pack_into('<I', actor, 0x1E8, DATA)
            struct.pack_into('<h', actor, 0x208, points)
            struct.pack_into('<h', actor, 0x21A, delta)
            struct.pack_into('<I', data, 0, 5000)
            struct.pack_into('<h', data, 0x2A, 1)
            memory = [(ROSTER, bytes(100 * 0x84)), (ROSTER, bytes(record)), (ACTOR, bytes(actor)), (DATA, bytes(data))]
            expected = delta - (points - 9999) if points > 9999 else struct.unpack_from('<H', kinds, 100 + 0x1A)[0]
            patches = [(ACTOR + 0x208, struct.pack('<h', 9999)), (ACTOR + 0x21A, struct.pack('<h', short(expected)))] if points > 9999 else []
            row = execute(main, overlay, blobs, 0x021E4500, [ACTOR, ACTOR + 0x20C], memory, patches, expected, seed + len(cap_results))
            row.update(points=points, delta=delta)
            cap_results.append(row)
    facts.append({'module': 'ov001', 'address': '0x021e4500', 'returnRepresentation': 'Full R0 difference on points clamp; stored delta uses low16 bits',
                  'malformedOverCapComponentInputsIncluded': True, 'results': cap_results})
    facts.append({'module': 'ov001', 'address': '0x021e409c',
                  'returnRepresentation': 'R0 signed16, sign-extended to32 bits by the sole terminal return path',
                  'structuralRange': [-32768, 32767], 'results': [],
                  'independentExecutionReference': 'evidence/matches/ov001-20261029-growth01.json',
                  'independentExecutionReplay': ['python', 'match_ov001_growth_20261029.py']})
    for fact in facts:
        raw, config, base = (main, main_config, 0x02000000) if fact['module'] == 'main' else (overlay, overlay_config, 0x021D7240)
        address = int(fact['address'], 0)
        boundary = re.search(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + '$', config, re.M)
        if not boundary:
            raise ValueError('Return ABI entry lacks canonical ARM boundary')
        size = int(boundary[1], 0)
        fact.update(processor='arm9', mode='arm', bytes=size, spanSha256=match_runtime.sha(raw[address - base:address - base + size]), additionalSourceCredit=0)
        words = struct.unpack_from('<' + 'I' * (size // 4), raw, address - base)
        returns = [index * 4 for index, word in enumerate(words) if word & 0x0FFF0000 == 0x08BD0000 and word & 0x8000]
        if address in GETTERS:
            if words[-3] != 0xE20000FF or returns != [size - 8]:
                raise ValueError('Clean-byte return range lacks its sole native AND/return proof')
            fact['returnTailProof'] = {'andOffset': size - 12, 'andWord': hex(words[-3]), 'soleReturnOffset': size - 8}
        elif address in (0x021E404C, 0x021E409C):
            if words[-2] != 0xE1A00840 or returns != [size - 4]:
                raise ValueError('Signed16 return range lacks its sole ASR16/return proof')
            fact['returnTailProof'] = {'signExtensionOffset': size - 8, 'signExtensionWord': hex(words[-2]), 'soleReturnOffset': size - 4}
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'moduleHashes': {'main': main_metadata['sha256'], 'ov001': overlay_metadata['sha256']},
              'abiFacts': facts, 'nativeActualReturns': sum(len(row['results']) for row in facts),
              'assetHashes': {name: match_runtime.sha(blob) for name, blob in blobs.items()},
              'hostCalleeStubs': False, 'sourceCredit': 0, 'generator': Path(__file__).name,
              'generatorSha256': sha256(Path(__file__)),
              'limitations': ['Deterministic component states do not establish scene reachability or save validity',
                              'Direct growth probes use valid measured species/ability curves and variants0..2; other data/variants remain unsupported',
                              'Over-cap points/delta probes qualify machine ABI behavior on malformed synthetic components',
                              'Original native bodies remain dependencies with zero additional source credit']}
    write_json(ROOT / 'evidence/abi/reward-scalar-returns-20261029.json', result)
    print(json.dumps({'nativeActualReturns': result['nativeActualReturns'], 'facts': len(facts), 'wideGrowthVectors': wider, 'sourceCredit': 0}))


if __name__ == '__main__':
    run()
