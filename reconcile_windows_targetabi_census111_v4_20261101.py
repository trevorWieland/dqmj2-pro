import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def main():
    path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v2-20261101.json'
    base = read_json(path)
    assert base['state'] == 'completed'
    snapshot = read_json(ROOT / base['snapshot'])
    assert sha256(ROOT / base['snapshot']) == base['snapshotSha256']
    detail_path = ROOT / base['details']['path']
    assert sha256(detail_path) == base['details']['sha256']
    raw = gzip.decompress(detail_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == base['details']['decodedSha256']
    detail = json.loads(raw)
    before_path = ROOT / 'evidence/verification/cohort112-before-adoption-20261101.json'
    selected = read_json(before_path)['selected']
    wanted = {}
    for entry in snapshot['functions']:
        wanted.setdefault(entry['source'], []).append(entry)
    report_cache = {}
    used_reports = {}
    resolved_units = 0
    resolved_instances = 0
    unresolved = []
    for row in detail['results']:
        if not row['compiled']:
            continue
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        symbols = set(row['emittedExternalFunctionSymbols'])
        missing = set(row['selectedSymbolsMissing'])
        row['priorUnresolvedLedgerNames'] = sorted(missing)
        additional = []
        for entry in wanted[row['source']]:
            if entry['name'] not in missing:
                continue
            records = [record for record in selected if record['source'] == row['source']
                and record['sourceSha256'] == row['sourceSha256']]
            candidates = []
            for record in records:
                report_name = record['report']
                if report_name not in report_cache:
                    report_cache[report_name] = read_json(ROOT / report_name)
                report = report_cache[report_name]
                for matched in report.get('matches', []) + report.get('functionMatches', []):
                    same_alias = matched.get('nativeAlias') == entry['name']
                    same_address = number(matched.get('address')) == number(entry['address'])
                    if not same_alias and not same_address:
                        continue
                    if matched.get('source', report.get('source')) != row['source']:
                        continue
                    if matched.get('sourceSha256', report.get('sourceSha256')) != row['sourceSha256']:
                        continue
                    name = matched['name']
                    emitted = sorted(symbols.intersection({name, '_' + name}))
                    if emitted:
                        candidates.append((name, emitted, report_name))
            unique_names = {name for name, emitted, report_name in candidates}
            if len(unique_names) == 1:
                missing.remove(entry['name'])
                for name, emitted, report_name in candidates:
                    used_reports[report_name] = sha256(ROOT / report_name)
                name, emitted, report_name = candidates[0]
                additional.append(dict(ledgerName=entry['name'], actualSourceName=name,
                    emittedSymbols=emitted, matchingArmReport=report_name,
                    processor=entry['processor'], program=entry['program'], module=entry['module'],
                    mode=entry['mode'], address=entry['address']))
        row['acceptedArmSymbolResolutions'] = additional
        row['selectedSymbolsMissing'] = sorted(missing)
        present = sum(entry['name'] not in missing for entry in wanted[row['source']])
        row['selectedSymbolsPresent'] = present
        resolved_instances += present
        if missing:
            unresolved.append(dict(source=row['source'], ledgerNames=sorted(missing),
                emittedExternalFunctionSymbols=row['emittedExternalFunctionSymbols']))
        else:
            resolved_units += 1
    diagnostic_classes = {}
    for row in detail['results']:
        if row['compiled']:
            continue
        text = (ROOT / row['source']).read_text(encoding='utf-8')
        if 'asm {' in text or 'asm u32 ' in text:
            row['diagnosticClass'] = 'target-register-or-cache-assembly'
        elif '[-Wint-conversion]' in row.get('stderr', ''):
            row['diagnosticClass'] = 'explicit-pointer-word-conversion-required'
        diagnostic_classes[row['diagnosticClass']] = diagnostic_classes.get(row['diagnosticClass'], 0) + 1
    output_raw = json.dumps(detail, sort_keys=True, separators=(',', ':')).encode()
    output_detail = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-details-20261101.json.gz'
    output_detail.write_bytes(gzip.compress(output_raw, mtime=0))
    report = dict(base, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        originalCensus=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)),
        acceptedSelection=dict(path=before_path.relative_to(ROOT).as_posix(), sha256=sha256(before_path)),
        armSymbolMetadata=[dict(path=name, sha256=digest) for name, digest in sorted(used_reports.items())],
        recompiledSources=0, unitsWithAllExpectedEntrySymbols=resolved_units,
        selectedInstancesWithEmittedEntrySymbols=resolved_instances,
        selectedSymbolOmissions=len(unresolved), unresolvedEntrySymbolUnits=unresolved, diagnosticClasses=diagnostic_classes,
        details=dict(path=output_detail.relative_to(ROOT).as_posix(), sha256=sha256(output_detail),
            decodedSha256=hashlib.sha256(output_raw).hexdigest()), sourceCredit=0, nativeExecutionCount=0,
        fullNativeLinkProven=False, fullWindowsGameProven=False)
    report['limitations'] = base['limitations'] + [
        'Public/source names are resolved only by source-hash-bound accepted ARM matching reports, never by inventing function definitions',
        'This reanalysis checks existing COFF hashes and does not execute or relink game logic']
    write_json(ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json', report)
    print(dict(compiled=base['compiled'], failed=base['failed'], unitsWithExpectedSymbols=resolved_units,
        selectedInstancesWithSymbols=resolved_instances, unresolvedUnits=len(unresolved), sourceCredit=0))


if __name__ == '__main__':
    main()
