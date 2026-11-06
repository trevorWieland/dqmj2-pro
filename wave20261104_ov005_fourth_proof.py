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

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005-fourth'
WORK = ROOT / 'work/w4o5d/proof'
SOURCE = ROOT / 'src/overlays/parallel_wave20261104/ov005/021d81f4.c'
ADDRESS = '021d81f4'
OBJECT = 0x02400000
EVENT = 0x02410000
CONFIGURATION = 0x02420000
ARM_CALLBACK = 0x02670000
THUMB_CALLBACK = 0x02671000


def build(source, directory, negative=False):
    original = C.FLAGS[:]
    try:
        C.FLAGS = original + ['-opt', 'speed']
        return H.build(ADDRESS, source, directory, negative)
    finally:
        C.FLAGS = original


def run(image, ordinal, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    origin = int(ADDRESS, 16)
    vm.mem_write(origin, image)
    scenario, variant = divmod(ordinal, 4)
    api = [0, 12, 14, 14, 99, 12][scenario]
    reason = 10 if scenario == 2 else 9
    event_pointer = 0 if scenario == 0 else EVENT
    callback = [ARM_CALLBACK, THUMB_CALLBACK | 1, 0, ARM_CALLBACK][variant]
    permitted = variant != 3
    selector = [0, 1, 32768, 65535][variant]
    first = [0, 65535, 1, 32768][variant]
    second = [65535, 0, 32768, 1][variant]
    flag = variant % 2
    descriptor = bytes((n * 17 + ordinal) & 255 for n in range(192))
    changed = bytes((0xA0 + n + ordinal) & 255 for n in range(192))
    vm.mem_write(0x021E78C8, struct.pack('<I', OBJECT))
    vm.mem_write(OBJECT + 0x5120, descriptor)
    vm.mem_write(OBJECT + 0x5624, bytes([0x5A]) * 24)
    vm.mem_write(OBJECT + 0x50E8, struct.pack('<HH', first, second))
    vm.mem_write(OBJECT + 0x50F8, struct.pack('<II', callback, CONFIGURATION))
    vm.mem_write(CONFIGURATION + 0x16, struct.pack('<H', flag))
    vm.mem_write(EVENT, struct.pack('<6H', api, 0xAAAA, reason, 0xBBBB, 0xCCCC, selector))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [event_pointer, EVENT, OBJECT, CONFIGURATION]
    initial[-2:] = [H.SP, H.STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal & 15) << 28 | 0x10)
    for register, value in zip(H.REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned = False
    targets = {ARM_CALLBACK, THUMB_CALLBACK, 0x021D7778, 0x02008E0C, 0x02012CB8, 0x021D773C, 0x02013080, 0x021D7874}

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

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
                raise ValueError('Provider/callback mode differs')
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex()
            calls.append(dict(address=location, mode=mode, words=args, stack=stack))
            result = 0x51000000 + len(calls)
            if location == 0x021D7778:
                result = int(permitted)
            elif location == 0x02008E0C:
                if not 0 <= args[2] <= 192:
                    raise ValueError('Copy provider exceeded fixture contract')
                put(args[1], bytes(uc.mem_read(args[0], args[2])))
            elif location in (ARM_CALLBACK, THUMB_CALLBACK):
                put(OBJECT + 0x5120, changed)
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
        raise ValueError(('Caller did not return', ordinal))
    registers = [vm.reg_read(register) for register in H.REGS]
    if registers[4:12] != initial[4:12] or registers[13] != H.SP:
        raise ValueError('Callee-saved/SP contract differs')
    failures = []
    sequence = [c['address'] for c in calls]
    expected = []
    if not event_pointer:
        expected = [0x02008E0C] + ([callback & ~1] if callback else []) + [0x02008E0C, 0x02008E0C, 0x02012CB8, 0x021D773C]
        payload = changed if callback else descriptor
        rebuilt_descriptor = payload[:12] + descriptor[12:18] + payload[18:]
        if bytes(vm.mem_read(OBJECT + 0x5120, 192)) != rebuilt_descriptor or bytes(vm.mem_read(OBJECT + 0x5624, 24)) != payload[20:44]:
            failures.append('Six-byte pre-callback snapshot restored independently of twenty-four-byte post-callback saved copy')
        if struct.unpack('<I', vm.mem_read(OBJECT + 0x50F0, 4))[0] != 1:
            failures.append('Startup state store')
        start = next(c for c in calls if c['address'] == 0x02012CB8)
        if start['words'] != [0x021D812C, OBJECT + 0x5120, OBJECT + 0x5624, 1] or bytes.fromhex(start['stack'])[:4] != bytes(4):
            failures.append('Five physical startup arguments')
        notifications = [c for c in calls if c['address'] in (ARM_CALLBACK, THUMB_CALLBACK)]
        if notifications and notifications[0]['words'][:2] != [9, OBJECT + 0x5120]:
            failures.append('Optional descriptor callback physical words')
    else:
        expected = [0x021D7778]
        if calls[0]['words'][:2] != [OBJECT, EVENT]:
            failures.append('Validation provider physical arguments')
        if permitted and api == 12:
            expected += [0x02013080, 0x021D773C]
            start = next(c for c in calls if c['address'] == 0x02013080)
            if start['words'] != [origin, OBJECT + 0x1120, second, OBJECT + 0xF00] or bytes.fromhex(start['stack'])[:8] != struct.pack('<II', first, int(flag == 0)):
                failures.append('Six physical request arguments and explicit low16 boolean')
            if struct.unpack('<H', vm.mem_read(OBJECT + 0x50E4, 2))[0] != selector:
                failures.append('Event low16 selector store')
        elif permitted and api == 14 and reason == 10:
            expected.append(0x021D7874)
            if calls[-1]['words'][:3] != [OBJECT, 5, EVENT]:
                failures.append('Measured completion forwarding')
    if sequence != expected:
        failures.append('Null/validation/API/reason/optional callback sequence')
    transitions = [c for c in calls if c['address'] == 0x021D773C]
    if transitions:
        transition = transitions[0]
        preceding = calls[-2]
        if transition['words'][:3] != [OBJECT, 12 if not event_pointer else 14, 0x51000000 + calls.index(preceding) + 1]:
            failures.append('Request result and transition code forwarding')
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
    row, body = build(SOURCE, WORK / 'positive')
    origin = int(ADDRESS, 16)
    native = overlay[origin - 0x021D7240:origin - 0x021D7240 + row['bytes']]
    old, new = 'native_fn_02008e0c(saved, object->descriptor + 12, 6);', 'native_fn_02008e0c(saved, object->descriptor + 12, 4);'
    text = SOURCE.read_text()
    if text.count(old) != 1:
        raise ValueError('Whole-C mutation ambiguous')
    wrong = WORK / 'negative/source.c'
    wrong.parent.mkdir(parents=True, exist_ok=True)
    wrong.write_text(text.replace(old, new))
    badrow, badbody = build(wrong, wrong.parent / 'build', True)
    traces, rejected = [], 0
    for ordinal in range(24):
        original = run(native, ordinal, overlay)
        rebuilt = run(body, ordinal, overlay)
        if original != rebuilt or original['modelFailures']:
            write_json(LANE / 'fixture-failure.json', dict(ordinal=ordinal, original=original, rebuilt=rebuilt))
            raise ValueError(('Positive state/model differs', ordinal, original['modelFailures']))
        bad = run(badbody, ordinal, overlay)
        rejected += bool(bad['modelFailures'])
        traces.append(dict(address=hex(origin), ordinal=ordinal, result=original))
    if not rejected:
        raise ValueError('Wrong restore extent not rejected independently')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='ov005', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=[row], canonicalMatchedFunctions=1, canonicalMatchedBytes=row['bytes'],
               cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               negativeEvidence=[dict(address=hex(origin), mutation=[old, new], rejectedCases=rejected, proof=badrow)],
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Ordinary C complete configured ARM extent with pinned genuine MW compile/link and unchanged relocation payloads.',
                       'Twenty-four bounded caller fixtures compare complete registers/CPSR/calls/writes/8MiB RAM and independent forwarding/snapshot/restore models.',
                       'Optional ARM and Thumb descriptor callbacks prescribe mutations; original callback and SDK/helper bodies are supplied boundaries, zero native execution/source credit.',
                       'Native field offsets and consumed physical word widths are measured; game-level meaning, arbitrary aliases, hardware and full module acceptance unproved.']))
    print(dict(functions=1, bytes=row['bytes'], cases=len(traces), wholeCNegativeRejected=rejected), flush=True)


if __name__ == '__main__':
    execute()
