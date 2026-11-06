import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_runtime_next_first_build import build
from wave20261105_main_runtime_next_first_models import SPECS, fixtures, run
from wave20261105_main_runtime_next_first_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/first'
WORK = ROOT / 'work/w5rn/first-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/first'


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
    cases = [('020602ec', 'wrong-return-padding', 'buffer) + 8);', 'buffer) + 9);', fixtures('020602ec')),
             ('020602ec', 'wrong-coordinate-advance', '(s16)(x + 8)', '(s16)(x + 7)', fixtures('020602ec')),
             ('020603ec', 'wrong-signed-modifier', 'parameters, style, modifier, output', 'parameters, style, modifier + 1, output', fixtures('020603ec')),
             ('020603ec', 'wrong-literal-success', 'return 1;', 'return 0;', fixtures('020603ec')),
             ('0206092c', 'wrong-command-opcode', '0xe2', '0xe3', fixtures('0206092c')),
             ('02060954', 'wrong-nibble-index', 'nibble4 + 13', 'nibble4 + 14', fixtures('02060954')),
             ('0206099c', 'wrong-kind-threshold', 'kind >= 8', 'kind > 8', [f for f in fixtures('0206099c') if f['value'] == 8]),
             ('02060a20', 'wrong-effect-field', '->symbol24', '->opaque00[0x23]', fixtures('02060a20'))]
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
               limits=['First closed6-function text/glyph subset of57/12340B main-runtime-next claim; full configured256/72/40/72/64/64-byte extents, ordinary C, pinned SP1 compiler/genuine MW full links and original ELF relocations/names. All previous98-claim26 sealed inputs remain immutable; no patches or allocation sweep.',
                       '432 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent full512-byte output,32-byte owner,two128-byte UI states,16-byte metadata and64-byte effect views. They cover all256 raw glyph bytes plus high words, all16 metadata nibbles/high flags, signed coordinate/extreme modifiers,32-bit IDs/modes, kind7/8 boundary and mapped low-byte truncation.',
                       '64-byte u16[32] buffer and32-byte parameter descriptor replace undersized generated draft scalars. Providers mutate owner/metadata/format/context between calls, prescribe complete bounded payloads and clobber caller-saved GPR/flags. UI is captured after metadata lookup and retained across owner mutation; metadata nibble and formatter fields are reloaded after the appropriate providers.',
                       'Original initialized data(any) table020dbc18 is qualified narrowly by exact original caller/pool/inventory, unsigned nibble+13+379 indexing,2-byte stride/load and observed392..407 entries;816 bytes is a minimum initialized prefix only. Formatter BSS021c9698 uses unchanged common BSS qualification as an opaque address; complete object types/extents/storage ownership remain unproved and receive0credit.',
                       'Unsigned4-bit native ABI projection is checked by512 compiled native probe returns and two wrong-order/signedness probes.48 data controls+36 original branch controls,4 real ABI layout failures and8 genuine wrong-C errors are required. Source-complete original/copied-root producer and generic canonical replay required;156or later only.',
                       'All original font/format/lookup/map/encoding bodies execute0 and gain0source credit. Provider results are prescribed ABI fixtures, not actual text rendering/game/hardware/platform execution. Formatter receives literal255 despite a64-byte local buffer; fixtures deliberately supply bounded output and make no all-message-length safety claim. Semantic field names are provisional caller interpretations.',
                       '312/320-byte width-accumulation neighbors and68-byte regional glyph caller remain partial/uncredited after bounded context assessment; their source is excluded from this packet. No full/source-only ROM or Windows/Android proof is claimed.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
