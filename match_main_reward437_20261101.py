import json
import sys
from pathlib import Path
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate, measured_module
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_reward437_fixtures_20261101 as F
SOURCE = ROOT / 'src/overlays/main_20261101_reward437/mode.c'
WORK = ROOT / 'work/ol437-proof'

def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, _ = c.compare(source, 'main', '2', 'off', True)
    row = rows[0]
    if row.get('compileFailed'):
        raise ValueError(('437 compiler failure', row))
    try:
        proof = validate(row, qualified_bindings(row), WORK / name / 'linked')
    except ValueError as error:
        if exact or not isinstance(error.args[0], dict):
            raise
        proof = error.args[0]
    return (row, proof, (WORK / name / 'linked/caller.bin').read_bytes())

def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('437 pinned runtime differs')
    snapshot = ROOT / 'evidence/verification/accepted-cohort97-identities-v2-20261101.json'
    selected = json.loads(snapshot.read_text())['functions']
    if any((r['processor'] == 'arm9' and (not r['program']) and (r['module'] == 'main') and (max(r['address'], F.ENTRY) < min(r['address'] + r['bytes'], F.ENTRY + 28)) for r in selected)):
        raise ValueError('437 already selected')
    metadata, image, symbols = measured_module('main')
    row, proof, body = compile_unit(SOURCE, 'caller', True)
    row['genuineLinkComparison'] = freeze_link(proof)
    row['exactBytes'] = 28
    cases = []
    observed = set()
    for mode in range(256):
        native = F.execute(image, mode)
        candidate = F.execute(image, mode, body)
        expected = int(mode in [2, 4])
        if native != candidate or native['returnedR0'] != expected:
            raise ValueError(('437 independent raw-byte predicate differs', mode))
        observed.update(native['observedAddresses'])
        cases.append(dict(rawModeByte=mode, expectedPredicate=expected, actualReturns=2, nativeDependencyActualReturns=2, result=native))
    badsource = ROOT / 'nonmatching/overlay-lane/20261101-reward437-negative/mode.c'
    badsource.parent.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text().replace('mode == 4', 'mode == 5')
    if text == SOURCE.read_text():
        raise ValueError('437 missing compiled negative source change')
    if badsource.exists() and badsource.read_text() != text:
        raise ValueError('437 frozen negative source differs')
    badsource.write_text(text)
    bad, badproof, badbody = compile_unit(badsource, 'negative', False)
    negative = []
    for mode in [4, 5]:
        result = F.execute(image, mode, badbody)
        if result['returnedR0'] == int(mode in [2, 4]):
            raise ValueError('437 compiled wrong-mode predicate was not rejected')
        negative.append(dict(rawModeByte=mode, actualReturns=1, nativeDependencyActualReturns=1, actualResult=result['returnedR0'], expected=int(mode in [2, 4]), rejected=True))
    if len(observed) != 10:
        raise ValueError(('437 incomplete native instruction coverage', len(observed)))
    record = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'], source=str(SOURCE.relative_to(ROOT)), sourceSha256=sha256(SOURCE), matches=[row], matchedFunctions=1, matchedBytes=28, isolatedLinkedBytes=28, wholeModuleLinked=False, genuineLinkedByteComparisons=[freeze_link(proof)], oracle=dict(actualReturns=512, nativeDependencyActualReturns=512, providedCalls=0, negativeActualReturns=2, negativeNativeDependencyActualReturns=2, originalCallerObservedCodeBytes=28, originalGetterObservedCodeBytes=12, allRawByteValuesCovered=True, rawByteIdentity=dict(address=hex(F.FIELD), objectAddress='0x020f69c4', offset='0x24'), callerSpecificBoundaryValues=[0, 1, 2, 3, 4, 5, 6, 7, 8, 127, 128, 255], fullNonstackMemoryUnchanged=True, actualReturnAndFrameRequired=True, instructionBound=128, maxInstructions=max((r['result']['instructions'] for r in cases)), freshMachinePerExecution=True, cpu='ARM946', cases=cases, compiledWrongModeControl=dict(source=badsource.relative_to(ROOT).as_posix(), sourceSha256=sha256(badsource), compilation=bad, genuineLinkComparison=badproof, results=negative)), generatorSha256=sha256(__file__), fixtureSha256=sha256(ROOT / 'main_reward437_fixtures_20261101.py'), acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(), sha256=sha256(snapshot)), reproductionCommand='python match_main_reward437_20261101.py', limitations=['Exact ordinary-C caller and genuine isolated MW link; full module integration remains separate', 'Selected main443EC getter remains unchanged and executes original native code;zero extra getter-source credit', '020F69C4+24 is measured as a raw byte; no enum name,current game value,scene initialization or application restriction is inferred', 'All256 synthetic stored byte values andreturning negative controls are supported;ordinary reward reachability is a separate chain proof'])
    write_json(ROOT / 'evidence/matches/main-20261101-reward437.json', record)
    print(json.dumps(dict(matchedFunctions=1, matchedBytes=28, actualReturns=512, nativeDependencyActualReturns=512, providedCalls=0, negativeActualReturns=2)))
if __name__ == '__main__':
    run()
