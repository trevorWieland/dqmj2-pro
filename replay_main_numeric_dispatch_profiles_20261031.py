from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

REPORTS = [
    'main-pcm-o3-replay', 'main-pcm-o3-expression', 'main-pcm-o3-compilers',
    'main-pcm-wide-product', 'main-pcm-wide-factor', 'main-pcm-c-division', 'main-pcm-product-local',
]


def main():
    results = []
    for name in REPORTS:
        path = ROOT / f'evidence/attempts/{name}-20261031.json'
        report = read_json(path)
        for index, previous in enumerate(report.get('results', [report])):
            row = previous['match']
            source = ROOT / row['source']
            assert sha256(source) == row['sourceSha256']
            flags = row['compilerFlags']
            compiler.WORK = ROOT / f'work/main-numeric-dispatch-profile-replay-20261031/{name}/{index}/compile'
            executable = ROOT / row.get('compilerPath', 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
            rows, unused = compiler.compare(source, 'main', int(flags[0][2:]),
                                           flags[flags.index('-inline') + 1], '-opt' in flags,
                                           '-thumb' in flags, compiler=executable,
                                           processor=flags[flags.index('-proc') + 1])
            assert len(rows) == 1
            current = rows[0]
            assert current['compilerSha256'] == row['compilerSha256']
            assert current['compilerFlags'] == flags
            assert (current['compiledBytes'], current['matchingBytes']) == (row['compiledBytes'], row['matchingBytes'])
            result = dict(input=path.relative_to(ROOT).as_posix(), inputSha256=sha256(path),
                          inputIndex=index, match=current, genuineLinkExact=False)
            try:
                proof = validate(current, qualified_bindings(current), compiler.WORK.parent / 'link')
            except (ValueError, KeyError) as error:
                result['linkFailure'] = str(error)
            else:
                result.update(genuineLinkExact=True, proof=proof)
            assert result['genuineLinkExact'] == previous['genuineExact']
            results.append(result)
    assert len(results) == 17 and sum(row['genuineLinkExact'] for row in results) == 1
    write_json(ROOT / 'evidence/attempts/main-numeric-dispatch-profile-replay-20261031.json',
               dict(results=results, sourceCredit=0, nativeExecutionCount=0, registered=False))
    print(dict(replayed=len(results), genuineLinks=1, genuineBytes=416, sourceCredit=0))


if __name__ == '__main__':
    main()
