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
import wave20261102_ov000_proof as B
from wave20261102_ov000_breadth_proof import build
from project import configuration, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/overlay000'
WORK = ROOT / 'work/parallel-wave20261102/overlay000/tag-scans'
SOURCE = ROOT / 'src/ov000/parallel_wave20261102/tag-scans'
TARGETS = {0x021EC308: (9, 0x021EC348), 0x021F0354: (23, 0x021F0448), 0x021F31CC: (19, 0x021F320C), 0x0222B524: (14, 0x0222B564)}
OBJECTS = 0x02400000


def dump(name, value):
    (LANE / name).write_text(json.dumps(value, indent=2) + '\n')


def prepare():
    if (LANE / 'tag-scans-inputs.json').exists():
        raise ValueError('Tag scan packet already sealed')
    module = ROOT / 'extract/arm9_overlays/ov000.bin'
    data = module.read_bytes()
    claim = json.loads((LANE / 'claim.json').read_text())
    ledger = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines()]
    for address in TARGETS:
        if any(row['module'] == 'ov000' and int(row['address'], 0) == address and row['states']['moduleLinked'] for row in ledger):
            raise ValueError('Tag scan already accepted')
        if not any(int(row['address'], 0) == address for row in claim['claimedFunctions']):
            claim['claimedFunctions'].append(dict(id=f'{configuration()["romSha256"]}/arm9/ov000/arm/{address:08x}', processor='arm9', program='', module='ov000', mode='arm', address=hex(address), bytes=64, moduleSha256=sha256(module), targetSha256=hashlib.sha256(data[address - 0x021D7240:address - 0x021D7240 + 64]).hexdigest(), sourceTarget=f'src/ov000/parallel_wave20261102/tag-scans/{address:08x}/native_ov000_{address:08x}.c'))
            claim['nativeOpportunityBytes'] += 64
    dump('claim.json', claim)
    attempts, entries = [], []
    for address, (count, helper) in TARGETS.items():
        text = f'''#include "context.h"
void native_ov000_{address:08x}(s32 tag)
{{
    s8 index;
    for (index = 0; index < {count}; index++) {{
        u8 *object;
        object = native_fn_main_02049ad0(index);
        if (*(s8 *) (object + 4) == tag)
            native_fn_ov000_{helper:08x}(index);
    }}
}}
'''
        header = f'''typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_main_02049ad0(s32);
extern void native_fn_ov000_{helper:08x}(s32);
'''
        for ordinal, (optimization, speed, profile) in enumerate(itertools.product(['2', '1', '3'], [True, False], range(4))):
            directory = WORK / f'{address:08x}/{ordinal:03d}'
            directory.mkdir(parents=True, exist_ok=True)
            source = directory / 'source.c'
            source.write_text(text)
            source.with_name('context.h').write_text(header)
            C.WORK = directory / 'compile'
            rows, unused = C.compare(source, 'ov000', optimization, 'off', speed, compiler=ROOT / list(C.COMPILER_PINS)[profile])
            row = rows[0]
            result = dict(source=row)
            if row.get('exactAfterDeclaredRelocation'):
                result['realLink'] = validate(row, qualified_bindings(row), directory / 'link')
                target = SOURCE / f'{address:08x}/native_ov000_{address:08x}.c'
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
                target.with_name('context.h').write_bytes(source.with_name('context.h').read_bytes())
                entries.append(dict(address=row['address'], bytes=64, count=count, helper=helper, source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target), header=target.with_name('context.h').relative_to(ROOT).as_posix(), headerSha256=sha256(target.with_name('context.h')), compilerPath=row['compilerPath'], compilerSha256=row['compilerSha256'], optimization=optimization, speed=speed, targetSha256=row['targetSha256']))
                attempts.append(result)
                print('EXACT', hex(address), ordinal, flush=True)
                break
            attempts.append(result)
    dump('tag-scans-sweep.json', dict(attempts=attempts, sourceCredit=0))
    dump('tag-scans-inputs.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], entries=entries, sourceCredit=0))
    print(dict(frozen=len(entries), bytes=sum(row['bytes'] for row in entries)), flush=True)


def run(item, image, origin, p, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(B.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(origin, image)
    statuses = [(index * 37 + p['salt']) & 255 for index in range(item['count'])]
    if p['pattern'] == 'all':
        statuses = [p['tag'] & 255] * item['count']
    elif p['pattern'] == 'alternating':
        statuses = [p['tag'] & 255 if index & 1 else (p['tag'] + 1) & 255 for index in range(item['count'])]
    for index, status in enumerate(statuses):
        vm.mem_write(OBJECTS + index * 16 + 4, bytes([status]))
    initial = [random.Random(p['ordinal'] * 31 + index).getrandbits(32) for index in range(len(B.REGS))]
    initial[0] = p['tag']
    initial[13:15] = [B.SP, B.STOP]
    vm.reg_write(B.UC_ARM_REG_CPSR, 0x10 | ((p['ordinal'] & 15) << 28))
    for register, value in zip(B.REGS, initial):
        vm.reg_write(register, value)
    vm.mem_write(B.SP - 0x1000, bytes([p['ordinal'] & 255]) * 0x1000)
    calls, writes, pcs, returned = [], [], [], []
    def memory(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(uc, address, size, unused):
        pcs.append(address)
        if address == B.STOP:
            returned.append(True)
            uc.emu_stop()
        elif address in [0x02049AD0, item['helper']]:
            index = uc.reg_read(B.UC_ARM_REG_R0)
            if index >= item['count']:
                raise ValueError('Tag scan supplied boundary index exceeds domain')
            calls.append(dict(address=address, words=[uc.reg_read(register) for register in B.REGS[:4]]))
            lr = uc.reg_read(B.UC_ARM_REG_LR)
            if address == item['helper'] and p['mutate'] and index + 1 < item['count']:
                writes.append([OBJECTS + (index + 1) * 16 + 4, 1, p['tag'] & 255])
                uc.mem_write(OBJECTS + (index + 1) * 16 + 4, bytes([p['tag'] & 255]))
            for offset, register in enumerate(B.REGS[:4] + [B.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + offset)
            uc.reg_write(B.UC_ARM_REG_R0, OBJECTS + index * 16 if address == 0x02049AD0 else 0xAABBCCDD)
            uc.reg_write(B.UC_ARM_REG_CPSR, 0xA0000010)
            uc.reg_write(B.UC_ARM_REG_PC, lr)
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin, B.STOP + 4, count=5000)
    if not returned:
        raise ValueError('Tag scan actual return missing')
    result = [vm.reg_read(register) for register in B.REGS]
    if result[4:12] != initial[4:12] or result[13] != B.SP:
        raise ValueError('Tag scan callee-saved/SP contract')
    target = p['tag'] - 0x100000000 if p['tag'] & 0x80000000 else p['tag']
    expected = []
    for index in range(item['count']):
        expected.append([0x02049AD0, index])
        status = statuses[index] - 256 if statuses[index] & 128 else statuses[index]
        if status == target:
            expected.append([item['helper'], index])
            if p['mutate'] and index + 1 < item['count']:
                statuses[index + 1] = p['tag'] & 255
    failures = [] if expected == [[call['address'], call['words'][0]] for call in calls] else ['Independent signed8 tag scan and dynamic next-record mutation model']
    return dict(registers=result, cpsr=vm.reg_read(B.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs, memorySha256=hashlib.sha256(bytes(vm.mem_read(0x02000000, 0x800000))).hexdigest(), modelFailures=failures, actualTopReturn=True)


def execute():
    inputs = json.loads((LANE / 'tag-scans-inputs.json').read_text())
    info, overlay, unused = measured_module('ov000')
    matches, controls, traces = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        if sha256(source) != item['sourceSha256'] or sha256(ROOT / item['header']) != item['headerSha256']:
            raise ValueError('Tag scan frozen input changed')
        address = int(item['address'], 0)
        match, body = build(item, source, WORK / f'proof/{address:08x}/source')
        native = overlay[address - 0x021D7240:address - 0x021D7240 + 64]
        if native != body:
            raise ValueError('Tag scan exact extent failed')
        directory = WORK / f'proof/{address:08x}/negative'
        directory.mkdir(parents=True, exist_ok=True)
        wrongSource = directory / source.name
        wrongSource.write_text(source.read_text().replace('== tag', '!= tag'))
        wrongSource.with_name('context.h').write_bytes((ROOT / item['header']).read_bytes())
        negative, wrongBody = build(item, wrongSource, directory, 0x02650000)
        control = dict(address=item['address'], proof=negative, rejected=0)
        for tag, pattern, mutate in itertools.product([0, 1, 127, 0xFFFFFF80, 0xFFFFFFFF, 0x10000080], ['mixed', 'all', 'alternating'], [False, True]):
            p = dict(ordinal=len(traces), tag=tag, pattern=pattern, mutate=mutate, salt=len(traces) & 255)
            original = run(item, native, address, p, overlay)
            candidate = run(item, body, address, p, overlay)
            if original != candidate or original['modelFailures']:
                raise ValueError(('Tag scan physical/model mismatch', p, original, candidate))
            wrong = run(item, wrongBody, 0x02650000, p, overlay)
            if not wrong['modelFailures']:
                raise ValueError('Tag scan whole-C negative passed')
            control['rejected'] += 1
            traces.append(dict(address=item['address'], profile=p, result=original))
        matches.append(match)
        controls.append(control)
        print('proved', item['address'], control['rejected'], flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'tag-scans-traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], module='ov000', processor='arm9', program='', moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(row['bytes'] for row in matches), sourceCreditPendingIntegrator=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceReturns=2 * len(traces), fullPhysicalRegistersCpsrCallsWritesAndRamEqual=True, negativeEvidence=controls, inputs=dict(path=(LANE / 'tag-scans-inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'tag-scans-inputs.json')), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)), limits=['Four full64-byte ordinary C caller loops with signed8 index/tag loads and distinct measured limits9/23/19/14; exact compiler and real MW linking established per extent.', 'Supplied object-lookup and action boundaries remain explicit; zero callee source credit or game-level identity/formal-arity claim.', 'Independent model verifies ordered physical call indices for all/no/alternating/mixed tags, signed-negative and poisoned full-word target values, and callback mutation of the next record. No arbitrary native object graph or runtime scene reachability claim.', 'All144 positive pairs actually return and preserve callee-saved/SP; complete registers/CPSR/raw calls/ordered writes/8MiB RAM match. Privately linked wrong-branch whole-C controls reject all144 cases. Whole-module/ROM checks remain coordinator-owned.'])
    dump('tag-scans-match.json', report)
    print(dict(functions=len(matches), bytes=report['canonicalMatchedBytes'], cases=len(traces)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'execute'])
    globals()[parser.parse_args().action]()
