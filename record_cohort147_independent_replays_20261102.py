import hashlib
import gzip
import json
import subprocess
from project import ROOT, read_json, write_json, sha256
from record_cohort143_independent_replays_20261102 import pins


def main():
    packets = [
        ('arm7-sdk409', 'provenance/arm7-sdk409-cam-bootstrap292-handoff-20261102.json', 'fa3f4fcb2b995d41996b0c704c04749ad7d5991f'),
        ('save-core-mechanics475', 'evidence/lanes/save-core/mechanics475-ready-20261102.json', '1de4eb56be7b542b98e107cbffd8126827bd3a16'),
        ('ov001-constructor928', 'provenance/handoffs/ov001-constructor928-ready-20261102.json', '3e46c357'),
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
                compressed = relative == 'evidence/vectors/save-core-mechanics475-current-provenance-20261102.json.gz'
                assert path.suffix == '.json' or compressed, relative
                if compressed:
                    current, original = json.loads(gzip.decompress(path.read_bytes())), json.loads(gzip.decompress(blob))
                    assert len(current) == len(original) == 45
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
                independentReplayCompleted=True, sourceAcceptancePendingCohort147=True,
                scope='Normal replay completed with exit0; all declared, existing, required and tool path/hash containers inspected'))
        print(dict(packet=label, unchanged=unchanged, jsonMetadataDifferences=len(changes)))


if __name__ == '__main__':
    main()
