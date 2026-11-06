import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile
import wave20261104_main_nextcmd_cmp_compiler as compiler
from wave20261104_main_nextcmd_cmp_bindings import verify_original
from qualify_explicit_c_frontend_20261102 import qualify
import wave20261104_main_nextcmd_cmp_abi as helper_abi
from wave20261104_main_nextcmd_cmp_controls import execute as controls, flattened_context
from wave20261104_main_nextcmd_cmp_fixture import run, GAME_CALLS, STATUS_ONE
import unicorn

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-next/sixth'
WORK = ROOT / 'work/w4nc/sixth/proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-next/sixth'


def build(source, directory, negative=False):
    rows, unused = compiler.compare(source, directory / 'c')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Caller compile failed', rows))
    row = rows[0]
    headers = [source.with_name('context.h'), ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h',
        ROOT / 'src/runtime/parallel_wave20261104/main-command-next/second/context.h']
    row.update(program='', sourceDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in headers],
        ordinaryCBytes=row['bytes'], justifiedAssemblyBytes=0, justifiedAssemblyRanges=[])
    bindings = qualified_bindings(row)
    if not negative:
        row['originalNamespaceWitnesses'] = verify_original(row, bindings)
    try:
        proof = L.validate(row, bindings, directory / 'l')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0], dict):
            raise
        proof = dict(exactCallerBytes=False, comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Whole-C wrong status unexpectedly matched')
    body = (directory / 'l/caller.bin').read_bytes()
    with (directory / 'l/linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        entry = next(symbol for symbol in symbols if symbol.name == row['name'])
        if entry['st_value'] != int(row['address'], 0) or entry['st_size'] != row['compiledBytes'] or len(body) != row['compiledBytes']:
            raise ValueError('Genuine linked caller extent differs')
        if not any(symbol.name == '$a' and symbol['st_value'] == entry['st_value'] for symbol in symbols):
            raise ValueError('Linked ARM mapping missing')
    if L.relocation_rows(ROOT / row['object'], row['name']) != L.relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Caller splitting changed relocation payloads')
    row['explicitC99Qualification'] = qualify(row, directory / 'c99')
    row.update(sourceLanguage='C', nativeSymbolEntries=bindings, realLink=proof)
    return row, body


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    if {format(int(item['address'], 0), '08x') for item in inputs['entries']} != set(GAME_CALLS):
        raise ValueError('Frozen family caller set differs')
    helper_abi.execute()
    info, main, unused = L.measured_module('main')
    matches, traces, negatives, component_negatives = [], [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        name = format(int(item['address'], 0), '08x')
        directory = WORK / name
        row, body = build(source, directory / 'positive')
        if row['targetSha256'] != item['targetSha256'] or row['bytes'] != item['bytes']:
            raise ValueError('Frozen caller native extent differs')
        origin = int(row['address'], 0)
        native = main[origin - 0x02000000:origin - 0x02000000 + row['bytes']]
        old = 'status = ' + str(int(name in STATUS_ONE)) + ';'
        new = 'status = ' + str(1 - int(name in STATUS_ONE)) + ';'
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError('Whole-C status mutation ambiguous')
        wrong = directory / 'negative/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        wrong.write_text(text.replace(old, new))
        wrong.with_name('context.h').write_text(flattened_context())
        badrow, badbody = build(wrong, wrong.parent / 'build', True)
        rejected = 0
        for ordinal in range(8):
            original = run(row, native, ordinal, main)
            rebuilt = run(row, body, ordinal, main)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], ordinal=ordinal, original=original, rebuilt=rebuilt))
                raise ValueError(('Positive full state/model differs', row['address'], ordinal, original['modelFailures']))
            bad = run(badrow, badbody, ordinal, main)
            rejected += bool(bad['modelFailures'])
            traces.append(dict(address=row['address'], ordinal=ordinal, result=original))
        if rejected != 8:
            raise ValueError('Wrong-C status failed to reject every independent context model')
        if name == '020528fc':
            old_component = 'ratio <= 0.2f'
            new_component = 'ratio <= 0.1f'
            if text.count(old_component) != 1:
                raise ValueError('Component mutation ambiguous')
            component_source = directory / 'negative-component/source.c'
            component_source.parent.mkdir(parents=True, exist_ok=True)
            component_source.write_text(text.replace(old_component, new_component))
            component_source.with_name('context.h').write_text(flattened_context())
            component_row, component_body = build(component_source, component_source.parent / 'build', True)
            component_cases = [bool(run(component_row, component_body, ordinal, main)['modelFailures']) for ordinal in range(8)]
            if sum(component_cases) != 2:
                raise ValueError(('Wrong fixed-component model coverage differs', component_cases))
            component_negatives.append(dict(address=row['address'], mutation=[old_component, new_component], cases=8,
                rejectedCases=2, equivalentCases=6, proof=component_row, nativeCalleeExecutionOrSourceCredit=0))
        negatives.append(dict(address=row['address'], mutation=[old, new], rejectedCases=rejected, proof=badrow))
        matches.append(row)
        print('proved', name, row['bytes'], rejected, flush=True)
    qualification = controls(matches)
    write_json(LANE / 'binding-layout-controls.json', qualification)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='',
        moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
        canonicalMatchedBytes=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
        nativeOriginalComparisonHelperBodiesExecuted=sum(len(item['result']['actualOriginalComparisonHelperReturns']) for item in traces) * 2,
        opaqueNativeGameOrConversionBodiesExecuted=0, comparisonHelperOrProbeSourceCredit=0, calleeSourceCredit=0, negativeEvidence=negatives, additionalComponentNegativeEvidence=component_negatives,
        originalComparisonHelperQualification=dict(path=(LANE / 'helper-abi.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'helper-abi.json')),
        inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
        bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
        generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
        producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
        limits=['Ordinary readable C command handlers; exact configured whole extents, pinned SP1 profile, actual original relocations and genuine MW links. Each production function also passes fresh explicitC99 complete function-byte and relocation equivalence before canonical C language classification.',
            'Eight finite synthetic caller fixtures per handler, actual top returns with 5000-instruction and two-second per-call bounds; complete GPR/CPSR/calls/writes/8MiB RAM equality and independent context models.',
            'Opaque game/count/record/buffer routines and integer-to-float/division helpers remain supplied contracts with zero native body execution/source credit. Three independently qualified original comparison-helper bodies actually execute and return with complete GPR/CPSR/reference and ordered-write checks inside every caller; those helper/scaffolding bytes receive zero source credit.',
            'Twenty-two native C99 layout checks plus wrongstride and eleven original binding/namespace controls; actual5430-case original-helper qualification with9native negative controls is separate. Independent zero/negative/dense counts, complete64-byte supplied buffers, signed/byte partial-record fields and four observed output codes include exact0.2and adjacent float boundaries. Wrong0.1threshold whole-C variant rejected in2discriminating cases with6equivalents.',
            'Original ambiguous multi-overlay records remain uncredited diagnostics outside this packet; no numeric-address or permissive module exception.',
            'Actual game value domains, arbitrary aliases, all record counts, NaNs/infinities, out-of-range float casts, native callee behavior, scene execution and hardware timing remain unproved.',
            'Configured function boundary confidence is retained, augmented by complete matching and bounded caller returns; shared acceptance belongs to the coordinator.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
