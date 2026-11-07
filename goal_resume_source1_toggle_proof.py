import copy
import gzip
import hashlib
import json
import shutil
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, sha256, write_json
from goal_resume_source1_compile import compare
import link_runtime_unit as linker
import match_runtime as compiler
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261106/goal-resume-source-1/first-toggle'
SOURCE = ROOT / 'src/runtime/goal_resume20261106/source_1/first'
WORK = ROOT / 'work/goal-resume-20261106/source-1/toggle-proof'
DATA, ADDRESS, STOP, SP = 0x021c5a11, 0x02072ea0, 0x027d0000, 0x027f0000
SYMBOL = 'native_data_021c5a11'


def original(row, binding, image, symbols, relocations):
    if (row.get('program') or '', row['processor'], row['module'], row['mode'], row['address'], row['bytes']) != ('', 'arm9', 'main', 'arm', hex(ADDRESS), 52):
        raise ValueError('Exact owned ARM caller namespace or extent differs')
    if (binding.get('program') or '', binding['processor'], binding['module'], binding['mode'], binding['kind'], binding['address']) != ('', 'arm9', 'main', 'data', 'data', hex(DATA)):
        raise ValueError('Exact common BSS row binding differs')
    native = image[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + 52]
    if hashlib.sha256(native).hexdigest() != row['targetSha256']:
        raise ValueError('Complete native toggle caller differs')
    if 'func_02072ea0 kind:function(arm,size=0x34) addr:0x02072ea0' not in symbols.splitlines():
        raise ValueError('Whole original caller boundary is missing')
    if 'data_021c5a11 kind:bss addr:0x021c5a11' not in symbols.splitlines():
        raise ValueError('Common row base lacks original BSS identity')
    expected = [(44, 6, 0, 0xe59f1024), (48, 7, 28, 0xe59f000c)]
    if len(row['relocations']) != len(expected):
        raise ValueError('Both and only original data pool references are required')
    witnesses = []
    for rel, (offset, addend, instruction_offset, instruction) in zip(row['relocations'], expected):
        if (rel['offset'], rel['type'], rel['symbol'], rel['target'], rel['addend']) != (offset, 2, SYMBOL, hex(DATA), addend):
            raise ValueError('Original common-object ABS32 origin or interior addend differs')
        pointer, origin = DATA + addend, ADDRESS + offset
        record = f'from:0x{origin:08x} kind:load to:0x{pointer:08x} module:main'
        inventory = f'data_{pointer:08x} kind:bss addr:0x{pointer:08x}'
        if record not in relocations.splitlines() or inventory not in symbols.splitlines():
            raise ValueError('Exact original interior-byte inventory or load record missing')
        word = struct.unpack_from('<I', native, instruction_offset)[0]
        calculated = ADDRESS + instruction_offset + 8 + (1 if word & 0x00800000 else -1) * (word & 4095)
        if word != instruction or calculated != origin or struct.unpack_from('<I', native, offset)[0] != pointer:
            raise ValueError('Original ARM PC-relative literal or pointer word differs')
        witnesses.append(dict(offset=offset, addend=addend, originalLoadRecord=record,
            originalInventoryRecord=inventory, pool=hex(origin), target=hex(pointer), width=1))
    if 'from:0x0206be1c kind:load to:0x02072ea0 module:main' not in relocations.splitlines():
        raise ValueError('Original callback pointer association missing')
    return dict(commonObjectBase=hex(DATA), stride=9, testedRowIndices=[0, 1],
        enabledByte=6, dirtyByte=7, minimumTypedBytes=18, completeObjectExtent=None,
        originalInteriorDataWitnesses=witnesses, externalStorageCredit=0,
        callbackPointerRecord='from:0x0206be1c kind:load to:0x02072ea0 module:main',
        callbackDispatcherExecuted=False)


def build(source, directory, negative=False):
    rows, unused = compare(source, directory / 'compile')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('One real compiled toggle caller is required')
    row = dict(rows[0], program='', sourceDependencies=[dict(path=source.with_name('toggle.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('toggle.h')))])
    binding = dict(program='', processor='arm9', module='main', mode='data', kind='data', address=hex(DATA))
    bindings = {SYMBOL: binding}
    info, image, symbols = linker.measured_module('main')
    if not negative:
        row['originalNamespaceWitnesses'] = original(row, binding, image, symbols, (ROOT / 'config/arm9/relocs.txt').read_text())
    try:
        proof = linker.validate(row, bindings, directory / 'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0], dict):
            raise
        proof = dict(exactCallerBytes=False, comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Wrong C unexpectedly matched the whole original caller')
    body = (directory / 'link/caller.bin').read_bytes()
    if linker.relocation_rows(ROOT / row['object'], row['name']) != linker.relocation_rows(directory / 'link/caller.o', row['name']):
        raise ValueError('Caller splitting modified original relocation payloads')
    row.update(nativeSymbolEntries=bindings, realLink=proof, sourceLanguage='C', ordinaryCBytes=0 if negative else 52, justifiedAssemblyBytes=0)
    return row, body


def fixtures():
    return [dict(index=i, enabled=e, dirty=d) for i in range(2) for e in [0, 1, 2, 0x7f, 0x80, 0xff] for d in [0, 1, 0xa7, 0xff]]


def run(body, fixture, image, ordinal):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, image)
    vm.mem_write(ADDRESS, body)
    start = DATA - 16
    seed = bytearray((n * 23 + ordinal * 17 + 11) & 255 for n in range(64))
    flag = 16 + fixture['index'] * 9 + 6
    seed[flag], seed[flag + 1] = fixture['enabled'], fixture['dirty']
    vm.mem_write(start, bytes(seed))
    initial = [0x11220000 + n * 0x1234 + ordinal for n in range(15)]
    initial[0], initial[13], initial[14] = fixture['index'], SP, STOP
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal % 16) << 28 | 0x10)
    for reg, value in zip(compiler.REGISTERS, initial):
        vm.reg_write(reg, value)
    writes, instructions = [], []
    returned = False
    def memory(vm, access, address, size, value, user):
        writes.append(dict(address=address, size=size, value=value))
    def code(vm, address, size, user):
        nonlocal returned
        if address == STOP:
            returned = True
            vm.emu_stop()
        elif ADDRESS <= address < ADDRESS + 44:
            instructions.append(address - ADDRESS)
        else:
            raise ValueError('Toggle entered an unowned instruction or literal pool')
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(ADDRESS, STOP + 4, count=100)
    if not returned:
        raise ValueError('Actual toggle caller did not return')
    result = 1 if fixture['enabled'] == 0 else 0
    expected = bytearray(seed)
    expected[flag], expected[flag + 1] = result, 1
    target = DATA + fixture['index'] * 9 + 6
    wanted_writes = [dict(address=target, size=1, value=result), dict(address=target + 1, size=1, value=1)]
    registers = [vm.reg_read(reg) for reg in compiler.REGISTERS]
    failures = []
    if bytes(vm.mem_read(start, len(seed))) != bytes(expected):
        failures.append('Independent logical-not and dirty-bit model; all other bytes untouched')
    if writes != wanted_writes:
        failures.append('Exactly two ordered byte writes at nine-byte row stride')
    if registers[4:] != initial[4:]:
        failures.append('Callee-saved registers, scratch r12, stack and actual return address preserved')
    if registers[:4] != [DATA + 7, 1, fixture['index'] * 9, result]:
        failures.append('Measured scratch-register exit observations')
    if vm.reg_read(R.UC_ARM_REG_CPSR) != (0x60000010 if fixture['enabled'] == 0 else 0x20000010):
        failures.append('Measured unsigned-byte compare exit condition flags')
    return dict(actualTopReturn=True, modelFailures=failures, registers=registers,
        cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), writes=writes, instructionOffsets=instructions,
        fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000, 0x800000))).hexdigest())


def data_controls(row):
    info, image, symbols = linker.measured_module('main')
    relocations = (ROOT / 'config/arm9/relocs.txt').read_text()
    binding = row['nativeSymbolEntries'][SYMBOL]
    changes = [('wrong-base', 'binding', 'address', hex(DATA + 1)), ('wrong-CPU', 'binding', 'processor', 'arm7'),
        ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
        ('function-kind', 'binding', 'kind', 'function'), ('wrong-mode', 'binding', 'mode', 'arm'),
        ('wrong-caller', 'row', 'address', hex(ADDRESS + 4)), ('partial-caller', 'row', 'bytes', 48)]
    rejected = []
    for label, owner, key, value in changes:
        a, b = copy.deepcopy(row), dict(binding)
        (a if owner == 'row' else b)[key] = value
        try:
            original(a, b, image, symbols, relocations)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Incorrect data/interface context admitted: ' + label)
    for label, key, value in [('wrong-origin', 'offset', 40), ('wrong-interior-addend', 'addend', 5), ('wrong-relocation-kind', 'type', 1)]:
        a = copy.deepcopy(row)
        a['relocations'][0][key] = value
        try:
            original(a, binding, image, symbols, relocations)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Incorrect original literal admitted: ' + label)
    for label, raw, inventory, records in [('changed-literal', image[:ADDRESS - 0x02000000 + 44] + bytes(4) + image[ADDRESS - 0x02000000 + 48:], symbols, relocations),
            ('missing-base-inventory', image, symbols.replace('data_021c5a11 kind:bss addr:0x021c5a11', ''), relocations),
            ('missing-origin-record', image, symbols, relocations.replace('from:0x02072ecc kind:load to:0x021c5a17 module:main', ''))]:
        try:
            original(row, binding, raw, inventory, records)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Missing original evidence admitted: ' + label)
    return dict(passed=True, rejected=rejected, sourceCredit=0, externalStorageCredit=0)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned fixture runtime differs')
    inputs = read_json(LANE / 'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen toggle input changed: ' + pin['path'])
    row, body = build(SOURCE / '02072ea0.c', WORK / 'positive')
    info, image, symbols = linker.measured_module('main')
    native = image[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + 52]
    traces = []
    for ordinal, fixture in enumerate(fixtures()):
        a, b = run(native, fixture, image, ordinal), run(body, fixture, image, ordinal)
        if a != b or a['modelFailures']:
            raise ValueError(('Original/rebuilt toggle or independent model differs', fixture, a, b))
        traces.append(dict(fixture=fixture, result=a))
    controls = data_controls(row)
    write_json(LANE / 'binding-controls.json', controls)
    variants = [('discard-toggle', '.enabled=!native_data_021c5a11[index].enabled', '.enabled=native_data_021c5a11[index].enabled'),
        ('wrong-dirty-value', '.dirty=1', '.dirty=0'),
        ('bitwise-instead-of-logical', '.enabled=!native_data_021c5a11[index].enabled', '.enabled=~native_data_021c5a11[index].enabled'),
        ('wrong-stride', '.dirty=1', '.dirty=1')]
    negatives = []
    text = (SOURCE / '02072ea0.c').read_text()
    for variant_index, (label, old, new) in enumerate(variants):
        if text.count(old) != 1:
            raise ValueError('Wrong-C mutation is not unique')
        folder = WORK / 'n' / str(variant_index)
        folder.mkdir(parents=True, exist_ok=True)
        source = folder / 'source.c'
        source.write_text(text.replace(old, new))
        header = (SOURCE / 'toggle.h').read_text()
        if label == 'wrong-stride':
            header = header.replace('enabled,dirty,padding', 'enabled,dirty').replace('sizeof(ToggleRow)==9', 'sizeof(ToggleRow)==8')
        (folder / 'toggle.h').write_text(header)
        bad, wrong = build(source, folder / 'build', True)
        rejected = []
        for ordinal, fixture in enumerate(fixtures()):
            result = run(wrong, fixture, image, ordinal)
            if result['modelFailures']:
                rejected.append(dict(fixture=fixture, failures=result['modelFailures'], actualTopReturn=result['actualTopReturn']))
        if not rejected:
            raise ValueError('Real compiled wrong C escaped independent toggle model')
        negatives.append(dict(case=label, proof=bad, rejected=rejected))
    folder = WORK / 'negative/prototype-width'
    folder.mkdir(parents=True, exist_ok=True)
    source = folder / 'source.c'
    source.write_text(text)
    (folder / 'toggle.h').write_text((SOURCE / 'toggle.h').read_text().replace('native_main_02072ea0(u32)', 'native_main_02072ea0(unsigned short)'))
    rejected, unused = compare(source, folder / 'compile')
    if len(rejected) != 1 or not rejected[0].get('compileFailed'):
        raise ValueError('Incompatible public C prototype was not rejected by the real compiler')
    write_json(LANE / 'prototype-control.json', dict(passed=True, case='conflicting-16-bit-index-prototype', actualCompilerRejected=True, sourceCredit=0))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    trace = LANE / 'traces.json.gz'
    trace.write_bytes(gzip.compress(raw, mtime=0))
    limits = ['One complete ordinary-C 52-byte leaf toggle; whole genuine pinned compiler/linker match, unchanged raw relocations and full literal pool.',
        '48 independent original/source fixture pairs require actual top returns, full GPR/CPSR/writes/8MiB RAM equality and an independent nine-byte-row logical-not/dirty-byte model.',
        'Rows0/1 and six Boolean/non-Boolean prior byte values are covered; other indices and invalid objects are unsupported, not credited.',
        'Common BSS base and both interior addends have exact original inventory, PC-relative literal/load records and callback-pointer provenance. Eighteen bytes are a minimum tested type view, not a storage completeness claim.',
        'Four real compiled wrong-C variants reject;14 namespace/origin/extent/data-evidence controls and a real incompatible-prototype compile reject. No imported callees, callback dispatcher, physical hardware or game scenes execute.',
        'All other reassigned functions remain unaccepted; no data/BSS/helper or assembly credit. Source-only ROM and Windows/Android execution remain separate obligations.']
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], program='', processor='arm9', module='main',
        moduleSha256=info['sha256'], allPassed=True, matches=[row], canonicalMatchedFunctions=1, canonicalMatchedBytes=52,
        cases=len(traces), actualNativeAndSourceCallerReturns=len(traces) * 2, nativeCalleeBodiesExecuted=0,
        externalStorageCredit=0, nativeSymbols={SYMBOL: hex(DATA)}, nativeSymbolBindings={SYMBOL: row['nativeSymbolEntries'][SYMBOL]},
        negativeEvidence=negatives, bindingLayoutControls=dict(path=(LANE / 'binding-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-controls.json')),
        generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), uncompressedSha256=hashlib.sha256(raw).hexdigest()),
        producer=Path(__file__).name, producerSha256=sha256(Path(__file__)), limits=limits))
    print(dict(functions=1, bytes=52, pairs=len(traces), wrongC=len(negatives), dataControls=len(controls['rejected'])), flush=True)


if __name__ == '__main__':
    execute()
