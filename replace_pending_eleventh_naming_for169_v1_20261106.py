from project import ROOT, read_json, write_json, sha256


def main():
    cfg_name = 'provenance/parallel-wave20261105-n-packets.json'
    cfg = read_json(ROOT / cfg_name)
    assert not cfg['membershipFrozen'] and cfg['cohort'] == 169
    old = 'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh/ready.json'
    new = 'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2/ready.json'
    assert sha256(ROOT / old) == 'e85ab323ba327b1dadaafe9895b76d0622ff826ec8ca1ca9d72e5044614bd47b'
    assert sha256(ROOT / new) == '9ba1c92e333951ae75c1544ad94ee3b134057c7c9c7045afab6faf638fb2ec4e'
    old_ready, new_ready = read_json(ROOT / old), read_json(ROOT / new)
    key = lambda row: (row.get('program') or '', row['processor'], row['module'], row['mode'], row['address'], row['bytes'])
    assert [key(row) for row in old_ready['identities']] == [key(row) for row in new_ready['identities']]
    assert old_ready['functions'] == new_ready['functions'] == 2 and old_ready['bytes'] == new_ready['bytes'] == 584
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in [*old_ready['files'], *new_ready['files']])
    assert old in cfg['readyPackets'] and new not in cfg['readyPackets']
    assert cfg['packetIds'][old] == 'socl-continuation-eleventh'
    operation_name = 'evidence/lanes/parallel-wave20261105/deferred-packet-intake/cohort169-socl-continuation-eleventh.json'
    operation = read_json(ROOT / operation_name)
    assert operation['ready'] == old and operation['readySha256'] == sha256(ROOT / old)
    archive_root = ROOT / 'evidence/attempts/cohort169-eleventh-naming-supersession-20261106'
    assert not archive_root.exists()
    names = [cfg_name, 'cohort169-parallel-wave20261105-n-specification.json',
        'cohort169-parallel-wave20261105-n-package.json', 'docs/2026-11-06-parallel-wave-n-acceptance.md']
    write_json(archive_root / 'verbatim-inputs.json', dict(sourceCredit=0,
        files=[dict(path=name, sha256=sha256(ROOT / name), text=(ROOT / name).read_text(encoding='utf-8')) for name in names]))
    old_operation = ROOT / operation_name
    destination = archive_root / old_operation.name
    assert old_operation.resolve().is_relative_to(ROOT.resolve()) and destination.resolve().is_relative_to(ROOT.resolve())
    operation_sha = sha256(old_operation)
    old_operation.replace(destination)
    assert sha256(destination) == operation_sha and not old_operation.exists()
    cfg['readyPackets'].remove(old)
    del cfg['packetIds'][old]
    receipt = 'evidence/verification/cohort169-eleventh-naming-supersession-20261106.json'
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], 'replace_pending_eleventh_naming_for169_v1_20261106.py',
        receipt, destination.relative_to(ROOT).as_posix(), (archive_root / 'verbatim-inputs.json').relative_to(ROOT).as_posix(),
        'evidence/lanes/parallel-wave20261105/socl-continuation-next/connection-fields-research.json']))
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, replacementOnlyNoNewIdentitiesOrBytes=True,
        oldReady=dict(path=old, sha256=sha256(ROOT / old)), newReady=dict(path=new, sha256=sha256(ROOT / new)),
        oldQueuedOperationPreservedVerbatim=dict(path=destination.relative_to(ROOT).as_posix(), sha256=operation_sha),
        correctedNames=['pub_algorithm', 'date_ok', 'issuer'], allFrozenSourceAndReadyPinsUnchanged=True,
        newReadyStillRequiresNormalIntakeReplayAndSharedAcceptance=True, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
