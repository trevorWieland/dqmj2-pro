from project import ROOT, read_json, write_json, sha256


def main():
    directory = ROOT / 'evidence/lanes/parallel-wave20261106/http-explicit-strncpy'
    ready = directory / 'ready.json'
    assert not ready.exists()
    report_name = 'evidence/matches/http-explicit-strncpy-20261106.json'
    report = read_json(ROOT / report_name)
    copied = read_json(directory / 'copied-root-controls.json')
    assert copied['passed'] and copied['freshMigratedCallers'] == 1
    assert copied['originalReportSha256'] == sha256(ROOT / report_name)
    assert report['allPassed'] and len(report['matches']) == 1
    assert report['newFunctionCredit'] == report['newByteCredit'] == 0
    files = {pin['path']: pin['sha256'] for pin in copied['copiedInputs']}
    for name, digest in files.items():
        assert sha256(ROOT / name) == digest
    for name in ['verify_http_explicit_strncpy_copy_20261106.py', 'freeze_http_explicit_strncpy_20261106.py']:
        files[name] = sha256(ROOT / name)
    manifest = directory / 'source-files.json'
    write_json(manifest, dict(sourceCredit=0, files=[dict(path=name, sha256=digest) for name, digest in sorted(files.items())],
        privateComparisonOrToolInputs=[dict(path=name, sha256=files[name]) for name in sorted(files)
                                       if name.startswith(('extract/', 'tools/', 'deps/native/'))],
        noOriginalRomSaveOrCachedObjectsNeeded=True))
    row = report['matches'][0]
    write_json(ready, dict(schemaVersion=1, status='ready-for-zero-byte-explicit-library-interface-migration',
        report=report_name, producer=['match_http_explicit_strncpy_20261106.py'], sourceCredit=0,
        newFunctionCredit=0, newByteCredit=0, migrationFunctions=1, preservedFunctionBytes=row['bytes'],
        sourceManifest=manifest.relative_to(ROOT).as_posix(), sourceManifestSha256=sha256(manifest),
        migrations=[dict(program='', processor='arm9', module='main', mode=row['mode'], address=row['address'],
                         bytes=row['bytes'], reason='Replace implicit strncpy declaration with explicit standard-header convention and measured three-word ABI; caller ignores returned R0 and all native bytes/relocations remain identical.')],
        freshOriginalAndExplicitViewsCompiledAndLinked=True, strictPrototypeDiagnosticControls=1,
        freshCopiedRootMigratedCallers=1, copiedRootTamperControls=2,
        originalFrozenSourcesHeadersInputsAndReadyUnchanged=True, requiredPredecessor=166,
        limits=['Only for explicit zero-byte source-preference migration after original caller acceptance.',
                'No new function/byte credit, new caller-model execution, callee-body proof or unique original formal return type proof.',
                'Full original shared gates and committed closure remain required.']))
    print(dict(ready=True, migrationFunctions=1, preservedBytes=row['bytes'], newByteCredit=0,
               readySha256=sha256(ready), frozenPaths=len(files)))


if __name__ == '__main__':
    main()
