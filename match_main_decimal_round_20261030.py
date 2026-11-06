from project import ROOT, configuration, sha256, write_json
import match_runtime as compiler
import link_runtime_unit as linker
from main_decimal_round_native_20261030 import execute, vectors
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-decimal-round-final-20261030'
SOURCE = ROOT / 'src/runtime/20261030_decimal_round/native_main_0201c2ec.c'


def main():
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', '3', 'off', True)
    assert len(rows) == 1
    row = rows[0]
    assert row['compiledBytes'] == 292 and row['exactAfterDeclaredRelocation']
    assert not row['relocations']
    row.update(ordinaryFunctionCredit=1, sourceLanguage='C', originalObjectScaffolding=False)
    directory = WORK / 'real-link'
    directory.mkdir(parents=True, exist_ok=True)
    proof = linker.validate(row, {}, directory)
    row['realMainLink'] = proof
    metadata, original, config = linker.measured_module('main')
    row['boundaries'] = dict(main_references(row, original, config), instructionBytes=292, literalPoolBytes=0, generatedLiteralOrPaddingBytes=0)
    rebuilt = bytearray(original)
    rebuilt[0x1C2EC:0x1C410] = (directory / 'caller.bin').read_bytes()
    results = []
    for tag, case in enumerate(vectors()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        results.append({'case': list(case), 'result': before})
        if len(results) % 500 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_decimal_round_20261030.py', 'main_decimal_round_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py', 'link_runtime_unit.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': [row],
              'matchedFunctions': 1, 'matchedBytes': 292, 'sourceCredit': 292, 'nativeSymbolEntries': {},
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'providedCalls': 0, 'independentRecordAndOrderedStoreModel': True,
                         'armAndThumbReturnContexts': True, 'rows': results},
              'limitations': ['Only this292-byte canonical routine receives source credit after acceptance',
                              'Record payloads are bounded to1..32 ASCII decimal digits with valid storage',
                              'At zero retained digits, tie parity reads the preceding length byte; no general numeric rounding contract is inferred',
                              'Signed exponent carry wraps as measured; padding and unrelated fields remain unchanged',
                              'Invalid record pointers, arbitrary malformed digits, source-only ROM and playable host game are not established']}
    path = ROOT / 'evidence/matches/main-decimal-round-20261030.json'
    write_json(path, report)
    print({'bytes': 292, 'actualReturns': len(results) * 2, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
