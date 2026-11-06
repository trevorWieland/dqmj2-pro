import sys
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def main():
    directory = ROOT / 'evidence/lanes/parallel-wave20261105/child-message-data'
    assert not (directory / 'ready.json').exists()
    report_name = 'evidence/data/child-message-semantic-20261106.json'
    report = read_json(ROOT / report_name)
    copied = read_json(directory / 'copied-root-controls.json')
    accounting = read_json(ROOT / 'evidence/verification/child-message-data-accounting-preflight-20261106.json')
    controls = read_json(ROOT / 'evidence/verification/child-message-data-accounting-controls-20261106.json')
    assert copied['passed'] and accounting['passed'] and controls['passed']
    assert copied['originalReportSha256'] == sha256(ROOT / report_name)
    assert report['dataMatchedBytes'] == 3808 and report['functionMatched'] == 0 and len(report['dataMatches']) == 8
    files = set(code_closure(['match_child_message_data_20261106.py']))
    for row in report['dataMatches']:
        files.add(row['source'])
        files.update(pin['path'] for pin in row['sourceDependencies'])
    files.update(['qualify_child_message_data_additions_20261106.py', 'prepare_source_data_cohort_v5_20261106.py',
                  'verify_child_message_data_copy_20261106.py', 'run_next_source_package_v23_20261106.py'])
    for package in ['ndspy', 'elftools']:
        files.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'deps/native' / package).rglob('*.py'))
    files.update(['tools/mwccarm/mwccarm/2.0/base/mwccarm.exe', 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe',
                  'tools/mwccarm/mwccarm/license.dat'])
    manifest = directory / 'source-files.json'
    layout = read_json(ROOT / 'src/utility/parallel_wave20261105/child-message-data/layout.json')
    write_json(manifest, dict(sourceCredit=0, files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(files)],
        privateComparisonInputs=[dict(path=name, sha256=sha256(ROOT / name)) for name in
                                 ['extract/files/dwc/utility.bin', layout['binary']]],
        noExecutablePayloadsCommitted=True, pythonVersion=sys.version))
    write_json(directory / 'ready.json', dict(status='ready-for-coordinator-initialized-data-acceptance', sourceCredit=0,
        report=report_name, producer=['match_child_message_data_20261106.py'], functionCount=0, dataObjects=8,
        initializedBytes=3808, encodedAssetBytes=3799, measuredZeroAlignmentBytes=9,
        sourceManifest=manifest.relative_to(ROOT).as_posix(), sourceManifestSha256=sha256(manifest),
        freshCopiedRootObjects=8, accountingControls=7, wrongDataObjects=8,
        generationOriginalReadRejections=2, executableBytes=0,
        limitations=['Shared acceptance and committed closure are pending.',
                    'Semantic asset data and measured alignment are separate from function and executable-byte accounting.']))
    print(dict(ready=True, dataObjects=8, initializedBytes=3808, sourceCredit=0,
               readySha256=sha256(directory / 'ready.json')))


if __name__ == '__main__':
    main()
