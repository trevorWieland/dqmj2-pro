from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    output = ROOT / 'evidence/attempts/main-sdk-word-rank-tuning-20261102.json'
    assert not output.exists(), 'Preserve first profile experiment'
    current = read_json(ROOT / 'evidence/attempts/main-sdk-remaining-breadth-20261102.json')['results']
    previous = read_json(ROOT / 'evidence/attempts/main-sdk-visibility-v4-breadth-20261102.json')['compilation']
    work = ROOT / 'work/main-sdk-word-rank-tuning-20261102'
    results = []
    for candidate in current:
        if candidate['identity']['address'] not in ['0x202caa4', '0x202cd18']: continue
        address = candidate['identity']['address']
        seeds = [r['candidate'] for r in previous if r.get('candidate', {}).get('identity', {}).get('address') == address]
        assert len(seeds) == 1
        seed = seeds[0]
        source = ROOT / candidate['source']
        assert sha256(source) == candidate['sourceSha256']
        changed = source.read_text(encoding='utf-8').replace('typedef unsigned int u32;', 'typedef unsigned long u32;').replace('typedef signed int s32;', 'typedef signed long s32;')
        source = ROOT / 'nonmatching/main/20261102-sdk-word-ranks' / source.name
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(changed, encoding='utf-8')
        old = compiler.FLAGS
        result = dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), identity=candidate['identity'], sourceCredit=0)
        try:
            compiler.FLAGS = seed['compilerFlags']
            compiler.WORK = work / source.stem / 'compile'
            rows, _ = compiler.compare(source, 'main', '2', 'off', compiler=ROOT / seed['compiler'])
            assert len(rows) == 1 and not rows[0].get('compileFailed')
            row = rows[0]
            proof = validate(row, qualified_bindings(row), work / source.stem / 'link')
            result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, genuineLinkedBytes=row['bytes'])
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        finally:
            compiler.FLAGS = old
        results.append(result)
    write_json(output, dict(sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        results=results, actualNativeFunctionReturns=0, sourceInterfacesAndModuleAcceptancePending=True))
    print(dict(attemptedFunctions=len(results), genuineExactFunctions=sum(r['genuineExact'] for r in results),
        genuineExactBytes=sum(r.get('genuineLinkedBytes', 0) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
