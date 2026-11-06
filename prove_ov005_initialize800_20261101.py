import gzip
import hashlib
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov005_initialize800_machine_20261101 as M

BASE = ROOT / 'nonmatching/overlay-lane/20261101-initialize800'


def build(variant, address):
    source = BASE / variant / 'source.c'
    c.WORK = ROOT / 'work/ol800' / variant / 'compile'
    rows, _ = c.compare(source, 'ov005', '2', 'off', False)
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = ROOT / 'work/ol800' / variant / 'canonical'
    bindings = qualified_bindings(row)
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, directory, ROOT / 'work/ol800' / variant / 'private', address)
    return row, canonical, proof, body


def profiles():
    flags = [0, 1, 2, 3, 0xFFFFFFFF, 0x80000000, 0x12345678, 0xFFFFFFFD, 0xAAAA5555, 0x5555AAAA, 0x40000000, 0x7FFFFFFF]
    return [dict(ordinal=index, flags=value, objectByte=(index * 23) & 255, mmioByte=(index * 37) & 255, x=index - 80, y=150 - index, returnWord=0 if index == 0 else 0x91230000 + index) for index, value in enumerate(flags)]


def compact(result):
    return {key: value for key, value in result.items() if key not in ['memory', 'mmio', 'vram']} | dict(nonStackRamSha256=hashlib.sha256(result['memory']).hexdigest(), mmioSha256=hashlib.sha256(result['mmio']).hexdigest(), vramSha256=hashlib.sha256(result['vram']).hexdigest())


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('800 pinned runtime differs')
    mainInfo, main, _ = measured_module('main')
    moduleInfo, overlay, _ = measured_module('ov005')
    near = build('near', 0x02650000)
    tile = build('wrong-tile', 0x02652000)
    zero = build('wrong-return', 0x02654000)
    images = {0x02650000: near[3], 0x02652000: tile[3], 0x02654000: zero[3]}
    totals = dict(pairs=0, actualTopReturns=0, actualNativeFillReturns=0, nativeVramWordWrites=0, suppliedCalls=0, independentModelPairs=0, returningTileControls=0, tileRejected=0, tilePositive=0, returningZeroControls=0, zeroRejected=0, zeroPositive=0)
    traces = []
    for profile in profiles():
        results = []
        failures = []
        for entry in [M.ENTRY, 0x02650000, 0x02652000, 0x02654000]:
            vm = M.Machine(main, overlay, images, profile)
            result = vm.run(entry)
            results.append(result)
            failures.append(M.model(vm, result))
        original, candidate, wrongTile, wrongZero = results
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov005-initialize800-model-rejected-20261101.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('800 original/near independent model failed', profile, failures[:2]))
        keys = ['rawR0', 'calls', 'writes', 'memory', 'mmio', 'vram', 'nativeReturns', 'fillArguments', 'vramWrites', 'vramWriteTraceSha256']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov005-initialize800-candidate-rejected-20261101.json', dict(profile=profile, differences=differences, results=list(map(compact, results))))
            raise ValueError(('800 near differs', profile, differences))
        tileRejected = bool(failures[2]) or any(original[key] != wrongTile[key] for key in keys)
        zeroRejected = bool(failures[3]) or any(original[key] != wrongZero[key] for key in keys)
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['actualNativeFillReturns'] += original['nativeReturns'] + candidate['nativeReturns']
        totals['nativeVramWordWrites'] += original['vramWrites'] + candidate['vramWrites']
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        totals['independentModelPairs'] += 1
        totals['returningTileControls'] += 1
        totals['tileRejected' if tileRejected else 'tilePositive'] += 1
        totals['returningZeroControls'] += 1
        totals['zeroRejected' if zeroRejected else 'zeroPositive'] += 1
        traces.append(dict(profile=profile, original=compact(original), candidate=compact(candidate), wrongTile=compact(wrongTile), wrongZero=compact(wrongZero), modelFailures=failures, differences=differences, tileRejected=tileRejected, zeroRejected=zeroRejected))
    if not totals['tileRejected'] or not totals['zeroRejected']:
        raise ValueError('800 missing returning control failures')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/generated/ov005-initialize800-traces-20261101.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, nativeMatchingCredit=0, module='ov005', processor='arm9', program='', mode='arm', address=hex(M.ENTRY), nativeBytes=1720, compiledBytes=near[0]['compiledBytes'], canonicalMatchingBytes=near[1]['matchingBytes'], candidate=near[0], canonicalComparison=near[1], privateLink=near[2], negativeEvidence=dict(tile=dict(source=tile[0], canonicalComparison=tile[1], privateLink=tile[2]), zeroReturn=dict(source=zero[0], canonicalComparison=zero[1], privateLink=zero[2])), romSha256=sha256(ROOT / 'inputs/game.nds'), mainSha256=mainInfo['sha256'], moduleSha256=moduleInfo['sha256'], totals=totals, allPassed=True, fullBehaviorQualified=False, fullTraces=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), uncompressedSha256=hashlib.sha256(raw).hexdigest()), generatorSha256=sha256(__file__), machineSha256=sha256(ROOT / 'ov005_initialize800_machine_20261101.py'), limits=['Synthetic prior flags, MMIO/VRAM shadows, row words, descriptor word and supplied constructor/file/graphics effects.', 'Original02008C58 executes all16 fills per top, including512KiB VRAM shadow; every VRAM write is individually checked as ascending aligned zero-word sequence and final image compared.', 'Remaining services are supplied. Captured caller-prepared views are not complete original formal ABI proof; hidden downstream effects, graphics/device coherence and ordinary scenes remain unsupported.', 'Private genuine links and all code images are identical across VMs; original executable intact; stack027E0000..027F0100 excluded from final RAM equality.', 'Zero exact source/function credit; full behavior is unqualified despite these boundary-model checks.'])
    write_json(ROOT / 'evidence/attempts/ov005-initialize800-functional-near-20261101.json', report)
    print(totals, flush=True)


if __name__ == '__main__':
    main()
