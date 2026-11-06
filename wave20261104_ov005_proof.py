import gzip
import json
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005'
WORK = ROOT / 'work/w4o5/proof'
SOURCE = ROOT / 'src/overlays/parallel_wave20261104/ov005'
ADDRESSES = ('021d755c', '021d87b4', '021da0bc', '021dbb80')
REGS = [getattr(R, 'UC_ARM_REG_R' + str(n)) for n in range(13)] + [R.UC_ARM_REG_SP, R.UC_ARM_REG_LR]
OBJECT = 0x02400000
INTERFACE = 0x02410000
METHODS = 0x02420000
INNER = 0x02430000
BUFFER = 0x02440000
OTHER = 0x02450000
SP = 0x027F0000
STOP = 0x027E0000


def build(address, source, directory, negative=False):
    C.WORK = directory / 'c'
    rows, unused = C.compare(source, 'ov005', '3,p' if address == '021dbb80' else '2',
                             'off', address == '021da0bc')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Compilation failed', rows))
    row = rows[0]
    bindings = qualified_bindings(row)
    try:
        proof = L.validate(row, bindings, directory / 'l')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0], dict):
            raise
        proof = dict(exactCallerBytes=False, comparison=error.args[0])
    body = (directory / 'l/caller.bin').read_bytes()
    with (directory / 'l/linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        symbol = next(s for s in symbols if s.name == row['name'])
        if symbol['st_value'] != int(row['address'], 0) or symbol['st_size'] != row['compiledBytes'] or len(body) != row['compiledBytes']:
            raise ValueError('Real linked caller boundary differs')
        if not any(s.name == '$a' and s['st_value'] == symbol['st_value'] for s in symbols):
            raise ValueError('Caller ARM mapping absent')
    if L.relocation_rows(ROOT / row['object'], row['name']) != L.relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Object relocation payload changed')
    row.update(program='', nativeSymbolEntries=bindings, realLink=proof)
    if not negative and (not proof['exactCallerBytes'] or not row['exactAfterDeclaredRelocation']):
        raise ValueError('Positive caller not exact')
    return row, body


def run(address, image, ordinal, overlay):
    origin = int(address, 16)
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(origin, image)
    word = [0, 1, 507, 508, 509, 65535, 65536, 0xFFFFFFFF][ordinal]
    supplied = [0, 1, 0xFFFFFFFF, 7, 0, 0x80000000, 1, 0][ordinal]
    randoms = [0xFEDCBA9876543210 ^ (ordinal * 0x102030405), 0x0123456789ABCDEF ^ (ordinal * 0x302010F0)]
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [OBJECT, BUFFER, word, OTHER]
    initial[-2:] = [SP, STOP]
    if address == '021d755c':
        vm.mem_write(OBJECT + 32, struct.pack('<I', INTERFACE))
        vm.mem_write(INTERFACE + 12, struct.pack('<I', METHODS))
        vm.mem_write(METHODS + 20, struct.pack('<I', 0x02670000))
        vm.mem_write(INTERFACE + 8, struct.pack('<I', 0x02670100 if ordinal % 3 else 0))
    elif address == '021da0bc':
        vm.mem_write(OBJECT + 32, struct.pack('<I', INTERFACE))
        vm.mem_write(INTERFACE + 12, struct.pack('<I', METHODS))
        vm.mem_write(METHODS + 36, struct.pack('<I', INNER))
        vm.mem_write(INNER, bytes([0xA5]) * 0x600)
        vm.mem_write(SP, struct.pack('<I', word))
    elif address == '021d87b4':
        vm.mem_write(OBJECT, bytes([0xA5]) * 80)
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal & 15) << 28 | 0x10)
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned = False
    targets = {0x02670000, 0x02670100, 0x02007A9C, 0x02008C28, 0x021D9910,
               0x02019BD4, 0x02008C14, 0x0201D444, 0x0205FF80, 0x02065730, 0x0205FF9C, 0x02045DC4}

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in targets:
            args = [uc.reg_read(r) for r in REGS[:4]]
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 24)).hex()
            calls.append(dict(address=location, words=args, stack=stack))
            result, high = 0x51000000 + len(calls), 0x62000000 + len(calls)
            if location == 0x02670000:
                result = supplied
            elif location == 0x02007A9C:
                value = randoms[len(calls) - 1]
                result, high = value & 0xFFFFFFFF, value >> 32
            elif location == 0x02008C28:
                put(args[1], bytes(uc.mem_read(args[0], args[2])))
            elif location == 0x02008C14:
                put(args[1], bytes([args[0] & 255]) * args[2])
            elif location == 0x02019BD4:
                result = 0x12345678 ^ ordinal
            elif location == 0x0201D444:
                put(args[0], bytes([0x40 + ordinal]) * 32)
            elif location == 0x02065730:
                result = 11 + len(calls)
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for n, register in enumerate(REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + n)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_R1, high)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((len(calls) + ordinal) & 15) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, STOP + 4, count=5000)
    if not returned:
        raise ValueError(('No actual caller return', address, ordinal))
    registers = [vm.reg_read(register) for register in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Caller callee-saved register/SP mismatch')
    failures = []
    sequence = [c['address'] for c in calls]
    if address == '021d755c':
        notify = bool(supplied and ordinal % 3)
        if sequence != [0x02670000] + ([0x02670100] if notify else []) or registers[0] != supplied:
            failures.append('Conditional notify and preserved provider return')
        if calls[0]['words'][:2] != [OBJECT, BUFFER] or notify and calls[-1]['words'][:2] != [5, OBJECT + 16]:
            failures.append('Callback physical arguments')
    elif address == '021d87b4':
        expected = struct.pack('<IIII', randoms[0] & 3, (randoms[1] >> 2) & 3, 0, 0)
        expected += overlay[0x021E6E24 - 0x021D7240:0x021E6E64 - 0x021D7240]
        if sequence != [0x02007A9C, 0x02007A9C, 0x02008C28] or bytes(vm.mem_read(OBJECT, 80)) != expected:
            failures.append('Two 64-bit return selections, zero fields and measured data copy')
        if calls[-1]['words'][:3] != [0x021E6E24, OBJECT + 16, 64]:
            failures.append('Copy boundary arguments')
    elif address == '021da0bc':
        first = struct.unpack('<I', vm.mem_read(INNER, 4))[0]
        count, chunks, buffer = struct.unpack('<III', vm.mem_read(INNER + 0x420, 12))
        checks = [registers[0] == 1, first == OTHER, count == word, chunks == (word + 507) // 508,
                  buffer == BUFFER, bytes(vm.mem_read(INNER + 0x42C, 0x158)) == bytes(0x158),
                  struct.unpack('<I', vm.mem_read(OBJECT + 4, 4))[0] == word & 65535,
                  struct.unpack('<I', vm.mem_read(OBJECT + 24, 4))[0] == word & 65535,
                  struct.unpack('<H', vm.mem_read(OBJECT + 12, 2))[0] == (0x5678 ^ ordinal)]
        if not all(checks) or sequence != [0x021D9910, 0x02019BD4, 0x02008C14]:
            failures.append('Full unsigned ceil division, low16 stores, measured clear and returned success')
        if calls[0]['words'][0] != INNER or calls[1]['words'][:2] != [BUFFER, word] or calls[2]['words'][:3] != [0, INNER + 0x42C, 0x158]:
            failures.append('Initialization/checksum/clear physical boundaries')
    else:
        expected = [0x0201D444, 0x0205FF80] + [0x02065730] * 3 + [0x0205FF9C, 0x02045DC4]
        position = 128
        if sequence != expected:
            failures.append('Exactly three record calls and final configuration')
        for n, call in enumerate([c for c in calls if c['address'] == 0x02065730]):
            offset = 0x021E6E84 - 0x021D7240 + n * 2
            signed = struct.unpack_from('<b', overlay, offset)[0] & 0xFFFFFFFF
            if call['words'] != [0x021E9894 + n * 12, signed, 0, overlay[offset + 1]] or int.from_bytes(bytes.fromhex(call['stack'])[:4], 'little') != position:
                failures.append('Signed/unsigned table fields and accumulated fifth argument')
            position += 14 + n
        if calls[-1]['words'] != [0, 2, 0, 0] or bytes.fromhex(calls[-1]['stack'])[:8] != struct.pack('<II', 32, 32):
            failures.append('Final outgoing six arguments')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes,
                pcs=pcs, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))),
                modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned execution runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    info, overlay, unused = L.measured_module('ov005')
    matches, traces, negatives = [], [], []
    changes = {'021d755c': ('notify(5,', 'notify(6,'), '021d87b4': ('state->third = 0;', 'state->third = 1;'),
               '021da0bc': ('length / 508 + (length % 508 != 0)', 'length / 507 + (length % 507 != 0)'),
               '021dbb80': ('int position = 128;', 'int position = 129;')}
    for address in ADDRESSES:
        source = SOURCE / (address + '.c')
        row, body = build(address, source, WORK / address / 'positive')
        native = overlay[int(address, 16) - 0x021D7240:int(address, 16) - 0x021D7240 + row['bytes']]
        wrong = WORK / address / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        old, new = changes[address]
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C control mutation ambiguous')
        wrong.write_text(text.replace(old, new))
        badrow, badbody = build(address, wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(8):
            original = run(address, native, ordinal, overlay)
            rebuilt = run(address, body, ordinal, overlay)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=address, ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive model/full state mismatch', address, ordinal, original['modelFailures']))
            bad = run(address, badbody, ordinal, overlay)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=address, ordinal=ordinal, result=original))
        if not rejected:
            raise ValueError('Wrong C model was not rejected')
        negatives.append(dict(address=address, mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', address, row['bytes'], rejected, flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='ov005', program='',
                  moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
                  canonicalMatchedBytes=sum(r['bytes'] for r in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
                  negativeEvidence=negatives, inputManifest=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
                  generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
                  producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
                  limits=['Complete ordinary C configured ARM extents, actual pinned MW compile/link, unchanged object relocations.',
                          'Synthetic caller fixtures with full GPR/CPSR/ordered writes/calls/8MiB RAM equality and independent postconditions.',
                          'All external callbacks/helpers are supplied boundaries; native callee execution and source credit are zero.',
                          'Boundaries remain configured heuristic except complete compiled/linked extent and observed caller returns.',
                          'No hardware timing, gameplay meanings, arbitrary aliases, whole-module link or shared acceptance claimed.'])
    write_json(LANE / 'match.json', report)
    print(dict(functions=len(matches), bytes=report['canonicalMatchedBytes'], cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
