import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from recover_linked_runtime import qualified_bindings


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def scalar(kind, aliases, parameter=False):
    text = kind.get('desugaredQualType', kind.get('qualType', '')) if isinstance(kind, dict) else kind
    for unused in range(12):
        prior = text
        text = re.sub(r'\b[A-Za-z_]\w*\b', lambda match:
            aliases[match[0]].get('desugaredQualType', aliases[match[0]].get('qualType', match[0]))
            if match[0] in aliases else match[0], text)
        if text == prior:
            break
    text = re.sub(r'\s+', ' ', text.strip()).replace(' *', '*').replace('* ', '*')
    text = re.sub(r'\bsigned int\b', 'int', text)
    text = re.sub(r'\bsigned short\b', 'short', text)
    if parameter and '*' not in text:
        text = re.sub(r'\b(?:const|volatile)\s*', '', text).strip()
    allowed = r'(?:const |volatile )*(?:void|char|signed char|unsigned char|short|unsigned short|int|unsigned int|long|unsigned long|long long|unsigned long long|float|double)(?:\*)*'
    return text if re.fullmatch(allowed, text) else None


def signature(record, aliases):
    raw = record['type'].get('qualType', '')
    found = re.fullmatch(r'(.+?)\s*\(([^()]*)\)', raw)
    if not found or record['variadic']:
        return None
    result = scalar(found[1], aliases)
    parameters = [scalar(value, aliases, parameter=True) for value in record['parameters']]
    if result is None or any(value is None for value in parameters):
        return None
    return dict(result=result, parameters=parameters, noPrototype=not found[2].strip())


def compatible(actual, wanted, argument):
    if actual == wanted:
        return True
    pairs = [{'int', 'unsigned int'}, {'long', 'unsigned long'}, {'long long', 'unsigned long long'}]
    if {actual, wanted} not in pairs or argument['literalValue'] is None:
        return False
    try:
        value = int(argument['literalValue'])
    except ValueError:
        return False
    bound = (1 << (63 if 'long long' in actual else 31)) - 1
    return 0 <= value <= bound


def main():
    catalogue_path = ROOT / 'evidence/portability/windows-native-call-types111-20261101.json'
    catalogue = read_json(catalogue_path)
    assert catalogue['state'] == 'completed' and catalogue['definitionsWithAllCoffFunctions'] == 8375
    path = ROOT / catalogue['details']['path']
    assert sha256(path) == catalogue['details']['sha256']
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == catalogue['details']['decodedSha256']
    rows = json.loads(raw)
    sources = {row['source']: row for row in rows}
    snapshot_path = ROOT / 'evidence/verification/cohort112-before-adoption-20261101.json'
    selected = read_json(snapshot_path)['selected']
    reports, used, physical, failures = {}, {}, defaultdict(set), []
    eligible_sources = {row['source'] for row in rows if any(processor == 'arm9' and not program
        for processor, program, module in row['scopes'])}
    source_records = defaultdict(list)
    for entry in selected:
        if entry['source'] in eligible_sources:
            source_records[entry['source']].append(entry)
    providers, bindings = defaultdict(set), defaultdict(lambda: defaultdict(set))
    for source, records in source_records.items():
        context = sources[source]
        for selected_entry in records:
            report_name = selected_entry['report']
            if report_name not in reports:
                raw_report = (ROOT / report_name).read_bytes()
                reports[report_name] = json.loads(raw_report)
                used[report_name] = hashlib.sha256(raw_report).hexdigest()
            report = reports[report_name]
            candidates = report.get('matches', report.get('functionMatches', []))
            if not isinstance(candidates, list):
                continue
            for entry in candidates:
                if entry.get('source', report.get('source')) != source or entry.get('sourceSha256', report.get('sourceSha256')) != selected_entry['sourceSha256']:
                    continue
                row = dict(report, **entry)
                key = selected_entry['key']
                if row.get('program') or row.get('processor', 'arm9') != 'arm9':
                    continue
                if row.get('module') != key[0] or row.get('mode', 'arm') != key[1] or number(row.get('address')) != number(key[2]):
                    continue
                emitted = '_' + row.get('name', '')
                if emitted not in context['functionDefinitions']:
                    continue
                identity = ('arm9', row['module'], row.get('mode', 'arm'), number(row['address']))
                providers[identity].add((source, emitted))
                try:
                    qualified = qualified_bindings(row)
                except Exception as error:
                    failures.append(dict(source=source, address=row['address'], reason=repr(error)))
                    continue
                for name, target in qualified.items():
                    if target['kind'] == 'function':
                        bindings[source]['_' + name].add((target['processor'], target['module'], target['mode'], number(target['address'])))
    consumers = defaultdict(list)
    for source in sorted(eligible_sources):
        context = sources[source]
        for name, declarations in context['externalDeclarations'].items():
            if name in context['functionDefinitions']:
                continue
            consumers[name].append(source)
    results = []
    for name, users in sorted(consumers.items()):
        targets = set().union(*(bindings[source].get(name, set()) for source in users))
        observations = []
        reason = None
        if not targets:
            reason = 'no-qualified-ARM-function-binding'
        elif len(targets) != 1 or any(not bindings[source].get(name) for source in users):
            reason = 'ambiguous-or-incomplete-qualified-target'
        target = next(iter(targets)) if len(targets) == 1 else None
        choices = providers.get(target, set()) if target else set()
        if not reason and len(choices) != 1:
            reason = 'target-has-no-unique-compiled-C-definition'
        provider_source, provider_name = next(iter(choices)) if len(choices) == 1 else (None, None)
        provider = sources[provider_source] if provider_source else None
        provided = signature(provider['functionDefinitions'][provider_name], provider['typedefs']) if provider else None
        if not reason and provided is None:
            reason = 'provider-type-needs-aggregate-or-calling-convention-review'
        if not reason and provider_name == name:
            reason = 'already-exact-native-symbol-name'
        for source in users if not reason else []:
            context = sources[source]
            declarations = [signature(value, context['typedefs']) for value in context['externalDeclarations'][name]]
            if any(value is None or value['result'] != provided['result'] for value in declarations):
                reason = 'consumer-return-or-opaque-type-mismatch'
                break
            if any(not value['noPrototype'] and value['parameters'] != provided['parameters'] for value in declarations):
                reason = 'fixed-prototype-parameter-mismatch'
                break
            calls = [call for call in context['directCalls'] if '_' + call['targetName'] == name]
            references = [reference for reference in context['functionReferences'] if '_' + reference['targetName'] == name]
            if any(value['noPrototype'] for value in declarations) and (not calls or len(calls) != len(references)):
                reason = 'unprototyped-function-escapes-direct-call-proof'
                break
            for call in calls:
                actual = [scalar(argument['type'], context['typedefs'], parameter=True) for argument in call['arguments']]
                if len(actual) != len(provided['parameters']) or any(value is None
                        or not compatible(value, expected, argument) for value, expected, argument in
                        zip(actual, provided['parameters'], call['arguments'])):
                    reason = 'call-argument-count-or-promoted-type-mismatch'
                    break
            observations.append(dict(source=source, declarations=declarations, directCalls=len(calls), references=len(references)))
            if reason:
                break
        results.append(dict(alias=name, consumerSources=users, qualifiedTargets=[list(value) for value in sorted(targets)],
            providerSource=provider_source, providerSymbol=provider_name, providerSignature=provided,
            observations=observations, classification=reason or 'type-and-qualified-identity-candidate', aliasApplied=False))
    counts = Counter(row['classification'] for row in results)
    encoded = json.dumps(dict(aliases=results, bindingFailures=failures), sort_keys=True, separators=(',', ':')).encode()
    detail = ROOT / 'evidence/portability/windows-qualified-alias111-details-20261101.json.gz'
    detail.write_bytes(gzip.compress(encoded, mtime=0))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        catalogue=dict(path=catalogue_path.relative_to(ROOT).as_posix(), sha256=sha256(catalogue_path)),
        sourceSelection=dict(path=snapshot_path.relative_to(ROOT).as_posix(), sha256=sha256(snapshot_path)),
        measuredArmReports=[dict(path=name, sha256=digest) for name, digest in sorted(used.items())],
        classificationCounts=dict(counts), eligibleHostSources=len(eligible_sources), measuredBindingsSourceCount=len(bindings),
        bindingFailures=len(failures), sourceCredit=0, aliasesApplied=0, nativeExecutionCount=0,
        fullWindowsGameProven=False, details=dict(path=detail.relative_to(ROOT).as_posix(), sha256=sha256(detail), decodedSha256=hashlib.sha256(encoded).hexdigest()),
        limitations=['Host ARM9 source111 only; child programs and ARM7 are never rebound into this namespace',
            'Candidates require a unique native-qualified target and unique compiled C definition plus compatible primitive C call types',
            'Unprototyped calls require complete direct-call arity/promoted-type observations and no function-pointer escape',
            'Corresponding signed/unsigned argument exceptions are admitted only for observed nonnegative integer literals representable in both types',
            'Opaque aggregate types, differing return types, callbacks and incomplete bindings remain unresolved',
            'This nominates aliases only; no linker option, source edit, runtime behavior or full-game acceptance is applied'])
    write_json(ROOT / 'evidence/portability/windows-qualified-alias111-20261101.json', report)
    print(dict(classifications=dict(counts), bindingFailures=len(failures), aliasesApplied=0, sourceCredit=0))


if __name__ == '__main__':
    main()
