import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_middle_build import build
from wave20261104_main_middle_models import SPECS, fixtures, run
from wave20261104_main_middle_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/first'
WORK = ROOT / 'work/w4mm/first-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/first'


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
    mutations = {'0204740c': ('case 21:', 'case 22:', [dict(value=21), dict(value=22)]),
                 '02047428': ('native_fn_02047b90(target, 1, 0, 255)', 'native_fn_02047b90(target, 3, 0, 255)',
                              [dict(opcode=0x2b, cursor=42, providerReturn=0)]),
                 '0204815c': ('bytes[1] = 0x15;', 'bytes[1] = 0x16;', [fixtures('0204815c')[4]]),
                 '02048188': ('bytes[1] = 0x1c;', 'bytes[1] = 0x1d;', [fixtures('02048188')[4]])}
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
    source = SOURCE / '02047428.c'
    text = source.read_text()
    folder = WORK / 'return-width/negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(text.replace('u8 native_main_', 'u32 native_main_').replace('u8 used =', 'u32 used ='))
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    wrapping = dict(opcode=0x2b, cursor=1, providerReturn=255)
    if not run(badrow, body, wrapping, main)['modelFailures']:
        raise ValueError('Missing unsigned-byte wrapping was not rejected')
    negatives.append(dict(case='missing-unsigned-byte-return-wrapping', fixture=wrapping, rejected=True, proof=badrow))
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
               limits=['First closed4-function text/control family from the67-function claim; complete configured extents, pinned SP1 compiler and genuine MW links; original ELF names/relocations preserved.',
                       'All256 discriminator bytes, every active provider case at four additional cursor/unsigned-byte-return boundaries, halfword predicate edges and marker payload cases; actual caller returns with complete GPR/CPSR/calls/writes/8MiB RAM equality and independent protocol models.',
                       'Opaque native helpers are modeled boundaries with prescribed returns and caller-saved-register/flag clobbers; no native callee body execution or source credit. No font/string content semantics or actual destination writes are claimed.',
                       'Original load records and BSS symbols prove two global bases; original unsigned-halfword field+0x80 and scaled index addition are separately decoded.130bytes is only a minimal typed source prefix. Actual BSS allocation extents and valid cursor/destination domains remain unknown; high cursor fixtures measure pointer formation without dereferencing the modeled output.',
                       'Generic frozen data qualification and original branch verifier are reused unchanged; strict halfword/pointer checks, meaningful wrong-C/width/binding/native-layout controls and copied-root reconstruction remain explicit.',
                       'Shared module acceptance, actual game/hardware execution and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
