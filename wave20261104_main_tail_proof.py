import gzip
import json
import math
import shutil
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile
import wave20261104_main_tail_compiler as compiler
from wave20261104_main_tail_bindings import verify_original
from wave20261104_main_tail_controls import execute as controls
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-runtime-tail'
WORK = ROOT / 'work/w4mt/proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail'
CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
REGS = C.REGISTERS
STATUS_ONE = {'02057238', '0205727c', '020572cc', '02057324', '0205737c'}
CONDITIONAL = {'02057324', '0205737c'}
GAME_CALLS = {
    '02056390': [0x021F3E5C, 0x021F3F68, 0x021F3DAC], '02056460': [0x021F3EC4],
    '02056508': [0x021F3FEC], '02056628': [0x021E71A4], '020566b4': [0x021F4110],
    '02056718': [0x021F4174], '02056778': [0x02064000, 0x02064038], '020567c0': [0x0205C668],
    '02056818': [0x021E96CC], '02056acc': [0x021E31F0], '02056b24': [0x021E9738],
    '02056c34': [0x0205D718], '02056e64': [0x02221444], '020571e8': [0x0205E3F0],
    '02057238': [0x02040820], '0205727c': [0x021E9DF4], '020572cc': [0x021E9E4C],
    '02057324': [0x021E9794], '0205737c': [0x021E9AA0], '020574a4': [],
    '02057688': [0x0204071C], '020576d0': [0x0204071C], '02058490': [0x02208DCC],
    '02058824': [0x02209670], '02058868': [0x022096BC], '020588ac': [0x02209554],
    '02058980': [0x0205E61C], '020589c4': [0x0205E520]}


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(word):
    return struct.unpack('<f', struct.pack('<I', word))[0]


def signed(word):
    return word - 0x100000000 if word & 0x80000000 else word


def fixed(value):
    product = floating(bits(4096.0 * value))
    return int(floating(bits(0.5 + product if value > 0 else product - 0.5))) & 0xFFFFFFFF


def build(source, directory, negative=False):
    rows, unused = compiler.compare(source, directory / 'c')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Caller compile failed', rows))
    row = rows[0]
    row.update(program='', sourceDependencies=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))])
    bindings = qualified_bindings(row)
    if not negative:
        row['originalNamespaceWitnesses'] = verify_original(row, bindings)
    try:
        proof = L.validate(row, bindings, directory / 'l')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0], dict):
            raise
        proof = dict(exactCallerBytes=False, comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Whole-C wrong status unexpectedly matched')
    body = (directory / 'l/caller.bin').read_bytes()
    with (directory / 'l/linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        entry = next(s for s in symbols if s.name == row['name'])
        if entry['st_value'] != int(row['address'], 0) or entry['st_size'] != row['compiledBytes'] or len(body) != row['compiledBytes']:
            raise ValueError('Genuine linked caller boundary differs')
        if not any(s.name == '$a' and s['st_value'] == entry['st_value'] for s in symbols):
            raise ValueError('Genuine linked ARM mapping absent')
    if L.relocation_rows(ROOT / row['object'], row['name']) != L.relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Caller splitting changed original relocation payloads')
    row.update(nativeSymbolEntries=bindings, realLink=proof)
    return row, body


def run(row, body, ordinal, main, overlay):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(address, body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    supplied = [0, 1, -1, 127, 128, 255, -32768, 65535][ordinal]
    first = [0, 1, 255, 256, 257, 65535, 16777216, 128][ordinal]
    if name == '02056628':
        first = [-1.25, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 0.5, 1.25][ordinal]
    values = [first, [-1.25, -0.5, -1 / 8192, 0, 1 / 8192, 0.5, 1.25, 100][ordinal],
              [-129, -128, -1, 0, 127, 128, 255, 256][ordinal], [1.5, -1.5, 0.5, -0.5, 100, -100, 0, 1][ordinal], 0, 1, 2, 3]
    values = [floating(bits(v)) for v in values]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<8I', context, 16, *[bits(v) for v in values])
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((n * 31 + ordinal) & 255 for n in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    vm.mem_write(CONTEXT, bytes(context))
    vm.mem_write(INSTRUCTION, bytes(instruction))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [CONTEXT, INSTRUCTION, 0xDEADBEEF, 0xA5A55A5A]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned, changed = False, False
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned, changed
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            symbol = imports[location]
            args = [uc.reg_read(r) for r in REGS[:4]]
            calls.append(dict(symbol=symbol, address=location, words=args, stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex()))
            result = supplied & 0xFFFFFFFF
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol in ('_ffix', '_ffixu'):
                result = int(floating(args[0])) & 0xFFFFFFFF
            elif symbol == '_fflt':
                result = bits(float(signed(args[0])))
            elif symbol == '_ffltu':
                result = bits(float(args[0]))
            elif symbol in ('_fadd', '_fsub', '_fmul', '_fdiv'):
                left, right = floating(args[0]), floating(args[1])
                result = bits(left + right if symbol == '_fadd' else left - right if symbol == '_fsub' else left * right if symbol == '_fmul' else left / right)
            elif symbol == '_fgr':
                comparison = floating(args[0]) > floating(args[1])
                flags = (0x20000000 if comparison else 0x40000000) | 0x10
            else:
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
                if location == 0x021F3E5C:
                    put(args[1], struct.pack('<iii', (ordinal + 1) * 4096, -(ordinal + 1) * 2048, 123))
                elif location == 0x021F3F68:
                    result = ((ordinal + 1) * 4096 - 2048) & 0xFFFFFFFF
                elif location in (0x021E9794, 0x021E9AA0):
                    result = ordinal % 2
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, flags)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=5000)
    if not returned:
        raise ValueError(('Caller did not actually return', name, ordinal))
    registers = [vm.reg_read(register) for register in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved/SP differs')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    if [call['address'] for call in game] != GAME_CALLS[name]:
        failures.append('Independent provider call sequence')
    integer = [int(v) & 0xFFFFFFFF for v in values]
    expected_words = {
        '02056460': [integer[0], fixed(values[1])],
        '02056508': [integer[0], fixed(values[1]), fixed(values[2]), fixed(values[3])],
        '02056628': [0, fixed(values[0])], '020566b4': [integer[0], integer[1] & 255],
        '02056718': integer[:2], '020567c0': [integer[0], 1],
        '02056818': [integer[0], integer[1], ((integer[2] & 255) - 256 if integer[2] & 128 else integer[2] & 255) & 0xFFFFFFFF, integer[3]],
        '02056acc': [integer[0], 0], '02056b24': integer[:3], '02056c34': integer[:1],
        '02056e64': [INSTRUCTION + 8], '020571e8': [integer[0] & 255], '0205727c': [integer[0] & 255],
        '020572cc': [integer[0] & 255, (16 - (integer[0] & 255)) & 255], '02057324': integer[:1],
        '02057688': [1], '020576d0': [0]}
    if name in expected_words and game[0]['words'][:len(expected_words[name])] != expected_words[name]:
        failures.append('Independent conversion, narrowing, fixed rounding and provider physical arguments')
    if name == '02056390' and (game[0]['words'][0] != integer[0] or game[1]['words'][0] != integer[0] or game[2]['words'][:2] != integer[:2]):
        failures.append('Object, output-buffer and two-object physical forwarding')
    if name == '02056778' and game[1]['words'][0] != supplied & 0xFFFFFFFF:
        failures.append('Opaque provider returned word forwarded unchanged')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {}
    if name == '02056390':
        outputs = {0: ordinal + 1.0, 1: -(ordinal + 1) * 0.5, 2: 123 / 4096.0, 3: ordinal + 0.5}
    elif name == '02056460':
        outputs = {0: supplied / 4096.0}
    elif name in ('020567c0', '02056818', '02056acc', '02056b24', '02056c34', '02056e64'):
        outputs = {0: float(supplied)}
    for index, value in outputs.items():
        struct.pack_into('<I', expected, 16 + index * 4, bits(value))
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, selected record stride, conditional position and status model')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent instruction forwarding and supplied mutation model')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes,
                pcs=pcs, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    if {item['address'][2:].zfill(8) for item in inputs['entries']} != set(GAME_CALLS):
        raise ValueError('Frozen family caller set differs')
    info, main, unused = L.measured_module('main')
    overlay_info, overlay, unused = L.measured_module('ov000')
    matches, traces, negatives = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        name = format(int(item['address'], 0), '08x')
        directory = WORK / name
        row, body = build(source, directory / 'positive')
        if row['targetSha256'] != item['targetSha256'] or row['bytes'] != item['bytes']:
            raise ValueError('Frozen native caller span differs')
        origin = int(row['address'], 0)
        native = main[origin - 0x02000000:origin - 0x02000000 + row['bytes']]
        old = 'status = ' + str(int(name in STATUS_ONE)) + ';'
        new = 'status = ' + str(1 - int(name in STATUS_ONE)) + ';'
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C status mutation ambiguous')
        wrong = directory / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        wrong.write_text(text.replace(old, new))
        shutil.copyfile(SOURCE / 'context.h', wrong.with_name('context.h'))
        badrow, badbody = build(wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(8):
            original = run(row, native, ordinal, main, overlay)
            rebuilt = run(row, body, ordinal, main, overlay)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive model/full state differs', row['address'], ordinal, original['modelFailures']))
            bad = run(badrow, badbody, ordinal, main, overlay)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=row['address'], ordinal=ordinal, result=original))
        if rejected != 8:
            raise ValueError('Whole-C wrong status did not fail every independent context model')
        negatives.append(dict(address=row['address'], mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', name, row['bytes'], rejected, flush=True)
    qualification = controls(matches)
    write_json(LANE / 'binding-layout-controls.json', qualification)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
               canonicalMatchedBytes=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Ordinary readable C handlers, exact configured full extents, pinned SP1 compiler and real MW links; original ELF names/relocations stay intact.',
                       'Eight finite synthetic caller fixtures per function, actual top returns, complete GPR/CPSR/calls/writes/8MiB RAM equality and independent full context models.',
                       'Float helpers and opaque game functions are supplied boundaries with prescribed finite arithmetic, scratch clobbers, outputs and context/instruction mutations; zero native callee execution/source credit.',
                       'Original main relocation records qualify each overlay import; numeric address alone cannot establish its module. Eight MW ABI assertions and wrong-overlay/helper/layout controls are separate evidence.',
                       'Flexible record count, actual game domains, arbitrary aliases, NaNs/infinities/out-of-range float conversion, hardware timing and scene execution remain unproved.',
                       'Function boundaries retain configured confidence plus complete source/link matching and bounded returns; full shared acceptance remains coordinator-owned.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
