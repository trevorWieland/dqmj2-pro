import hashlib
import subprocess
from project import ROOT, read_json, sha256, write_json
from recovery_registry import batches, verify_sources


def main(cohort, preferences_only=False):
    verify_sources()
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    paths, dependencies = {}, {}
    for batch in ([] if preferences_only else batches()):
        for path, expected in batch['sourceHashes'].items():
            canonical = path.replace('\\', '/')
            if canonical.split('/')[0] in ['tools', 'deps', 'inputs']:
                dependencies[canonical] = expected
                continue
            if canonical in paths and paths[canonical] != expected:
                raise ValueError('Conflicting registered source hashes:' + canonical)
            if '\n' in canonical or '\r' in canonical:
                raise ValueError('Invalid registered source pathname')
            paths[canonical] = expected
    batch_path_count = len(paths)
    from source_selection import preferences
    from project import configuration
    policies = preferences(configuration()['romSha256'])
    preference_files = {'source-preferences.json': sha256(ROOT / 'source-preferences.json')}
    for preference in policies.values():
        preference_files[preference['evidence']] = preference['evidenceSha256']
        migration = read_json(ROOT / preference['evidence'])
        for version in [migration['previous'], migration['preferred']]:
            preference_files[version['source']] = version['sourceSha256']
            preference_files[version['report']] = sha256(ROOT / version['report'])
    for path, expected in preference_files.items():
        canonical = path.replace('\\', '/')
        if canonical in paths and paths[canonical] != expected:
            raise ValueError('Conflicting preference source hash:' + canonical)
        paths[canonical] = expected
    names = sorted(paths)
    query = ''.join(revision + ':' + path + '\n' for path in names).encode()
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=query, capture_output=True, check=True)
    offset, missing, mismatch = 0, [], []
    for path in names:
        end = result.stdout.index(b'\n', offset)
        header = result.stdout[offset:end].decode()
        offset = end + 1
        if header.endswith(' missing'):
            missing.append(path)
            continue
        object_id, kind, length = header.split()
        if kind != 'blob':
            raise ValueError('Registered source is not a Git blob:' + path)
        length = int(length)
        payload = result.stdout[offset:offset + length]
        offset += length + 1
        if hashlib.sha256(payload).hexdigest() != paths[path]:
            mismatch.append(path)
    assert offset == len(result.stdout)
    report = {'schemaVersion': 1, 'commit': revision, 'registeredRepositoryPathsChecked': len(paths),
              'registeredBatchSourcePathsChecked': batch_path_count, 'sourcePreferenceRowsChecked': len(policies),
              'preferencesOnly': preferences_only, 'explicitCopiedDependencyPaths': len(dependencies), 'windowsPathSeparatorsNormalized': True,
              'missingRegisteredSourcePaths': missing, 'sourceHashMismatches': mismatch,
              'passed': not missing and not mismatch, 'sourceBytesOrCoverageAdded': 0,
              'generator': 'verify_committed_source_closure_20261030.py',
              'generatorSha256': sha256(ROOT / 'verify_committed_source_closure_20261030.py'),
              'limitations': ['Checks committed registered-source bytes, not a fresh build or all external binary dependencies']}
    output = 'source-preferences-committed-closure-20261030.json' if preferences_only else f'cohort{cohort}-committed-source-closure-20261030.json'
    write_json(ROOT / 'evidence/verification' / output, report)
    print({k: report[k] for k in ['registeredRepositoryPathsChecked', 'explicitCopiedDependencyPaths', 'passed', 'missingRegisteredSourcePaths', 'sourceHashMismatches']})
    assert report['passed']


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, default=62)
    parser.add_argument('--preferences-only', action='store_true')
    options = parser.parse_args()
    main(options.cohort, options.preferences_only)
