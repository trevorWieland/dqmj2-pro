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
import match_runtime as C
from project import configuration, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import wave20261102_ov000_proof as B

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/overlay000'
WORK = ROOT / 'work/parallel-wave20261102/overlay000/breadth-proof'
SOURCE = ROOT / 'src/ov000/parallel_wave20261102/breadth'


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def prepare():
    if (LANE / 'breadth-inputs.json').exists():
        raise ValueError('Breadth packet already sealed')
    entries = []
    for name in ['breadth-sweep.json', 'breadth-refined.json', 'families-sweep.json']:
        report = json.loads((LANE / name).read_text())
        for result in report['exact']:
            row = result['source']
            address = int(row['address'], 0)
            target = SOURCE / f'{address:08x}' / f'native_ov000_{address:08x}.c'
            target.parent.mkdir(parents=True, exist_ok=True)
            source = ROOT / row['source']
            text = source.read_text().replace(' { ', '\n{\n    ').replace('; ', ';\n    ').replace(' }', '\n}')
            target.write_text(text)
            target.with_name('context.h').write_bytes(source.with_name('context.h').read_bytes())
            entries.append(dict(address=row['address'], bytes=row['bytes'], mode='arm', module='ov000', processor='arm9', program='', source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target), header=target.with_name('context.h').relative_to(ROOT).as_posix(), headerSha256=sha256(target.with_name('context.h')), compilerPath=row['compilerPath'], compilerSha256=row['compilerSha256'], optimization=row['compilerFlags'][0][2:], speed='speed' in row['compilerFlags'], targetSha256=row['targetSha256'], priorMeasurement=dict(report=name, sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])))
    dump(LANE / 'breadth-inputs.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], entries=entries, sourceCredit=0))
    claim = json.loads((LANE / 'claim.json').read_text())
    for item in entries:
        selected = next(row for row in claim['claimedFunctions'] if row['address'] == item['address'])
        selected['sourceTarget'] = item['source']
    dump(LANE / 'claim.json', claim)
    print(dict(frozen=len(entries), bytes=sum(row['bytes'] for row in entries)), flush=True)


def build(item, source, directory, origin=None):
    C.WORK = directory / 'compile'
    rows, unused = C.compare(source, 'ov000', item['optimization'], 'off', item['speed'], compiler=ROOT / item['compilerPath'])
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Breadth compile failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    try:
        proof = validate(row, qualified_bindings(row), directory / 'canonical')
    except ValueError as error:
        if origin is None:
            raise
        proof = error.args[0]
    if origin is None:
        return dict(**row, realLink=proof), (directory / 'canonical/caller.bin').read_bytes()
    private, body = link_private(row, qualified_bindings(row), directory / 'canonical', directory / 'private', origin)
    return dict(source=row, canonicalComparison=proof, privateLink=private), body


def profile_rows(entry):
    if entry in [0x021E8C18, 0x021E8C34, 0x02210864, 0x02210880]:
        return [dict(kind='exchange', index=i, before=a, value=b) for i, a, b in itertools.product([0, 1, 7, 15], [0, 127, 128, 255], [0, 0x80, 0x123456FF])]
    if entry == 0x021DA434:
        return [dict(kind='flag', flag=value) for value in [0, 1, 0x80000000, 0xFFFFFFFF]]
    if entry in [0x021E3444, 0x021E7BF4, 0x02209C34]:
        stride, offset, count = {0x021E3444: (0x34, 0x1C, 64), 0x021E7BF4: (0x2CC, 0x274, 8), 0x02209C34: (0x2C4, 0x274, 48)}[entry]
        return [dict(kind='search', stride=stride, offset=offset, count=count, firstZero=i) for i in range(-1, count)]
    if entry == 0x021D8AE8:
        return [dict(kind='copy', null=null, vector=vector) for null, vector in itertools.product([True, False], [[0, 0, 0], [0xFFFFFFFF, 0x80000000, 0x7FFFFFFF], [0x12345678, 0x87654321, 0xA5A5A5A5]])]
    return [dict(kind='forward', index=i, raw=[0xFFFFFFFF, 0x87654321, 0x80000000]) for i in [0, 1, 7, 15]]


def run(entry, image, origin, p, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(B.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(origin, image)
    rng = random.Random(p['ordinal'])
    registers = [rng.getrandbits(32) for unused in B.REGS]
    registers[13:15] = [B.SP, B.STOP]
    extent = dict(exchange=28, flag=32, search=52, copy=40, forward=36)[p['kind']]
    literal = struct.unpack_from('<I', overlay, entry - 0x021D7240 + extent - 4)[0]
    if p['kind'] == 'exchange':
        stride = 0x2CC if entry < 0x02200000 else 0x2C4
        target = literal + p['index'] * stride
        vm.mem_write(target, bytes([p['before']]))
        registers[:2] = [p['index'], p['value']]
    elif p['kind'] == 'flag':
        registers[0] = B.CONTEXT
        vm.mem_write(B.CONTEXT, struct.pack('<I', p['flag']))
    elif p['kind'] == 'search':
        for index in range(p['count']):
            vm.mem_write(literal + index * p['stride'] + p['offset'], bytes([0 if index == p['firstZero'] else 0x80 | (index & 127)]))
    elif p['kind'] == 'copy':
        registers[0] = 0 if p['null'] else B.POINT
        vm.mem_write(B.POINT, struct.pack('<III', *p['vector']))
        vm.mem_write(literal, bytes([0xA5]) * 12)
    else:
        registers[:4] = [p['index'], *p['raw']]
    vm.reg_write(B.UC_ARM_REG_CPSR, 0x10 | ((p['ordinal'] & 15) << 28))
    for register, value in zip(B.REGS, registers):
        vm.reg_write(register, value)
    vm.mem_write(B.SP - 0x1000, bytes([p['ordinal'] & 255]) * 0x1000)
    helper = {0x021D8AE8: 0x021D8B10, 0x021DFE5C: 0x0202871C, 0x021DFE80: 0x020287AC}.get(entry)
    calls, writes, pcs, returned = [], [], [], []
    def memory(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(uc, address, size, unused):
        pcs.append(address)
        if address == B.STOP:
            returned.append(True)
            uc.emu_stop()
        elif address == helper:
            calls.append([uc.reg_read(register) for register in B.REGS[:4]])
            lr = uc.reg_read(B.UC_ARM_REG_LR)
            uc.reg_write(B.UC_ARM_REG_R0, 0xAABBCCDD)
            uc.reg_write(B.UC_ARM_REG_CPSR, 0xA0000010)
            uc.reg_write(B.UC_ARM_REG_PC, lr)
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, B.STOP + 4, count=2000)
    if not returned:
        raise ValueError('Breadth return sentinel not reached')
    result = [vm.reg_read(register) for register in B.REGS]
    if result[4:12] != registers[4:12] or result[13] != B.SP:
        raise ValueError('Breadth callee-saved/SP contract')
    failures = []
    if p['kind'] == 'exchange' and (result[0] != p['before'] or vm.mem_read(target, 1)[0] != (p['value'] & 255)):
        failures.append('Independent byte exchange model')
    if p['kind'] == 'flag' and (result[0] != int(bool(p['flag'])) or bytes(vm.mem_read(B.CONTEXT, 4)) != bytes(4)):
        failures.append('Independent flag consume model')
    if p['kind'] == 'search' and result[0] != (p['firstZero'] & 0xFFFFFFFF):
        failures.append('Independent first-zero search model')
    if p['kind'] == 'copy':
        if p['null']:
            if calls or bytes(vm.mem_read(literal, 12)) != bytes([0xA5]) * 12:
                failures.append('Null vector input changed state')
        elif len(calls) != 1 or calls[0][0] != literal or bytes(vm.mem_read(literal, 12)) != struct.pack('<III', *p['vector']):
            failures.append('Independent vector copy/forward model')
    if p['kind'] == 'forward' and (calls != [[literal + p['index'] * 0x18 + 4, *p['raw']]] or result[0] != 1):
        failures.append('Independent four-word forward model')
    return dict(registers=result, cpsr=vm.reg_read(B.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs, memorySha256=hashlib.sha256(bytes(vm.mem_read(0x02000000, 0x800000))).hexdigest(), modelFailures=failures, actualTopReturn=True)


def execute():
    inputs = json.loads((LANE / 'breadth-inputs.json').read_text())
    info, overlay, unused = measured_module('ov000')
    matches, traces, controls = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        if sha256(source) != item['sourceSha256'] or sha256(ROOT / item['header']) != item['headerSha256']:
            raise ValueError('Frozen breadth source/header changed')
        address = int(item['address'], 0)
        match, body = build(item, source, WORK / f'{address:08x}/source')
        native = overlay[address - 0x021D7240:address - 0x021D7240 + item['bytes']]
        if native != body:
            raise ValueError('Breadth complete exact bytes failed')
        text = source.read_text()
        if 'return previous;' in text:
            wrong = text.replace('return previous;', 'return previous ^ 1U;')
        elif 'return result;' in text:
            wrong = text.replace('return result;', 'return result ^ 1U;')
        elif '*flag = 0;' in text:
            wrong = text.replace('*flag = 0;', '*flag = 1;')
        elif 'return 1;' in text:
            wrong = text.replace('return 1;', 'return 0;')
        else:
            wrong = text.replace('021d8b10(&', '021d8b10((Vec3 *) ((u8 *) &').replace(');', ' + 4));')
        if wrong == text:
            raise ValueError('Breadth wrong-C site missing')
        controlDirectory = WORK / f'{address:08x}/negative'
        controlDirectory.mkdir(parents=True, exist_ok=True)
        controlSource = controlDirectory / source.name
        controlSource.write_text(wrong)
        controlSource.with_name('context.h').write_bytes((ROOT / item['header']).read_bytes())
        negative, wrongBody = build(item, controlSource, controlDirectory, 0x02650000)
        control = dict(address=item['address'], proof=negative, rejected=0, positive=0)
        for p in profile_rows(address):
            p['ordinal'] = len(traces)
            original = run(address, native, address, p, overlay)
            candidate = run(address, body, address, p, overlay)
            if original != candidate or original['modelFailures']:
                raise ValueError(('Breadth physical state/model failed', hex(address), p, original, candidate))
            wrongResult = run(address, wrongBody, 0x02650000, p, overlay)
            control['rejected' if wrongResult['modelFailures'] else 'positive'] += 1
            traces.append(dict(address=item['address'], profile=p, result=original))
        if not control['rejected']:
            raise ValueError(('Breadth wrong-C control not rejected', item['address']))
        controls.append(control)
        matches.append(match)
        print('proved', item['address'], 'cases', control['rejected'] + control['positive'], flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'breadth-traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], module='ov000', processor='arm9', program='', moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(row['bytes'] for row in matches), sourceCreditPendingIntegrator=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceReturns=len(traces) * 2, fullPhysicalRegistersCpsrCallsWritesAndRamEqual=True, negativeEvidence=controls, inputs=dict(path=(LANE / 'breadth-inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'breadth-inputs.json')), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)), limits=['Eleven ordinary C full-span exact functions; real pinned MW links include declared relocation bindings. Whole-module/ROM checks and shared acceptance remain coordinator-owned.', 'Synthetic bounded RAM domains; no aliasing, object lifetime, hardware, gameplay or original formal-arity claim. Main2871C/287AC and ov0008B10 remain supplied call boundaries, with zero callee source credit.', 'All positive functions actually return with preserved callee-saved GPRs/SP; exact native/source cases compare full registers/CPSR/raw calls/ordered writes and complete8MiB RAM. Independent models and privately linked wrong-C controls qualify byte exchanges, first-zero scans, flag consumption, vector copying and physical call forwarding.'])
    dump(LANE / 'breadth-match.json', report)
    print(dict(functions=len(matches), bytes=report['canonicalMatchedBytes'], cases=len(traces)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'execute'])
    globals()[parser.parse_args().action]()
