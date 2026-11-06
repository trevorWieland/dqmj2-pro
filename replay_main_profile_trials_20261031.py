import argparse
from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('reports', nargs='+')
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert args.label.replace('-', '').replace('_', '').isalnum()
    results = []
    for report_index, relative in enumerate(args.reports):
        path = ROOT / relative
        assert path.resolve().is_relative_to(ROOT)
        document = read_json(path)
        for index, old in enumerate(document.get('results', [document.get('result', document)])):
            row = old['match']
            assert sha256(ROOT / row['source']) == row['sourceSha256']
            flags = row['compilerFlags']
            executable = ROOT / row.get('compilerPath', 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
            compiler.FLAGS = [value for value in flags if value != '-thumb']
            directory = ROOT / f'work/main-profile-trial-replay-20261031/{args.label}/{report_index}/{index}'
            compiler.WORK = directory / 'compile'
            current, unused = compiler.compare(ROOT / row['source'], row['module'], flags[0][2:],
                flags[flags.index('-inline') + 1], False, '-thumb' in flags, compiler=executable,
                processor=flags[flags.index('-proc') + 1])
            assert len(current) == 1
            current = current[0]
            assert current['compilerFlags'] == flags and current['compilerSha256'] == row['compilerSha256']
            assert all(current[field] == row[field] for field in ['bytes', 'compiledBytes', 'matchingBytes', 'targetSha256'])
            result = dict(input=relative, inputSha256=sha256(path), index=index, match=current, genuine=False)
            try:
                result['proof'] = validate(current, qualified_bindings(current), directory / 'link')
            except (ValueError, KeyError) as error:
                result['failure'] = str(error)
            else:
                result['genuine'] = True
            results.append(result)
    write_json(ROOT / f'evidence/attempts/main-profile-trial-replay-{args.label}-20261031.json',
               dict(results=results, sourceCredit=0, nativeExecutionCount=0))
    print(dict(profiles=len(results), genuine=sum(row['genuine'] for row in results), sourceCredit=0))


if __name__ == '__main__':
    main()
