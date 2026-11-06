import json
from project import ROOT, configuration, now, read_json, sha256, write_json, write_text
from ledger_state import collect_matches, union_size


def main():
    namespace = configuration()['romSha256']
    known, rejected = collect_matches(namespace)
    records = {}
    inputs = []
    for path in sorted((ROOT / 'evidence/nonmatching').glob('*/*.json')):
        report = read_json(path)
        for row in report.get('functions', []):
            inputs.append((path, row, row.get('source'), row.get('sourceSha256'), row.get('compileSucceeded', False), row['nativeBytes']))
    for path in sorted((ROOT / 'nonmatching/ov000/20261029-broad01/functions').glob('*/result.json')):
        row = read_json(path)
        inputs.append((path, row, row.get('source'), row.get('sourceSha256'), row.get('compiled', False), row['bytes']))
    for path, row, source, digest, compiled, size in inputs:
        address = int(row['address'], 0)
        module, mode = row['module'], row['mode'].lower()
        key = row.get('processor', 'arm9'), module, mode, address
        identity = f'{namespace}/{key[0]}/{module}/{mode}/{address:08x}'
        current = bool(source and (ROOT / source).is_file() and sha256(ROOT / source) == digest)
        implementation = {'source': str(source).replace('\\', '/') if source else None, 'sourceSha256': digest,
                          'report': path.relative_to(ROOT).as_posix(), 'reportSha256': sha256(path),
                          'sourceCurrent': current, 'compiledUnderRecordedScope': bool(compiled and current),
                          'nativeSemanticsVerified': bool(row.get('executionValidated', False)),
                          'nativeMatchingAccepted': False, 'acceptedSourceCredit': 0,
                          'knownSemanticMismatch': row.get('knownSemanticMismatch', False),
                          'matchingBytes': row.get('matchingBytes'), 'compiledBytes': row.get('compiledBytes'),
                          'compilerFlags': row.get('compilerFlags'), 'objectSha256': row.get('objectSha256'),
                          'failure': row.get('draftFailure', row.get('failure'))}
        record = records.setdefault(key, {'id': identity, 'buildSha256': namespace, 'processor': key[0], 'module': module,
                                         'mode': mode, 'address': hex(address), 'nativeBytes': size,
                                         'nativeSpanSha256': row['nativeSpanSha256'], 'implementations': []})
        if record['nativeBytes'] != size or record['nativeSpanSha256'] != row['nativeSpanSha256']:
            raise ValueError('Draft implementations disagree on qualified native extent')
        record['implementations'].append(implementation)
        record['nativeFunctionHasAcceptedImplementation'] = (module, mode, address) in known
    preferences = read_json(ROOT / 'evidence/nonmatching/preferred-implementations.json')['entries']
    for preference in preferences:
        key = preference['processor'], preference['module'], preference['mode'], int(preference['address'], 0)
        if key in records:
            records[key]['preferredSemanticHypothesis'] = preference
            for implementation in records[key]['implementations']:
                if implementation['sourceSha256'] == preference.get('rejectedOriginSourceSha256'):
                    implementation['knownSemanticMismatch'] = True
                    implementation['nativeSemanticsVerified'] = False
                    implementation['semanticRejectionEvidence'] = preference['rejectionEvidence']
    rows = []
    modules = []
    for key, record in sorted(records.items()):
        record['states'] = {'analyzed': True, 'drafted': any(row['sourceCurrent'] for row in record['implementations']),
                            'compiled': any(row['compiledUnderRecordedScope'] for row in record['implementations']),
                            'functionMatched': False, 'moduleLinked': False, 'wholeRomMatchedFromSource': False}
        rows.append(record)
    for module in sorted({row['module'] for row in rows}):
        selected = [row for row in rows if row['module'] == module]
        drafted = [row for row in selected if row['states']['drafted']]
        compiled = [row for row in selected if row['states']['compiled']]
        intervals = [(int(row['address'], 0), int(row['address'], 0) + row['nativeBytes']) for row in compiled]
        modules.append({'module': module, 'analyzedFunctions': len(selected), 'draftedFunctions': len(drafted),
                        'compiledFunctions': len(compiled), 'uniqueCompiledNativeBytes': union_size(intervals)})
    write_text(ROOT / 'ledger/drafts.jsonl', ''.join(json.dumps(row, separators=(',', ':')) + '\n' for row in rows))
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': namespace, 'modules': modules,
              'compiledFunctions': sum(row['compiledFunctions'] for row in modules),
              'compiledNativeBytes': sum(row['uniqueCompiledNativeBytes'] for row in modules),
              'draftLedgerSha256': sha256(ROOT / 'ledger/drafts.jsonl'), 'acceptedSourceCredit': 0,
              'limitations': ['Draft compilation is a recorded source/report scope, not a clean build of all nonmatching code',
                              'Native semantics, matching bytes, function boundaries and module/ROM acceptance remain independent',
                              'Generated untranslated candidates are analyzed but not counted as authored drafts',
                              'Preferred semantic hypotheses and known failures remain separate from byte-proximity ranking']}
    write_json(ROOT / 'evidence/nonmatching/progress-20261029.json', report)
    print({key: report[key] for key in ['compiledFunctions', 'compiledNativeBytes', 'acceptedSourceCredit']})


if __name__ == '__main__':
    main()
