import hashlib
import json
import random
import re
import struct
import sys
from pathlib import Path

import match_runtime
from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json
from trace_enemy_initialization_context_20261029 import span
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, __version__ as unicorn_version
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

BASE, ENTRY, CONTEXT = 0x02000000, 0x021EC03C, 0x02238D7C
ACTOR, TARGETS, DESCRIPTOR = 0x02360000, 0x02362000, 0x02368000
LIST, TOKENS = 0x02238DE0, 0x02238E50
POINTERS = [0x02370000, 0x02371000, 0x02372000]
TOKEN_WORDS = [0, 128, 255]
SP, STOP, ACTION = 0x0301FFF0, 0x07000000, 7
REPORT = ROOT / 'evidence/application/ov001-nonzero-state-r4-native-20261030.json'


def read_word(raw, base, address):
    return struct.unpack_from('<I', raw, address - base)[0]


def branch_target(address, word):
    return address + 8 + (((word & 0xFFFFFF) ^ 0x800000) - 0x800000) * 4


def arm_functions(config):
    return [(int(address, 0), int(size, 0)) for mode, size, address in re.findall(
        r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', config) if mode == 'arm']


def static_audit(main, overlay, main_config, overlay_config):
    incoming, interiors, pointer_words = [], [], []
    for module, raw, config, base in [('main', main, main_config, BASE), ('ov001', overlay, overlay_config, 0x021D7240)]:
        for start, length in arm_functions(config):
            if module == 'ov001' and start == ENTRY:
                continue
            for site in range(start, start + length, 4):
                word = read_word(raw, base, site)
                if word & 0x0E000000 != 0x0A000000 or word >> 28 == 15:
                    continue
                target = branch_target(site, word)
                if ENTRY <= target < ENTRY + 1508:
                    row = {'module': module, 'mode': 'arm', 'caller': hex(start),
                           'site': hex(site), 'opcode': hex(word), 'target': hex(target)}
                    (incoming if target == ENTRY else interiors).append(row)
        for offset in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, offset)[0]
            if ENTRY <= word < ENTRY + 1508:
                pointer_words.append({'module': module, 'address': hex(base + offset), 'word': hex(word)})
    if incoming != [{'module': 'ov001', 'mode': 'arm', 'caller': '0x21ec6c0',
                     'site': '0x21ec824', 'opcode': '0xebfffe04', 'target': '0x21ec03c'}]:
        raise ValueError(('Measured ARM incoming-call census changed', incoming))
    witnesses = {hex(address): hex(read_word(overlay, 0x021D7240, address)) for address in
        (0x021EC6D8, 0x021EC1C8, 0x021EC1CC, 0x021EC1D0, 0x021EC1DC, 0x021EC1E0,
         0x021EC214, 0x021EC218, 0x021EC2B0, 0x021EC2B8, 0x021F0590, 0x021F06F0,
         0x021F0708, 0x021F00E0, 0x021F00E4, 0x021F00E8, 0x021F0128, 0x021F0140)}
    if branch_target(0x021EC1D0, read_word(overlay, 0x021D7240, 0x021EC1D0)) != 0x021EC23C:
        raise ValueError('Nonzero +19 branch no longer bypasses the local R4 assignment')
    if read_word(overlay, 0x021D7240, 0x021EC6D8) != 0xE1A04000:
        raise ValueError('Parent descriptor return no longer occupies R4 at its measured assignment')
    for address, expected in ((0x021F0590, 0xE1A05003), (0x021F06F0, 0xE58D5000),
                              (0x021F00E0, 0xE59D1010), (0x021F00E4, 0xE3510000)):
        if read_word(overlay, 0x021D7240, address) != expected:
            raise ValueError('Critical-word forwarding/test instruction changed')
    for address, expected in ((0x021F0708, 0x021F00C4), (0x021F00E8, 0x021F01B0),
                              (0x021F0140, 0x0203D294)):
        if branch_target(address, read_word(overlay, 0x021D7240, address)) != expected:
            raise ValueError('Critical-word downstream branch witness changed')
    overlay0_entries = [span('ov000', address)[0] for address in (0x021EC4EC, 0x021EC5A0, 0x021EED08)]
    overlay0_metadata, unused, unused_config = measured_module('ov000')
    table = main[0xE2D64:0xE2DDC]
    if struct.unpack_from('<III', table, 24) != (0x021EC4EC, 0x021EC5A0, 0x021EED08):
        raise ValueError('Ambiguous overlapping-overlay callback words changed')
    if read_word(main, BASE, 0x020C3DEC) != 0x020E2D64:
        raise ValueError('Callback table literal changed')
    main_witnesses = {hex(address): hex(read_word(main, BASE, address)) for address in
                      (0x020C3B6C, 0x020C3B70, 0x020C3B74, 0x020C3B78, 0x020C3DEC)}
    return {'armIncomingBranches': incoming, 'armInteriorBranches': interiors,
            'alignedWordsInEntryRange': pointer_words, 'instructionWords': witnesses,
            'overlappingAddressCandidates': {'module': 'ov000', 'moduleSha256': overlay0_metadata['sha256'],
                'qualifiedEntryCandidates': overlay0_entries, 'overlayLoadMappingProven': False,
                'mainTable': {'address': '0x020e2d64', 'bytes': len(table), 'sha256': hashlib.sha256(table).hexdigest(),
                              'stride': 12, 'numericRow': 2, 'consumer': 'main/arm/020c3b60',
                              'consumerSpan': span('main', 0x020C3B60)[0],
                              'instructionWords': main_witnesses,
                              'selectorRead': 'u32(021D5398+2C)', 'stageRead': 'u32(021D5398+30)'},
                'interpretation': 'The two words are exact ov000 entries and numeric ov001 interiors; neither is accepted as an ov001 alternate entry'},
            'scope': 'ARM function spans and aligned words in initialized main and overlay001 only',
            'limitations': ['Thumb, BLX, indirect, dynamically populated pointers, other overlay load contexts and IRQ paths are not a complete census',
                            'Branch scanning does not independently certify every heuristic literal-pool boundary',
                            'Parent R4 carry relies on intervening callees preserving their ABI register; parent is not executed here']}


def execute(main, overlay, function_spans, providers, seed, state, count, entry_r4):
    rng = random.Random(seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(address, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    context = bytearray(0x64)
    context[0xB], context[0x15], context[0x19] = count & 255, 1, state
    struct.pack_into('<H', context, 0x36, ACTION)
    struct.pack_into('<I', context, 0x60, ACTOR)
    machine.mem_write(CONTEXT, bytes(context))
    machine.mem_write(LIST, struct.pack('<3I', *POINTERS))
    machine.mem_write(TOKENS, bytes(TOKEN_WORDS))
    actor = bytearray(rng.randbytes(1088))
    actor[0x31E] = 0
    for index, value in enumerate((-32768, -1, 32767)):
        struct.pack_into('<h', actor, 0x34E + 2 * index, value)
    machine.mem_write(ACTOR, bytes(actor))
    targets = []
    for index in range(3):
        target = bytearray(rng.randbytes(1088))
        target[0x31E], target[0x31F], target[0x357] = 1, index, (254, 255, 0)[index]
        struct.pack_into('<H', target, 0x34C, 0)
        targets.append(target)
        machine.mem_write(TARGETS + 1088 * index, bytes(target))
    descriptor = bytearray(rng.randbytes(40))
    descriptor[0x1E] = 3
    machine.mem_write(DESCRIPTOR, bytes(descriptor))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0], registers[1], registers[4] = ACTOR, ACTION, entry_r4
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected = bytearray(machine.mem_read(BASE, 0x400000))
    damage = 2 * max(0, count)
    for index in range(3):
        value = struct.unpack_from('<h', actor, 0x34E + index * 2)[0]
        value = ((value + damage + 32768) & 65535) - 32768
        if damage:
            struct.pack_into('<h', expected, ACTOR - BASE + 0x34E + index * 2, value)
        expected[TARGETS - BASE + index * 1088 + 0x357] = (targets[index][0x357] + 1) & 255
    expected_packets = [[POINTERS[member], TARGETS + target * 1088, ACTION, entry_r4,
                         0, TOKEN_WORDS[member], 0, 0, 0, 1, 0]
                        for target in range(3) for member in range(max(0, count))]
    packets, trace, writes, calls, pending, returned = [], [], [], [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp']:
                raise ValueError('Original nested helper did not restore SP on actual return')
            returned.append(item)
        if pc in (0x021E1A60, 0x021F0818):
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Original helper entered with wrong native mode')
            pending.append({'address': hex(pc), 'returnPc': engine.reg_read(UC_ARM_REG_LR),
                            'entrySp': engine.reg_read(UC_ARM_REG_SP)})
        if pc in providers:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('ARM provider entered in Thumb mode')
            arguments = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(4)]
            calls.append({'address': hex(pc), 'arguments': arguments})
            if pc == 0x0207AFEC:
                result = DESCRIPTOR
            elif pc == 0x021DB438:
                if arguments[0] != 1 or arguments[1] not in (0, 1, 2):
                    raise ValueError('Target provider domain exceeded')
                result = TARGETS + arguments[1] * 1088
            elif pc == 0x021DB8D0:
                result = 1
            elif pc == 0x021F2304:
                result = (arguments[0] - TARGETS) // 1088
            elif pc == 0x021F0578:
                call_sp = engine.reg_read(UC_ARM_REG_SP)
                packet = arguments + list(struct.unpack('<7I', bytes(engine.mem_read(call_sp, 28))))
                if len(packets) >= len(expected_packets) or packet != expected_packets[len(packets)]:
                    raise ValueError(('Original inherited R4/pointer-array/core packet differs', packet, expected_packets))
                packets.append(packet)
                result = 2
            elif pc == 0x021E9B84:
                raise ValueError('Nonzero +19 unexpectedly called the local critical initializer')
            else:
                result = 0
            engine.reg_write(UC_ARM_REG_R0, result & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        elif not any(start <= pc < start + length for start, length in function_spans):
            raise ValueError(('Native R4 probe escaped its explicit program/provider domains', hex(pc)))

    def written(engine, access, address, size, value, unused):
        regions = [(0x03010000, 0x10000), (ACTOR + 0x34E, 6)]
        regions += [(TARGETS + index * 1088 + 0x357, 1) for index in range(3)]
        if not any(base <= address and address + size <= base + length for base, length in regions):
            raise ValueError(('Native R4 probe exceeded declared stack/data writes', hex(address), size))
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending:
        raise ValueError('Original top-level/nested native code did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != 0 or len(packets) != len(expected_packets):
        raise ValueError('Original result or core-call count differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError('Original native executor changed preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected:
        raise ValueError(('Independent original caller memory model differs', seed))
    if len(returned) != 3 + len(packets):
        raise ValueError('Original helper/wrapper return count differs')
    return {'seed': seed, 'state19': state, 'signedCountB': count, 'entryR4': hex(entry_r4),
            'actualReturn': True, 'nestedNativeReturns': returned, 'corePackets': packets,
            'instructions': len(trace), 'providers': calls,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': hashlib.sha256(json.dumps(trace).encode()).hexdigest(),
            'writesSha256': hashlib.sha256(json.dumps(writes).encode()).hexdigest()}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    main_metadata, main, main_config = measured_module('main')
    metadata, overlay, config = measured_module('ov001')
    entries = [span('ov001', address)[0] for address in (ENTRY, 0x021E1A60, 0x021F0818, 0x021F0578, 0x021F00C4, 0x021EC6C0)]
    native_ranges = [(int(row['address'], 0), row['bytes']) for row in entries[:3]]
    providers = {0x021F0578}
    for site in range(ENTRY, ENTRY + 1508, 4):
        word = read_word(overlay, 0x021D7240, site)
        if word >> 24 == 0xEB:
            target = branch_target(site, word)
            if target not in (0x021E1A60, 0x021F0818):
                entry, unused, unused_metadata = span('main' if target < 0x02100000 else 'ov001', target)
                if entry['mode'] != 'arm':
                    raise ValueError('Native provider target is not qualified ARM')
                providers.add(target)
    audit = static_audit(main, overlay, main_config, config)
    results = []
    for state in (1, 255):
        for count in (-128, -1, 0, 1, 2, 3):
            for entry_r4 in (0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, DESCRIPTOR):
                results.append(execute(main, overlay, native_ranges, providers, 810000 + len(results), state, count, entry_r4))
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'moduleHashes': {'main': main_metadata['sha256'], 'ov001': metadata['sha256']},
              'qualifiedNativeSpans': entries, 'staticIncomingAndInteriorAudit': audit,
              'executions': len(results), 'actualTopReturns': len(results),
              'actualNestedNativeReturns': sum(len(row['nestedNativeReturns']) for row in results),
              'corePackets': sum(len(row['corePackets']) for row in results),
              'sourceMatchCredit': 0, 'nativeRngExecuted': False, 'ordinaryParentExecuted': False,
              'gameplayMeaningOfState19AndListCertified': False,
              'providerContract': 'Explicit ARM return-only providers preserve all registers except R0 and perform no writes; core result is fixed2',
              'limitations': ['Original executor, original nonzero-flags021E1A60 initialization path and original64B wrapper execute',
                             'Core021F0578, arithmetic, HP/status/IO/presentation bodies are providers; no game outcome or RNG trace certified',
                             'Entry R4 is an explicit synthetic machine register, not an invented C function parameter or source match',
                             'Descriptor-pointer R4 is compatible with the static ordinary parent under preserved-register ABI assumptions',
                             'Field19 nonzero and list membership are supplied fixture prerequisites, not observed scene state',
                             'No complete indirect/shared-entry, Thumb or loaded-overlay lifecycle proof'],
              'results': results, 'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': 'trace_enemy_initialization_context_20261029.py',
                  'sha256': sha256(ROOT / 'trace_enemy_initialization_context_20261029.py')}]}
    write_json(REPORT, report)
    print(json.dumps({key: report[key] for key in ('executions', 'actualNestedNativeReturns', 'corePackets', 'sourceMatchCredit')}))


if __name__ == '__main__':
    run()
