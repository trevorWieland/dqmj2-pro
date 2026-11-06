import argparse
import ast
import json
import re
import shutil
from pathlib import Path
import utility_code
import utility_runtime
from utility_types import fixed_references
from match_utility_primitives import native_bindings
from slice_reference_sdk_entities_v3_20261102 import functions
import wave20261102_child_third_link as linker
from wave20261102_child_third_prepare import ROOT, LANE, WORK, SOURCE
from project import write_json, sha256, now

INPUT_KEYS = ['name', 'program', 'processor', 'module', 'address', 'mode', 'bytes',
    'inputModuleSha256', 'targetSha256', 'source', 'sourceSha256', 'sourceDependencies',
    'compiler', 'compilerSha256', 'compilerFlags', 'researchEvidence', 'sourceReuseProvenance',
    'normalizedFingerprint', 'sourceAdaptationMethod', 'qualifiedOriginalConstants', 'referenceFunction',
    'recoveredGlobalStorageCredit', 'sourceLinkageNormalization']


def generators():
    pending = [ROOT / name for name in ['wave20261102_child_third_prepare.py',
        'wave20261102_child_third_catalog.py', 'wave20261102_child_third_adapt.py',
        'wave20261102_child_third_crosscompile.py', 'wave20261102_child_third_draft.py',
        'wave20261102_child_third_abi.py', 'wave20261102_child_third_cfg_draft.py',
        'wave20261102_child_third_link.py', 'wave20261102_child_third_self_modes.py',
        'wave20261102_child_third_sdk.py', 'wave20261102_child_third_sdk_repair.py',
        'wave20261102_child_third_sdk_literals.py', 'wave20261102_child_third_binding_controls.py',
        'wave20261102_child_third_packet.py']]
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 else []
            for name in names:
                child = ROOT / (name.split('.')[0] + '.py') if name else None
                if child is not None and child.is_file():
                    pending.append(child)
    return [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in sorted(seen)]


def policy(entry):
    paths = [ROOT / entry['source'], *[ROOT / p['path'] for p in entry['sourceDependencies']]]
    pins = {entry['source']: entry['sourceSha256'], **{p['path']: p['sha256'] for p in entry['sourceDependencies']}}
    for path in paths:
        text = path.read_text()
        if not path.resolve().is_relative_to(SOURCE) or sha256(path) != pins[path.relative_to(ROOT).as_posix()]:
            raise ValueError('Source/include identity escaped frozen private closure')
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
            raise ValueError('Source/include policy failed')
    expected = {p.resolve() for p in paths[1:]}
    found, pending = set(), [paths[0]]
    while pending:
        path = pending.pop()
        for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"', path.read_text(), re.M):
            child = (path.parent / name).resolve()
            if child not in found:
                found.add(child)
                pending.append(child)
    if found != expected:
        raise ValueError('Actual include closure differs')
    return dict(ordinaryC=True, commentFree=True, sourceDependenciesVerified=True,
                maximumFileLines=max(len(p.read_text().splitlines()) for p in paths))


def build(entry, spec):
    spec = dict(spec, name=entry['name'])
    source_policy = policy(entry)
    flags = entry['compilerFlags']
    configured = dict(spec, compilerPath=ROOT / entry['compiler'], compilerProc=flags[flags.index('-proc') + 1],
                      interworking='-nointerworking' not in flags)
    row, code = utility_code.compile_compare(ROOT / entry['source'], configured, flags[0][2:],
                                           flags[flags.index('-inline') + 1], 'speed' in flags)
    if code is None:
        raise ValueError(row)
    if row['compilerFlags'] != flags:
        raise ValueError('Frozen compiler flags differ')
    for key in ['sourceDependencies', 'researchEvidence', 'sourceReuseProvenance', 'normalizedFingerprint',
                'sourceAdaptationMethod', 'qualifiedOriginalConstants', 'referenceFunction', 'recoveredGlobalStorageCredit']:
        if key in entry:
            row[key] = entry[key]
    if 'sourceLinkageNormalization' in entry:
        row['sourceLinkageNormalization'] = entry['sourceLinkageNormalization']
    row.update(sourceLanguage='C', ordinaryFunctionCredit=1, ordinaryCBytes=spec['bytes'], justifiedAssemblyBytes=0,
        originalObjectScaffolding=False, originalDataSourceCredit=0, wholeModuleLinked=False, sourcePolicy=source_policy,
        executableInstructionBytes=sum(i.size for i in spec['instructions']),
        generatedLiteralBytes=spec['bytes'] - sum(i.size for i in spec['instructions']))
    references = []
    for path in [ROOT / entry['source'], *[ROOT / p['path'] for p in entry['sourceDependencies']]]:
        references.extend(fixed_references(path.read_text(), spec))
    row['fixedWorkAreaReferences'] = references
    self_rows = [r for r in row['relocations'] if r['symbol'] == row['name']]
    if any((int(r['target'], 0) & ~1) != spec['address'] or r['targetMode'] != spec['mode'] for r in self_rows):
        raise ValueError('Recursive relocation has a conflicting native identity')
    link_entry = dict(row, relocations=[r for r in row['relocations'] if r not in self_rows])
    proof = linker.validate(link_entry, WORK / 'final-links' / ('%08x' % spec['address']))
    proof['selfBoundRelocations'] = self_rows
    proof['selfCallsResolvedToActualCallerDefinition'] = True
    row.update(realLink=proof, exactAfterRealMwLink=True,
        oracle=dict(supported=False, nativeAndRecompiledCalls=0, executionCredit=0,
            limitation='Full canonical bytes and genuine isolated link are exact; independent SDK behavioral fixtures are not established'))
    return row


def selected():
    result = {}
    for stage in ['research', 'expanded', 'candidates', 'cfg/research', 'cfg/expanded', 'cfg2/research', 'cfg2/expanded']:
        for path in sorted((LANE / stage).glob('*.json')):
            report = json.loads(path.read_text())
            if not report.get('match'):
                continue
            entry = report['match']
            entry['researchEvidence'] = path.relative_to(ROOT).as_posix()
            if entry['address'] not in result or entry.get('sourceReuseProvenance'):
                result[entry['address']] = entry
    exclusions = LANE / 'ready-exclusions.json'
    if exclusions.exists():
        for row in json.loads(exclusions.read_text())['functions']:
            result.pop(row['address'], None)
    return result


def promote(entry):
    source = ROOT / entry['source']
    paths = [source, *[ROOT / p['path'] for p in entry.get('sourceDependencies', [])]]
    directory = SOURCE / ('%08x' % int(entry['address'], 0))
    directory.mkdir(parents=True, exist_ok=True)
    copies, normalizations = [], []
    for original in paths:
        text = original.read_text()
        text = text.replace('M2C_FIELD', 'CHILD_FIELD')
        revised = False
        if original == ROOT / entry['source']:
            pattern = r'\bstatic\s+((?:(?![;{}]).)*?\b' + re.escape(entry['name']) + r'\s*\()'
            text, declarations = re.subn(pattern, r'\1', text, flags=re.S)
            if declarations:
                revised = True
                normalizations.append(dict(symbol=entry['name'], declarations=declarations,
                    purpose='External caller linkage for source declarations and definition at the genuine isolated-link root', sourceCredit=0))
            for function in functions(text):
                if function['name'] == entry['name']:
                    header = text[function['start']:function['opening']]
                    changed = re.sub(r'\bstatic\s+', '', header, count=1)
                    if changed != header:
                        text = text[:function['start']] + changed + text[function['opening']:]
                        revised = True
                        normalizations.append(dict(symbol=entry['name'], purpose='External caller linkage for the genuine isolated-link root', sourceCredit=0))
                    break
            pattern = r'(?m)^([ \t]*)(?:static\s+)?(u32|s32|BOOL|FSArchive|FSDirPos|CARDRomStat|CARDiCommon)\s+(\**native_utility_child_\w+_data_[0-9a-f]{8})(?:\s+__attribute__[^;]*)?(?:\s*=\s*[^;]*)?;[ \t]*$'
            def external(match):
                normalizations.append(dict(symbol=match[3], purpose='Explicit original external storage binding', sourceCredit=0, dataStorageCredit=0))
                return match[1] + 'extern ' + match[2] + ' ' + match[3] + ';'
            text, count = re.subn(pattern, external, text)
            revised = revised or count != 0
        destination = directory / (original.stem + '_external_' + utility_runtime.sha(text.encode())[:10] + '.c' if revised else original.name)
        if destination.exists() and destination.read_text() != text:
            raise ValueError('Refusing promoted source overwrite')
        if not destination.exists():
            destination.write_text(text)
        copies.append(destination)
    return dict(entry, source=copies[0].relative_to(ROOT).as_posix(), sourceSha256=sha256(copies[0]),
        sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in copies[1:]],
        sourceLinkageNormalization=normalizations,
        sourceReuseProvenance=[dict(source=p['source'], sourceSha256=p['sourceSha256']) for p in entry.get('sourceReuseProvenance', [])])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--inputs-sha256')
    args = parser.parse_args()
    path, pins_path = LANE / 'packet-ready.json', LANE / 'packet-ready-inputs.json'
    specs = {hex(s['address']): s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'}
    utility_code.WORK = WORK / 'final-compiled'
    if args.verify:
        if not args.inputs_sha256 or sha256(pins_path) != args.inputs_sha256:
            raise ValueError('Explicit immutable manifest SHA256 required')
        pins = json.loads(pins_path.read_text())
        for pin in pins['generatorSources']:
            if sha256(ROOT / pin['path']) != pin['sha256']:
                raise ValueError('Frozen producer/include closure changed')
        entries = {e['address']: e for e in pins['entries']}
        archive = LANE / 'packet-ready-original.json'
        if not archive.exists():
            archive.write_bytes(path.read_bytes())
    else:
        if path.exists() or pins_path.exists():
            raise ValueError('Sealed packet exists')
        entries = {address: promote(entry) for address, entry in selected().items()}
    matches, failed = [], []
    for address, entry in sorted(entries.items()):
        try:
            row = build(entry, specs[address])
            if any(row.get(k) != entry.get(k) for k in INPUT_KEYS if k not in ['researchEvidence', 'sourceReuseProvenance', 'normalizedFingerprint', 'sourceAdaptationMethod']):
                raise ValueError('Fresh source/native/compiler contract differs')
            matches.append(row)
            print(dict(address=address, bytes=row['bytes'], exactRealLink=True), flush=True)
        except Exception as error:
            failed.append(dict(address=address, failure=str(error)))
            print(dict(address=address, failure=str(error)[:160]), flush=True)
    if failed:
        write_json(LANE / 'packet-replay-failed.json', dict(failed=failed, matches=matches))
        raise SystemExit(1)
    if not args.verify:
        write_json(pins_path, dict(schemaVersion=1, immutableInputManifest=True,
            romSha256=utility_runtime.audit_regions.ROM_HASH, entries=[{k: e[k] for k in INPUT_KEYS if k in e} for e in matches],
            generatorSources=generators(), claimIsRuntimeDependency=False, researchProductsAreRuntimeDependencies=False,
            originalExecutableCompilerInput=False))
    digest = sha256(pins_path)
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=utility_runtime.audit_regions.ROM_HASH,
        program=utility_runtime.PROGRAM, processor='arm9', runtimeMappingCanonical=True, matches=matches,
        nativeSymbols={r['symbol']: r['target'] for e in matches for r in e['relocations']},
        nativeSymbolBindings=native_bindings(matches), sourceDependencies=[],
        generator='wave20261102_child_third_packet.py', generatorSha256=sha256(__file__),
        generatorSources=json.loads(pins_path.read_text())['generatorSources'],
        inputManifest=pins_path.relative_to(ROOT).as_posix(), inputManifestSha256=digest,
        exactFunctions=len(matches), exactInitializedBytes=sum(e['bytes'] for e in matches), failed=[],
        wholeModuleLinked=False, acceptedSourceCredit=0, sourceReconstructionComplete=False,
        replayCanonicalReportRefreshed=True, replayRoot=str(ROOT), sourceContractsUnchanged=True,
        reproduce=['python wave20261102_child_third_packet.py --verify --inputs-sha256 ' + digest],
        limitations=['Every source extent still requires coordinator acceptance and affected module links',
            'Template names and SDK meanings are inferred unless separately measured',
            'No independent SDK behavior, hardware, gameplay, source-only ROM or native platform execution is claimed'])
    write_json(path, report)
    write_json(LANE / 'canonical-replay-latest.json', dict(functions=len(matches), bytes=report['exactInitializedBytes'],
        root=str(ROOT), canonicalReportSha256=sha256(path), sourceContractsUnchanged=True))
    print(dict(functions=len(matches), bytes=report['exactInitializedBytes'], inputsSha256=digest))


if __name__ == '__main__':
    main()
