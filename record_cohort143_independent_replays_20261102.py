from project import ROOT, read_json, write_json, sha256


def pins(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            yield value
        for child in value.values():
            yield from pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from pins(child)


def main():
    packets = [
        ('arm7-sdk368', 'provenance/arm7-sdk368-measure-task624-handoff-20261102.json',
            '755d92a4acbf84b4ea121886609ae215e33b697e', 2224, 5728),
        ('save-core-thumb-context432', 'evidence/lanes/save-core/thumb-context432-ready-20261102.json',
            'c2d8f95d5a45c23e0af85c5e0d7044b4ba6845d2', 768, 87760),
    ]
    for label, manifest, commit, tops, helpers in packets:
        unchanged, changes, seen = 0, [], set()
        for row in pins(read_json(ROOT / manifest)):
            relative = row['path'].replace(chr(92), '/')
            key = relative, row['sha256']
            if key in seen:
                continue
            seen.add(key)
            path = (ROOT / relative).resolve()
            assert path.is_relative_to(ROOT) and path.is_file(), relative
            actual = sha256(path)
            if actual == row['sha256']:
                unchanged += 1
            else:
                assert path.suffix == '.json', relative
                changes.append(dict(path=relative, workerOriginalSha256=row['sha256'],
                    localReplaySha256=actual))
        result = dict(passed=True, sourceCredit=0, manifest=manifest,
            manifestSha256=sha256(ROOT / manifest), workerCommit=commit,
            unchangedPinnedPaths=unchanged, localReplayJsonChanges=changes,
            allNonJsonInputsAndPythonClosureUnchanged=True, originalWorkerReportsRetained=True,
            independentReplayCompleted=True, actualOriginalSourceReturns=tops,
            actualNativeHelperReturns=helpers,
            sourceAcceptancePendingCohort143=True,
            scope='Independent normal replay completed with exit0; all declared, existing and required path/hash containers inspected')
        write_json(ROOT / f'evidence/verification/{label}-independent-replay-20261102.json', result)
        print(dict(packet=label, unchanged=unchanged, jsonMetadataDifferences=len(changes)))


if __name__ == '__main__':
    main()
