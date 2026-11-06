import gzip
import hashlib
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov003_config795_machine_20261101 as M

BASE = ROOT / 'nonmatching/overlay-lane/20261101-config795'


def build(name, address):
    source = BASE / name / 'source.c'
    c.WORK = ROOT / 'work/ol795' / name / 'compile'
    rows, _ = c.compare(source, 'ov003', '2', 'off', True)
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    bindings = qualified_bindings(row)
    canonicalDirectory = ROOT / 'work/ol795' / name / 'canonical'
    try:
        canonical = validate(row, bindings, canonicalDirectory)
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, canonicalDirectory, ROOT / 'work/ol795' / name / 'private', address)
    return row, canonical, proof, body


def profiles():
    output = []
    for mode in [0, 1, 2, 3, 4, 255, 256, 259, 0xFFFFFFFF]:
        for mask in [0, 1, 2, 3, 0x800, 0x801, 0x802, 0xFFFF]:
            for salt in [0x301, 0xF0FF]:
                output.append(dict(ordinal=len(output), state=mode, mask=mask, salt=salt, custom=[0x81234567, salt, 0xFFFFFFFF, 0x80000000, 0x12345678, 0], serviceReturn=(0x90000000 + len(output))))
    for mode in range(256):
        output.append(dict(ordinal=len(output), state=mode, mask=0x800, salt=0x8001, custom=[0, 1, 2, 3, 4, 5], serviceReturn=0xA5A5A5A5))
    return output


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'} | dict(nonStackMemorySha256=hashlib.sha256(result['memory']).hexdigest())


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('795 runtime mismatch')
    mainInfo, main, _ = measured_module('main')
    moduleInfo, overlay, _ = measured_module('ov003')
    near = build('near', 0x02650000)
    byte = build('wrong-u8', 0x02652000)
    zero = build('wrong-return', 0x02654000)
    images = {0x02650000: near[3], 0x02652000: byte[3], 0x02654000: zero[3]}
    traces = []
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, logicalNativeCompletions=0, suppliedCalls=0, independentModelPairs=0, orderedWriteDifferences=0, wrongByteReturns=0, wrongByteRejected=0, wrongBytePositive=0, wrongReturnReturns=0, wrongReturnRejected=0, wrongReturnPositive=0)
    for profile in profiles():
        results = []
        failures = []
        for entry in [M.ENTRY, 0x02650000, 0x02652000, 0x02654000]:
            vm = M.Machine(main, overlay, images, profile)
            result = vm.run(entry)
            results.append(result)
            failures.append(M.model(vm, result))
        original, candidate, wrongByte, wrongReturn = results
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov003-config795-model-rejected-20261101.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('795 original/near independent model failed', profile, failures[:2]))
        keys = ['rawR0', 'calls', 'arrayInputs', 'memory', 'writes', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov003-config795-candidate-rejected-20261101.json', dict(profile=profile, differences=differences, results=list(map(compact, results))))
            raise ValueError(('795 near differs', profile, differences))
        byteRejected = bool(failures[2]) or any(original[key] != wrongByte[key] for key in keys)
        zeroRejected = bool(failures[3]) or any(original[key] != wrongReturn[key] for key in keys)
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        totals['actualNativeReturnInstructions'] += original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['logicalNativeCompletions'] += len(original['nativeCompletions']) + len(candidate['nativeCompletions'])
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        totals['wrongByteReturns'] += 1
        totals['wrongByteRejected' if byteRejected else 'wrongBytePositive'] += 1
        totals['wrongReturnReturns'] += 1
        totals['wrongReturnRejected' if zeroRejected else 'wrongReturnPositive'] += 1
        traces.append(dict(profile=profile, original=compact(original), candidate=compact(candidate), wrongByte=compact(wrongByte), wrongReturn=compact(wrongReturn), modelFailures=failures, differences=differences, byteRejected=byteRejected, zeroRejected=zeroRejected))
    if not totals['wrongByteRejected'] or not totals['wrongReturnRejected']:
        raise ValueError('795 missing returning control rejection')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/generated/ov003-config795-traces-20261101.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, nativeMatchingCredit=0, processor='arm9', program='', module='ov003', mode='arm', address=hex(M.ENTRY), nativeBytes=756, compiledBytes=near[0]['compiledBytes'], canonicalMatchingBytes=near[1]['matchingBytes'], romSha256=sha256(ROOT / 'inputs/game.nds'), mainSha256=mainInfo['sha256'], moduleSha256=moduleInfo['sha256'], candidate=near[0], canonicalComparison=near[1], privateLink=near[2], negativeEvidence=dict(byte=dict(source=byte[0], canonicalComparison=byte[1], privateLink=byte[2]), zeroReturn=dict(source=zero[0], canonicalComparison=zero[1], privateLink=zero[2])), totals=totals, allPassed=True, fullBehaviorQualified=False, fullTraces=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), uncompressedSha256=hashlib.sha256(raw).hexdigest()), generatorSha256=sha256(__file__), machineSha256=sha256(ROOT / 'ov003_config795_machine_20261101.py'), limits=['Explicit synthetic mode word, input mask, 256 unsigned16 table values, prior global contents and six custom words.', 'Actual getters, six setters,24-byte copy tail chain and dirty writer execute. Three remaining services are supplied without RAM effects; captured caller-prepared views are not complete formal signatures.', 'Private images are identically mapped; original code untouched; stack027E0000..027F0100 excluded from final memory equality.', 'Zero exact/source credit; no ordinary-scene or full service behavior claim.'])
    write_json(ROOT / 'evidence/attempts/ov003-config795-functional-near-20261101.json', report)
    print(totals, flush=True)


if __name__ == '__main__':
    main()
