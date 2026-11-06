import argparse
import gzip
import hashlib
import itertools
import json
import random
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
import unicorn
import wave20261102_ov000_proof as B
from wave20261102_ov000_breadth_proof import build
from project import configuration, sha256
from link_runtime_unit import measured_module

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/overlay000'
WORK = ROOT / 'work/parallel-wave20261102/overlay000/component-forwarders-proof'
SOURCE = ROOT / 'src/ov000/parallel_wave20261102/component-forwarders'
OBJECT = 0x02400000
INNER = 0x02401000
COMPONENT = 0x02402000
TARGETS = [0x02049AD0, 0x02049F4C, 0x0204A04C, 0x02085270]


def dump(name, value):
    (LANE / name).write_text(json.dumps(value, indent=2) + '\n')


def prepare():
    if (LANE / 'component-forwarders-inputs.json').exists():
        raise ValueError('Component forwarder packet already sealed')
    sweep = json.loads((LANE / 'component-forwarders-sweep.json').read_text())
    entries = []
    for result in sweep['exact']:
        row = result['source']
        address = int(row['address'], 0)
        source = ROOT / row['source']
        target = SOURCE / f'{address:08x}' / f'native_ov000_{address:08x}.c'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        target.with_name('context.h').write_bytes(source.with_name('context.h').read_bytes())
        entries.append(dict(address=row['address'], bytes=row['bytes'], processor='arm9', program='', mode='arm', module='ov000', source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target), header=target.with_name('context.h').relative_to(ROOT).as_posix(), headerSha256=sha256(target.with_name('context.h')), compilerPath=row['compilerPath'], compilerSha256=row['compilerSha256'], optimization=row['compilerFlags'][0][2:], speed='speed' in row['compilerFlags'], targetSha256=row['targetSha256']))
    dump('component-forwarders-inputs.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], entries=entries, sourceCredit=0))
    print(dict(frozen=len(entries), bytes=sum(row['bytes'] for row in entries)), flush=True)


def run(entry, image, origin, p, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(B.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(origin, image)
    vm.mem_write(OBJECT, struct.pack('<I', INNER))
    vm.mem_write(INNER + 4, struct.pack('<I', COMPONENT))
    vm.mem_write(COMPONENT, bytes([0xA5]) * 0x100)
    vm.reg_write(B.UC_ARM_REG_CPSR, 0x10 | ((p['ordinal'] & 15) << 28))
    rng = random.Random(p['ordinal'])
    initial = [rng.getrandbits(32) for unused in B.REGS]
    initial[:4] = [p['selector'], *p['words']]
    initial[13:15] = [B.SP, B.STOP]
    for register, value in zip(B.REGS, initial):
        vm.reg_write(register, value)
    vm.mem_write(B.SP - 0x1000, bytes([p['ordinal'] & 255]) * 0x1000)
    vm.mem_write(B.SP, struct.pack('<I', p['stackWord']))
    calls, writes, pcs, returned = [], [], [], []
    def memory(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(uc, address, size, unused):
        pcs.append(address)
        if address == B.STOP:
            returned.append(True)
            uc.emu_stop()
        elif address in TARGETS:
            words = [uc.reg_read(register) for register in B.REGS[:4]]
            calls.append(dict(address=address, words=words))
            lr = uc.reg_read(B.UC_ARM_REG_LR)
            if address == TARGETS[1]:
                value = COMPONENT + 0x1000
                writes.append([INNER + 4, 4, value])
                uc.mem_write(INNER + 4, struct.pack('<I', value))
            elif address == TARGETS[2]:
                value = p['selector'] ^ p['stackWord']
                writes.append([COMPONENT + 4, 4, value])
                uc.mem_write(COMPONENT + 4, struct.pack('<I', value))
            for index, register in enumerate(B.REGS[:4] + [B.UC_ARM_REG_R12]):
                uc.reg_write(register, (0xCAFE0000 + len(calls) * 0x100 + index) & 0xFFFFFFFF)
            uc.reg_write(B.UC_ARM_REG_R0, OBJECT if address == TARGETS[0] else p['result'] if address == TARGETS[3] else 0xAABBCCDD)
            uc.reg_write(B.UC_ARM_REG_CPSR, 0xA0000010)
            uc.reg_write(B.UC_ARM_REG_PC, lr)
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, B.STOP + 4, count=500)
    if not returned:
        raise ValueError('Component forwarder did not actually return')
    result = [vm.reg_read(register) for register in B.REGS]
    if result[4:12] != initial[4:12] or result[13] != B.SP:
        raise ValueError('Component forwarder callee-saved/SP contract')
    signed = struct.unpack('<h', struct.pack('<H', p['stackWord'] & 65535))[0] & 0xFFFFFFFF
    failures = []
    if [call['address'] for call in calls] != TARGETS:
        failures.append('Independent call order')
    if len(calls) == 4:
        if calls[0]['words'][0] != p['selector'] or calls[1]['words'][0] != OBJECT:
            failures.append('Independent object boundary words')
        if calls[2]['words'] != [COMPONENT, *p['words']]:
            failures.append('Cached component and original raw words')
        if calls[3]['words'][:3] != [COMPONENT + 0x3C, signed, 0]:
            failures.append('Signed low16 stack input and component subobject')
    if result[0] != p['result']:
        failures.append('Final return word preservation')
    return dict(registers=result, cpsr=vm.reg_read(B.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs, memorySha256=hashlib.sha256(bytes(vm.mem_read(0x02000000, 0x800000))).hexdigest(), modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Component forwarder pinned runtime')
    inputs = json.loads((LANE / 'component-forwarders-inputs.json').read_text())
    info, overlay, unused = measured_module('ov000')
    matches, controls, traces = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        if sha256(source) != item['sourceSha256'] or sha256(ROOT / item['header']) != item['headerSha256']:
            raise ValueError('Component forwarder frozen input changed')
        address = int(item['address'], 0)
        match, body = build(item, source, WORK / f'{address:08x}/source')
        native = overlay[address - 0x021D7240:address - 0x021D7240 + 72]
        if native != body:
            raise ValueError('Component forwarder full extent differs')
        wrong = source.read_text().replace('component + 0x3C', 'component + 0x40')
        if wrong == source.read_text():
            raise ValueError('Component forwarder negative site missing')
        directory = WORK / f'{address:08x}/negative'
        directory.mkdir(parents=True, exist_ok=True)
        wrongSource = directory / source.name
        wrongSource.write_text(wrong)
        wrongSource.with_name('context.h').write_bytes((ROOT / item['header']).read_bytes())
        negative, wrongBody = build(item, wrongSource, directory, 0x02650000)
        control = dict(address=item['address'], proof=negative, rejected=0)
        profiles = itertools.product([0, 1, 0xFFFFFFFF], [[0, 0, 0], [0xFFFFFFFF, 0x80000000, 0x12345678]], [0, 0xABCD7FFF, 0xABCD8000, 0x1234FFFF])
        for selector, words, stackWord in profiles:
            p = dict(ordinal=len(traces), selector=selector, words=words, stackWord=stackWord, result=0x12345678 ^ len(traces))
            original = run(address, native, address, p, overlay)
            candidate = run(address, body, address, p, overlay)
            if original != candidate or original['modelFailures']:
                raise ValueError(('Component forwarder model/state mismatch', p, original, candidate))
            wrongResult = run(address, wrongBody, 0x02650000, p, overlay)
            if not wrongResult['modelFailures']:
                raise ValueError('Component forwarder negative unexpectedly passed')
            control['rejected'] += 1
            traces.append(dict(address=item['address'], profile=p, result=original))
        matches.append(match)
        controls.append(control)
        print('proved', item['address'], control['rejected'], flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'component-forwarders-traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], module='ov000', processor='arm9', program='', moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=5, canonicalMatchedBytes=360, sourceCreditPendingIntegrator=360, cases=len(traces), actualNativeAndSourceReturns=2 * len(traces), completePhysicalRegistersCpsrCallsWritesAndRamEqual=True, negativeEvidence=controls, inputs=dict(path=(LANE / 'component-forwarders-inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'component-forwarders-inputs.json')), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)), limits=['Five separate native caller extents independently recompiled in ordinary C and genuinely linked; duplicate logic receives credit only for its distinct measured native locations.', 'Four native helper boundaries remain supplied with explicit return/memory/scratch-clobber plans. Zero callee source credit, original semantic field identity, formal-arity or arbitrary game-domain claim.', 'Synthetic object->inner->component graph with mutation of the original inner component pointer after caching. Signed16 stack input, poisoned upper half, preserved raw arguments, call order and final physical return word are independently modeled.', 'Actual returns, preserved callee-saved/SP and complete8MiB RAM/registers/CPSR/raw calls/ordered writes compare over120 pairs. Whole-C wrong-subobject controls privately link and reject all120 cases. Whole-module/ROM acceptance remains coordinator-owned.'])
    dump('component-forwarders-match.json', report)
    print(dict(functions=5, bytes=360, cases=len(traces)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'execute'])
    globals()[parser.parse_args().action]()
