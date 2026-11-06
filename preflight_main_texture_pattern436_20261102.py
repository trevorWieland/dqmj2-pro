from pathlib import Path
from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    builder.WORK = ROOT / 'work/main-texture-pattern436-preflight-20261102'
    report = ROOT / 'evidence/attempts/main-texture-pattern436-preflight-20261102.json'
    assert not report.exists(), 'Preserve the original preflight'
    results = []
    for source in sorted((ROOT / 'src/runtime/20261102_texture_pattern436').glob('*.c')):
        try:
            row, proof, body = builder.build(source, source.stem, True)
            results.append(dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
                compiledEntry=row, genuineLinkProof=proof, genuineLinkedBytes=len(body), passed=True))
        except Exception as error:
            results.append(dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
                passed=False, errorType=type(error).__name__, refusal=str(error)))
    write_json(report, dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        sourceCredit=0, results=results, nativeProofAndAcceptancePending=True))
    print(dict(candidates=len(results), genuineFunctions=sum(r['passed'] for r in results),
        genuineBytes=sum(r.get('genuineLinkedBytes', 0) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
