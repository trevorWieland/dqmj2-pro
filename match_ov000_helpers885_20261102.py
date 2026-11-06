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
import ov000_helpers885_machine_20261102 as M
import ov000_helpers885_model_20261102 as G

SOURCE = ROOT / 'src/overlays/ov000_20261102_helpers885'
WORK = ROOT / 'work/ol885-proof'


def build(source, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov000', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('885 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        proof = validate(row, bindings, directory)
        return dict(**row, realLink=proof), (directory / 'caller.bin').read_bytes()
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=canonical, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('885 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov000-helpers885-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('885 input differs', row['path']))
    accepted = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    for entry, size in M.EXTENTS.items():
        if any(row['processor'] == 'arm9' and row['program'] == '' and row['module'] == 'ov000' and max(row['address'], entry) < min(row['address'] + row['bytes'], entry + size) for row in accepted):
            raise ValueError('885 accepted interval overlaps')
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov000')
    table = overlay[0x0222B854 - M.BASE:0x0222B854 - M.BASE + 49]
    expectedTable = bytes(M.word(-((i + 1) // 2) if i & 1 else (i + 1) // 2) & 255 for i in range(49))
    if table != expectedTable:
        raise ValueError('885 independent signed-distance table differs')
    matches = []
    bodies = {}
    controls = []
    images = {}
    sites = {0x021DA4D4: ('order-byte', '((u8 *) output)[written] = (u8) choice;', '((u8 *) output)[written] = (u8) (choice + 1U);'), 0x021DA57C: ('context-flag', 'context[0] = 1;', 'context[0] = 0;'), 0x021DBB50: ('walk-limit', 'processed < count && processed < limit', 'processed < count && processed <= limit')}
    for index, (entry, size) in enumerate(M.EXTENTS.items()):
        source = SOURCE / f'native_ov000_{entry:08x}.c'
        match, body = build(source, 'source-' + hex(entry))
        matches.append(match)
        bodies[entry] = body
        name, before, after = sites[entry]
        template = source.read_text()
        wrong = template.replace(before, after)
        if template == wrong:
            raise ValueError('885 control site absent')
        directory = ROOT / 'nonmatching/overlay-lane/20261102-helpers885-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        wrongSource = directory / 'source.c'
        if wrongSource.exists() and wrongSource.read_text() != wrong:
            raise ValueError('885 frozen wrong source differs')
        wrongSource.write_text(wrong)
        wrongSource.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        origin = 0x02650000 + index * 0x2000
        proof, image = build(wrongSource, name, origin)
        images[origin] = image
        controls.append(dict(name=name, target=entry, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeHelperReturns=0, suppliedCalls=0, independentModelPairs=0)
    perEntry = {entry: dict(pairs=0, actualTopReturns=0, nativeHelperReturns=0, suppliedCalls=0) for entry in M.EXTENTS}
    traces, cases = [], []
    ownPcs = {entry: set() for entry in M.EXTENTS}
    ignoredDigests = []
    for p in G.profiles():
        entry = p['entry']
        control = next(row for row in controls if row['target'] == entry)
        results, failures = [], []
        for kind, start in [('native', entry), ('source', entry), (control['name'], control['origin'])]:
            vm = M.Machine(main, overlay, images, p)
            if kind == 'source':
                vm.u.mem_write(entry, bodies[entry])
            result = vm.run(start)
            result['kind'] = kind
            results.append(result)
            failures.append(G.model(vm, result))
        original, candidate = results[:2]
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov000-helpers885-model-rejected-20261102.json', dict(profile=p, failures=failures, results=list(map(compact, results))))
            raise ValueError(('885 independent model rejected', p['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'contextHex', 'meshHex', 'outputHex', 'indicesHex', 'memory', 'calls', 'writes', 'originalHelperReturns', 'ownPcs', 'helperPcs', 'instructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            raise ValueError(('885 original/source full physical state differs', p['ordinal'], differences))
        helperReturns = len(original['originalHelperReturns']) + len(candidate['originalHelperReturns'])
        supplied = len(original['calls']) + len(candidate['calls'])
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        totals['actualNativeHelperReturns'] += helperReturns
        totals['suppliedCalls'] += supplied
        for key, value in [('pairs', 1), ('actualTopReturns', 2), ('nativeHelperReturns', helperReturns), ('suppliedCalls', supplied)]:
            perEntry[entry][key] += value
        ownPcs[entry].update(original['ownPcs'])
        control['actualTopReturns'] += 1
        control['rejected' if failures[2] else 'positive'] += 1
        trace = dict(profile=p, results=list(map(compact, results)), modelFailures=failures, allPhysicalDifferences=differences)
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        traces.append(trace)
        cases.append(dict(ordinal=p['ordinal'], entry=hex(entry), actualTopReturns=2, nativeHelperReturns=helperReturns, suppliedCalls=supplied, traceSha256=hashlib.sha256(raw).hexdigest()))
        if p.get('ignoredGroup'):
            ignoredDigests.append(hashlib.sha256(json.dumps({key: original[key] for key in keys if key != 'memory'}, sort_keys=True).encode() + original['memory']).hexdigest())
    if len(set(ignoredDigests)) != 1 or len(ignoredDigests) != 5:
        raise ValueError('885 incoming R3 poison invariance failed')
    for entry, size in M.EXTENTS.items():
        if ownPcs[entry] != set(range(entry, entry + size, 4)):
            raise ValueError(('885 own code coverage incomplete', hex(entry)))
    if any(not row['rejected'] for row in controls):
        raise ValueError('885 returning control rejection missing')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov000-helpers885-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov000', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=matches, canonicalMatchedFunctions=3, canonicalMatchedBytes=284, sourceCreditPendingIntegrator=284, allPassed=True, totals=totals, perEntry={hex(key): value for key, value in perEntry.items()}, allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allRawCallWordsAndOrderedWritesEqual=True, ownCodeObserved={hex(key): len(value) * 4 for key, value in ownPcs.items()}, incomingR3IgnoredProbe=dict(cases=5, samePhysicalStateSha256=ignoredDigests[0], originalFirstR3Definition='ov000:ARM:021DBB74 MOV R3,#1', originalFormalArityClaim=False), signedLookupData=dict(address='ov000:0222B854', bytes=49, sha256=hashlib.sha256(table).hexdigest(), formula='0,-1,+1,-2,+2,...,-24,+24', sourceCredit=0), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Three ordinary C full-span genuine matches284B; source admission/full module/ROM build remain integrator-owned.', 'A4D4 executes actual previously accepted A484 lookup80B and original49-byte data, with bounded ordinals0..48. Count<=0 still performs one output write; that observed malformed-input behavior is separate from legal game domain.', 'A57C writes context flag0/index8/triangleC then block byte1/local word4. Signed16 block count, signed32 boundary comparisons and unsigned32 cumulative wrapping are independently modeled; no record33 or game-meaning claim.', 'DBB50 physically prepares seven words for providedDB968. IncomingR3 is overwritten before use, so the C spacer parameter preserves stack-word positions without claiming seven semantic inputs or original formal types. Five fixed-state all-word poison probes agree.', 'DB968 lower traversal remains supplied with explicit array mutations/response plans and legal caller-saved/CPSR clobbers. No native DB968 return/source credit, full query reachability, valid game index set or downstream scene effects are claimed.', 'All positive physical registers/CPSR/raw calls/ordered writes/complete8MiB RAM including stack agree; each VM actually returns with preserved SP/callee-saved state. Wrong whole-C images genuinely link at private origins without overwriting neighbors.', 'No shared registry/preference/application/UI edits or duplicate credit for acceptedA484/A520. BBB8 remains a separate92/96 near hypothesis.'])
    write_json(ROOT / 'evidence/matches/ov000-20261102-helpers885.json', report)
    print(dict(**totals, matchedBytes=284, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    execute()
