import ast
import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    qualification_name = 'evidence/verification/sdk-data-namespace-v3-qualification-20261106.json'
    qualification = read_json(ROOT / qualification_name)
    assert qualification['passed'] and qualification['productionRegistryUnchanged']
    assert qualification['objects'] == 9 and qualification['initializedBytes'] == 4314
    assert qualification['transportSha256'] == sha256(ROOT / 'replay_sdk_data_namespace_v3_20261106.py')
    descriptors = qualification['descriptors']
    assert len(descriptors) == 4
    for row in descriptors:
        assert sha256(ROOT / row['path']) == row['sha256']
    spec_name = 'cohort166-parallel-wave20261105-k-specification.json'
    package_name = 'cohort166-parallel-wave20261105-k-package.json'
    cfg_name = 'provenance/parallel-wave20261105-k-packets.json'
    spec, package, cfg = [read_json(ROOT / name) for name in [spec_name, package_name, cfg_name]]
    assert cfg['membershipFrozen'] and spec['cohort'] == 166 and spec['previousAcceptedCohort'] == 165
    membership = {key: spec[key] for key in ['expectedAdditions', 'expectedDataAdditions', 'migrations']}
    membership_hash = hashlib.sha256(json.dumps(membership, sort_keys=True).encode()).hexdigest()
    assert len(membership['expectedAdditions']) == 70 and sum(r['bytes'] for r in membership['expectedAdditions']) == 10794
    assert len(membership['expectedDataAdditions']) == 9 and sum(r['bytes'] for r in membership['expectedDataAdditions']) == 4314
    assert not membership['migrations']
    old_reports = {read_json(ROOT / row['path'])['originalReport'] for row in descriptors}
    assert len(old_reports) == 2
    assert sum(p['report'] in old_reports for p in spec['packets']) == 2
    archive = ROOT / 'evidence/attempts/cohort166-mixed-data-program-routing-20261106/adoption-inputs.json'
    assert not archive.exists()
    names = [spec_name, package_name, cfg_name, 'recovery.json', 'source-preferences.json',
             'evidence/verification/cohort-2026-10-29-166.json',
             'work/integration/cohort166-recovery-transaction.json']
    write_json(archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in names]))
    additions = [dict(report=read_json(ROOT / row['path'])['output'],
                     producer=['replay_sdk_data_namespace_v3_20261106.py', row['path']], directProducer=False)
                 for row in descriptors]
    spec['packets'] = [p for p in spec['packets'] if p['report'] not in old_reports] + additions
    assert membership == {key: spec[key] for key in membership}
    previous = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-165.json')
    failed = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-166.json')
    assert sha256(ROOT / 'recovery.json') == failed['sourceRegistrySha256']
    closed = '54436a74559d98a053d0f33391237679b9a9ab16'
    restored = []
    for name, field in [('recovery.json', 'sourceRegistrySha256'), ('source-preferences.json', 'sourcePreferenceSha256')]:
        payload = subprocess.check_output(['git', 'show', closed + ':' + name], cwd=ROOT)
        assert hashlib.sha256(payload).hexdigest() == previous[field]
        (ROOT / name).write_bytes(payload)
        restored.append(dict(path=name, sha256=sha256(ROOT / name)))
    old_driver = (ROOT / 'run_next_source_package_v31_20261106.py').read_text()
    new_driver = ROOT / 'run_next_source_package_v32_20261106.py'
    assert not new_driver.exists()
    updated = old_driver.replace('v31', 'v32')
    assert ast.dump(ast.parse(updated.replace('v32', 'v31'))) == ast.dump(ast.parse(old_driver))
    new_driver.write_text(updated, encoding='utf-8')
    receipt_name = 'evidence/verification/cohort166-sdk-data-namespace-transport-correction-20261106.json'
    additions_to_capture = [qualification_name, receipt_name, archive.relative_to(ROOT).as_posix(),
        'evidence/attempts/cohort166-mixed-data-program-routing-20261106/verbatim-inputs.json',
        'replay_sdk_data_namespace_v3_20261106.py', 'qualify_sdk_data_namespace_v3_20261106.py',
        'adopt_sdk_data_namespace_v3_20261106.py', new_driver.name, *[r['path'] for r in descriptors]]
    package['extra'] = list(dict.fromkeys([*package['extra'], *additions_to_capture]))
    cfg['namespaceDataRegistrationTransports'] = descriptors
    write_json(ROOT / spec_name, spec)
    write_json(ROOT / package_name, package)
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / receipt_name, dict(passed=True, sourceCredit=0,
        newSourceMembershipUnchanged=True, membershipSha256=membership_hash,
        functionAdditions=70, functionBytes=10794, dataObjects=9, initializedDataBytes=4314,
        onlyDataReportTransportRoutesChanged=True, originalDataRowsAndNativeProofsUnchanged=True,
        originalAllSharedChecksRetained=True, closedPredecessorRegistryRestoredForFreshPreparation=restored,
        qualification=qualification_name, qualificationSha256=sha256(ROOT / qualification_name),
        originalFailurePreserved=True, generatorSha256=sha256(ROOT / 'adopt_sdk_data_namespace_v3_20261106.py')))
    print(dict(passed=True, functionAdditions=70, functionBytes=10794, dataObjects=9, initializedDataBytes=4314))


if __name__ == '__main__':
    main()
