import hashlib
import json
from project import ROOT, read_json, write_json, sha256


def main():
    cfg_name = 'provenance/parallel-wave20261105-q-packets.json'
    spec_name = 'cohort172-parallel-wave20261105-q-specification.json'
    package_name = 'cohort172-parallel-wave20261105-q-package.json'
    cfg, spec, package = [read_json(ROOT / n) for n in [cfg_name, spec_name, package_name]]
    assert cfg['cohort'] == spec['cohort'] == 172 and cfg['previousAcceptedCohort'] == 171
    assert not cfg['membershipFrozen'] and spec['migrations'] == [] and not spec.get('expectedDataAdditions')
    assert len(spec['expectedAdditions']) == 30 and sum(r['bytes'] for r in spec['expectedAdditions']) == 8720
    identities, readys = {}, []
    key = lambda row: (row.get('program', ''), row.get('processor', 'arm9'), row['module'], row['mode'], int(row['address'], 0))
    for path in cfg['readyPackets']:
        ready = read_json(ROOT / path)
        assert ready.get('ordinaryCBytes', ready['bytes']) == ready['bytes'] and ready.get('justifiedAssemblyBytes', 0) == 0
        for packet in ready['packets']:
            report = read_json(ROOT / packet['report'])
            for row in report['matches']:
                item = {**report, **row}
                assert item['source'].endswith('.c') and not item.get('assemblyJustification')
                flags = item['compilerFlags']
                assert flags.count('-lang') == 1 and flags[flags.index('-lang') + 1] in ['c', 'c99']
        assert ready['functions'] == len(ready['identities'])
        for row in ready['identities']:
            assert key(row) not in identities
            identities[key(row)] = row['bytes']
        descriptor = ready['canonicalDescriptor']
        assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
        for manifest in read_json(ROOT / descriptor['path'])['frozenInputs']:
            assert sha256(ROOT / manifest['path']) == manifest['sha256']
        readys.append(dict(path=path, sha256=sha256(ROOT / path)))
    assert identities == {key(r): r['bytes'] for r in spec['expectedAdditions']}
    archive = 'evidence/attempts/cohort172-ordinary-membership-freeze-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in [cfg_name, spec_name, package_name]]))
    membership_hash = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    cfg['membershipFrozen'] = True
    cfg['frozenOrdinaryMembership'] = dict(functions=30, ordinaryCBytes=8720, membershipSha256=membership_hash, readys=readys)
    receipt = 'evidence/verification/cohort172-frozen-ordinary-union-20261106.json'
    package['extra'] = list(dict.fromkeys([*package['extra'], archive, receipt, 'freeze_cohort172_ordinary_union_20261106.py']))
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], archive, receipt, 'freeze_cohort172_ordinary_union_20261106.py']))
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / package_name, package)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, functions=30, ordinaryCBytes=8720,
        dataAdditions=0, justifiedAssemblyBytes=0, readys=readys, membershipSha256=membership_hash,
        additionalInterfaceMigrationsPreserveOnlyExistingBytes=True,
        generatorSha256=sha256(ROOT / 'freeze_cohort172_ordinary_union_20261106.py')))
    print(dict(passed=True, frozenFunctions=30, frozenOrdinaryBytes=8720, sourceCredit=0))


if __name__ == '__main__':
    main()
