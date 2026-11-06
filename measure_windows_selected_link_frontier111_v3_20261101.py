import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from inspect_windows_native_link_frontier111_20261101 import coff, address
from reconcile_windows_link_frontier_comdat_v2_20261101 import section_metadata


def load_details(report):
    path = ROOT / report['details']['path']
    assert sha256(path) == report['details']['sha256']
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == report['details']['decodedSha256']
    return json.loads(raw)


def main():
    frontier_path = ROOT / 'evidence/portability/windows-native-link-frontier111-20261101.json'
    frontier = read_json(frontier_path)
    original = load_details(frontier)
    variant_path = ROOT / 'evidence/portability/windows-selected-functions111-20261101.json'
    variants = read_json(variant_path)
    assert variants['state'] == 'completed' and variants['compiled'] == variants['sourceUnits'] == 247
    updates = {row['source']: row for row in variants['results']}
    groups, objects = defaultdict(list), []
    snapshot = read_json(ROOT / frontier['sourceSnapshot']['path'])
    assert sha256(ROOT / frontier['sourceSnapshot']['path']) == frontier['sourceSnapshot']['sha256']
    known = defaultdict(list)
    for entry in snapshot['functions']:
        location = int(entry['address'], 0) if isinstance(entry['address'], str) else entry['address']
        known[entry['processor'], entry.get('program') or '', location].append(entry)
    for previous in original['objects']:
        assert sha256(ROOT / previous['source']) == previous['sourceSha256']
        row = {key: previous[key] for key in ['source', 'sourceSha256', 'object', 'objectSha256', 'scopes', 'selectedInstances']}
        if row['source'] in updates:
            update = updates[row['source']]
            assert update['compiled'] and update['selectedBodiesPreserved']
            assert sha256(ROOT / update['candidate']) == update['candidateSha256']
            row.update(object=update['object'], objectSha256=update['objectSha256'],
                nativeCompileSource=update['candidate'], nativeCompileSourceSha256=update['candidateSha256'],
                selectedBodyHashes=update['selectedBodyHashes'])
        assert sha256(ROOT / row['object']) == row['objectSha256']
        parsed = coff(ROOT / row['object'])
        sections = section_metadata(ROOT / row['object'])
        for definition in parsed['definitions']:
            definition['coffSection'] = sections.get(definition['section'])
        row.update(parsed)
        objects.append(row)
        for scope in row['scopes']:
            groups[tuple(scope)].append(row)
    modules = []
    for scope, members in sorted(groups.items()):
        processor, program, module = scope
        local, available = defaultdict(list), defaultdict(list)
        for other_scope, providers in groups.items():
            if other_scope[:2] != scope[:2]:
                continue
            for provider in providers:
                for symbol in provider['definitions']:
                    record = dict(source=provider['source'], module=other_scope[2], **symbol)
                    available[symbol['name']].append(record)
                    if other_scope == scope:
                        local[symbol['name']].append(record)
        needs = defaultdict(list)
        for row in members:
            for symbol in row['undefined']:
                needs[symbol['name']].append(row['source'])
        symbols, counts = [], defaultdict(int)
        for name, consumers in sorted(needs.items()):
            candidates = known.get((processor, program, address(name)), [])
            if name in local:
                classification = 'exact-name-defined-in-same-module'
            elif name in available:
                classification = 'exact-name-defined-in-same-program-other-module'
            elif candidates:
                classification = 'qualified-address-candidates-need-alias-or-platform-work'
            elif name in ['_memcpy', '_memset', '_memmove', '__fltused'] or name.startswith('___'):
                classification = 'native-runtime-symbol'
            else:
                classification = 'unresolved-symbol'
            counts[classification] += 1
            symbols.append(dict(symbol=name, classification=classification, consumers=sorted(set(consumers)),
                exactNameProviderSources=[dict(source=row['source'], module=row['module']) for row in available.get(name, [])],
                addressCandidates=[{key: entry[key] for key in ['processor', 'program', 'module', 'mode', 'address', 'source']}
                    for entry in candidates], aliasApplied=False))
        duplicates = []
        for name, providers in sorted(local.items()):
            if len({provider['source'] for provider in providers}) < 2:
                continue
            values = [provider['coffSection'] for provider in providers]
            same = len({(value['rawBytes'], value['initializedBytesSha256']) for value in values if value}) == 1
            foldable = name.startswith(('__real@', '__xmm@')) and same and all(value and value['comdat']
                and value['selection'] == 2 and value['relocationCount'] == 0 for value in values)
            foldable &= not any(provider['function'] for provider in providers)
            duplicates.append(dict(symbol=name, providers=providers,
                classification='identical-compiler-literal-COMDAT-pick-any' if foldable else 'unresolved-definition-conflict'))
        modules.append(dict(processor=processor, program=program, module=module, objectUnits=len(members),
            undefinedNames=len(needs), resolutionCounts=dict(counts), symbols=symbols,
            duplicateDefinitionNames=len(duplicates), duplicateFunctionNames=sum(any(row['function'] for row in item['providers']) for item in duplicates),
            unresolvedDefinitionConflicts=sum(item['classification'] == 'unresolved-definition-conflict' for item in duplicates),
            duplicateDefinitions=duplicates))
    detail = dict(objects=objects, modules=modules)
    encoded = json.dumps(detail, sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-details-20261101.json.gz'
    path.write_bytes(gzip.compress(encoded, mtime=0))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        originalFrontier=dict(path=frontier_path.relative_to(ROOT).as_posix(), sha256=sha256(frontier_path)),
        isolationProof=dict(path=variant_path.relative_to(ROOT).as_posix(), sha256=sha256(variant_path)),
        verifiedObjects=len(objects), isolatedSourceUnits=len(updates), scopeCount=len(modules),
        sourceCredit=0, acceptedArmSourceModified=False, nativeExecutionCount=0,
        fullNativeLinkProven=False, fullWindowsGameProven=False,
        undefinedNames=sum(row['undefinedNames'] for row in modules),
        duplicateFunctionNames=sum(row['duplicateFunctionNames'] for row in modules),
        unresolvedDefinitionConflicts=sum(row['unresolvedDefinitionConflicts'] for row in modules),
        modules=[{key: value for key, value in row.items() if key not in ['symbols', 'duplicateDefinitions']} for row in modules],
        details=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), decodedSha256=hashlib.sha256(encoded).hexdigest()),
        limitations=['Only accepted111 successful C/C++ source objects are included; blocked C and ARM assembly remain excluded',
            'Unselected public bodies are declarations in separate source variants; selected body text remains unchanged',
            'Removing neighboring definitions changes inlining opportunities; native behavioral equivalence is still unproved',
            'Remaining undefined symbols and data conflicts are genuine build work; no aliases, stubs or linker suppression applied',
            'Module namespaces remain distinct; an address alone never establishes a cross-overlay or child-program binding'])
    write_json(ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-20261101.json', report)
    print({key: report[key] for key in ['verifiedObjects', 'isolatedSourceUnits', 'undefinedNames',
        'duplicateFunctionNames', 'unresolvedDefinitionConflicts', 'sourceCredit']})


if __name__ == '__main__':
    main()
