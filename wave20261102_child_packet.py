import argparse
import ast
import json
import re
from pathlib import Path
import utility_code
import utility_runtime
from utility_types import fixed_references
from match_utility_primitives import native_bindings
from wave20261102_child_prepare import ROOT, LANE, WORK, SOURCE
import wave20261102_child_link as linker
import wave20261102_child_list_oracle as list_oracle
from project import write_json, sha256, now


def policy(path):
    text = path.read_text()
    if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
        raise ValueError('Source policy violation')
    if '#include' in text:
        raise ValueError('Unexpected source dependency')
    return dict(commentFree=True, physicalLines=len(text.splitlines()), ordinaryC=True,
                originalExecutableBytesAsSource=False, sourceDependencies=[])


def build(entry, spec):
    source = ROOT / entry['source']
    if sha256(source) != entry['sourceSha256']:
        raise ValueError('Frozen source changed')
    source_policy = policy(source)
    flags = entry['compilerFlags']
    configured = dict(spec, compilerPath=ROOT / entry['compiler'], compilerProc=flags[flags.index('-proc') + 1])
    row, code = utility_code.compile_compare(source, configured, flags[0][2:], flags[flags.index('-inline') + 1], 'speed' in flags)
    if code is None:
        raise ValueError(row)
    row.update(sourceDependencies=[], sourceLanguage='C', ordinaryFunctionCredit=1,
        ordinaryCBytes=spec['bytes'], justifiedAssemblyBytes=0, originalObjectScaffolding=False,
        originalDataSourceCredit=0, wholeModuleLinked=False,
        executableInstructionBytes=sum(i.size for i in spec['instructions']),
        generatedLiteralBytes=spec['bytes'] - sum(i.size for i in spec['instructions']),
        sourcePolicy=source_policy, fixedWorkAreaReferences=fixed_references(source.read_text(), spec))
    row['realLink'] = linker.validate(row, WORK / 'final-links' / ('%08x' % spec['address']))
    row['exactAfterRealMwLink'] = True
    row['oracle'] = dict(supported=False, nativeAndRecompiledCalls=0, executionCredit=0,
        limitation='Independent SDK runtime fixtures have not been constructed for this candidate; compile and genuine isolated link equality cover its complete canonical span')
    oracle = list_oracle.validate(row, (WORK / 'final-links' / ('%08x' % spec['address']) / 'caller.bin').read_bytes())
    if oracle is not None:
        row['oracle'] = oracle
    return row


def generator_sources():
    pending = [ROOT / name for name in ['wave20261102_child_packet.py', 'wave20261102_child_link.py',
        'wave20261102_child_list_oracle.py', 'wave20261102_child_lists.py', 'wave20261102_child_research.py',
        'wave20261102_child_sweep.py', 'wave20261102_child_prepare.py']]
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 else []
            for name in names:
                candidate = ROOT / (name.split('.')[0] + '.py') if name else None
                if candidate is not None and candidate.is_file():
                    pending.append(candidate)
    return [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in sorted(seen)]


def freeze_inputs(matches, path):
    keys = ['name', 'program', 'processor', 'module', 'address', 'mode', 'bytes', 'binary',
            'inputModuleSha256', 'targetSha256', 'source', 'sourceSha256', 'sourceDependencies',
            'compiler', 'compilerSha256', 'compilerFlags']
    entries = [{k: e[k] for k in keys if k in e} for e in matches]
    write_json(path, dict(schemaVersion=1, immutableInputManifest=True,
        romSha256=utility_runtime.audit_regions.ROM_HASH, entries=entries,
        generatorSources=generator_sources(), claimIsRuntimeDependency=False,
        inputKinds=['authored ordinary C', 'pinned compiler/linker/scripts', 'private measured native comparison target'],
        originalExecutableCompilerInput=False))
    return entries


def candidates():
    selected = {}
    for stage in ['research', 'sweeps', 'sweeps-scalar', 'lists']:
        for path in sorted((LANE / stage).glob('*.json')):
            result = json.loads(path.read_text())
            if result.get('match'):
                entry = result['match']
                selected[entry['address']] = dict(result, researchEvidence=path.relative_to(ROOT).as_posix())
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--packet', default='packet.json')
    args = parser.parse_args()
    specs = {hex(s['address']): s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'}
    utility_code.WORK = WORK / 'final-compiled'
    if Path(args.packet).name != args.packet or not args.packet.endswith('.json'):
        raise ValueError('Packet name must be a local JSON filename')
    report_path = LANE / args.packet
    input_path = report_path.with_name(report_path.stem + '-inputs.json')
    failed, matches = [], []
    if args.verify:
        previous = json.loads(report_path.read_text())
        if sha256(input_path) != previous['inputManifestSha256']:
            raise ValueError('Immutable packet input manifest changed')
        inputs = json.loads(input_path.read_text())
        for pin in inputs['generatorSources']:
            if sha256(ROOT / pin['path']) != pin['sha256']:
                raise ValueError('Producer/oracle/linker closure changed: ' + pin['path'])
        selected = {r['address']: dict(match=r) for r in inputs['entries']}
    else:
        if report_path.exists():
            raise ValueError('Packet exists; use --verify')
        selected = candidates()
    for address, result in sorted(selected.items()):
        entry = dict(result['match'])
        spec = specs[address]
        try:
            if not args.verify:
                text = (ROOT / entry['source']).read_text()
                text = re.sub(r'^#define M2C_FIELD.*$', '#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))', text, flags=re.M)
                text = text.replace('M2C_FIELD', 'CHILD_FIELD')
                source = SOURCE / (spec['name'] + '.c')
                source.parent.mkdir(parents=True, exist_ok=True)
                if source.exists() and source.read_text() != text:
                    raise ValueError('Refusing source overwrite')
                if not source.exists():
                    source.write_text(text)
                entry.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source))
            row = build(entry, spec)
            row['researchEvidence'] = result.get('researchEvidence', entry.get('researchEvidence'))
            matches.append(row)
            print(dict(address=address, bytes=spec['bytes'], realLinked=True), flush=True)
        except Exception as error:
            failed.append(dict(address=address, failure=str(error), source=entry.get('source')))
            print(dict(address=address, failed=str(error)[:150]), flush=True)
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=utility_runtime.audit_regions.ROM_HASH,
        program=utility_runtime.PROGRAM, processor='arm9', runtimeMappingCanonical=True,
        matches=matches,
        nativeSymbolBindings=native_bindings(matches),
        nativeSymbols={r['symbol']: r['target'] for e in matches for r in e['relocations']},
        sourceDependencies=[], failed=failed, exactFunctions=len(matches),
        exactInitializedBytes=sum(r['bytes'] for r in matches), wholeModuleLinked=False,
        acceptedSourceCredit=0, sourceReconstructionComplete=False,
        reproduce=['python wave20261102_child_packet.py --packet ' + args.packet + ' --verify'],
        limitations=['Isolated exact candidates await shared acceptance and all affected module links',
                    'Named SDK behavior and field meanings remain interpretations unless independently fixture-validated',
                    'No full-game/native-platform execution is claimed; no original executable receives source credit'])
    if not args.verify:
        freeze_inputs(matches, input_path)
    report.update(inputManifest=input_path.relative_to(ROOT).as_posix(), inputManifestSha256=sha256(input_path),
                  generatorSources=json.loads(input_path.read_text())['generatorSources'])
    write_json(LANE / (report_path.stem + '-verification.json') if args.verify else report_path, report)
    print(dict(exactFunctions=len(matches), exactBytes=report['exactInitializedBytes'], failed=len(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
