import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_runtime_next_second_build import build
from wave20261105_main_runtime_next_second_models import SPECS, fixtures, run
from wave20261105_main_runtime_next_second_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/second'
WORK = ROOT / 'work/w5rn/second-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/second'


def mutation(source, name, old, new, row, main, selected):
    text = source.read_text()
    if text.count(old) != (2 if name == 'wrong-late-desired-copy' else 1):
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
    f = fixtures('02067380')
    not_terminal = [x for x in f if x['step'] != 65535]
    initialized = [x for x in f if x['mode'] == 2 and x['step'] == 0]
    choice3 = [x for x in f if x['mode'] == 2 and x['step'] == 10 and x['choice'] == 3]
    copied = [x for x in f if x['mode'] in [1, 3] and x['step'] == 10 and x['outcome'] or
              x['mode'] == 2 and x['step'] == 10 and x['choice'] not in [1, 2, 3] and x['mode'] != x['desired']]
    cases = [('02067380', 'wrong-terminal-marker', 'step4 == 65535', 'step4 == 65534', [x for x in f if x['step'] == 65535 and x['mode'] != 0]),
             ('02067380', 'wrong-mode-zero-result', 'case 0:\n        result = 1;', 'case 0:\n        result = 0;', [x for x in not_terminal if x['mode'] == 0]),
             ('02067380', 'wrong-main-provider-word', 'native_fn_02041560(10)', 'native_fn_02041560(9)', initialized),
             ('02067380', 'wrong-ordered-choice', 'choice0 == 3', 'choice0 == 4', choice3),
             ('02067380', 'wrong-overlay-initial-step', 'step4 = 5;', 'step4 = 6;', [x for x in f if x['mode'] in [1, 3] and x['step'] == 0]),
             ('02067380', 'wrong-one-specific-poll', 'if (native_fn_02041800() != 1) result = 1;', 'if (native_fn_02041800() == 1) result = 1;', [x for x in f if x['mode'] == 2 and x['step'] == 20]),
             ('02067380', 'wrong-overlay-nonzero-test', 'if (native_fn_ov000_022149dc())', 'if (native_fn_ov000_022149dc() == 1)', [x for x in f if x['mode'] in [1, 3] and x['step'] == 10 and x['outcome'] not in [0, 1]]),
             ('02067380', 'wrong-late-desired-copy', 'current4 = native_data_020de23c.desired0;', 'current4 = 2;', copied),
             ('02067380', 'wrong-final-result', 'return result;', 'return result + 1;', not_terminal)]
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
               limits=['Second closed552-byte ordered-state caller from57/12340B main-runtime-next claim. Full configured extent, readable ordinary C and genuine pinned MW link with original ELF relocations/names; no patches, ordinary-logic asm, allocator search or plural-overlay assumption.',
                       '360 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent complete two8-byte state views. Outer modes0/1/2/3/4/all-ones, steps0/5/10/20/65535/negative1, choice0/1/2/3/255, desired equal/different, and prescribed return0/1/2/all-ones cover dispatch/ordered choice/terminal marker and distinct nonzero-versus-one comparisons.',
                       'Every provider mutates choice,step,current,desired and clobbers caller-saved registers/flags. Models distinguish captured dispatch from late desired-word copy, source stores after provider mutations, provider-state persistence on polling/nonready branches, exact literal call arguments and result0/1.',
                       'Only main and one explicitly named overlay namespaceov000 are imported. Unchanged original branch verifier supplies exact original relocation,module,address,ARM mode and CPU/program checks;54 meaningful wrong bindings cover every import, including same-number wrong overlay. No native main/overlay provider body executes or gains source credit.',
                       'BSS021c36fc uses unchanged common data validator; initialized data(any)020de23c is narrowly qualified by exact original pool/inventory/caller hash and byte/word access instructions. The two8-byte typed prefixes and provisional step/current/desired/choice names do not establish full original declarations/allocations/storage ownership; storage credit0.',
                       '30 data controls+54 branch controls,4 real native ABI failures,9 genuine wrong-C errors and source-complete original/copied-root/generic canonical replay required. Measured ordered inner if/else chains replace overgeneralized decompiler switches; that control-flow recovery removed12 extra bytes without allocation tuning.',
                       'All previous98-claim26 READYs and new first6/568B packet remain frozen. Native caller/ABI proof does not establish actual transition/game/hardware/platform/source-only ROM execution;156or later only.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
