import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
import unicorn
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_neighbors892_machine_20261102 as M
import ov000_neighbors892_model_20261102 as G

SOURCE = ROOT / 'src/overlays/ov000_20261102_lookup893'
WORK = ROOT / 'work/ol893-proof'


def build(source, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov000', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('893 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        proof = validate(row, bindings, directory)
        return dict(**row, realLink=proof), (directory / 'caller.bin').read_bytes()
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'}


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('893 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov000-lookup893-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('893 input differs', row['path']))
    selected = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    if any(row['processor'] == 'arm9' and row['program'] == '' and row['module'] == 'ov000' and max(row['address'], M.FIND) < min(row['address'] + row['bytes'], M.FIND + 60) for row in selected):
        raise ValueError('893 accepted overlap')
    mainInfo, arm, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov000')
    match, body = build(SOURCE / 'lookup.c', 'source')
    template = (SOURCE / 'lookup.c').read_text()
    controls = []
    images = {}
    variants = [('wrong-return', template.replace('return found;', 'return found ^ 1U;')), ('truncated-needle', template.replace('needle ==', '(s16) needle ==')), ('zero-count-entry', template.replace('if (count > 0)', 'if (count >= 0)'))]
    for index, (name, text) in enumerate(variants):
        if text == template:
            raise ValueError('893 control site absent')
        directory = ROOT / 'nonmatching/overlay-lane/20261102-lookup893-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('893 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        origin = 0x02650000 + index * 0x2000
        proof, image = build(source, name, origin)
        images[origin] = image
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    traces, cases = [], []
    pcs = set()
    for p in [row for row in G.profiles() if row['kind'] == 'find']:
        results, failures = [], []
        for kind, start in [('native', M.FIND), ('source', M.FIND)] + [(row['name'], row['origin']) for row in controls]:
            vm = M.Machine(arm, overlay, images, p)
            if kind == 'source':
                vm.u.mem_write(M.FIND, body)
            result = vm.run(start, M.FIND)
            result['kind'] = kind
            results.append(result)
            failures.append(G.model(vm, result))
        if failures[0] or failures[1]:
            raise ValueError(('893 independent model failed', p['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'indicesHex', 'memory', 'calls', 'writes', 'originalHelperPhysicalReturns', 'helperPcs', 'instructions']
        differences = [key for key in keys if results[0][key] != results[1][key]]
        if differences:
            raise ValueError(('893 full physical state differs', differences))
        pcs.update(results[0]['helperPcs'])
        for index, row in enumerate(controls):
            row['actualTopReturns'] += 1
            row['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=p, results=list(map(compact, results)), modelFailures=failures, physicalDifferences=differences)
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        traces.append(trace)
        cases.append(dict(ordinal=p['ordinal'], actualTopReturns=2, traceSha256=hashlib.sha256(raw).hexdigest()))
    if pcs != set(range(M.FIND, M.FIND + 60, 4)) or any(not row['rejected'] for row in controls):
        raise ValueError('893 coverage/returning controls incomplete')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov000-lookup893-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov000', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=60, sourceCreditPendingIntegrator=60, allPassed=True, totals=dict(pairs=len(cases), actualTopReturns=len(cases) * 2, actualNativeHelperReturns=0, suppliedCalls=0, independentModelPairs=len(cases)), allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allOrderedWritesEqual=True, allOwnCodeObserved=dict(codeBytes=60, literalBytes=0, unclassifiedBytes=0), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Ordinary C60-byte full-span genuine match, pending integrator module/ROM acceptance.', 'Pure signed16-array membership against a full signed32 needle; zero/negative counts do not enter the loop. Synthetic buffers provide at least the tested count words.', 'Standalone finite needle/count cases include high-word aliases that a narrowed formal would incorrectly accept. Original formal types/legal game domains are not established beyond this measured facade.', 'All target instructions observed; physical GPR/CPSR/complete RAM including stack and writes agree. Three complete wrong-C images return and reject independently. No providers, game scene, application/UI edits or callee source credit.'])
    write_json(ROOT / 'evidence/matches/ov000-20261102-lookup893.json', report)
    print(dict(pairs=len(cases), actualTopReturns=len(cases) * 2, matchedBytes=60, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    main()
