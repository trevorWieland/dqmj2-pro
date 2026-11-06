from project import ROOT, read_json, write_json, sha256


def main():
    directory = ROOT / 'evidence/lanes/parallel-wave20261106/http-explicit-interfaces'
    ready = directory / 'ready.json'
    assert not ready.exists()
    report_name = 'evidence/matches/http-explicit-interfaces-20261106.json'
    report = read_json(ROOT / report_name)
    copied = read_json(directory / 'copied-root-controls.json')
    assert copied['passed'] and copied['freshMigratedCallers'] == 5
    assert copied['originalReportSha256'] == sha256(ROOT / report_name)
    assert report['allPassed'] and len(report['matches']) == 5
    assert report['newFunctionCredit'] == report['newByteCredit'] == 0
    files = {pin['path']: pin['sha256'] for pin in copied['copiedInputs']}
    for name, digest in files.items():
        assert sha256(ROOT / name) == digest
    for name in ['verify_http_explicit_interfaces_copy_20261106.py', 'freeze_http_explicit_interfaces_20261106.py']:
        files[name] = sha256(ROOT / name)
    comparisons = [name for name in files if name.startswith(('extract/', 'tools/', 'deps/native/'))]
    for label, name in [('initial-diagnostic-label-assertion', 'logs/integration/http-explicit-interfaces-primary-proof-20261106.txt'),
                        ('recorded-generic-diagnostic', 'logs/integration/http-explicit-interfaces-negative-diagnostic-20261106.txt')]:
        data = (ROOT / name).read_bytes()
        write_json(directory / (label + '.json'), dict(sourceCredit=0, path=name, sha256=sha256(ROOT / name),
            exactUtf8Text=data.decode('utf-8'), role='Unsuccessful private diagnostic-label assertion before qualification; no frozen or accepted inputs changed.'))
    manifest = directory / 'source-files.json'
    write_json(manifest, dict(sourceCredit=0, files=[dict(path=name, sha256=digest) for name, digest in sorted(files.items())],
        privateComparisonOrToolInputs=[dict(path=name, sha256=files[name]) for name in sorted(comparisons)],
        noOriginalRomSaveOrCachedObjectsNeeded=True))
    write_json(ready, dict(schemaVersion=1, status='ready-for-zero-byte-explicit-interface-migration',
        report=report_name, producer=['match_http_explicit_interfaces_20261106.py'], sourceCredit=0,
        newFunctionCredit=0, newByteCredit=0, migrationFunctions=5, preservedFunctionBytes=report['matchedBytes'],
        sourceManifest=manifest.relative_to(ROOT).as_posix(), sourceManifestSha256=sha256(manifest),
        migrations=[dict(program='', processor='arm9', module='main', mode=row['mode'], address=row['address'],
                         bytes=row['bytes'], reason='Replace implicit HTTP declaration with measured explicit callee and entry prototypes; complete native function bytes, relocations and original source body remain identical.')
                    for row in report['matches']],
        freshOriginalAndExplicitViewsCompiledAndLinked=True, strictPrototypeDiagnosticControls=5,
        freshCopiedRootMigratedCallers=5, copiedRootTamperControls=2,
        originalFrozenSourcesHeadersInputsAndReadyUnchanged=True,
        requiredPredecessor=166, limits=[
            'Use only through the explicit source-preference migration path after these callers are accepted.',
            'No ordinary additive intake, new function/byte credit or new caller-model executions.',
            'Full original shared gates and committed closure remain mandatory.',
            'The separate strncpy declaration and unused-field clarification remain independent work.']))
    print(dict(ready=True, migrationFunctions=5, preservedBytes=report['matchedBytes'], newByteCredit=0,
               readySha256=sha256(ready), frozenPaths=len(files)))


if __name__ == '__main__':
    main()
