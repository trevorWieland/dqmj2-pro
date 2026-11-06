import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_tail_next_second_build import build
from wave20261105_main_tail_next_second_models import SPECS, fixtures
from wave20261105_main_tail_next_second_execution import run
from wave20261105_main_tail_next_second_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-tail-next/second'
WORK = ROOT / 'work/w5tn/second-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/second'


def mutation(label, old, new, count, main, selected):
    source = SOURCE / '020d2e68.c'
    text = source.read_text()
    if text.count(old) != count or not selected:
        raise ValueError('Bounded whole-C summary mutation ambiguous/empty: ' + label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', directory / 'context.h')
    row, body = build(wrong, directory / 'build', True)
    rejected, aborted = [], []
    for ordinal, fixture in enumerate(selected):
        result = run(row, body, fixture, main, ordinal)
        if result['modelFailures']:
            rejected.append(ordinal)
            if not result['actualTopReturn']:
                aborted.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Whole-C summary error not independently rejected', label, rejected, len(selected)))
    return dict(case=label, old=old, new=new, expectedOccurrences=count, rejectedCases=rejected,
                rejectedAtObservedProtocolBoundary=aborted, abortedRunsAreNotCallerReturns=True, fixtures=selected, proof=row)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned private native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen summary input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Exact exclusive summary caller identity differs')
    info, main, unused = L.measured_module('main')
    item = inputs['entries'][0]
    row, body = build(ROOT / item['source'], WORK / 'positive')
    if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
        raise ValueError('Full1472-byte native caller target differs')
    start = int(row['address'], 0) - 0x02000000
    native = main[start:start + row['bytes']]
    traces = []
    for ordinal, fixture in enumerate(fixtures('020d2e68')):
        original = run(row, native, fixture, main, ordinal)
        rebuilt = run(row, body, fixture, main, ordinal)
        if original != rebuilt or original['modelFailures'] or not original['actualTopReturn']:
            write_json(LANE / 'fixture-failure.json', dict(fixture=fixture, original=original, rebuilt=rebuilt))
            raise ValueError(('Independent summary protocol/full state differs', ordinal, original['modelFailures']))
        traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
    print('proved', row['address'], row['bytes'], len(traces), flush=True)
    f = fixtures('020d2e68')
    selected_cap = [x for x in f if not x['mutate'] and x['values'] in [2, 3]]
    selected_packed = [x for x in f if not x['mutate'] and x['packed'] in [4, 5, 6]]
    first_loop = 'native_fn_02049f4c(native_fn_02061dcc((s8)(i + 6)));\n        ++i;\n    } while (i < 22);'
    cases = [('wrong-zero-position', '    u32 value;', '    u32 value;\n    position.x = 1;', 1, f[:8]),
             ('wrong-widget-count', first_loop, first_loop.replace('i < 22', 'i < 21'), 1, f[:8]),
             ('wrong-descriptor-flag', 'descriptor, 255)', 'descriptor, 254)', 1, f[:8]),
             ('wrong-decimal-cap', 'if (value > 99999) value = 99999;', 'if (value > 99998) value = 99998;', 4, selected_cap),
             ('wrong-empty-sentinel', 'if (value == 0)', 'if (value == 1)', 4, [x for x in f if not x['mutate'] and x['values'] == 0]),
             ('wrong-packed-cap', 'if (value > 999) value = 999;', 'if (value > 998) value = 998;', 4, selected_packed),
             ('wrong-packed-field', 'packed38.middle10', 'packed38.high20', 1, [x for x in f if not x['mutate'] and x['packed'] == 0]),
             ('wrong-halfword-value', 'native_data_021d7098.value22', 'native_data_021d7098.value20', 1, f[:8]),
             ('wrong-final-word-result', 'return native_fn_020d2a14(27, native_data_021d7098.value20);', 'native_fn_020d2a14(27, native_data_021d7098.value20);\n    return 0;', 1, f[:8])]
    negatives = [mutation(label, old, new, count, main, chosen) for label, old, new, count, chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls([row]))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits = ['First closed1472-byte summary-rendering caller from exclusively reserved66/16700B main-tail-next claim. Every code/literal byte matches through genuine pinned MW linking of ordinary readable C and original untouched ELF names/relocations. No instruction/object/register patch, ordinary-logic ASM, allocation sweep or shared pipeline changes.',
              '168 independent original/source fixture pairs require actual caller returns, full GPR/CPSR, all calls/writes and8MiB RAM equality. They cover two22-widget phases, mutable handles/objects and repeated fresh getters, the aliased16-byte summary text, local Vec2 and32-byte UTF16 descriptor, all observed provider argument words and full final return.',
              'Four unsigned-word numbers have zero-vs-numeric display branches and99999 caps; four unsigned10-bit projections have999 caps. Zero,1,99998,99999,100000,all-ones and packed0/511/512/998/999/1000/1023 cases exercise boundaries. Providers may mutate all64 summary bytes after every call and clobber caller-saved registers/flags; fresh reads, point/descriptor persistence and aliased views remain independently checked.',
              'No actual widget/formatter/game/SDK provider body executes or gains credit. Providers are scripted minimum observed ABI boundaries; complete original callee source declarations, game UI semantics and untested formatter/string-length safety remain unproved. Descriptor writes in fixtures are deliberately bounded to32 bytes, and Vec2/widget/summary structures are ABI views with provisional names.',
              'Three BSS bindings use unchanged branch/data qualification plus immutable original caller/pool/raw inventory/load/field words. The summary64-byte view and input-text16-byte alias at+12 share one backing model; the formatter address is opaque. Complete original allocations/authorship and data storage credit remain unknown/zero.',
              '45 original-data negatives,54 all-import identity controls,4 real native layout rejections and3072 actual native unsigned10-bit ABI probe returns plus signed/order rejection controls are required.9 genuine whole-C errors must fail independent protocol/result checks; protocol-aborted negative executions are labeled and never counted as actual caller returns.',
              'Original/copied producer and generic canonical original/copied replay require source-complete private inputs. Capturing the formatter context and recovering unsigned10-bit views removed spurious lifetime/mask-literal differences. All prior57-claim READYs remain frozen; no overall game/hardware/platform/source-only ROM completion is established before serialized coordinator acceptance.']
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='', moduleSha256=info['sha256'],
               allPassed=True, matches=[row], canonicalMatchedFunctions=1, canonicalMatchedBytes=1472, cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)), producer=Path(__file__).name, producerSha256=sha256(Path(__file__)), limits=limits))
    print(dict(functions=1, bytes=1472, cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
