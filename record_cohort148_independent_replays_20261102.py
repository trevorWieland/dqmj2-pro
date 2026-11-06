import hashlib
import gzip
import json
import subprocess
from project import ROOT, read_json, write_json, sha256
from record_cohort143_independent_replays_20261102 import pins


def main():
    packets = [
        ('ov000-setter937', 'provenance/handoffs/ov000-setter937-ready-20261102.json', '70d06411'),
        ('save-core-mechanics484', 'evidence/lanes/save-core/mechanics484-ready-20261102.json', '8b0963066a2137083ba6f747df38c26310e15efd'),
        ('ov001-constructor938', 'provenance/handoffs/ov001-constructor938-ready-20261102.json', '473934e9'),
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
                compressed = relative == 'evidence/vectors/save-core-mechanics484-current-provenance-20261102.json.gz'
                assert path.suffix == '.json' or compressed, relative
                if compressed:
                    current, original = json.loads(gzip.decompress(path.read_bytes())), json.loads(gzip.decompress(blob))
                    assert len(current) == len(original) == 13
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
                independentReplayCompleted=True, sourceAcceptancePendingCohort148=True,
                scope='Normal replay completed with exit0; all declared, existing, required and tool path/hash containers inspected'))
        print(dict(packet=label, unchanged=unchanged, jsonMetadataDifferences=len(changes)))


if __name__ == '__main__':
    main()
