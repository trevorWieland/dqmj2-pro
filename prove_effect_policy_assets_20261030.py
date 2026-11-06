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
from ndspy.rom import NintendoDSRom
from ov001_actor_writeback_fixture_20261030 import status_ids
from ov001_award_fixture_20261029 import functions
from project import ROOT, configuration, now, sha256, write_json
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, __version__ as unicorn_version
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

ARCHIVE, SLOT, STACK, STOP = 0x02300000, 0x02102E2C, 0x03010000, 0x07000000
INITIAL_SP = STACK + 0xFFF0
REPORT = ROOT / 'evidence/application/effect-policy-asset-provenance-20261030.json'


def members(blob):
    if blob[:4] != b'FPK\x00':
        raise ValueError('Effect archive lacks measured FPK header')
    count = struct.unpack_from('<I', blob, 4)[0]
    if count > 256 or 8 + count * 40 > len(blob):
        raise ValueError('Effect archive directory is outside supported bounds')
    result = []
    for index in range(count):
        start = 8 + index * 40
        name = blob[start:start + 32].split(b'\x00')[0].decode('ascii')
        offset, size = struct.unpack_from('<II', blob, start + 32)
        if offset + size > len(blob):
            raise ValueError('Effect archive member is outside its measured bytes')
        result.append({'name': name, 'offset': offset, 'bytes': size})
    return result


def execute(machine, address, arguments, seed, patches, allowed):
    rng = random.Random(seed)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:len(arguments)] = [value & 0xFFFFFFFF for value in arguments]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, INITIAL_SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.mem_write(INITIAL_SP, bytes(4))
    expected = bytearray(machine.mem_read(0x02000000, 0x400000))
    for location, payload in patches:
        expected[location - 0x02000000:location - 0x02000000 + len(payload)] = payload
    starts, ranges = functions()
    seen, cache = set(), {}
    counts = {'instructions': 0, 'writes': 0}
    trace, writes = hashlib.sha256(), hashlib.sha256()

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Effect provenance escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Effect provenance entered wrong native mode')
        seen.add(entry)

    def write(engine, access, destination, size, value, unused):
        if not (STACK <= destination < destination + size <= STACK + 0x10000 or
                any(start <= destination < destination + size <= start + length for start, length in allowed)):
            raise ValueError(('Effect provenance wrote outside declared effects', hex(destination)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    code_hook = machine.hook_add(UC_HOOK_CODE, step)
    write_hook = machine.hook_add(UC_HOOK_MEM_WRITE, write)
    try:
        machine.emu_start(address, STOP, count=100000)
    finally:
        machine.hook_del(code_hook)
        machine.hook_del(write_hook)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != INITIAL_SP:
        raise ValueError('Effect provenance native routine did not actually return')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Effect provenance native routine damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected):
        raise ValueError('Effect provenance effects differ from independent byte-copy/reset model')
    return {'actualReturn': True, 'entry': hex(address), 'arguments': arguments,
            'physicalR0': hex(machine.reg_read(UC_ARM_REG_R0)), **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'ramSha256': hashlib.sha256(ram).hexdigest(),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    descriptors = bytes(rom.getFileByName('BtlStsTbl.bin'))
    ids = sorted(set(status_ids(descriptors)))
    files = {rom.filenames.filenameOf(i).lower(): (i, rom.filenames.filenameOf(i)) for i in range(len(rom.files)) if rom.filenames.filenameOf(i)}
    main_metadata, main, main_config = measured_module('main')
    stamp_word = struct.unpack_from('<I', main, 0x5C770)[0]
    if stamp_word != 0xE8850280:
        raise ValueError('Original loader pointer/ID stamp instruction changed')
    results, missing = [], []
    for identity in ids:
        key = f'efc_{identity:03d}.e'
        if key not in files:
            missing.append({'nativeId': identity, 'requestedName': key, 'romArchiveAbsent': True})
            continue
        file_id, filename = files[key]
        blob = bytes(rom.files[file_id])
        member = next(row for row in members(blob) if row['name'].lower() == f'efc_{identity:03d}.ep')
        ep = blob[member['offset']:member['offset'] + member['bytes']]
        if len(ep) != 56 or ep[:4] != b'EP\x00\x00':
            raise ValueError('Effect policy metadata lacks the measured56-byte EP representation')
        flags = struct.unpack_from('<H', ep, 4)[0]
        for found in [True, False]:
            requested = identity if found else 999
            machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
            machine.ctl_set_cpu_model(UC_CPU_ARM_946)
            for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
                machine.mem_map(start, size)
            machine.mem_write(0x02000000, main)
            machine.mem_write(ARCHIVE, blob)
            index = len(results)
            reset = execute(machine, 0x0205C3C4, [], 202610305000 + index,
                            [(SLOT, bytes(0x1580)), (0x021043AC, bytes(0x2380)), (0x020DDB80, b'\x01')],
                            [(SLOT, 0x1580), (0x021043AC, 0x2380), (0x020DDB80, 1)])
            patches = [(SLOT + 0x74, ep)] if found else []
            loaded = execute(machine, 0x0205C49C, [ARCHIVE, SLOT, requested, 5], 202610305100 + index,
                             patches, [(SLOT + 0x74, 56)])
            formatted = bytes(machine.mem_read(INITIAL_SP - 40, 16)).split(b'\x00')[0].decode('ascii')
            if formatted != f'efc_{requested:03d}.ep' or loaded['physicalR0'] != '0x0':
                raise ValueError('Native effect member-name or case5 physical return differs')
            if found:
                machine.mem_write(SLOT, struct.pack('<II', ARCHIVE, identity))
            queried = execute(machine, 0x0205D7CC, [requested], 202610305200 + index, [], [])
            zero = execute(machine, 0x0205D7CC, [0], 202610305300 + index, [], [])
            if int(queried['physicalR0'], 0) != (flags if found else 0) or zero['physicalR0'] != '0x0':
                raise ValueError('Native effect flags getter differs from asset/reset model')
            results.append({'nativeId': identity, 'fileId': file_id, 'filename': filename,
                'archiveSha256': match_runtime.sha(blob), 'member': member, 'memberSha256': match_runtime.sha(ep),
                'memberFlagsU16': flags, 'memberExpectedPresent': found, 'formattedNativeMemberName': formatted,
                'nativeCaseInsensitiveMemberResolutionObserved': found,
                'cacheIdStampRecipe': 'For a found member, seed file-pointer/ID words as the original loader0205C668 STMIAR5{R7,R9} does; full loader is not executed',
                'stages': {'reset': reset, 'copy': loaded, 'flags': queried, 'zeroAfterReset': zero}})
    entries = []
    for address in [0x0205C3C4, 0x0205C49C, 0x0205C668, 0x0205CA0C, 0x0205D7CC]:
        boundary = re.search(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + '$', main_config, re.M)
        size = int(boundary[1], 0)
        entries.append({'processor': 'arm9', 'module': 'main', 'address': hex(address), 'mode': 'arm',
                        'bytes': size, 'spanSha256': match_runtime.sha(main[address - 0x02000000:address - 0x02000000 + size])})
    dependencies = ['ov001_actor_writeback_fixture_20261030.py', 'match_ov001_current_stat_restore_20261030.py',
                    'prove_reward_return_abi_20261029.py', 'ov001_award_fixture_20261029.py', 'config/arm9/symbols.txt']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'evidenceClass': 'native-resource-property-provenance', 'mainInputSha256': main_metadata['sha256'],
              'qualifiedFunctions': entries, 'statusDescriptorSha256': match_runtime.sha(descriptors),
              'nativeStatusIds': ids, 'absentArchives': missing, 'vectors': len(results),
              'originalLoaderStamp': {'address': '0x0205c770', 'word': hex(stamp_word),
                  'operation': 'STMIA R5,{R7,R9}; file pointer and native ID at slot0/+4',
                  'executedInThisProof': False},
              'nativeActualReturns': len(results) * 4, 'hostCalleeStubs': False, 'hostIoProviders': False,
              'gpuOrDeviceExecution': False, 'sourceMatchCredit': 0, 'sourceDataCredit': 0,
              'results': results, 'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['This executes native reset, in-memory archive type5 extraction and flags query, not the complete file/graphics loader',
                  'File archives are selected by measured case-folded ROM filename identity; outer filesystem case behavior is not certified',
                  'Post-copy cache pointer/ID stamping is explicit setup justified by original loader instructions, not an executed full-loader result',
                  'Actual current cache membership, later mutation, cleanup/stale-ID0 behavior and ordinary scene reachability remain unresolved',
                  'Missing-member999 is a deterministic error probe; ID0 lacks an archive and is qualified only in reset/matching-input cache states',
                  'Member sizes other than the measured56 bytes and malformed archive directories remain unsupported',
                  'Native case5 returns0 even when metadata is copied; success is measured by bytes and the flags getter, not that residue']}
    write_json(REPORT, report)
    print(json.dumps({'vectors': len(results), 'nativeActualReturns': len(results) * 4,
                      'propertyFlags': sorted({row['memberFlagsU16'] for row in results}),
                      'sourceMatchCredit': 0, 'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
