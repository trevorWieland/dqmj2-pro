import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_bank_build import build
from wave20261104_main_bank_fifth_models import SPECS, run
from wave20261104_main_bank_fifth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-bank-next/fifth'
WORK = ROOT / 'work/w4mb/fifth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-bank-next/fifth'


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Frozen fourth family identity set differs')
    info, main, unused = L.measured_module('main')
    overlay_info, overlay, unused = L.measured_module('ov000')
    matches, traces, negatives = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        name = format(int(item['address'], 0), '08x')
        row, body = build(source, WORK / name / 'positive')
        if row['targetSha256'] != item['targetSha256'] or row['bytes'] != item['bytes']:
            raise ValueError('Frozen caller span differs')
        origin = int(row['address'], 0)
        native = main[origin - 0x02000000:origin - 0x02000000 + row['bytes']]
        old = 'status = ' + str(SPECS[name].get('status', 0)) + ';'
        new = 'status = ' + str(1 - SPECS[name].get('status', 0)) + ';'
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C status control ambiguous')
        wrong = WORK / name / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        wrong.write_text(text.replace(old, new))
        shutil.copyfile(SOURCE / 'context.h', wrong.with_name('context.h'))
        badrow, badbody = build(wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(8):
            original = run(row, native, ordinal, main, overlay)
            rebuilt = run(row, body, ordinal, main, overlay)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive model/full state differs', row['address'], ordinal, original['modelFailures']))
            bad = run(badrow, badbody, ordinal, main, overlay)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=row['address'], ordinal=ordinal, result=original))
        if rejected != 8:
            raise ValueError('Whole-C mutation not rejected by all independent models')
        negatives.append(dict(address=row['address'], mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', name, row['bytes'], rejected, flush=True)
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
               canonicalMatchedBytes=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Fifth disjoint family from main-bank-next ownership, full configured extents, pinned SP1 compiler and genuine MW links; original ELF names/relocations intact.',
                       'Eight finite caller fixtures per function; actual caller returns plus complete GPR/CPSR/calls/writes/8MiB RAM equality and independent complete context models.',
                       'Opaque game providers and soft float conversion, comparison and arithmetic helpers are modeled boundaries with prescribed results and state mutations; zero original native callee execution/source credit.',
                       'Float inputs stay in supported integer-conversion and fixed-rounding ranges, record capacity is four synthetic banks, and four entries consume incomingR2 as an opaque selector; vector providers can overwrite context parameters, and independent models require snapshots from before the getter; actual game object extents/domains unproved.',
                       'Pinned original relocation records qualify overlay imports; 16 native compiler layout assertions and wrong-helper/overlay/stride controls remain explicit.',
                       'All prior packets remain frozen; shared module integration, game semantics, hardware and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
