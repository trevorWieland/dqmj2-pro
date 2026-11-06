import gzip
import hashlib
import json
import subprocess
from collections import Counter
from project import ROOT, read_json, write_json, sha256


REVISION = '9e6aea5ee032dd24a884041a098b669534d88629'
CENSUS = 'evidence/portability/windows-source-census168-targetabi-v1-20261101.json'


def address(value):
    return int(value, 0) if isinstance(value, str) else value


def identity(row, parent=None):
    parent = parent or {}
    return (row.get('program', parent.get('program')) or '', row.get('processor', parent.get('processor', 'arm9')),
        row.get('module', parent.get('module')), row.get('mode', parent.get('mode')), address(row.get('address')))


def main():
    census = read_json(ROOT / CENSUS)
    assert census['state'] == 'completed' and census['sourceUnits'] == 10559
    assert sha256(ROOT / census['snapshot']) == census['snapshotSha256']
    detail_name = census['details']['path']
    assert sha256(ROOT / detail_name) == census['details']['sha256']
    raw = gzip.decompress((ROOT / detail_name).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == census['details']['decodedSha256']
    detail = json.loads(raw)
    snapshot = read_json(ROOT / census['snapshot'])
    ledger_raw = subprocess.check_output(['git', 'show', REVISION + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = {identity(row): row for line in ledger_raw.splitlines() if
        (row := json.loads(line))['states']['functionMatched']}
    grouped = {}
    for entry in snapshot['functions']:
        record = ledger[identity(entry)]
        assert record['sourceUnit'] == entry['source'] and record['sourceSha256'] == entry['sourceSha256']
        grouped.setdefault(entry['source'], []).append(entry)
    reports, report_pins, resolved, remaining = {}, {}, [], []
    for row in detail['results']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        if not row['compiled']:
            continue
        assert sha256(ROOT / row['object']) == row['objectSha256']
        missing = set(row['selectedSymbolsMissing'])
        if not missing:
            continue
        symbols = set(row['emittedExternalFunctionSymbols'])
        additions = []
        for entry in grouped[row['source']]:
            if entry['name'] not in missing:
                continue
            selected = ledger[identity(entry)]
            name = selected['evidence']
            assert isinstance(name, str)
            if name not in reports:
                report_raw = subprocess.check_output(['git', 'show', REVISION + ':' + name], cwd=ROOT)
                reports[name] = json.loads(report_raw)
                report_pins[name] = hashlib.sha256(report_raw).hexdigest()
            report = reports[name]
            matches = report.get('matches', report.get('functionMatches', []))
            candidates = []
            for matched in matches:
                if identity(matched, report) != identity(entry):
                    continue
                if matched.get('source', report.get('source')) != row['source']:
                    continue
                if matched.get('sourceSha256', report.get('sourceSha256')) != row['sourceSha256']:
                    continue
                if matched.get('bytes', matched.get('size')) != entry['bytes']:
                    continue
                actual_name = matched['name']
                emitted = sorted(symbols & {actual_name, '_' + actual_name})
                if emitted:
                    candidates.append((actual_name, emitted))
            if len({item[0] for item in candidates}) == 1:
                actual_name, emitted = candidates[0]
                missing.remove(entry['name'])
                additions.append(dict(identity=list(identity(entry)), bytes=entry['bytes'],
                    ledgerName=entry['name'], actualAcceptedSourceName=actual_name, emittedCoffNames=emitted,
                    committedArmReport=dict(path=name, sha256=report_pins[name]),
                    fullProgramProcessorModuleModeAddressSourceHashAndExtentMatched=True))
        row['priorSelectedSymbolsMissing'] = row['selectedSymbolsMissing']
        row['selectedSymbolsMissing'] = sorted(missing)
        row['strictCommittedArmSymbolResolutions'] = additions
        resolved.extend(additions)
        if missing:
            remaining.append(dict(source=row['source'], ledgerNames=sorted(missing),
                emittedExternalFunctionSymbols=row['emittedExternalFunctionSymbols']))
    failures = Counter()
    for row in detail['results']:
        if row['compiled']:
            continue
        stderr = row.get('stderr', '')
        if '[-Wint-conversion]' in stderr:
            kind = 'pointer-word-type-conversion'
        elif 'conflicting types' in stderr or 'incompatible function pointer' in stderr:
            kind = 'function-type-conflict'
        elif 'undeclared identifier' in stderr or 'unknown type name' in stderr:
            kind = 'missing-type-or-declaration'
        else:
            kind = row['diagnosticClass']
        row['refinedDiagnosticClass'] = kind
        failures[kind] += 1
    output_raw = json.dumps(detail, sort_keys=True, separators=(',', ':')).encode()
    output_detail = 'evidence/portability/windows-source-census168-symbols-v1-details-20261106.json.gz'
    (ROOT / output_detail).write_bytes(gzip.compress(output_raw, mtime=0))
    result = dict(passed=True, sourceCredit=0, acceptedCohort=168, sourceRevision=REVISION,
        originalCensus=dict(path=CENSUS, sha256=sha256(ROOT / CENSUS)),
        committedLedgerSha256=hashlib.sha256(ledger_raw).hexdigest(),
        rawCompiledUnits=census['compiled'], rawCompilerFailures=census['failed'],
        priorSymbolOmissionUnits=census['selectedSymbolOmissions'], additionalExactSourceSymbolMappings=resolved,
        remainingSymbolOmissionUnits=len(remaining), unresolvedEntrySymbolUnits=remaining,
        refinedCompilerFailureClasses=dict(failures),
        details=dict(path=output_detail, sha256=sha256(ROOT / output_detail), decodedSha256=hashlib.sha256(output_raw).hexdigest()),
        checkedCommittedArmReports=[dict(path=name, sha256=digest) for name, digest in sorted(report_pins.items())],
        existingInitialSymbolMappingsUnchanged=True, recompiledSources=0, newAliasesOrDefinitions=0,
        fullNativeLinkProven=False, fullWindowsGameProven=False, nativeExecutionCount=0,
        limits=['Additional names require exact committed ARM report identity across program/CPU/module/mode/address/source hash/extent.',
            'Original direct/address-suffix mappings remain compilation observations; this does not validate a full native game symbol graph.',
            'No compiler diagnostic was suppressed and no production source was changed.'], generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/portability/windows-source-census168-symbols-v1-20261106.json', result)
    print(dict(passed=True, compiled=census['compiled'], failed=census['failed'],
        extraExactMappings=len(resolved), remainingSymbolOmissionUnits=len(remaining), failureClasses=dict(failures)))


if __name__ == '__main__':
    main()
