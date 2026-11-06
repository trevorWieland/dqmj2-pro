import gzip
import hashlib
import json
import struct
import sys
import match_runtime as c
import unicorn
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov006_record807_machine_20261102 as M

BASE = ROOT / 'nonmatching/overlay-lane/20261102-record807'


def build(variant, address):
    source = BASE / variant / 'source.c'
    c.WORK = ROOT / 'work/ol807' / variant / 'compile'
    rows, _ = c.compare(source, 'ov006', '2', 'off', True)
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = ROOT / 'work/ol807' / variant / 'canonical'
    bindings = qualified_bindings(row)
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, directory, ROOT / 'work/ol807' / variant / 'private', address)
    return row, canonical, proof, body


def profiles():
    seeds = {}
    for seed in range(10000):
        state = (seed * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        seeds.setdefault((state >> 16) % 17, seed)
        if len(seeds) == 17:
            break
    if len(seeds) != 17:
        raise ValueError('807 deterministic RNG corpus incomplete')
    output = []
    for mask in range(32):
        output.append(dict(ordinal=mask, mask=mask, species=[-1, 1, 511, 32767][mask % 4], variant=[0, 1, 3, 255][mask % 4], level=[0, 50, 51, 75, 76, 255][mask % 6], seed=seeds[mask % 17], controlWord=0x81230000 + mask, returnWord=0 if mask % 13 == 0 else 0x95230000 + mask, baseWords=[(0xFFF08001 + index * 0x1111 + mask) & 0xFFFFFFFF for index in range(6)], capWords=[(0x7FFF7FFF - index * 0x101 + mask) & 0xFFFFFFFF for index in range(6)], statWords=[(0xFFFF8000 + index * 0x222 + mask) & 0xFFFFFFFF for index in range(6)]))
    return output


def compact(result):
    return {key: value for key, value in result.items() if key not in ['memory', 'record']} | dict(recordHex=result['record'].hex(), nonStackRamSha256=hashlib.sha256(result['memory']).hexdigest())


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('807 pinned runtime mismatch')
    mainInfo, main, _ = measured_module('main')
    moduleInfo, overlay, _ = measured_module('ov006')
    near = build('near', 0x02650000)
    buffer = build('wrong-second-byte', 0x02652000)
    zero = build('wrong-return', 0x02654000)
    originalBody = overlay[M.ENTRY - 0x021D7240:M.ENTRY - 0x021D7240 + 1092]
    canonicalBody = (ROOT / 'work/ol807/near/canonical/caller.bin').read_bytes()
    differingOffsets = [offset for offset in range(0, 1092, 4) if originalBody[offset:offset + 4] != canonicalBody[offset:offset + 4]]
    if differingOffsets != [0x26C, 0x270] or struct.unpack_from('<2I', originalBody, 0x26C) != (0xE58D0024, 0xE1A02007) or struct.unpack_from('<2I', canonicalBody, 0x26C) != (0xE1A02007, 0xE58D0024):
        raise ValueError('807 preserved canonical near mismatch changed')
    images = {0x02650000: near[3], 0x02652000: buffer[3], 0x02654000: zero[3]}
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, actualRngReturns=0, actualSlotReturns=0, suppliedCalls=0, independentModelPairs=0, returningBufferControls=0, bufferRejected=0, bufferPositive=0, returningZeroControls=0, zeroRejected=0, zeroPositive=0)
    traces = []
    for profile in profiles():
        results = []
        failures = []
        for entry in [M.ENTRY, 0x02650000, 0x02652000, 0x02654000]:
            vm = M.Machine(main, overlay, images, profile)
            result = vm.run(entry)
            results.append(result)
            failures.append(M.model(vm, result))
        original, candidate, wrongBuffer, wrongZero = results
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov006-record807-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('807 original/near model failed', profile, failures[:2]))
        keys = ['rawR0', 'calls', 'rawCalls', 'writes', 'record', 'rng', 'memory', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov006-record807-candidate-rejected-20261102.json', dict(profile=profile, differences=differences, results=list(map(compact, results))))
            raise ValueError(('807 near differs', profile, differences))
        bufferRejected = bool(failures[2]) or any(original[key] != wrongBuffer[key] for key in keys)
        zeroRejected = bool(failures[3]) or any(original[key] != wrongZero[key] for key in keys)
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        totals['actualNativeReturnInstructions'] += original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['actualRngReturns'] += sum(row['address'] == '0x203d294' for row in original['nativeCompletions'] + candidate['nativeCompletions'])
        totals['actualSlotReturns'] += sum(row['address'] == '0x2062e44' for row in original['nativeCompletions'] + candidate['nativeCompletions'])
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        totals['returningBufferControls'] += 1
        totals['bufferRejected' if bufferRejected else 'bufferPositive'] += 1
        totals['returningZeroControls'] += 1
        totals['zeroRejected' if zeroRejected else 'zeroPositive'] += 1
        traces.append(dict(profile=profile, original=compact(original), candidate=compact(candidate), wrongBuffer=compact(wrongBuffer), wrongZero=compact(wrongZero), modelFailures=failures, differences=differences, bufferRejected=bufferRejected, zeroRejected=zeroRejected))
    if not totals['bufferRejected'] or not totals['zeroRejected']:
        raise ValueError('807 missing returning negative controls')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/generated/ov006-record807-traces-20261102.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, nativeMatchingCredit=0, processor='arm9', program='', module='ov006', mode='arm', address=hex(M.ENTRY), nativeBytes=1092, compiledBytes=near[0]['compiledBytes'], canonicalMatchingBytes=near[1]['matchingBytes'], candidate=near[0], canonicalComparison=near[1], privateLink=near[2], negativeEvidence=dict(buffer=dict(source=buffer[0], canonicalComparison=buffer[1], privateLink=buffer[2]), zeroReturn=dict(source=zero[0], canonicalComparison=zero[1], privateLink=zero[2])), instructionDifference=dict(offsets=[hex(x) for x in differingOffsets], native='STR R0,[SP,#0x24]; MOV R2,R7', candidate='MOV R2,R7; STR R0,[SP,#0x24]', unchangedEveryOtherCanonicalByte=True, commuteScope='Distinct register/mapped aligned normal-stack destinations; no asynchronous observer, faults, code/PC introspection or instruction timing claim.'), romSha256=sha256(ROOT / 'inputs/game.nds'), mainSha256=mainInfo['sha256'], moduleSha256=moduleInfo['sha256'], totals=totals, allPassed=True, fullBehaviorQualified=False, fullTraces=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), uncompressedSha256=hashlib.sha256(raw).hexdigest()), generatorSha256=sha256(__file__), machineSha256=sha256(ROOT / 'ov006_record807_machine_20261102.py'), limits=['Allocator result and preallocated132-byte record are supplied; no native allocation/final byte33 initialization claim.', 'Actual template getter, UID lookup,2-byte clear, direct template-byte selector, slot copier, raw-byte setter,RNG17 and divider execute. Main7AEBC observer and stat/resource/cleanup services remain supplied.', 'Template holes exercise count-of-nonzero then prefix copying; legal game-template constraints unproved. All17 RNG outputs occur from explicitly supplied seeds, not future scene prediction.', 'All observed supplied-call GPR/stack snapshots, nonstack writes/RAM,132-byte record and RNG state compare; stack027E0000..027F0100 excluded for private frame/code addresses.', 'Zero exact source/function credit; ordinary scenes, true stat algorithm and downstream observer/service effects remain unsupported.'])
    write_json(ROOT / 'evidence/attempts/ov006-record807-functional-near-20261102.json', report)
    print(totals, flush=True)


if __name__ == '__main__':
    main()
