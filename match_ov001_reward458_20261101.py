import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_reward458_machine_20261101 as M
import ov001_reward458_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov001_20261101_reward458/source.c'
WORK = ROOT / 'work/ol458-proof'
PINS = ROOT / 'evidence/verification/ov001-reward458-inputs-20261101.json'

def encoded(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':')).encode()

def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('458 compiler failure', rows))
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
        raise ValueError('458 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('458 frozen input differs', item['path']))
    snapshot = ROOT / 'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected = json.loads(snapshot.read_text())['functions']
    if any(r['processor'] == 'arm9' and not r['program'] and r['module'] == 'ov001' and max(r['address'], M.ENTRY) < min(r['address']+r['bytes'], M.ENTRY+M.SIZE) for r in selected):
        raise ValueError('458 subject already selected')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'caller', True)
    row['genuineLinkComparison'] = freeze_link(proof)
    row['exactBytes'] = M.SIZE
    profiles = P.profiles()
    traces, cases, controls, observed = [], [], [], set()
    counts = dict(actualTopReturns=0, actualNativeDependencyReturns=0, actualRngReturnsWithinDependencyTotal=0, providedCalls=0)
    for p in profiles:
        native = M.Machine(original, p).run()
        nm = P.model(native)
        candidate = M.Machine(original, p, body).run()
        cm = P.model(candidate)
        if nm != cm or native['nativeReturns'] != candidate['nativeReturns'] or native['calls'] != candidate['calls']:
            raise ValueError(('458 original/source contracts differ', p['name']))
        observed.update(native['ownObserved'])
        counts['actualTopReturns'] += 2
        dep = len(native['nativeReturns']) + len(candidate['nativeReturns'])
        counts['actualNativeDependencyReturns'] += dep
        counts['actualRngReturnsWithinDependencyTotal'] += nm['actualRngReturnsWithinDependencyTotal'] * 2
        result = dict(profile=p, model=nm, nativeReturns=native['nativeReturns'], actualRngCalls=native['calls'], nativeInstructions=native['instructions'], sourceInstructions=candidate['instructions'])
        traces.append(result)
        cases.append(dict(profile=p['name'], actualTopReturns=2, actualNativeDependencyReturns=dep, traceSha256=c.sha(encoded(result))))
    if len(observed)*4 != 220:
        raise ValueError(('458 incomplete native code coverage', len(observed)*4))
    for tag in ['flag', 'width']:
        badsource = ROOT / 'nonmatching/overlay-lane/20261101-reward458-controls' / tag / 'source.c'
        bad, bp, badbody = compile_unit(badsource, tag, False)
        p = dict(profiles[-3], name='control-' + tag, enemies=[dict(e, fallback=0) for e in profiles[-3]['enemies']])
        result = M.Machine(original, p, badbody).run()
        failure = None
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        if failure is None:
            raise ValueError(('458 wrong C did not fail model', tag))
        controls.append(dict(tag=tag, source=badsource.relative_to(ROOT).as_posix(), sourceSha256=sha256(badsource), compilation=bad, link=bp, profile=p['name'], actualTopReturns=1, actualNativeDependencyReturns=len(result['nativeReturns']), rejected=True, rejection=failure))
    payload = encoded(traces)
    archive = ROOT / 'evidence/generated/ov001-reward458-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload, mtime=0))
    functions = []
    for a, r in sorted(original['ranges'].items()):
        image, base = (original['arm'], M.BASE) if r['module']=='main' else (original['overlay'], M.OVERLAY)
        functions.append(dict(address=hex(a), **r, sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], matches=[row], matchedFunctions=1, matchedBytes=228, isolatedLinkedBytes=228, wholeModuleLinked=False, oracle=dict(pairs=len(profiles), **counts, actualReturnAndFrameRequired=True, freshMachinePerExecution=True, cpu='ARM946', instructionBound=20000, maxInstructions=max(max(r['nativeInstructions'], r['sourceInstructions']) for r in traces), originalObservedCodeBytes=220, literalBytes=8, compiledReturningControls=controls, negativeActualTopReturns=len(controls), functions=functions, cases=cases, traceArchive=dict(path=archive.relative_to(ROOT).as_posix(), sha256=sha256(archive), decodedSha256=c.sha(payload)), independentWholeNonstackEffects=True, independentRngCallOrderAndFinalState=True), outputContract=dict(addressHex='0x02238D10', bytes=6, elementWidthBytes=2, elementSignedness='unsigned16 store view', capacity=3, fallbackFlagsHex='0x02238D18', fallbackFlagWidthBytes=1, rawRateAndItemViews=True), generatorSha256=sha256(__file__), fixtureSha256=sha256(ROOT/'ov001_reward458_machine_20261101.py'), modelSha256=sha256(ROOT/'ov001_reward458_models_20261101.py'), acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(), sha256=sha256(snapshot)), inputPins=dict(path=PINS.relative_to(ROOT).as_posix(), sha256=sha256(PINS)), reproductionCommand='python match_ov001_reward458_20261101.py', limitations=['Ordinary C and isolated genuine MWLD caller are exact; full module acceptance is separate', 'All child helpers, raw64-byte ability-list modifiers and global RNG execute original code; no supplied body or extra callee source credit', 'RNG return counts are already included in native dependency totals; seeds are supplied synthetic inputs, not future scene state', 'Numeric actor pools and descriptors, readiness/raw1FF/AC/suppression/rate/item bytes, fallback flags, mask word and list entries are supplied; initialization, overlay loading and whole-battle reachability remain unproved', 'A successful fallback can append zero and return1; primary zero selection appends nothing; return is not any(nonzero output words)', 'No inventory mutation, item consumption, actual scene identity, record+0x33 lifecycle or application policy is inferred', 'Full substituted-code interval has precedence over original entry watching for negative images'])
    write_json(ROOT/'evidence/matches/ov001-20261101-reward458.json', report)
    print(json.dumps(dict(matchedBytes=228, pairs=len(profiles), **counts, negativeActualTopReturns=len(controls))))
if __name__ == '__main__':
    run()
