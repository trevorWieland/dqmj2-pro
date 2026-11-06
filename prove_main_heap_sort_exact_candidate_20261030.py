import hashlib
import re
from project import ROOT, configuration, sha256, write_json
import prove_main_heap_sort_near_20261030 as proof

SOURCE = 'nonmatching/main-sort/20261030/heap_sort_exact_candidate.c'
WORK = ROOT / 'work/coordinator-main-sort-20261030/exact-candidate-proof'


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    proof.WORK = WORK
    assert sha256(proof.compiler.COMPILER) == proof.compiler.COMPILER_PINS[proof.compiler.COMPILER.relative_to(ROOT).as_posix()]
    metadata, binary, config = proof.linker.measured_module('main')
    offset = proof.ENTRY - int(metadata['base'], 0)
    native = binary[offset:offset + proof.SIZE]
    obj, compiled = proof.build(ROOT / SOURCE, 'native_main_0201d470', 'source')
    assert len(compiled) == 356 and compiled == native
    configured = int(re.search(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x0201d470$', config, re.M)[1], 0)
    assert configured in (348, 356)
    entry = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': hex(proof.ENTRY),
             'bytes': configured, 'targetSha256': hashlib.sha256(native[:configured]).hexdigest(),
             'source': SOURCE, 'sourceSha256': sha256(ROOT / SOURCE),
             'object': obj.relative_to(ROOT).as_posix(), 'objectSha256': sha256(obj),
             'name': 'native_main_0201d470'}
    output = (WORK / 'real-link').resolve()
    assert output.is_relative_to(WORK.resolve())
    for name in ['caller.bin', 'linked.elf']:
        target = output / name
        if target.exists():
            target.unlink()
    try:
        proof.linker.validate(entry, {}, output)
    except ValueError as error:
        assert configured == 348
        boundary_failure = str(error)
        normal_boundary_accepted = False
    else:
        assert configured == 356
        normal_boundary_accepted = True
        legacy = dict(entry, bytes=348, targetSha256=hashlib.sha256(native[:348]).hexdigest())
        try:
            proof.linker.validate(legacy, {}, WORK / 'legacy-boundary-rejection')
        except ValueError as error:
            boundary_failure = str(error)
        else:
            raise AssertionError('Legacy348ByteBoundaryUnexpectedlyAccepted356ByteObject')
    linked = (output / 'caller.bin').read_bytes()
    assert linked == native == compiled
    callback_source = WORK / 'synthetic_comparator.c'
    callback_source.write_text('int synthetic_comparator(const signed char *a, const signed char *b) { return (*a > *b) - (*a < *b); }\n', encoding='utf-8')
    callback_obj, callback = proof.build(callback_source, 'synthetic_comparator', 'comparator')
    vectors = []
    for count in [0, 1, 2, 3, 5, 8, 17]:
        for width in [0, 1, 2, 4, 7]:
            for pattern in range(5):
                payload = bytes(((i * [0, 1, 255, 17, 113][pattern] + pattern * 63) & 255) for i in range(count * width))
                vectors.append((count, width, payload))
    vectors += [(16, 1, bytes(range(start, start + 16))) for start in range(0, 256, 16)]
    records = []
    for count, width, payload in vectors:
        original = proof.execute(native, callback, payload, count, width)
        rebuilt = proof.execute(linked, callback, payload, count, width)
        assert original == rebuilt
        records.append({'count': count, 'width': width, 'inputSha256': hashlib.sha256(payload).hexdigest(),
                        'stateSha256': hashlib.sha256(repr(original).encode()).hexdigest(),
                        'syntheticComparatorReturns': original['syntheticComparatorReturns'] * 2})
    report = {'romSha256': configuration()['romSha256'], 'module': 'main', 'processor': 'arm9', 'mode': 'arm',
              'address': hex(proof.ENTRY), 'provisionalWholeExtent': 356, 'configuredExtent': configured, 'normalCurrentBoundaryAccepted': normal_boundary_accepted,
              'source': SOURCE, 'sourceSha256': sha256(ROOT / SOURCE), 'object': obj.relative_to(ROOT).as_posix(),
              'objectSha256': sha256(obj), 'exact356OriginalBytes': compiled == native,
              'genuineLinkExact356OriginalBytes': linked == native,
              'legacyBoundaryAcceptanceFailure': boundary_failure, 'boundaryConfigChanged': False,
              'freshGenuineLinkOutputRequired': True, 'linkerSha256': sha256(proof.linker.LINKER),
              'compilerSha256': sha256(proof.compiler.COMPILER), 'compilerFlags': proof.FLAGS,
              'sourceCredit': 0, 'cases': len(records), 'actualOriginalAndSourceReturns': len(records) * 2,
              'syntheticComparatorSourceSha256': sha256(callback_source), 'syntheticComparatorObjectSha256': sha256(callback_obj),
              'hostProviders': 0, 'syntheticComparatorGameSourceCredit': 0, 'records': records,
              'limitations': ['The historical combined extent needs an explicit boundary migration before source acceptance',
                  'The fixture provides no additional registered source credit; legacy 348-byte acceptance remains rejected',
                  'Synthetic signed-byte comparator is compiled test context, not an original game callback',
                  'Unsupported indirect entry into the final eight bytes has not been universally excluded']}
    write_json(ROOT / 'evidence/functional/main-heap-sort-exact-candidate-20261030.json', report)
    print({'cases': len(records), 'actualReturns': len(records) * 2, 'exact356Bytes': linked == native, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
