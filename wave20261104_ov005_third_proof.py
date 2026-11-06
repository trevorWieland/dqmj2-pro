import gzip
import json
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import wave20261104_ov005_proof as H
import match_runtime as C
import link_runtime_unit as L
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005-third'
WORK = ROOT / 'work/w4o5c/proof'
SOURCE = ROOT / 'src/overlays/parallel_wave20261104/ov005'
ADDRESSES = ('021d7ee0', '021d7ab4')
OBJECT = 0x02400000
EVENT = 0x02410000
DATA = 0x02420000
CONFIGURATION = 0x02430000
ARM_CALLBACK = 0x02670000
THUMB_CALLBACK = 0x02671000


def build(address, source, directory, negative=False):
    original = C.FLAGS[:]
    try:
        C.FLAGS = original + (['-opt', 'speed'] if address == '021d7ab4' else [])
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
    variant = ordinal % 4
    index = [0, 15, 16, 31][variant]
    selector = ([0, 1, 2, 7, 9, 26, 8, 65535] if address == '021d7ee0' else
                [7, 8, 9, 21, 22, 26, 0, 65535])[ordinal // 4]
    callback = [ARM_CALLBACK, ARM_CALLBACK, THUMB_CALLBACK | 1, 0][variant]
    mask = 0x55AA if variant == 2 else 0 if address == '021d7ee0' else 65535
    length = [0, 1, 65535, 32768][variant]
    vm.mem_write(0x021E78C8, struct.pack('<I', OBJECT))
    vm.mem_write(OBJECT + 0x50E6, struct.pack('<H', mask))
    vm.mem_write(OBJECT + 0x50F8, struct.pack('<II', callback, CONFIGURATION))
    event = bytearray(20)
    struct.pack_into('<HHH', event, 0, 0xA5A5, 1 if variant == 1 else 0, selector if address == '021d7ab4' else 0x1234)
    struct.pack_into('<H', event, 8, selector if address == '021d7ee0' else 0xABCD)
    struct.pack_into('<IHH', event, 12, DATA, index if address == '021d7ee0' else length, index)
    vm.mem_write(EVENT, bytes(event))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [EVENT, DATA, CONFIGURATION, OBJECT]
    initial[-2:] = [H.SP, H.STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal & 15) << 28 | 0x10)
    for register, value in zip(H.REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned = False
    targets = {ARM_CALLBACK, THUMB_CALLBACK, 0x021D7FCC, 0x021D77AC, 0x021D7778}

    def memory(uc, access, location, size, value, user):
        writes.append(dict(address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == H.STOP:
            returned = True
            uc.emu_stop()
        elif location in targets:
            args = [uc.reg_read(r) for r in H.REGS[:4]]
            mode = 'thumb' if uc.reg_read(R.UC_ARM_REG_CPSR) & 32 else 'arm'
            if mode != ('thumb' if location == THUMB_CALLBACK else 'arm'):
                raise ValueError('Callback/provider entered in an unqualified instruction mode')
            call = dict(address=location, mode=mode, words=args,
                        stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex())
            if location in (ARM_CALLBACK, THUMB_CALLBACK) and args[0] in (8, 9):
                call['payload'] = bytes(uc.mem_read(args[1], 8)).hex()
            calls.append(call)
            result = int(variant != 1) if location == 0x021D7778 else 0x51000000 + len(calls)
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for n, register in enumerate(H.REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + n)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((len(calls) + ordinal) & 15) << 28 | 0x10 | (lr & 1) << 5)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, H.STOP + 4, count=5000)
    if not returned:
        raise ValueError(('Caller return missing', address, ordinal))
    registers = [vm.reg_read(register) for register in H.REGS]
    if registers[4:12] != initial[4:12] or registers[13] != H.SP:
        raise ValueError('Callee-saved/SP differs')
    failures = []
    sequence = [c['address'] for c in calls]
    expected_mask = mask
    notification = None
    expected = []
    if address == '021d7ee0':
        if selector == 0:
            expected = [0x021D7FCC]
            if calls[0]['words'][0] != EVENT:
                failures.append('Zero-code event forwarding')
        elif variant != 1 and selector == 7:
            expected_mask = (mask | (1 << index)) & 65535
            notification = [10, EVENT]
            if callback:
                expected.append(callback & ~1)
            if mask == 0:
                expected.append(0x021D77AC)
                if calls[-1]['words'][0] != OBJECT:
                    failures.append('First-mask transition object forwarding')
        elif variant != 1 and selector == 2:
            notification = [5, CONFIGURATION]
            if callback:
                expected.append(callback & ~1)
    else:
        expected = [0x021D7778]
        if calls[0]['words'][:2] != [OBJECT, EVENT]:
            failures.append('Validation provider physical arguments')
        if variant != 1 and selector == 21:
            notification = [8, None]
            if callback:
                expected.append(callback & ~1)
        elif variant != 1 and selector in (9, 26):
            expected_mask = mask & ~(1 << index) & 65535
            notification = [11, (1 << index) & 0xFFFFFFFF]
            if callback:
                expected.append(callback & ~1)
    if sequence != expected:
        failures.append('Independent event/filter/optional callback sequence')
    if struct.unpack('<H', vm.mem_read(OBJECT + 0x50E6, 2))[0] != expected_mask:
        failures.append('Exact low16 mask update')
    callbacks = [c for c in calls if c['address'] in (ARM_CALLBACK, THUMB_CALLBACK)]
    if callbacks:
        call = callbacks[0]
        if notification is None or call['words'][0] != notification[0] or notification[1] is not None and call['words'][1] != notification[1]:
            failures.append('Notification physical words')
        if notification and notification[0] == 8 and call.get('payload') != struct.pack('<IHH', DATA, length, (1 << index) & 65535).hex():
            failures.append('Stack payload pointer/low16 length/low16 bit field')
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
    changes = {'021d7ee0': ('object->notify(10, event);', 'object->notify(12, event);'),
               '021d7ab4': ('object->notify(8, &parameters);', 'object->notify(9, &parameters);')}
    for address in ADDRESSES:
        source = SOURCE / (address + '.c')
        row, body = build(address, source, WORK / address / 'positive')
        native = overlay[int(address, 16) - 0x021D7240:int(address, 16) - 0x021D7240 + row['bytes']]
        wrong = WORK / address / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        old, new = changes[address]
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C negative ambiguous')
        wrong.write_text(text.replace(old, new))
        badrow, badbody = build(address, wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(32):
            original = run(address, native, ordinal, overlay)
            rebuilt = run(address, body, ordinal, overlay)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=address, ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive full state/model differs', address, ordinal, original['modelFailures']))
            bad = run(address, badbody, ordinal, overlay)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=address, ordinal=ordinal, result=original))
        if not rejected:
            raise ValueError('Whole-C mutation not rejected')
        negatives.append(dict(address=address, mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', address, row['bytes'], rejected, flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='ov005', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
               canonicalMatchedBytes=sum(r['bytes'] for r in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               negativeEvidence=negatives, inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Ordinary C exact configured ARM extents and genuine pinned MW caller links with unchanged relocation payloads.',
                       '64 synthetic caller fixtures, eight selector values each, filter/status/null callbacks, low16 bit indices and actual ARM/Thumb callback modes.',
                       'Complete GPR/CPSR/calls/writes/8MiB RAM equality and independent mask/payload/transition postconditions; actual caller returns required.',
                       'All callbacks, validation and startup providers are supplied boundaries; zero native callee execution and source credit.',
                       'Source types describe consumed offsets/physical words; game semantics, arbitrary pointer aliasing, out-of-domain shifts and hardware behavior unproved.',
                       'Whole module admission and accepted source credit remain coordinator-owned.']))
    print(dict(functions=len(matches), bytes=sum(r['bytes'] for r in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
