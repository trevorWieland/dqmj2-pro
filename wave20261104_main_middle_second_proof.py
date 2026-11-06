import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_middle_second_build import build
from wave20261104_main_middle_second_models import SPECS, fixtures, run
from wave20261104_main_middle_second_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/second'
WORK = ROOT / 'work/w4mm/second-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/third'


def mutation(source, name, old, new, row, main, selected):
    text = source.read_text()
    if text.count(old) != 1:
        raise ValueError('Whole-C mutation ambiguous: ' + name)
    folder = WORK / name / 'negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    rejected = []
    for ordinal, fixture in enumerate(selected):
        if run(badrow, body, fixture, main, ordinal)['modelFailures']:
            rejected.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Whole-C mutation not independently rejected', name, rejected))
    return dict(case=name, old=old, new=new, rejectedCases=rejected, fixtures=selected, proof=badrow)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Frozen text-family identity set differs')
    info, main, unused = L.measured_module('main')
    matches, traces, negatives = [], [], []
    mutations = {'02047ac0': ('    return 0;', '    return 1;', fixtures('02047ac0')),
                 '0204837c': ('target->words[index] = 0;', 'target->words[index] = 1;', fixtures('0204837c')),
                 '020483c0': ('target->words[index] = 0;', 'target->words[index] = 1;', fixtures('020483c0'))}
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        source = ROOT / item['source']
        row, body = build(source, WORK / name / 'positive')
        if row['targetSha256'] != item['targetSha256'] or row['bytes'] != item['bytes']:
            raise ValueError('Frozen caller span differs')
        at = int(row['address'], 0) - 0x02000000
        native = main[at:at + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent text protocol/full-state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        old, new, selected = mutations[name]
        negatives.append(mutation(source, name, old, new, row, main, selected))
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    source = SOURCE / '02047ac0.c'
    wrapping = next(item for item in fixtures('02047ac0') if len(item['providers']) == 2 and item['start'] == 127)
    negatives.append(mutation(source, 'missing-eight-bit-position-wrap', 'position = (u8)(position + 1);',
                              'position = position + 1;', matches[0], main, [wrapping]))
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
               canonicalMatchedBytes=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Second disjoint3-function text-reader/record-clear family from67-function claim; complete configured spans, pinned SP1 compiler, genuine MW links and original ELF/relocations intact.',
                       'Finite reader fixtures cover start bounds, NUL and E3/1B termination, E3/15 and E3/1C providers, unknown escape fallback, ordinary-byte providers, prescribed text mutation and8-bit position wrapping; clears execute128 real word stores across four synthetic records.',
                       'Native/source callers actually return with complete GPR/CPSR/calls/writes/8MiB RAM equality and independent full text/record memory models. Three native text providers are modeled boundaries; zero actual native callee execution/source credit.',
                       'Original configured BSS bases and load records are measured.130-byte minimal source prefix,0x3744 record stride,0x3544 word offset,128 words and signed16-bit counter are separately instruction/constant/ABI qualified. Complete original allocations, actual record count and valid game domains remain unknown; original data storage credit0.',
                       'Generic frozen data validator and branch verifier are reused unchanged. New narrow original byte/word/counter witnesses, real wrong-C return/store/wrap controls, changed native-layout controls and copied-root replay remain explicit.',
                       'All earlier READY/helper/input/source paths remain frozen; shared module acceptance, game/hardware execution and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
