from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from replay_initialized_data_packet_20261106 import projection


def main():
    directory = ROOT / 'evidence/lanes/parallel-wave20261106/sdk-sound-data'
    assert not (directory / 'ready.json').exists()
    report_name = 'evidence/data/sdk-sound-data-20261106.json'
    report = read_json(ROOT / report_name)
    copied = read_json(directory / 'copied-root-controls.json')
    accounting = read_json(ROOT / 'evidence/verification/sdk-sound-data-accounting-controls-20261106.json')
    module_proof = read_json(ROOT / 'evidence/verification/sdk-sound-data-complete-module-preflight-20261106.json')
    assert copied['passed'] and accounting['passed'] and module_proof['passed']
    assert copied['originalReportSha256'] == accounting['originalReportSha256'] == sha256(ROOT / report_name)
    assert accounting['qualifierSha256'] == sha256(ROOT / 'qualify_sdk_sound_data_additions_20261106.py')
    assert len(report['dataMatches']) == 6 and report['dataMatchedBytes'] == 3752 and report['functionMatched'] == 0
    assert module_proof['sourceObjects'] == 6 and module_proof['completeModuleBytesAndSymbolsExact']
    files = set(code_closure(['match_sdk_sound_data_20261106.py', 'replay_initialized_data_packet_20261106.py']))
    for row in report['dataMatches']:
        files.add(row['source'])
        files.update(pin['path'] for pin in row['sourceDependencies'])
    files.update(['qualify_sdk_sound_data_additions_20261106.py', 'verify_sdk_sound_data_copy_20261106.py',
                  'verify_sdk_sound_data_accounting_20261106.py'])
    files.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'deps/native/elftools').rglob('*.py'))
    files.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'tools/mwccarm/mwccarm/2.0/base').iterdir()
                 if path.suffix.lower() in ('.exe', '.dll'))
    files.add('tools/mwccarm/mwccarm/license.dat')
    private = sorted({row['binary'] for row in report['dataMatches']})
    manifest = directory / 'source-files.json'
    write_json(manifest, dict(sourceCredit=0, files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(files)],
        privateComparisonInputs=[dict(path=name, sha256=sha256(ROOT / name)) for name in private],
        sourceGenerationUsesOnlyCanonicalTypedJson=True, noRomOrPublishedSdkSourceRequiredForGeneration=True))
    canonical_report = 'evidence/matches/sdk-sound-data-canonical-20261106.json'
    descriptor = 'provenance/sdk-sound-data-canonical-transport-20261106.json'
    ready_path = directory / 'ready.json'
    write_json(ready_path, dict(status='ready-for-coordinator-initialized-data-acceptance', sourceCredit=0,
        report=report_name, producer=['match_sdk_sound_data_20261106.py'], functionCount=0, dataObjects=6,
        initializedBytes=3752, typedConstantDataBytes=3752, encodedAssetBytes=0, measuredZeroAlignmentBytes=0,
        sourceManifest=manifest.relative_to(ROOT).as_posix(), sourceManifestSha256=sha256(manifest),
        canonicalReport=canonical_report, canonicalProducer=['replay_initialized_data_packet_20261106.py', descriptor],
        claim=(directory / 'data-claim.json').relative_to(ROOT).as_posix(), claimSha256=sha256(directory / 'data-claim.json'),
        freshCopiedRootObjects=6, wrongDataObjects=6, accountingControls=8, copiedRootTamperControls=5,
        completeModuleComparisons=2, executableBytes=0, limitations=[
            'Shared acceptance and committed closure remain required.',
            'SDK sound lookup data adds zero function, native audio execution or game completion credit.']))
    write_json(ROOT / descriptor, dict(sourceCredit=0, transportOnly=True,
        ready=ready_path.relative_to(ROOT).as_posix(), readySha256=sha256(ready_path), originalReport=report_name,
        originalProducer=['match_sdk_sound_data_20261106.py'], output=canonical_report,
        immutableDataProjection=projection(report)))
    print(dict(ready=True, dataObjects=6, initializedBytes=3752, sourceCredit=0,
               readySha256=sha256(ready_path), frozenFiles=len(files), canonicalDescriptor=descriptor))


if __name__ == '__main__':
    main()
