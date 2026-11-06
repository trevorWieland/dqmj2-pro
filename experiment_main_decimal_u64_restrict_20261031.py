import match_runtime
from project import ROOT, write_json, sha256


def main():
    original = ROOT / 'src/runtime/20261031_decimal_u64/native_main_02022a94.c'
    frozen_hash = sha256(original)
    directory = ROOT / 'nonmatching/main-runtime/20261031-decimal-u64-restrict'
    directory.mkdir(parents=True, exist_ok=True)
    results = []
    for keyword in ['restrict', '__restrict', '__restrict__']:
        source = directory / keyword / 'native_main_02022a94.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(original.read_text().replace('decimal *pDecimal,', f'decimal *{keyword} pDecimal,'), encoding='utf-8')
        for optimization, speed in [(2, False), (3, False), (3, True)]:
            rows, exact = match_runtime.compare(source, 'main', optimization, 'off', speed=speed)
            results.append(dict(keyword=keyword, optimization=optimization, speed=speed, source=source.relative_to(ROOT).as_posix(),
                sourceSha256=sha256(source), rows=rows, exactFunctionCount=len(exact), sourceCredit=0))
            print(dict(keyword=keyword, optimization=optimization, speed=speed,
                sizes=[row.get('compiledBytes') for row in rows], exact=len(exact)), flush=True)
    assert sha256(original) == frozen_hash
    write_json(ROOT / 'evidence/attempts/main-decimal-u64-restrict-20261031.json', dict(
        generator=__file__, generatorSha256=sha256(__file__), originalSourceSha256=frozen_hash,
        originalSourceUnchanged=True, trials=results, sourceCredit=0,
        limitations=['Pointer alias assumptions are candidate source hypotheses; no new match or behavior is accepted by this experiment']))


if __name__ == '__main__':
    main()
