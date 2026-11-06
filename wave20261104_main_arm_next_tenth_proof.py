import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_tenth_build import build
from wave20261104_main_arm_next_tenth_models import SPECS, fixtures, run
from wave20261104_main_arm_next_tenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/tenth'
WORK = ROOT / 'work/w4an/tenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/tenth'


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
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    def provided(name):
        return [f for f in fixtures(name) if f['provided']]
    timer = [f for f in provided('0203a01c') if not f['flags'] & 8 and f['value']]
    config = fixtures('02039fc4')
    cases = [('02039fa4', 'wrong-player-bit', 'flags110.bit2 = 1;', 'flags110.bit1 = 1;', [f for f in provided('02039fa4') if not f['flags'] & 4]),
             ('0203a000', 'wrong-second-word', 'handle->player, value);', 'handle->player, value + 1);', provided('0203a000')),
             ('0203a050', 'wrong-third-word', 'handle->player, value, extra);', 'handle->player, value, extra ^ 1);', provided('0203a050')),
             ('0203a01c', 'wrong-fixed-frame-shift', 'frame << 8, extra', 'frame << 7, extra', timer),
             ('0203a01c', 'wrong-blocking-bit', 'flags110.bit3', 'flags110.bit2', [f for f in provided('0203a01c') if bool(f['flags'] & 8) != bool(f['flags'] & 4)]),
             ('02039fc4', 'wrong-fifth-stack-word', 'handle, a, b, c, d)', 'handle, a, b, c, d + 1)', config),
             ('02039fc4', 'wrong-literal-success', 'return 1;', 'return 2;', [f for f in config if f['first_result']])]
    for name, label, old, new, selected in cases:
        if not selected:
            raise ValueError('Meaningful mutation has no selected fixtures')
        row = next(r for r in matches if r['address'] == hex(int(name, 16)))
        negatives.append(mutation(SOURCE / (name + '.c'), label, old, new, row, main, selected))
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
               limits=['Tenth closed5-function playback-handle subset of98/12440B claim, complete32/28/28/52/60-byte extents, ordinary C and genuine MW full links. A NEW scoped pinned SP1 -inline on profile and ordinary pointer accessor preserve measured guard/reload boundaries; no volatile qualifier, allocator sweep or patch is used. All old compiler/helper/source pins remain unchanged.',
                       '384 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM, read counts and complete handle/two possible384-byte player states. Signed flags span all16 low-bit combinations, argument/frame0/1/high-bit/all-ones, null/non-null guard and modeled valid pointer reassignment between two actual handle reads. These CPU memory-observation fixtures do not establish actual concurrent game behavior or original accessor/declaration semantics.',
                       'Source bitfields model signed1-bit access on pinned MW;72 actual compiled native ABI probe returns verify bit positions/signed projection, and wrong order/signedness probes fail. Measured player prefix offsets timer232/flags272/counter352 and neighboring four-record372-byte stride are read-only layout evidence, never complete original type/storage/source ownership credit.',
                       'Original379c4 and3b8dc code capture/forward incoming R2 before clobber, supporting independently tested third32-bit arguments. Native source/input witnesses preserve full original identities/code hashes and words; read-only inspections execute0 original bodies and gain0 source credit.',
                       'Four wrapper boundaries forward actual player/word/shifted-frame/extra/fifth-stack arguments. Config result0 skips the second boundary, every nonzero32-bit result calls the flag action and returns literal1. Providers mutate handle/player/timer and clobber caller-saved registers/flags; all actual native callee bodies execute0 and gain0 source credit, even the separately reconstructed flag setter.',
                       '27 read-only ABI witness controls+24 branch controls,4 real layout failures,72 positive ABI probe returns+2 wrong-bitfield native failures and7 genuine whole-C errors are required. Source-complete copied-root producer and generic canonical replay required; no data storage, SDK/game/hardware/platform or source-only ROM proof is claimed;156or later only. The52-byte64-bit scalar caller remains uncredited.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
