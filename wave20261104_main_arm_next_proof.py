import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_build import build
from wave20261104_main_arm_next_models import SPECS, fixtures, run
from wave20261104_main_arm_next_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/first'
WORK = ROOT / 'work/w4an/first-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/first'


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
    mutations = {'020281b8': ('total >> 12', '(total >> 12) + 1', fixtures('020281b8')),
                 '0202859c': ('return &node->position;', 'return &node->target;', fixtures('0202859c')),
                 '020285c8': ('return &node->target;', 'return &node->position;', fixtures('020285c8')),
                 '02028dac': ('state->flag8 = 0;', 'state->flag8 = 1;', fixtures('02028dac')[1:]),
                 '02028dcc': ('state->flagc = 0;', 'state->flagc = 1;', fixtures('02028dcc')[1:])}
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
               limits=['First closed5-function vector/current-node/byte-acknowledge subset of exclusive98/12440B claim. Full configured extents, pinned SP1 compiler, genuine MW links and original ELF names/relocations preserved.',
                       'All256 input byte values for each acknowledge function prove normalized return and exactly one conditional zero store. Eight vector-getter fixtures each cover explicit/default node, NULL output, separate output, same-vector output and other-vector output aliases; complete modeled node/output/flag/current regions are independently checked.',
                       'Eight signed32 vector triplets include extrema and64-bit sum wrapping; independent integer model checks low32 of modulo64 sum-of-squares shifted12 and the forwarded scalar-provider return. Original scalar helper body does not execute; no actual square-root/game/hardware behavior is claimed.',
                       'Actual native/source callers return with full GPR/CPSR/calls/writes/8MiB RAM equality. Native callee execution/source credit0; only the scalar helper is a prescribed boundary with caller-saved-register/flag clobbers.',
                       'Original data base and conditional current-pointer field+8 loads are qualified; current12-byte, node52-byte and flag13-byte types are minimum source views, not actual full allocations or original declarations. No original global data storage credit; valid actual game domains remain unproved.',
                       'Frozen common data qualification and original branch verifier are unchanged. Genuine wrong-C off-by-one scalar argument/field pointer/zero-store controls and wrong namespace/data/field/ABI controls remain explicit, with copied-root replay required.',
                       'No MMIO startup, primitive assembly, allocation search, old frozen source/helper modification or shared acceptance mutation occurs; module integration and source-only/full-game/platform proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
