import argparse
import ast
import json
import re
from pathlib import Path
import utility_code
import utility_runtime
import wave20261102_child_packet as shared
from match_utility_primitives import native_bindings
from wave20261102_child_next_prepare import ROOT, LANE, WORK, SOURCE
from project import write_json, sha256, now


def generators():
    pending = [ROOT / name for name in ['wave20261102_child_next_prepare.py',
        'wave20261102_child_next_research.py', 'wave20261102_child_next_expand.py', 'wave20261102_child_next_packet.py']]
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 else []
            for name in names:
                candidate = ROOT / (name.split('.')[0] + '.py') if name else None
                if candidate is not None and candidate.is_file():
                    pending.append(candidate)
    return [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in sorted(seen)]


def input_rows(matches):
    keys = ['name', 'program', 'processor', 'module', 'address', 'mode', 'bytes', 'binary',
            'inputModuleSha256', 'targetSha256', 'source', 'sourceSha256', 'sourceDependencies',
            'compiler', 'compilerSha256', 'compilerFlags']
    return [{k: e[k] for k in keys if k in e} for e in matches]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--packet', default='packet-ready.json')
    args = parser.parse_args()
    if Path(args.packet).name != args.packet or not args.packet.endswith('.json'):
        raise ValueError('Packet name must be a JSON filename')
    report_path = LANE / args.packet
    pins_path = report_path.with_name(report_path.stem + '-inputs.json')
    specs = {hex(s['address']): s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'}
    utility_code.WORK = WORK / 'final-compiled'
    shared.WORK = WORK
    if args.verify:
        previous = json.loads(report_path.read_text())
        if sha256(pins_path) != previous['inputManifestSha256']:
            raise ValueError('Immutable input manifest changed')
        pins = json.loads(pins_path.read_text())
        for pin in pins['generatorSources']:
            if sha256(ROOT / pin['path']) != pin['sha256']:
                raise ValueError('Producer/include closure changed: ' + pin['path'])
        selected = {r['address']: dict(match=r) for r in pins['entries']}
    else:
        if report_path.exists() or pins_path.exists():
            raise ValueError('Packet exists; use --verify')
        selected = {}
        for stage in ['research', 'expanded', 'expanded2']:
            for path in sorted((LANE / stage).glob('*.json')):
                result = json.loads(path.read_text())
                if result.get('match'):
                    selected[result['match']['address']] = dict(result, researchEvidence=path.relative_to(ROOT).as_posix())
    matches, failed = [], []
    for address, result in sorted(selected.items()):
        entry, spec = dict(result['match']), specs[address]
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
            row = shared.build(entry, spec)
            row['researchEvidence'] = result.get('researchEvidence', entry.get('researchEvidence'))
            matches.append(row)
            print(dict(address=address, bytes=spec['bytes'], exactRealLink=True), flush=True)
        except Exception as error:
            failed.append(dict(address=address, source=entry.get('source'), failure=str(error)))
            print(dict(address=address, failure=str(error)[:160]), flush=True)
    if not args.verify:
        write_json(pins_path, dict(schemaVersion=1, immutableInputManifest=True,
            romSha256=utility_runtime.audit_regions.ROM_HASH, entries=input_rows(matches),
            generatorSources=generators(), claimIsRuntimeDependency=False, originalExecutableCompilerInput=False))
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=utility_runtime.audit_regions.ROM_HASH,
        program=utility_runtime.PROGRAM, processor='arm9', runtimeMappingCanonical=True,
        generator='wave20261102_child_next_packet.py', generatorSha256=sha256(__file__),
        matches=matches, nativeSymbolBindings=native_bindings(matches),
        nativeSymbols={r['symbol']: r['target'] for e in matches for r in e['relocations']},
        sourceDependencies=[], generatorSources=json.loads(pins_path.read_text())['generatorSources'],
        inputManifest=pins_path.relative_to(ROOT).as_posix(), inputManifestSha256=sha256(pins_path),
        exactFunctions=len(matches), exactInitializedBytes=sum(e['bytes'] for e in matches), failed=failed,
        wholeModuleLinked=False, acceptedSourceCredit=0, sourceReconstructionComplete=False,
        reproduce=['python wave20261102_child_next_packet.py --packet ' + args.packet + ' --verify'],
        limitations=['All candidates require shared source acceptance and affected module links',
                    'Independent SDK behavioral fixtures are unsupported unless an entry explicitly records them',
                    'No hardware, gameplay, source-only ROM or native platform execution is claimed'])
    write_json(report_path.with_name(report_path.stem + '-verification.json') if args.verify else report_path, report)
    print(dict(functions=len(matches), bytes=report['exactInitializedBytes'], failed=len(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
