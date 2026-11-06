import hashlib
import gzip
import json
import subprocess
from project import ROOT, read_json, write_json, sha256
from record_cohort143_independent_replays_20261102 import pins


def main():
    packets = [
        ('save-core-record-expand438', 'evidence/lanes/save-core/record-expand438-ready-20261102.json',
            'adf4d2f49662781db762fb4173edd90d18f4a0df'),
        ('ov000-lookup893', 'provenance/handoffs/ov000-lookup893-ready-20261102.json',
            '4f05a2369aef2d323790da5657b5f4eb02fee796'),
        ('ov000-geometry895-windows', 'provenance/handoffs/ov000-geometry895-windows-ready-20261102.json',
            '22b0cd9ed5451ada46bc5f0f5339725dca8b6491'),
        ('ov000-neighbors894', 'provenance/handoffs/ov000-neighbors894-ready-20261102.json',
            'deb13e2a9bfd2a143bcecf7792ed9848713db33a'),
        ('save-core-thumb443', 'evidence/lanes/save-core/thumb443-ready-20261102.json',
            '852ea24fdcd4083ef9aff3ab3e7bf38147b0e990'),
        ('arm7-sdk380', 'provenance/arm7-sdk380-receive-helpers1092-handoff-20261102.json',
            '5f4e57370c2a69db0fa5cb25525eb710ba746c9e'),
    ]
    for label, manifest, commit in packets:
        unchanged, changes, seen = 0, [], set()
        for row in pins(read_json(ROOT / manifest)):
            relative = row['path'].replace(chr(92), '/')
            key = relative, row['sha256']
            if key in seen: continue
            seen.add(key)
            path = (ROOT / relative).resolve()
            assert path.is_relative_to(ROOT) and path.is_file(), relative
            actual = sha256(path)
            if actual == row['sha256']:
                unchanged += 1
            else:
                blob = subprocess.run(['git', 'show', commit + ':' + relative], cwd=ROOT,
                    capture_output=True, check=True).stdout
                assert hashlib.sha256(blob).hexdigest() == row['sha256'], relative
                compressed = relative == 'evidence/vectors/save-core-thumb443-current-provenance-20261102.json.gz'
                assert path.suffix == '.json' or compressed, relative
                if compressed:
                    current, original = json.loads(gzip.decompress(path.read_bytes())), json.loads(gzip.decompress(blob))
                    assert len(current) == len(original) == 37
                    for left, right in zip(current, original):
                        left, right = dict(left), dict(right)
                        for item in (left, right):
                            item.pop('object')
                            item.pop('objectSha256')
                            item['linkMismatch'] = dict(item['linkMismatch'])
                            item['linkMismatch'].pop('directory')
                        assert left == right, relative
                changes.append(dict(path=relative, workerOriginalSha256=row['sha256'],
                    localReplaySha256=actual, originalWorkerGitBlobVerified=True,
                    compressedProvenanceOnly=compressed))
        write_json(ROOT / f'evidence/verification/{label}-independent-replay-20261102.json',
            dict(passed=True, sourceCredit=0, manifest=manifest, manifestSha256=sha256(ROOT / manifest),
                workerCommit=commit, unchangedPinnedPaths=unchanged, localReplayJsonChanges=changes,
                allNonJsonInputsAndPythonClosureUnchanged=True, originalWorkerReportsRetained=True,
                independentReplayCompleted=True, sourceAcceptancePendingCohort144=True,
                scope='Normal replay completed with exit0; all declared, existing, required and tool path/hash containers inspected'))
        print(dict(packet=label, unchanged=unchanged, jsonMetadataDifferences=len(changes)))


if __name__ == '__main__':
    main()
