import os
import project
from project import ROOT, write_json, sha256
from closed_snapshot_hash_cache_20261105 import ORIGINAL, SnapshotHashes, scope


def main():
    folder = ROOT / 'work/closed-snapshot-hash-controls-20261105'
    folder.mkdir(parents=True, exist_ok=True)
    first, second = folder / 'first.txt', folder / 'second.txt'
    first.write_bytes(b'correct')
    second.write_bytes(b'correct')
    executions = []

    def measured(path):
        executions.append(str(path))
        return ORIGINAL(path)

    positive = SnapshotHashes(measured)
    for unused in range(100):
        assert positive(first) == ORIGINAL(first)
    receipt = positive.verify()
    assert len(executions) == 2 and receipt['hits'] == 99
    controls = ['every-distinct-file-fully-rehashed-at-closure']
    separate = SnapshotHashes()
    separate(first)
    separate(second)
    assert separate.verify()['uniqueFiles'] == 2
    controls.append('equal-content-paths-remain-separate-epoch-inputs')
    for label, restore_time, check_second_read in [
        ('mutation-at-second-read', False, True),
        ('mutation-at-closure', False, False),
        ('same-size-restored-mtime-mutation-at-closure', True, False),
    ]:
        first.write_bytes(b'correct')
        before = first.stat()
        cache = SnapshotHashes()
        cache(first)
        first.write_bytes(b'changed')
        if restore_time:
            os.utime(first, ns=(before.st_atime_ns, before.st_mtime_ns))
        try:
            if check_second_read:
                cache(first)
            cache.verify()
        except ValueError:
            controls.append(label)
        else:
            raise ValueError(label)
    first.write_bytes(b'correct')
    cache = SnapshotHashes()
    cache(first)
    first.unlink()
    try:
        cache.verify()
    except FileNotFoundError:
        controls.append('missing-file-at-closure')
    else:
        raise ValueError('Missing snapshot input accepted')
    first.write_bytes(b'changed')
    fresh = SnapshotHashes()
    assert fresh(first) == ORIGINAL(first)
    fresh.verify()
    controls.append('separate-snapshots-never-reuse-prior-content')
    snapshots = []
    with scope(snapshots):
        assert project.sha256 is not ORIGINAL
        assert project.sha256(first) == ORIGINAL(first)
        with scope(snapshots):
            assert project.sha256(first) == ORIGINAL(first)
    assert project.sha256 is ORIGINAL and len(snapshots) == 1
    controls.append('nested-snapshot-and-original-function-restoration')
    try:
        with scope(snapshots):
            raise LookupError('controlled')
    except LookupError:
        assert project.sha256 is ORIGINAL
    controls.append('exception-restores-original-functions-without-acceptance')
    write_json(ROOT / 'evidence/verification/closed-snapshot-hash-cache-controls-20261105.json', dict(
        passed=True, sourceCredit=0, controls=controls, controlCount=len(controls),
        originalHashFunctionUnchanged=True, positive=receipt,
        qualifierSha256=sha256(ROOT / 'closed_snapshot_hash_cache_20261105.py')))
    print(dict(passed=True, controls=len(controls), originalHashExecutions=len(executions)))


if __name__ == '__main__':
    main()
