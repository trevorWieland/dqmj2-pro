from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import measured_module


def main():
    pins = read_json(ROOT / 'evidence/verification/main-async-status-inputs-20261031.json')
    sources = {}
    for pin in pins['sources']:
        path = ROOT / pin['path']
        assert sha256(path) == pin['sha256']
        sources[path.parent.name] = path
    profiles = []
    for opt in [1, 2, 3, 4]:
        for inline in ['off', 'auto']:
            for speed in [False, True]:
                profiles.append(('word-array', opt, inline, speed, None, None))
    profiles.extend((name, 2, 'off', True, None, None) for name in ['old', 'word-array-zero'])
    profiles.extend((name, 2, 'auto', True, None, None) for name in ['inline-bit', 'inline-boolean', 'inline-branches'])
    profiles.extend(('word-array', 2, 'off', True, None, option) for option in ['nocse', 'noprop', 'nocse,noprop', 'nosched'])
    profiles.extend(('word-array', 2, 'off', True, relative, None) for relative in compiler.COMPILER_PINS)
    saved = compiler.FLAGS[:]
    results = []
    try:
        for index, (name, opt, inline, speed, tool, option) in enumerate(profiles):
            compiler.FLAGS = saved + (['-opt', option] if option else [])
            compiler.WORK = ROOT / f'work/main-async-status-attempts-20261031/{index:02}'
            rows, _ = compiler.compare(sources[name], 'main', opt, inline, speed, compiler=ROOT / tool if tool else None)
            assert len(rows) == 1
            row = rows[0]
            assert not row.get('compileFailed') and not row['exactAfterDeclaredRelocation']
            results.append(dict(source=sources[name].relative_to(ROOT).as_posix(), sourceSha256=sha256(sources[name]),
                compiler=row['compilerPath'], compilerSha256=row['compilerSha256'], flags=row['compilerFlags'],
                compiledBytes=row['compiledBytes'], matchingBytes=row['matchingBytes'], exact=False))
    finally:
        compiler.FLAGS = saved
    _, original, _ = measured_module('main')
    write_json(ROOT / 'evidence/attempts/main-async-status-reproduced-20261031.json', dict(
        generator=__file__, generatorSha256=sha256(__file__), address='0x0202aa58', bytes=92,
        originalRangeSha256=compiler.sha(original[0x2AA58:0x2AAB4]), profiles=results,
        sourceCredit=0, accepted=False, limitations=['Compilation comparisons only; no exact source or new native execution claim']))
    print(dict(profiles=len(results), exact=0, sourceCredit=0))


if __name__ == '__main__':
    main()
