import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_clamp453_machine_20261101 as M
import ov001_clamp453_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov001_20261101_clamp453'
WORK = ROOT / 'work/ol453-proof'
PINS = ROOT / 'evidence/verification/ov001-clamp453-inputs-20261101.json'

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('453 compiler failure', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'link'
    try:
        proof = validate(row, qualified_bindings(row), directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0], dict):
            raise
        proof = error.args[0]
    return row, proof, (directory / 'caller.bin').read_bytes()

def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('453 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('453 frozen input differs', item['path']))
    snapshot = ROOT / 'evidence/verification/accepted-cohort98-identities-v2-20261101.json'
    selected = json.loads(snapshot.read_text())['functions']
    if any(r['processor'] == 'arm9' and not r['program'] and r['module'] == 'ov001' and max(r['address'], a) < min(r['address'] + r['bytes'], a + n) for r in selected for a, n in M.SUBJECTS.items()):
        raise ValueError('453 source is already selected')
    original = M.inputs()
    profiles = P.profiles()
    matches, traces, summaries, controls = [], [], [], []
    totals = dict(actualTopReturns=0, actualNativeDependencyReturns=0, providedCalls=0)
    functions = []
    for address, row in sorted(original['ranges'].items()):
        image, base = (original['arm'], M.BASE) if row['module'] == 'main' else (original['overlay'], M.OVERLAY)
        functions.append(dict(address=hex(address), **row, sha256=c.sha(image[address-base:address-base+row['bytes']])))
    coverage = {}
    for name, entry in [('actor', 0x021E4500), ('record', 0x021E46D8)]:
        source = SOURCE / (name + '.c')
        row, proof, body = compile_unit(source, name, True)
        row['genuineLinkComparison'] = freeze_link(proof)
        row['exactBytes'] = M.SUBJECTS[entry]
        matches.append(row)
        observed = set()
        for p in profiles:
            native = M.Machine(original, p, entry).run()
            nm = P.model(native)
            candidate = M.Machine(original, p, entry, body).run()
            cm = P.model(candidate)
            if nm != cm or native['calls'] != candidate['calls'] or native['nativeReturns'] != candidate['nativeReturns'] or native['returnedR0'] != candidate['returnedR0']:
                raise ValueError(('453 original/source effects differ', name, p['name']))
            observed.update(native['ownObserved'])
            totals['actualTopReturns'] += 2
            totals['actualNativeDependencyReturns'] += len(native['nativeReturns']) + len(candidate['nativeReturns'])
            result = dict(name=name, profile=p, model=nm, returnedR0Physical=native['returnedR0'], nativeReturns=native['nativeReturns'], calls=native['calls'], nativeInstructions=native['instructions'], sourceInstructions=candidate['instructions'])
            traces.append(result)
            summaries.append(dict(name=name, profile=p['name'], actualTopReturns=2, actualNativeDependencyReturns=len(native['nativeReturns']) + len(candidate['nativeReturns']), traceSha256=c.sha(encoded(result))))
        coverage[name] = dict(entry=hex(entry), observedCodeBytes=len(observed)*4, observedAddresses=[hex(a) for a in sorted(observed)], literalBytes=4 if name == 'actor' else 0)
        required = M.SUBJECTS[entry] - (4 if name == 'actor' else 0)
        if len(observed) * 4 != required:
            raise ValueError(('453 incomplete native subject code', name, len(observed)*4, required))
        for tag in ['comparison', 'delta']:
            badsource = ROOT / 'nonmatching/overlay-lane/20261101-clamp453-controls' / name / tag / 'source.c'
            bad, badproof, badbody = compile_unit(badsource, name + '-' + tag, False)
            chosen = profiles[192 if tag == 'comparison' else -1]
            result = M.Machine(original, chosen, entry, badbody).run()
            failure = None
            try:
                P.model(result)
            except ValueError as error:
                failure = str(error)
            if failure is None:
                raise ValueError(('453 returning compiled control was not rejected', name, tag))
            controls.append(dict(name=name, tag=tag, source=badsource.relative_to(ROOT).as_posix(), sourceSha256=sha256(badsource), compilation=bad, link=badproof, profile=chosen['name'], actualTopReturns=1, actualNativeDependencyReturns=len(result['nativeReturns']), rejectedByModel=True, rejection=failure))
    payload = encoded(traces)
    archive = ROOT / 'evidence/generated/ov001-clamp453-native-traces-20261101.json.gz'
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(gzip.compress(payload, mtime=0))
    returnUse = []
    for caller, size, branch, overwrite in [(0x021E485C, 372, 0x021E49A8, 0x021E49AC), (0x021E4C34, 636, 0x021E4E20, 0x021E4E28)]:
        returnUse.append(dict(module='ov001', mode='arm', caller=hex(caller), callerBytes=size, callerSpanSha256=c.sha(original['overlay'][caller-M.OVERLAY:caller-M.OVERLAY+size]), callPc=hex(branch), callInstructionHex=original['overlay'][branch-M.OVERLAY:branch-M.OVERLAY+4].hex(), overwriteR0Pc=hex(overwrite), overwriteInstructionHex=original['overlay'][overwrite-M.OVERLAY:overwrite-M.OVERLAY+4].hex(), observation='Direct original caller overwrites R0 without a prior read after this call; this does not establish all indirect users'))
    record = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], matches=matches, matchedFunctions=2, matchedBytes=860, isolatedLinkedBytes=860, wholeModuleLinked=False, oracle=dict(pairs=len(summaries), **totals, compiledReturningControls=controls, negativeActualTopReturns=len(controls), nativeSubjectCoverage=coverage, maxInstructions=max(max(r['nativeInstructions'], r['sourceInstructions']) for r in traces), instructionBound=20000, actualReturnAndFrameRequired=True, freshMachinePerExecution=True, cpu='ARM946', allNonstackEffectsIndependentlyChecked=True, callerPreparedSixWordsIndependentlyChecked=True, nativeLimitReturnsIndependentlyModeled=True, functions=functions, cases=summaries, traceArchive=dict(path=archive.relative_to(ROOT).as_posix(), sha256=sha256(archive), decodedSha256=c.sha(payload))), generatorSha256=sha256(__file__), physicalR0CallerEvidence=returnUse, fixtureSha256=sha256(ROOT / 'ov001_clamp453_machine_20261101.py'), modelSha256=sha256(ROOT / 'ov001_clamp453_models_20261101.py'), inputPins=dict(path=PINS.relative_to(ROOT).as_posix(), sha256=sha256(PINS)), acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(), sha256=sha256(snapshot)), reproductionCommand='python match_ov001_clamp453_20261101.py', limitations=['Both ordinary C callers and isolated genuine MW links are exact; full module acceptance remains separate', 'All 21 measured helper/function bodies execute original code; zero supplied helper bodies and zero extra helper source credit', 'Two caller pointers and physically prepared six limit-call words are qualified; unused downstream words do not establish original formal arity or global semantic requirements', 'Synthetic table rows, record UID, actors, descriptor pointers, masks and stat/delta buffers are supplied; no ordinary battle reachability, invalid-pointer error behavior or lifecycle claim', 'Native kind class0/1/2 and bounded progression values, tag0/1/7/255, zero and raw modifier IDs, signed current/delta extremes, u16 limits, 64 clamp masks, alias ordering and full100-row UID search are covered', 'Void source expresses side effects; physical R0 is retained and compared without inventing a semantic return value', 'No ordinary saved-record+0x33 writer or scratch initialization claim; source targets do not establish that lifecycle'])
    write_json(ROOT / 'evidence/matches/ov001-20261101-clamp453.json', record)
    print(json.dumps(dict(matchedFunctions=2, matchedBytes=860, pairs=len(summaries), **totals, negativeActualTopReturns=len(controls))))
if __name__ == '__main__':
    run()
