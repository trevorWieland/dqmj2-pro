import importlib.util
import json
from project import ROOT, configuration, native_dependencies, sha256, read_json, write_json


ORACLE = ROOT / 'nonmatching/encounter/verify_20261029_context.py'
ORACLE_SHA256 = '95f20f2568374a55f5471d28b017ff9fefe4933b1bf7a73c5327ccb13d9272a2'
SOURCE = 'src/encounter/20261029-context'
REPORT = ROOT / 'evidence/matches/encounter-20261029-context.json'


def main():
    native_dependencies(configuration())
    if sha256(ORACLE) != ORACLE_SHA256:
        raise ValueError('Frozen encounter oracle identity changed')
    specification = importlib.util.spec_from_file_location('encounter_context_oracle_20261029', ORACLE)
    oracle = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(oracle)
    oracle.SOURCE = SOURCE
    oracle.WORK = ROOT / 'work/encounter-recovery/20261029/accepted-replay'
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
    report['generator'] = 'match_encounter_20261029_context.py'
    report['generatorSha256'] = sha256(ROOT / report['generator'])
    report['generatorDependencies'].append({'path': ORACLE.relative_to(ROOT).as_posix(), 'sha256': ORACLE_SHA256})
    report['reproductionCommand'] = 'python match_encounter_20261029_context.py'
    report['acceptedSourceDirectory'] = SOURCE
    report['generatorSources'] = [{'path': report['generator'], 'sha256': report['generatorSha256']},
                                  {'path': ORACLE.relative_to(ROOT).as_posix(), 'sha256': ORACLE_SHA256}]
    write_json(REPORT, report)
    print(json.dumps({'functions': report['matchedFunctionCount'], 'bytes': report['matchedExecutableBytes'],
                      'actualReturns': report['actualReturningCallsTotal'], 'sourceDirectory': SOURCE}))


if __name__ == '__main__':
    main()
