import gzip
import json
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import wave20261104_ov005_proof as H
import match_runtime as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005-second'
WORK = ROOT / 'work/w4o5b/proof'
SOURCE = ROOT / 'src/overlays/parallel_wave20261104/ov005'
ADDRESSES = ('021db6f8', '021db808')
REGS = H.REGS
SP = H.SP
STOP = H.STOP
STATE = 0x02400000
VALUE = 0x02410000
TICKS = 0x02420000
NAME = 0x02430000


def build(address, source, directory, negative=False):
    original = C.FLAGS[:]
    try:
        C.FLAGS = original + ['-opt', 'speed']
        return H.build(address, source, directory, negative)
    finally:
        C.FLAGS = original


def run(address, image, ordinal, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    origin = int(address, 16)
    vm.mem_write(origin, image)
    number = [0, 1, 9, 10, 99, 999, 1000, 65535][ordinal]
    first = [0, 999, 1000, 9999, 10000, 0xFFFFFFFF, 0x80000000, 100][ordinal]
    second = [0, 998, 999, 1000, 65535, 0xFFFFFFFF, 1, 123][ordinal]
    current = [0, 1, 0xFFFF, 123, 0x8000, 0x7FFF, 255, 42][ordinal]
    ticks = [0, 29, 30, 31, 65535, 0xFFFFFFFF, 0x80000000, 3600][ordinal]
    extra = [0, 1, 0xFFFF, 0x10000, 0xFFFFFFFF, 0x7FFFFFFF, 0x80000000, 100][ordinal]
    vm.mem_write(STATE + 0x40, struct.pack('<II', first, second))
    vm.mem_write(VALUE, struct.pack('<H', current))
    vm.mem_write(TICKS, struct.pack('<I', ticks))
    vm.mem_write(0x021E9A28 + 0x7C, struct.pack('<I', 0xA0000000 | ordinal))
    vm.mem_write(0x021E9818 + 0x14, struct.pack('<I', 0x5A5A5A5A))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[0] = number
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned = False
    targets = {0x020643B0, 0x02026144, 0x020877BC, 0x021DDED4, 0x02063F6C, 0x020633B0,
               0x02046AF4, 0x021DDEC4, 0x0206442C, 0x021DDDEC, 0x021DF3BC, 0x020643FC,
               0x021DF434, 0x020633BC, 0x021DB5D0, 0x0206434C, 0x021DB6F8, 0x02067DD4, 0x02067D54}
    targets.discard(origin)

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
            call = dict(address=location, words=args, stack=stack)
            if location in (0x021DDEC4, 0x021DDED4):
                call['buffer'] = bytes(uc.mem_read(args[1], 16)).hex()
            calls.append(call)
            result = 0x51000000 + len(calls)
            if location == 0x020643B0:
                result = 1000
            elif location == 0x02026144:
                result = number
            elif location == 0x02063F6C:
                result = STATE
            elif location == 0x020633B0:
                result = NAME
            elif location == 0x0206442C:
                result = VALUE
            elif location == 0x020633BC:
                result = TICKS
            elif location == 0x020643FC:
                result = current ^ 0x5A5A
            elif location == 0x0206434C:
                result = number
            elif location == 0x02067D54:
                result = extra
            elif location == 0x02046AF4:
                destination = struct.unpack('<I', bytes.fromhex(stack)[:4])[0]
                put(destination, struct.pack('<8H', *range(0x61, 0x69)))
            elif location == 0x020877BC:
                count = min(args[2] // 2, args[3])
                if not 0 <= count <= 8:
                    raise ValueError('Synthetic formatter exceeds bounded contract')
                put(args[1], struct.pack('<' + 'H' * count, *[0x41 + n for n in range(count)]))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for n, register in enumerate(REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + n)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((len(calls) + ordinal) & 15) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, STOP + 4, count=5000)
    if not returned:
        raise ValueError(('No returning caller fixture', address, ordinal))
    registers = [vm.reg_read(register) for register in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Caller callee-saved/SP contract differs')
    failures = []
    sequence = [c['address'] for c in calls]
    if address == '021db6f8':
        expected = [0x020643B0, 0x02026144, 0x020877BC]
        if number < 1000:
            expected += [0x020877BC]
        expected += [0x021DDED4]
        if sequence != expected or calls[1]['words'][:2] != [number * 1000, 1000]:
            failures.append('Input scaling and supplied signed division boundary')
        formatting = [c for c in calls if c['address'] == 0x020877BC]
        expected_numbers = [number // 10, number % 10] if number < 1000 else [100]
        expected_sizes = [16, 10] if number < 1000 else [4]
        expected_digits = [2, 1] if number < 1000 else [3]
        if [c['words'][0] for c in formatting] != expected_numbers or [c['words'][2] for c in formatting] != expected_sizes or [c['words'][3] for c in formatting] != expected_digits:
            failures.append('Narrow result branch, decimal division and byte capacity forwarding')
        display = calls[-1]
        if display['words'][0] != 11 or display['words'][2] != (4 if number < 1000 else 8):
            failures.append('Displayed selector and extent')
        if number < 1000 and bytes.fromhex(display['buffer'])[4:6] != struct.pack('<H', ord('.')):
            failures.append('Literal decimal separator in caller-owned halfword buffer')
    else:
        expected = [0x02063F6C, 0x020633B0, 0x02046AF4, 0x021DDEC4, 0x0206442C, 0x021DDDEC,
                    0x021DF3BC, 0x0206442C, 0x020643FC, 0x021DF434, 0x020877BC, 0x021DDEC4,
                    0x020877BC, 0x021DDEC4, 0x020633BC, 0x021DB5D0, 0x0206434C, 0x021DB6F8,
                    0x02067DD4, 0x02067D54, 0x021DDDEC]
        if sequence != expected:
            failures.append('Complete measured refresh call order')
        formatting = [c for c in calls if c['address'] == 0x020877BC]
        if [c['words'][0] for c in formatting] != [min(first, 9999), min(second, 999)] or [c['words'][2:] for c in formatting] != [[16, 4], [16, 3]]:
            failures.append('Independent unsigned cap and display width')
        entries = [c for c in calls if c['address'] == 0x021DDDEC]
        if [c['words'] for c in entries] != [[1, 19, 4, current], [14, 19, 3, (extra + 21) & 65535]]:
            failures.append('Measured scalar and low16 add conversion')
        if next(c for c in calls if c['address'] == 0x021DB5D0)['words'][0] != ticks // 30:
            failures.append('Unsigned tick division boundary')
        if next(c for c in calls if c['address'] == 0x021DB6F8)['words'][0] != number:
            failures.append('Forwarded scalar provider return')
        if struct.unpack('<I', vm.mem_read(0x021E9A28 + 0x7C, 4))[0] != (0xA0000000 | ordinal | 2) or struct.unpack('<I', vm.mem_read(0x021E9818 + 0x14, 4))[0] != 1:
            failures.append('Caller-owned flag OR and control state store')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes,
                pcs=pcs, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    info, overlay, unused = L.measured_module('ov005')
    matches, traces, negatives = [], [], []
    changes = {'021db6f8': ("buffer[cursor] = '.';", "buffer[cursor] = ',';"),
               '021db808': ('native_data_021e9818.value = 1;', 'native_data_021e9818.value = 0;')}
    for address in ADDRESSES:
        source = SOURCE / (address + '.c')
        row, body = build(address, source, WORK / address / 'positive')
        native = overlay[int(address, 16) - 0x021D7240:int(address, 16) - 0x021D7240 + row['bytes']]
        wrong = WORK / address / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        old, new = changes[address]
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C mutation ambiguous')
        wrong.write_text(text.replace(old, new))
        badrow, badbody = build(address, wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(8):
            original = run(address, native, ordinal, overlay)
            rebuilt = run(address, body, ordinal, overlay)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=address, ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive model/full state differs', address, ordinal, original['modelFailures']))
            bad = run(address, badbody, ordinal, overlay)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=address, ordinal=ordinal, result=original))
        if not rejected:
            raise ValueError('Whole-C negative model accepted')
        negatives.append(dict(address=address, mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', address, row['bytes'], rejected, flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='ov005', program='',
                  moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
                  canonicalMatchedBytes=sum(r['bytes'] for r in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
                  negativeEvidence=negatives, inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
                  generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
                  producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
                  limits=['Ordinary C complete configured ARM extents with genuine pinned MW links, unchanged object relocation payloads.',
                          'Sixteen bounded positive synthetic caller fixtures compare full GPR/CPSR/calls/writes/8MiB RAM with independent postconditions.',
                          'External scalar/formatting/display helpers and matched peer functions are supplied boundaries; native callee execution/source credit zero.',
                          'Formatting providers produce prescribed synthetic halfwords; actual formatter semantics, valid gameplay domains and hardware behavior remain unproved.',
                          'Full module integration and source acceptance are coordinator-owned; boundary confidence remains configured heuristic plus complete extent matching.'])
    write_json(LANE / 'match.json', report)
    print(dict(functions=len(matches), bytes=report['canonicalMatchedBytes'], cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
