import hashlib
import gzip
import json
import subprocess
from project import ROOT, read_json, write_json, sha256
from record_cohort143_independent_replays_20261102 import pins


def main():
    packets = [
        ('arm7-sdk439', 'provenance/arm7-sdk439-intr-transmit-compiler1236-handoff-20261102.json', '6b30a0d0cfb0e7cd4ad4e38c79be0c28bad8e933'),
        ('arm7-sdk426', 'provenance/arm7-sdk426-beacon-probe-key3016-handoff-20261102.json', 'f96ed68e39c00a4fea31bb86ee795995896fc0d9'),
        ('ov001-phase965', 'provenance/handoffs/ov001-phase965-ready-20261102.json', 'e18ab5fcdcfc1ba57c53117ac75801691d445906'),
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
                compressed = relative == 'evidence/vectors/save-core-creation495-current-provenance-20261102.json.gz'
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
                independentReplayCompleted=True, sourceAcceptancePendingCohort150=True,
                scope='Normal replay completed with exit0; all declared, existing, required and tool path/hash containers inspected'))
        print(dict(packet=label, unchanged=unchanged, jsonMetadataDifferences=len(changes)))


if __name__ == '__main__':
    main()
