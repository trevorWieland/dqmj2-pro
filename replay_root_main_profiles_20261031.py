import argparse
import concurrent.futures
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256

INPUT = 'evidence/verification/root-main-qualified-frontier-20261031.json'
WORK = ROOT / 'work/root-main-profile-replay-full-20261031'


def replay_one(index):
    import match_runtime as compiler
    from link_runtime_unit import validate
    from recover_linked_runtime import qualified_bindings
    item = read_json(ROOT / INPUT)['qualified'][index]
    source = ROOT / item['source']
    assert sha256(source) == item['sourceSha256']
    assert sha256(ROOT / item['compiler']) == item['compilerSha256']
    flags = item['compilerFlags']
    directory = WORK / str(index)
    directory.mkdir(parents=True, exist_ok=True)
    compiler.WORK = directory / 'compile'
    compiler.FLAGS = [flag for flag in flags if flag != '-thumb']
    rows, unused = compiler.compare(source, 'main', flags[0][2:], flags[flags.index('-inline') + 1],
                                   False, '-thumb' in flags, compiler=ROOT / item['compiler'],
                                   processor=flags[flags.index('-proc') + 1])
    assert all(row.get('failed') or row.get('compilerFlags') == flags for row in rows)
    selected = [row for row in rows if row.get('address') == item['address'] and row.get('mode') == item['mode']]
    result = dict(input=item, genuineLinkExact=False, sourceCredit=0, nativeExecutionCount=0)
    if len(selected) == 1:
        row = selected[0]
        result['match'] = row
        try:
            proof = validate(row, qualified_bindings(row), directory / 'link')
        except (ValueError, KeyError) as error:
            result['linkFailure'] = str(error)
        else:
            result.update(genuineLinkExact=True, proof=proof)
        linked = directory / 'link/caller.bin'
        if linked.is_file():
            from link_runtime_unit import measured_module
            metadata, binary, unused = measured_module('main')
            offset = int(item['address'], 0) - int(metadata['base'], 0)
            target = binary[offset:offset + item['bytes']]
            image = linked.read_bytes()
            result['linkedComparison'] = dict(bytes=len(image), matchingBytes=sum(a == b for a, b in zip(image, target)),
                                              sha256=sha256(linked), targetSha256=item['targetSha256'])
    else:
        result['compileOrIdentityFailure'] = rows
    write_json(directory / 'result.json', result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--one', type=int)
    args = parser.parse_args()
    if args.one is not None:
        replay_one(args.one)
        return
    inputs = read_json(ROOT / INPUT)['qualified']
    identities, selected = {}, []
    for index, item in enumerate(inputs):
        key = (item['address'], item['mode'])
        count = identities.setdefault(key, 0)
        if count >= 2:
            continue
        identities[key] += 1
        selected.append(index)
    WORK.mkdir(parents=True, exist_ok=True)

    def run(index):
        log = WORK / f'job-{index}.txt'
        with log.open('w', encoding='utf-8') as stream:
            process = subprocess.run([sys.executable, str(ROOT / __file__), '--one', str(index)],
                                     cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
        if process.returncode:
            return dict(index=index, failed=True, log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log))
        return dict(index=index, result=read_json(WORK / str(index) / 'result.json'))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, selected))
    exact = [row for row in results if row.get('result', {}).get('genuineLinkExact')]
    best = {}
    for row in results:
        record = row.get('result', {})
        comparison = record.get('linkedComparison')
        if comparison:
            key = (record['input']['address'], record['input']['mode'])
            if key not in best or comparison['matchingBytes'] > best[key]['linkedComparison']['matchingBytes']:
                best[key] = record
    write_json(ROOT / 'evidence/attempts/root-main-current-profile-replay-full-20261031.json',
               dict(input=INPUT, inputSha256=sha256(ROOT / INPUT), results=results,
                    selectedIdentities=len(identities), profiles=len(selected), genuineProfiles=len(exact),
                    linkedIdentities=len(best), bestPerIdentity=list(best.values()),
                    linkedIdentityBytes=sum(row['input']['bytes'] for row in best.values()),
                    matchingLinkedBytes=sum(row['linkedComparison']['matchingBytes'] for row in best.values()),
                    sourceCredit=0, nativeExecutionCount=0,
                    limits=['Genuine unit matches remain proposals until native and module/ROM qualification',
                            'Historical scores and duplicate profiles never receive source credit']))
    print(dict(identities=len(identities), profiles=len(selected), genuineProfiles=len(exact),
               failedJobs=sum(bool(r.get('failed')) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
