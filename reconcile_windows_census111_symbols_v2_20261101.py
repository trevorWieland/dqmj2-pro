import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256


def aliases(name):
    names = {name}
    if name.startswith('func_'):
        names.add('native_' + name[5:])
    return sorted(names | {'_' + item for item in names})


def main():
    original_path = ROOT / 'evidence/portability/windows-source-census111-20261101.json'
    original = read_json(original_path)
    assert original['state'] == 'completed'
    assert sha256(ROOT / original['snapshot']) == original['snapshotSha256']
    snapshot = read_json(ROOT / original['snapshot'])
    groups = {}
    for row in snapshot['functions']:
        groups.setdefault(row['source'], []).append(row)
    detail_path = ROOT / original['details']['path']
    assert sha256(detail_path) == original['details']['sha256']
    raw = gzip.decompress(detail_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == original['details']['decodedSha256']
    detail = json.loads(raw)
    assert '_native_arm7_main_027e54e8' in aliases('func_arm7_main_027e54e8')
    assert '_native_arm7_main_027e54e8' not in aliases('func_main_0badf00d')
    missing_units = []
    all_present = 0
    instances_present = 0
    for row in detail['results']:
        if not row['compiled']:
            continue
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        symbols = set(row['emittedExternalFunctionSymbols'])
        expected = groups[row['source']]
        resolved = []
        missing = []
        for entry in expected:
            matches = sorted(symbols.intersection(aliases(entry['name'])))
            if matches:
                resolved.append(dict(ledgerName=entry['name'], processor=entry['processor'],
                    program=entry['program'], module=entry['module'], mode=entry['mode'], address=entry['address'],
                    emittedSymbols=matches))
            else:
                missing.append(entry['name'])
        row['originalUnresolvedLedgerNames'] = row['selectedSymbolsMissing']
        row['resolvedSelectedAliases'] = resolved
        row['selectedSymbolsMissing'] = sorted(set(missing))
        row['selectedSymbolsPresent'] = len(resolved)
        instances_present += len(resolved)
        if missing:
            missing_units.append(dict(source=row['source'], missingNames=sorted(set(missing))))
        else:
            all_present += 1
    output_raw = json.dumps(detail, sort_keys=True, separators=(',', ':')).encode()
    output_detail = ROOT / 'evidence/portability/windows-source-census111-v2-details-20261101.json.gz'
    output_detail.write_bytes(gzip.compress(output_raw, mtime=0))
    report = dict(original, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        originalCensus=dict(path=original_path.relative_to(ROOT).as_posix(), sha256=sha256(original_path)),
        ledgerAliasRule='func_<qualified identity> maps to source native_<qualified identity>; optional i686 external underscore',
        aliasNegativeControlsPassed=True, originalObjectHashesIndependentlyRechecked=True,
        recompiledSources=0, unitsWithAllExpectedEntrySymbols=all_present,
        selectedInstancesWithEmittedEntrySymbols=instances_present,
        selectedSymbolOmissions=len(missing_units), unresolvedEntrySymbolUnits=missing_units,
        details=dict(path=output_detail.relative_to(ROOT).as_posix(), sha256=sha256(output_detail),
            decodedSha256=hashlib.sha256(output_raw).hexdigest()),
        sourceCredit=0, nativeExecutionCount=0, fullNativeLinkProven=False, fullWindowsGameProven=False)
    report['limitations'] = original['limitations'] + [
        'V1 unresolved counts compared ledger func aliases directly with source native aliases; V2 resolves that naming convention without changing code or recompiling',
        'COFF definition presence does not prove argument/return compatibility, control behavior or whole-game completion']
    output = ROOT / 'evidence/portability/windows-source-census111-v2-20261101.json'
    write_json(output, report)
    print(dict(compiled=report['compiled'], failed=report['failed'], allExpectedSymbols=all_present,
        emittedSelectedInstances=instances_present, unresolvedUnits=len(missing_units), sourceCredit=0))


if __name__ == '__main__':
    main()
