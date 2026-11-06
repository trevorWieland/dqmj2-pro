from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

INPUTS = 'evidence/verification/main-near-frontier85-inputs-20261031.json'


def main():
    inputs = read_json(ROOT / INPUTS)
    results = []
    for item in inputs['candidates']:
        source = ROOT / item['source']
        if sha256(source) != item['sourceSha256']:
            raise ValueError('Retained frontier source differs')
        compiler.WORK = ROOT / 'work/main-near-frontier85-20261031' / item['address'] / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', True)
        for row in rows:
            result = dict(input=item, match=row, sourceCredit=0)
            if not row.get('compileFailed'):
                directory = compiler.WORK.parent / 'link'
                try:
                    proof = validate(row, qualified_bindings(row), directory)
                except (ValueError, KeyError) as error:
                    result.update(genuineLinkExact=False, linkFailure=str(error))
                else:
                    result.update(genuineLinkExact=True, linkProof=proof)
            results.append(result)
        print(dict(address=item['address'], results=[dict(compiledBytes=row.get('compiledBytes'),
                   matchingBytes=row.get('matchingBytes')) for row in rows]), flush=True)
    report = dict(inputs=INPUTS, inputsSha256=sha256(ROOT / INPUTS), results=results,
                  genuineLinkedCandidates=sum(bool(r.get('genuineLinkExact')) for r in results),
                  sourceCredit=0, registered=False, nativeExecutionCount=0,
                  limitations=['Historical scores are selection hypotheses; only fresh compilation and linking are measured',
                               'Input views and original prototypes still require native behavioral qualification'])
    write_json(ROOT / 'evidence/attempts/main-near-frontier85-fresh-links-20261031.json', report)
    print(dict(candidates=len(inputs['candidates']), genuineLinked=report['genuineLinkedCandidates']))


if __name__ == '__main__':
    main()
