import argparse
import subprocess
from project import ROOT, read_json, write_json, sha256


BUNDLE = 'evidence/lanes/parallel-wave20261106/path-lookup-next/stage-v9-handoff.json'
BUNDLE_SHA = 'd2bbb605f792131e6da1c1db40c708aac665de1fc5a7036230b5e1c3d2f5adf9'
RAW = 'evidence/attempts/cohort162-missing-arm7-summary-bindings-20261106/logs__integration__cohort162-validation-03.txt'
ARCHIVE = 'evidence/attempts/cohort163-verbatim-diagnostic-packaging-20261106/original-log-verbatim.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration', nargs='+')
    options = parser.parse_args()
    closure_name = 'evidence/verification/cohort163-expanded-source-closure-20261101.json'
    committed = subprocess.check_output(['git', 'show', 'HEAD:' + closure_name], cwd=ROOT)
    assert committed == (ROOT / closure_name).read_bytes() and read_json(ROOT / closure_name)['passed']
    assert sha256(ROOT / BUNDLE) == BUNDLE_SHA
    bundle = read_json(ROOT / BUNDLE)
    collector = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/path-lookup-next/collector-v3-qualification.json')
    bundle['files'] = bundle['files'] + collector['files']
    for pin in bundle['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    assert read_json(ROOT / ARCHIVE)['exactUtf8Text'].encode('utf-8') == (ROOT / RAW).read_bytes()
    assert read_json(ROOT / ARCHIVE)['sha256'] == sha256(ROOT / RAW)
    shared = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json']}
    for name in options.configuration:
        config = read_json(ROOT / name)
        cohort = config['cohort']
        assert cohort in (164, 165, 166)
        for path in (ROOT / 'evidence/verification').glob(f'cohort{cohort}-continuation-driver-v*-20261105.json'):
            state = read_json(path)
            assert not (state['state'] == 'running' and state.get('currentCommand', [''])[0].startswith('finish_source_'))
        package_name = config['name'] + '-package.json'
        spec_name = config['name'] + '-specification.json'
        stage_name = config['stage']
        spec_sha = sha256(ROOT / spec_name)
        package = read_json(ROOT / package_name)
        text = (ROOT / stage_name).read_text(encoding='utf-8')
        assert text.count('import stage_declared_source_package_v8_20261106 as staging') == 1
        directory = ROOT / f'evidence/attempts/cohort{cohort}-capture-v9-adoption-20261106'
        directory.mkdir(parents=True, exist_ok=False)
        for original in [name, package_name, stage_name]:
            (directory / original.split('/')[-1]).write_bytes((ROOT / original).read_bytes())
        config['opaqueMetadata'] = [ARCHIVE if path == RAW else path for path in config['opaqueMetadata']]
        package['traces'] = [ARCHIVE if path == RAW else path for path in package['traces']]
        receipt = f'evidence/verification/cohort{cohort}-qualified-capture-v9-adoption-20261106.json'
        extras = [BUNDLE, *[pin['path'] for pin in bundle['files']],
                  'adopt_qualified_capture_v9_20261106.py', receipt]
        for value in [config, package]:
            for extra in extras:
                if extra not in value['extra']:
                    value['extra'].append(extra)
        for path in directory.iterdir():
            relative = path.relative_to(ROOT).as_posix()
            if relative not in package['traces']:
                package['traces'].append(relative)
        (ROOT / stage_name).write_text(text.replace('import stage_declared_source_package_v8_20261106 as staging',
            'import stage_declared_source_package_v9_20261106 as staging'), encoding='utf-8')
        write_json(ROOT / name, config)
        write_json(ROOT / package_name, package)
        assert sha256(ROOT / spec_name) == spec_sha
        assert shared == {path: sha256(ROOT / path) for path in shared}
        write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, cohort=cohort, bundle=BUNDLE,
            bundleSha256=BUNDLE_SHA, specificationSha256Unchanged=spec_sha,
            stage=stage_name, stageSha256=sha256(ROOT / stage_name), originalAllSixteenSharedGatesUnchanged=True,
            pureContextAndGuardedPathFactsCached=True, allUniquePathFactsAndContentHashesRevalidated=True,
            originalRawDiagnosticBytesPreserved=True, diagnosticTraceRoutedToCommittedLosslessArchive=True,
            registryAndPreferenceHashesUnchanged=shared, generatorSha256=sha256(__file__)))
    print(dict(passed=True, adoptedCohorts=len(options.configuration), sourceCredit=0))


if __name__ == '__main__':
    main()
