import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_runtime_next_eleventh_build import build
from wave20261105_main_runtime_next_eleventh_models import SPECS, fixtures, run, scenario
from wave20261105_main_runtime_next_eleventh_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/eleventh'
WORK = ROOT / 'work/w5rn/eleventh-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/eleventh'


def mutation(source, label, old, new, main, selected):
    text = source.read_text()
    if text.count(old) != 1 or not selected:
        raise ValueError('Meaningful whole-C collection mutation is ambiguous/empty: ' + label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', directory / 'context.h')
    row, body = build(wrong, directory / 'build', True)
    rejected = []
    for ordinal, fixture in enumerate(selected):
        if run(row, body, fixture, main, ordinal)['modelFailures']:
            rejected.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Wrong collection C not independently rejected', label, rejected, len(selected)))
    return dict(case=label, old=old, new=new, rejectedCases=rejected, fixtures=selected, proof=row)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen collection input changed: ' + pin['path'])
    if {format(int(x['address'], 0), '08x') for x in inputs['entries']} != set(SPECS):
        raise ValueError('Frozen collection caller set differs')
    info, main, unused = L.measured_module('main')
    matches, traces = [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        row, body = build(ROOT / item['source'], WORK / name / 'positive')
        if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
            raise ValueError('Frozen full native collection extent differs')
        start = int(row['address'], 0) - 0x02000000
        native = main[start:start + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent collection/classification full state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    weighted = fixtures('02066f84')
    cases = [('02066f84', 'wrong-zero-range-gate', 'if (available > 0)', 'if (available >= 0)', [x for x in weighted if x['high'] - x['low'] + 1 == 0]),
             ('02066f84', 'wrong-inclusive-threshold', 'required <= available + group->low', 'required < available + group->low', [x for x in weighted if x['required'] == scenario(x)['threshold'] and scenario(x)['weightedCall']]),
             ('02066f84', 'wrong-ignored-fifth-weight', 'for (i = 0; i < 5; ++i) total += group->weights[i];', 'for (i = 0; i < 4; ++i) total += group->weights[i];', [x for x in weighted if not x['mutate'] and x['weights'] == [0, 0, 0, 0, 1] and scenario(x)['weightedCall']]),
             ('02066f84', 'wrong-signed-weight-roll', 'if (random < running)', 'if ((u32)random < (u32)running)', [x for x in weighted if x['high'] - x['low'] + 1 <= 0 and x['outcome'] == 3 and scenario(x)['weightedCall']]),
             ('02066f84', 'wrong-fresh-low-byte', 'required <= available + group->low', 'required <= available', [x for x in weighted if scenario(x)['weightedCall'] and scenario(x)['rangeValue'] < x['required'] <= scenario(x)['threshold']]),
             ('02065d00', 'wrong-signed-first-dimension', 'return native_data_020de091[kind * 4];', 'return (u8)native_data_020de091[kind * 4];', [x for x in fixtures('02065d00') if x['replacement'] in [128, 255]]),
             ('02065d14', 'wrong-signed-second-dimension', 'return native_data_020de092[kind * 4];', 'return (u8)native_data_020de092[kind * 4];', [x for x in fixtures('02065d14') if x['replacement'] in [128, 255]]),
             ('02065c48', 'wrong-signed-tile-word', 'u16 native_main_', 's16 native_main_', [x for x in fixtures('02065c48') if x['replacement'] in [0x8000, 0xffff]])]
    negatives = [mutation(SOURCE / (name + '.c'), label, old, new, main, selected) for name, label, old, new, selected in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits = ['Fifth closed4/228-byte table/weighted-choice packet from57/12340B main-runtime-next claim. Exact whole configured extents have readable ordinary C and genuine pinned MW links with untouched original ELF names/relocations. No ordinary-logic ASM, object/register/instruction patch or allocation sweep.',
              'The weighted selector independently checks interval-size gating, inclusive threshold against a fresh low byte, all five weights, cumulative selection and signed return/default minus-one. Zero/reversed intervals, zero/single/all/high weights, required negative/zero/high values and first/middle/last outcomes are covered. Provider callbacks can mutate all7 group bytes between reads and clobber caller-saved words/flags.',
              'Negative and out-of-range RNG returns are explicitly counterfactual ABI controls, not claims about actual RNG/game outcomes. No actual RNG/SDK/game body executes or receives credit. Weighted-call fixtures map only caller/provider/group/stack/stop pages and compare every mapped byte, complete GPR/CPSR, calls, writes and actual caller returns.',
              'Read-only lookup fixtures cover20 unsigned-halfword cells and93 measured signed-byte dimension indexes in each of two stride4 views. Additional synthetic in-VM byte/halfword values exercise sign boundaries; original native image/files remain unchanged. These synthetic contexts prove the caller ABI, not alternate ROM contents or initialized-data authorship.',
              'The narrowly scoped initialized-data qualifier requires exact raw data(any) inventory/load entries, complete original caller hashes, ABS32 origins/addends, literal values and field/stride/load words; original function vs data/module/CPU/program/mode confusion must reject. Measured40/369-byte lookup prefixes have unknown complete original object extents and zero storage credit.',
              '45 original-data negatives,6 all-import identity negatives,3 real native-layout rejections,8 genuine whole-C mistakes and source-complete original/copied producer plus generic canonical original/copied replay are required. Only the160-byte selector uses measured SP1p5 O4,p/on,noauto/file-IPA/C99; three lookup callers use pinned SP1p5 O2/speed/inline-on.',
              'Adjacent binary search96B, transition172B and encounter caller720B remain uncredited partials. The binary-search inspection proves a forwarded key in encounter R0 and an actual pointer at state+8; first-draft unused-argument assumptions were corrected. All earlier READY inputs remain frozen. No game/hardware/platform/source-only ROM execution or accepted source credit is claimed before serialized coordinator publication.']
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='', moduleSha256=info['sha256'],
               allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(x['bytes'] for x in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)), producer=Path(__file__).name, producerSha256=sha256(Path(__file__)), limits=limits))
    print(dict(functions=len(matches), bytes=sum(x['bytes'] for x in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
