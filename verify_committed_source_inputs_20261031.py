import argparse
import hashlib
import struct
import subprocess
from project import ROOT, configuration, read_json, write_json, sha256
from recovery_registry import batches, verify_sources
from source_selection import preferences


DERIVED = 'extract/arm7/arm7.bin'
DERIVED_SHA = '9f40087972ccb8b89d4cc4baf8288123e26a479bb43fa68b18a30a59650633a1'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    verify_sources()
    config = configuration()
    assert config['romSha256'] == ROM_SHA and sha256(config['rom']) == ROM_SHA
    rom = config['rom'].read_bytes()
    offset, size = struct.unpack_from('<I', rom, 0x30)[0], struct.unpack_from('<I', rom, 0x3C)[0]
    binary = (ROOT / DERIVED).read_bytes()
    assert offset == 0x98800 and size == 160048 and binary == rom[offset:offset + size]
    assert hashlib.sha256(binary).hexdigest() == DERIVED_SHA
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    paths, copied, derived_batches = {}, {}, []
    for batch in batches():
        for path, expected in batch['sourceHashes'].items():
            path = path.replace('\\', '/')
            if path == DERIVED:
                assert expected == DERIVED_SHA
                derived_batches.append(batch['report'])
                continue
            if path.split('/')[0] in ['tools', 'deps', 'inputs']:
                copied[path] = expected
                continue
            assert '\n' not in path and '\r' not in path
            assert path not in paths or paths[path] == expected
            paths[path] = expected
    assert derived_batches
    for report_path in derived_batches:
        report = read_json(ROOT / report_path)
        rows = report.get('matches', report.get('functionMatches', []))
        assert rows and all(row.get('processor', report.get('processor')) == 'arm7' and not row.get('program', report.get('program')) and row.get('module', report.get('module', '')).startswith('arm7-') for row in rows)
    policy = preferences(ROM_SHA)
    extra = {'source-preferences.json': sha256(ROOT / 'source-preferences.json')}
    for row in policy.values():
        extra[row['evidence']] = row['evidenceSha256']
        evidence = read_json(ROOT / row['evidence'])
        for version in [evidence['previous'], evidence['preferred']]:
            extra[version['source']] = version['sourceSha256']
            extra[version['report']] = sha256(ROOT / version['report'])
    for path, expected in extra.items():
        assert path not in paths or paths[path] == expected
        paths[path] = expected
    names = sorted(paths)
    query = ''.join(revision + ':' + path + '\n' for path in names).encode()
    raw = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=query, capture_output=True, check=True).stdout
    cursor, missing, changed = 0, [], []
    for path in names:
        end = raw.index(b'\n', cursor)
        header, cursor = raw[cursor:end].decode(), end + 1
        if header.endswith(' missing'):
            missing.append(path)
            continue
        unused, kind, length = header.split()
        length = int(length)
        assert kind == 'blob'
        payload, cursor = raw[cursor:cursor + length], cursor + length + 1
        if hashlib.sha256(payload).hexdigest() != paths[path]:
            changed.append(path)
    assert cursor == len(raw)
    report = dict(schemaVersion=1, cohort=options.cohort, commit=revision,
        registeredRepositoryPathsChecked=len(paths), explicitCopiedDependencyPaths=len(copied),
        sourcePreferenceRowsChecked=len(policy), missingRegisteredSourcePaths=missing,
        sourceHashMismatches=changed, passed=not missing and not changed,
        derivedExecutableInputs=[dict(path=DERIVED, sha256=DERIVED_SHA, bytes=size,
            romOffset=hex(offset), romSha256=ROM_SHA, independentlyRegeneratedBy='Exact ROM header ARM7 offset/size slice',
            referencedBy=derived_batches, committedAsAuthoredSource=False,
            reconstructedSourceBytes=0, reconstructedAssemblyBytes=0)],
        generator='verify_committed_source_inputs_20261031.py', generatorSha256=sha256(__file__),
        registryOrFrameworkChanged=False, sourceCredit=0,
        limitations=['Only the exact measured ARM7 physical ROM slice is classified as a derived executable input',
            'Every other registered repository path is checked byte-for-byte against the selected commit',
            'Original strict verifier failure is retained; no executable blob is committed as recovered source',
            'This packaging/input audit is not a complete fresh build or a source-only game proof'])
    write_json(ROOT / f'evidence/verification/cohort{options.cohort}-committed-source-inputs-20261031.json', report)
    print(dict(pathsChecked=len(paths), derivedExecutableInputs=1, passed=report['passed'], missing=missing, changed=changed))
    assert report['passed']


if __name__ == '__main__':
    main()
