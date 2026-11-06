import argparse
import hashlib
from unittest.mock import patch
import match_runtime as compiler
import match_ov001_effect_queue_20261030 as frozen
from project import ROOT, read_json, write_json, sha256

REPORT = 'evidence/matches/ov001-20261030-effect-queue01.json'
SOURCES = {
    'src/overlays/ov001_20261030_effect_queue_slot_6d6ed92d1440.c': '6d6ed92d1440e5650e494d38f0423ead1ba64d190c4071aaec2dfba58e98faf6',
    'src/overlays/ov001_20261030_effect_resource_constructor_74c8a98915b2.c': '74c8a98915b2f05b4c8de44ab59037b9ca193d3eda9b687c63baead097da9073'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--canonical', action='store_true')
    options = parser.parse_args()
    canonical_before = sha256(ROOT / REPORT)
    producer_hash, framework_hash = sha256(frozen.__file__), sha256(compiler.__file__)
    for path, expected in SOURCES.items():
        assert sha256(ROOT / path) == expected
    original_generator_work = frozen.WORK
    compare = compiler.compare
    routed = []

    def short_compare(source, module, optimization, inline, speed=False, thumb=False, compiler=None, processor=None):
        relative = source.relative_to(ROOT).as_posix()
        assert relative in SOURCES and sha256(source) == SOURCES[relative]
        assert module == 'ov001' and str(optimization) == '2' and inline == 'off' and speed is True
        assert thumb is False and compiler is None and processor is None
        base = ROOT / 'work/eq-short-20261101'
        predicted = base / source.stem / hashlib.sha256(str(source).encode()).hexdigest()[:12] / '2-off-speed.o'
        assert len(str(predicted)) < 220 and predicted.resolve().is_relative_to(ROOT)
        label = source.stem.removeprefix('ov001_20261030_')
        assert label in [unit[0] for unit in frozen.UNITS]
        original_work = original_generator_work / label / 'compiler'
        with patch.object(globals()['compiler'], 'WORK', base):
            result = compare(source, module, optimization, inline, speed, thumb, compiler, processor)
        for row in result[0]:
            assert not row.get('compileFailed')
            fresh_object = ROOT / row['object']
            preserved = original_work / 'objects' / (row['objectSha256'] + '.o')
            preserved.parent.mkdir(parents=True, exist_ok=True)
            if preserved.exists():
                assert preserved.read_bytes() == fresh_object.read_bytes()
            else:
                preserved.write_bytes(fresh_object.read_bytes())
            row['object'] = preserved.relative_to(ROOT).as_posix()
            assert sha256(preserved) == row['objectSha256']
        routed.append(dict(source=relative, sourceSha256=sha256(source),
            outputPath=predicted.relative_to(ROOT).as_posix(), outputCharacters=len(str(predicted))))
        return result

    target = REPORT if options.canonical else 'evidence/attempts/effect-queue-short-path-positive-v3-20261101.json'
    with patch.object(compiler, 'compare', short_compare), patch.object(frozen, 'REPORT', ROOT / target), \
         patch.object(frozen, 'WORK', ROOT / 'work/eq-short-link-20261101'):
        frozen.run()
    report = read_json(ROOT / target)
    assert len(report['matches']) == 2 and sum(row['bytes'] for row in report['matches']) == 324
    assert len(routed) == 2
    assert sha256(frozen.__file__) == producer_hash and sha256(globals()['compiler'].__file__) == framework_hash
    for path, expected in SOURCES.items():
        assert sha256(ROOT / path) == expected
    if not options.canonical:
        assert sha256(ROOT / REPORT) == canonical_before
    receipt = 'evidence/verification/effect-queue-short-path-transport-v3-20261101.json'
    if not options.canonical:
        receipt = 'evidence/attempts/effect-queue-short-path-diagnostic-v3-20261101.json'
    write_json(ROOT / receipt, dict(generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
        originalProducer='match_ov001_effect_queue_20261030.py', originalProducerSha256=producer_hash,
        originalCompilerFrameworkSha256=framework_hash, report=target, reportSha256=sha256(ROOT / target),
        routed=routed, compilerFlagsOrNativeInputsChanged=False, originalSourceBytesChanged=False,
        canonicalPublication=options.canonical, canonicalBeforeSha256=canonical_before,
        exactFunctions=2, exactBytes=324, sourceCredit=0, passed=True))
    print(dict(passed=True, exactFunctions=2, unchangedSourceBytes=324,
               actualReturns=sum(row['oracle']['executions'] for row in report['matches']), sourceCredit=0))


if __name__ == '__main__':
    main()
