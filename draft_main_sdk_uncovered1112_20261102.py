import concurrent.futures
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
import survey_main_sdk_visibility_v4_20261102 as survey


def main():
    output = ROOT / 'evidence/attempts/main-sdk-uncovered1112-closure-20261102.json'
    assert not output.exists()
    old = read_json(ROOT / 'evidence/attempts/main-sdk-visibility-v4-breadth-20261102.json')
    contexts = {(r['source'], r['profile']): r for r in old['preprocessed']}
    selected = {0x02036538, 0x0202E434, 0x0202E300, 0x0202E2E0}
    queue = [r for r in read_json(ROOT / 'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json')['candidates']
        if r['sourceOwner'] == 'root' and int(r['identity']['address'], 0) in selected
        and (r['referenceSource'], r['profile']) in contexts]
    survey.WORK = ROOT / 'work/main-sdk-uncovered1112-20261102'
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(survey.prepare, [(i, row, contexts) for i, row in enumerate(queue)]))
    write_json(output, dict(sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        sourceIdentities=len({r['identity']['address'] for r in queue}),
        sourceInitializedBytes=sum({r['identity']['address']: r['identity']['bytes'] for r in queue}.values()),
        results=results, actualNativeFunctionReturns=0, ordinarySourceAndGenuineLinkQualificationPending=True))
    print(dict(profiles=len(results), standaloneCompiling=sum(bool(r.get('candidate')) for r in results),
        identities=len({r['identity']['address'] for r in queue}), sourceCredit=0))


if __name__ == '__main__':
    main()
