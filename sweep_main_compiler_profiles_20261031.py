import argparse
import match_runtime
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', type=int, required=True)
    parser.add_argument('--lanes', type=int, default=3)
    options = parser.parse_args()
    assert 0 <= options.lane < options.lanes
    groups, exact_addresses = {}, set()
    for lane in range(3):
        report = read_json(ROOT / f'evidence/attempts/main-void-view-sweep-20261031-lane-{lane}.json')
        for row in report['rows']:
            if any(trial.get('exactCount') for trial in row['trials']):
                exact_addresses.add(row['address'])
            comparisons = [item for trial in row['trials'] for item in trial.get('comparisons', [])]
            score = max((item.get('matchingBytes', 0) - abs(item.get('compiledBytes', 0) - item.get('bytes', 0)) for item in comparisons), default=-100000)
            previous = groups.get(row['address'])
            if previous is None or score > previous[0]:
                groups[row['address']] = score, row
    inputs = [(address, row) for address, (score, row) in sorted(groups.items()) if address not in exact_addresses]
    output = ROOT / f'evidence/attempts/main-compiler-profile-sweep-20261031-lane-{options.lane}.json'
    results = []
    for address, row in inputs[options.lane::options.lanes]:
        trials = []
        for source_name in [row['originalSource'], row['generatedSource']]:
            source = ROOT / source_name
            before = sha256(source)
            for compiler_name in match_runtime.COMPILER_PINS:
                profiles = [(4, False), (4, True)] if ROOT / compiler_name == match_runtime.COMPILER else [(2, False), (3, True)]
                for optimization, speed in profiles:
                    match_runtime.WORK = ROOT / f'work/main-compiler-profile-sweep-20261031/lane-{options.lane}'
                    try:
                        comparisons, exact = match_runtime.compare(source, 'main', optimization, 'off', speed=speed, compiler=ROOT / compiler_name)
                        trials.append(dict(source=source_name, sourceSha256=before, compiler=compiler_name,
                            optimization=optimization, speed=speed, comparisons=comparisons, exactCount=len(exact)))
                    except Exception as error:
                        trials.append(dict(source=source_name, compiler=compiler_name, optimization=optimization,
                            speed=speed, error=type(error).__name__ + ': ' + str(error)))
            assert sha256(source) == before
        results.append(dict(address=address, trials=trials))
        write_json(output, dict(generator=__file__, generatorSha256=sha256(__file__), sourceCredit=0,
            lane=options.lane, selectedUnacceptedIdentities=len(inputs), testedIdentities=len(results), rows=results,
            limitations=['Per-source compiler candidates only; no compiler profile is generalized to another source unit',
                'A compiler equality requires fresh genuine linking, explicit ABI review and bounded qualification before acceptance']))
        exact_count = sum(trial.get('exactCount', 0) for trial in trials)
        if len(results) % 20 == 0 or exact_count:
            print(dict(lane=options.lane, tested=len(results), address=address, exactTrials=exact_count), flush=True)
    print(dict(lane=options.lane, tested=len(results), eligible=len(inputs), sourceCredit=0), flush=True)


if __name__ == '__main__':
    main()
