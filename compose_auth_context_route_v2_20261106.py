import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualified_auth_context_guard_v2_20261106 import verify


def main():
    qualification = verify()
    cfg_name = 'provenance/parallel-wave20261105-l-packets.json'
    spec_name = 'cohort167-parallel-wave20261105-l-specification.json'
    package_name = 'cohort167-parallel-wave20261105-l-package.json'
    cfg, spec, package = [read_json(ROOT / n) for n in [cfg_name, spec_name, package_name]]
    assert cfg['membershipFrozen'] is True and spec['cohort'] == 167 and spec['previousAcceptedCohort'] == 166
    assert not spec.get('expectedDataAdditions') and spec['migrations'] == []
    pending = cfg['pendingQualifiedContextTransport']
    assert pending['composeOnlyAfterMembershipFreeze'] and not cfg.get('qualifiedContextTransportComposed')
    descriptor_name = pending['descriptor']
    descriptor = read_json(ROOT / descriptor_name)
    original_descriptor = read_json(ROOT / descriptor['originalReplayDescriptor'])
    old_report, new_report = original_descriptor['canonicalReport'], descriptor['output']
    selected = [p for p in spec['packets'] if p['report'] == old_report]
    assert len(selected) == 1 and not any(p['report'] == new_report for p in spec['packets'])
    report = read_json(ROOT / new_report)
    assert len(report['matches']) == 3 and sum(r['bytes'] for r in report['matches']) == 1264
    assert report['contextCanonicalTransport']['contextDataCredit'] == 0
    expected = {(r['module'], r['mode'], r['address']): r['bytes'] for r in spec['expectedAdditions']}
    for row in report['matches']:
        assert expected[(row['module'], row['mode'], row['address'])] == row['bytes']
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        assert row['realLink']['exactCallerBytes']
    membership = json.dumps(spec['expectedAdditions'], sort_keys=True)
    archive_name = 'evidence/attempts/cohort167-context-transport-composition-20261106/verbatim-inputs.json'
    assert not (ROOT / archive_name).exists()
    write_json(ROOT / archive_name, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in [cfg_name, spec_name, package_name]]))
    for packet in spec['packets']:
        if packet['report'] == old_report:
            packet.update(report=new_report, producer=['replay_auth_context_packet_v2_20261106.py', descriptor_name], directProducer=False)
    commands = spec['postSealCommands']
    assert sum(c[0] == 'qualify_mixed_arm9_reference_inputs_20261105.py' for c in commands) == 1
    for command in commands:
        if command[0] == 'qualify_mixed_arm9_reference_inputs_20261105.py':
            command[0] = 'qualify_mixed_arm9_reference_context_v2_20261106.py'
    assert membership == json.dumps(spec['expectedAdditions'], sort_keys=True)
    receipt_name = 'evidence/verification/cohort167-auth-context-transport-composition-20261106.json'
    package['extra'] = list(dict.fromkeys([*package['extra'], archive_name, receipt_name,
        'compose_auth_context_route_v2_20261106.py', descriptor_name]))
    cfg['qualifiedContextTransportComposed'] = dict(sourceCredit=0, contextDataCredit=0,
        oldReport=old_report, newReport=new_report, qualification=qualification)
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / spec_name, spec)
    write_json(ROOT / package_name, package)
    write_json(ROOT / receipt_name, dict(passed=True, sourceCredit=0, contextDataCredit=0,
        membershipSha256=hashlib.sha256(membership.encode()).hexdigest(),
        functionMembershipUnchanged=True, onlyQualifiedCanonicalTransportAndReferenceRouteSelected=True,
        functionBytes=1264, contextCallerBytes=192, actualCompilerContextBytesUncredited=28,
        originalSourceAndCompilerObjectsAndFlagsUnchanged=True, allLogicalSharedChecksRetained=True,
        futureContinuation='run_next_source_package_v33_20261106.py',
        generatorSha256=sha256(ROOT / 'compose_auth_context_route_v2_20261106.py')))
    print(dict(passed=True, sourceCredit=0, contextDataCredit=0, frozenMembershipUnchanged=True))


if __name__ == '__main__':
    main()
