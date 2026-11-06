import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_second_build import build
from wave20261104_main_arm_next_second_models import SPECS, fixtures, run
from wave20261104_main_arm_next_second_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/second'
WORK = ROOT / 'work/w4an/second-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/second'


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
    mutations = {'0202841c': ('up.y = 4096;', 'up.y = 0;', fixtures('0202841c')),
                 '020284f4': ('(u32)camera->target.x + (u32)transformed.x', '(u32)camera->target.x - (u32)transformed.x', fixtures('020284f4'))}
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
    source = SOURCE / '0202841c.c'
    negatives.append(mutation(source, 'wrong-pre-provider-angle-store', 'camera->angle18 = angle;',
                              'camera->angle18 = (s32)((u32)angle + 1u);', matches[0], main, fixtures('0202841c')))
    source = SOURCE / '020284f4.c'
    negatives.append(mutation(source, 'wrong-post-provider-position-base', 'camera->position.x = (s32)((u32)camera->target.x',
                              'camera->position.x = (s32)((u32)camera->position.x', matches[1], main, fixtures('020284f4')))
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
               limits=['Second disjoint2-function matrix/triplet caller subset of98/12440B claim; full configured104/168-byte extents, pinned SP1 compiler and genuine MW links; original ELF names/relocations preserved.',
                       'Eight fixtures per caller, actual native/source returns and complete GPR/CPSR/calls/writes/8MiB RAM equality; explicit/default object, input angle extremes,36-byte matrix and12-byte vector stack boundaries and complete object/current-state models.',
                       'Providers prescribe matrix/output vectors, mutate current object/angle/position/target and clobber caller-saved registers/flags. Models check input vector before any provider, persistent original object/angle, three-provider order, pre-provider angle store and prior-angle return, modulo32 difference/addition and post-provider target reload.',
                       'Native provider bodies do not execute and receive zero source credit; no actual matrix initialization, rotation, transformation, graphics, camera/game or hardware behavior is claimed. Field names are caller-level geometric interpretations with full original types/declarations/object allocations and valid game domains unproved.',
                       'Original data base and conditional pointer+8 are separately qualified;12-byte current state and76-byte object are minimum views, with36/12-byte native stack objects. No original global data storage credit. Exact native stack layout follows measured local-object declaration ordering, with no allocation sweep.',
                       'Frozen common data qualification and original branch verifier remain unchanged. Native ABI/namespace/data/field controls and genuine whole-C input-vector/angle/store/arithmetic/base errors are required, along with copied-root reconstruction.',
                       'The140-byte trig setter remains unmatched/uncredited; all first READY/helper/source/input pins are unchanged. Shared integration and source-only/full-game/platform proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
