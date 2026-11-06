import argparse
import hashlib
import struct
import subprocess
import sys
import utility_runtime
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
    sys.path.insert(0, str(ROOT / 'evidence/encounter'))
    import script_assets_20261029 as assets
    original_rom, files = assets.original_files()
    assert original_rom == rom
    start, end = files['dwc/utility.bin']
    container = rom[start:end]
    assert container == (ROOT / 'extract/files/dwc/utility.bin').read_bytes()
    assert sha256(ROOT / 'extract/files/dwc/utility.bin') == utility_runtime.INPUT_HASH
    utility_report, products = utility_runtime.derive()
    derived = {DERIVED: dict(data=binary, role='Original host ARM7 header slice', romOffset=hex(offset)),
        'extract/files/dwc/utility.bin': dict(data=container, role='Original utility archive FAT file', romOffset=hex(start))}
    for name in ['utility-child-arm7-main', 'utility-child-arm7-wram']:
        path = 'extract/utility/runtime/' + name + '.bin'
        data = products[ROOT / path]
        assert (ROOT / path).read_bytes() == data
        derived[path] = dict(data=data, role='Child ARM7 runtime section derived from the verified archive/NDS loader map', program=utility_runtime.PROGRAM)
    references = {path: [] for path in derived}
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    paths, copied, derived_batches = {}, {}, []
    for batch in batches():
        for path, expected in batch['sourceHashes'].items():
            path = path.replace('\\', '/')
            if path in derived:
                assert expected == hashlib.sha256(derived[path]['data']).hexdigest()
                references[path].append(batch['report'])
                if batch['report'] not in derived_batches:
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
        assert rows
        for row in rows:
            processor = row.get('processor', report.get('processor'))
            program = row.get('program', report.get('program')) or ''
            module = row.get('module', report.get('module', ''))
            host = program == '' and module.startswith('arm7-')
            child = program == 'dwc/utility.bin/move/child.srl' and module in ['utility-child-arm7-main', 'utility-child-arm7-wram']
            assert processor == 'arm7' and (host or child)
    namespace_controls = [
        dict(processor='arm9', program='', module='main'),
        dict(processor='arm7', program='wrong-child', module='utility-child-arm7-wram')]
    for invalid in namespace_controls:
        host = invalid['program'] == '' and invalid['module'].startswith('arm7-')
        child = invalid['program'] == 'dwc/utility.bin/move/child.srl' and invalid['module'] in ['utility-child-arm7-main', 'utility-child-arm7-wram']
        assert not (invalid['processor'] == 'arm7' and (host or child))
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
        derivedExecutableInputs=[dict(path=path, sha256=hashlib.sha256(item['data']).hexdigest(), bytes=len(item['data']),
            role=item['role'], romSha256=ROM_SHA, referencedBy=references[path], committedAsAuthoredSource=False,
            reconstructedSourceBytes=0, reconstructedAssemblyBytes=0) for path, item in derived.items()],
        utilityDerivation=dict(generator='utility_runtime.py', generatorSha256=sha256(ROOT / 'utility_runtime.py'),
            childProgram=utility_runtime.PROGRAM, archiveInputSha256=utility_runtime.INPUT_HASH,
            childHeaderCrcVerified=utility_report['child']['crcVerified'], originalFileTableVerified=True),
        generator='verify_committed_source_inputs_v3_20261031.py', generatorSha256=sha256(__file__),
        registryOrFrameworkChanged=False, sourceCredit=0, rejectedNamespaceControls=namespace_controls,
        previousHostOnlyVerifierPreserved=True,
        limitations=['Only four exact derived physical/container/runtime inputs are classified, each regenerated from the authoritative ROM and verified archive loader mapping',
            'Every other registered repository path is checked byte-for-byte against the selected commit',
            'Original strict verifier failure is retained; no executable blob is committed as recovered source',
            'This packaging/input audit is not a complete fresh build or a source-only game proof'])
    write_json(ROOT / f'evidence/verification/cohort{options.cohort}-committed-source-inputs-v3-20261031.json', report)
    print(dict(pathsChecked=len(paths), derivedExecutableInputs=len(derived), passed=report['passed'], missing=missing, changed=changed))
    assert report['passed']


if __name__ == '__main__':
    main()
