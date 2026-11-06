import importlib.util
import json
import sys
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json


ORACLE = ROOT / 'nonmatching/encounter/verify_20261029_threads.py'
ORACLE_SHA256 = '93b8b5c3f52a89022fbfe12f3ec6773eb33f673583e54e8d84aaf954bed446ac'
REPORT = ROOT / 'evidence/matches/encounter-20261029-threads.json'


def main():
    native_dependencies(configuration())
    if sha256(ORACLE) != ORACLE_SHA256:
        raise ValueError('Frozen thread oracle identity changed')
    sys.path.insert(0, str(ORACLE.parent))
    specification = importlib.util.spec_from_file_location('encounter_thread_oracle_20261029', ORACLE)
    oracle = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(oracle)
    oracle.main()
    report = read_json(REPORT)
    from recover_linked_runtime import qualified_bindings
    for entry in report['matches']:
        entry['nativeSymbolEntries'] = qualified_bindings(entry)
        for name, binding in entry['nativeSymbolEntries'].items():
            if name in report['nativeRuntimeHelperAliases']:
                binding['compilerRuntimeAbi'] = report['nativeRuntimeHelperAliases'][name]['abi']
        entry['ordinaryCBytes'] = entry['bytes']
        entry['justifiedAssemblyBytes'] = 0
    report['nativeSymbols'] = {relocation['symbol']: relocation['target']
                               for entry in report['matches'] for relocation in entry['relocations']}
    report['oracleGenerator'] = report['generator']
    report['oracleGeneratorSha256'] = report['generatorSha256']
    report['generator'] = 'match_encounter_20261029_threads.py'
    report['generatorSha256'] = sha256(ROOT / report['generator'])
    report['reproductionCommand'] = 'python match_encounter_20261029_threads.py'
    report['generatorSources'] = [{'path': report['generator'], 'sha256': report['generatorSha256']},
                                  {'path': ORACLE.relative_to(ROOT).as_posix(), 'sha256': ORACLE_SHA256},
                                  report['additionalFixtureGenerator']]
    write_json(REPORT, report)
    print(json.dumps({'functions': report['matchedFunctionCount'], 'bytes': report['matchedExecutableBytes'],
                      'actualReturns': report['actualReturningCallsTotal']}))


if __name__ == '__main__':
    main()
