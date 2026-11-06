import gzip
import json
from pathlib import Path
import sys
import arm7_lane_spi_native_20261031 as native
import link_arm7_spi_hypotheses_20261031 as compiler
from project import ROOT, sha256, write_json

REPORT = ROOT / 'evidence/arm7/lane-spi-functional1204-20261031.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def main():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned synthetic native/compiler execution runtime differs')
    if sha256(ROOT / 'inputs/game.nds') != ROM:
        raise ValueError('Measured original ROM changed')
    raw = (ROOT / native.MODULE).read_bytes()
    if native.digest(raw) != native.MODULE_SHA:
        raise ValueError('Measured child module changed')
    rows = json.loads(compiler.PROFILE.read_text())['results']
    results, controls = [], []

    def rejection(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid functional source context accepted: ' + name)

    for row in rows:
        address = int(row['address'], 0)
        spec = native.SPECS[address]
        original = raw[address - native.BASE:address - native.BASE + spec['bytes']]
        proof, rebuilt = compiler.build(row)
        offsets = sorted(relocation['offset'] for relocation in proof['unchangedRelocations'])
        if offsets != [len(rebuilt) - 8, len(rebuilt) - 4]:
            raise ValueError('Compiled code/pool limit is not independently attributed')
        records, original_visited, compiled_visited = [], set(), set()
        scratch_differences = 0
        for seed, case in enumerate(native.cases(address)):
            expected = native.execute(address, original, case, seed)
            actual = native.execute(address, rebuilt, case, seed, virtual=True)
            if not expected['actualReturn'] or not actual['actualReturn'] or native.functional(expected) != native.functional(actual):
                raise ValueError('Original/real-MW-linked complete C routine functional behavior differs')
            first, second = expected['internalUnmatchedMachineState'], actual['internalUnmatchedMachineState']
            original_visited.update(first['visitedOwnInstructionOffsets'])
            compiled_visited.update(second['visitedOwnInstructionOffsets'])
            scratch_differences += first != second
            records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': 2,
                'functional': native.functional(expected), 'originalInternal': first, 'compiledInternal': second})
        raw_records = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
        compressed = gzip.compress(raw_records, mtime=0)
        trace = compiler.WORK / (row['address'][2:] + '-cases.json.gz')
        trace.write_bytes(compressed)
        unsupported = []
        for name, case, budget in (('permanent-raw-control-mask', dict(native.cases(address)[2], stuck=True), 1000),
            ('one-instruction-budget', dict(native.cases(address)[2]), 1)):
            first = native.execute(address, original, case, 0, budget=budget)
            second = native.execute(address, rebuilt, case, 0, virtual=True, budget=budget)
            if first['actualReturn'] or second['actualReturn']:
                raise ValueError('Unsupported bounded context received source return credit')
            unsupported.append({'name': name, 'original': first, 'compiled': second, 'returnCredit': 0, 'supportedErrorPathCredit': 0})
        results.append({'identity': {key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode', 'bytes')},
            'source': row['source'], 'sourceSha256': row['sourceSha256'], 'link': proof,
            'supportedCases': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
            'actualOriginalInstructionOffsetsVisited': sorted(original_visited), 'actualCompiledInstructionOffsetsVisited': sorted(compiled_visited),
            'internalStateDifferencesExplicitlyOutsideFunctionalClaim': scratch_differences,
            'caseTrace': {'path': trace.relative_to(ROOT).as_posix(), 'sha256': sha256(trace), 'compressedBytes': len(compressed),
                'rawSha256': native.digest(raw_records), 'rawBytes': len(raw_records), 'format': 'gzip JSON', 'gzipMtime': 0},
            'unsupported': unsupported, 'sourceMatchedBytes': 0, 'wholeModuleLinked': False})
        print(json.dumps({'address': row['address'], 'nativeBytes': row['bytes'], 'compiledBytes': len(rebuilt),
            'cases': len(records), 'returns': len(records) * 2, 'internalDifferenceCases': scratch_differences, 'exactCredit': 0}), flush=True)
    writers = [row for row in rows if native.SPECS[int(row['address'], 0)]['kind'] == 'emit']
    for row in writers:
        prior = dict(row, source=row['priorHypothesis'], sourceSha256=row['priorHypothesisSha256'])
        proof, wrong_body = compiler.build(prior, label='old-unmasked-clamp-' + row['address'][2:])
        case = {'address': 0x1234F0, 'count': 32, 'busyReadsPerPoll': 0, 'stuck': False}

        def old_clamp(address=int(row['address'], 0), wrong_body=wrong_body):
            state = native.execute(address, wrong_body, case, 0, virtual=True, budget=5000)
            if not state['actualReturn']:
                raise ValueError('Old typed clamp did not return in the bounded16-byte transfer context')

        rejection('old-u8-implicit-clamp-mask-lost-' + row['address'], old_clamp)
        controls[-1]['actualCompiledWrongSource'] = proof
    for path, expected in ((ROOT / 'inputs/game.nds', ROM), (ROOT / native.MODULE, native.MODULE_SHA)):
        if sha256(path) != expected:
            raise ValueError('Original input changed during functional proof')
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha256(__file__),
        'romSha256': ROM, 'inputModule': native.MODULE, 'inputModuleSha256': native.MODULE_SHA,
        'profile': compiler.PROFILE.relative_to(ROOT).as_posix(), 'profileSha256': sha256(compiler.PROFILE),
        'runtimeVersions': {'python': '.'.join(map(str, sys.version_info[:3])), 'unicorn': unicorn.__version__, 'pyelftools': elftools.__version__},
        'generatorSources': [{'path': Path(module.__file__).name, 'sha256': sha256(module.__file__)} for module in (native, compiler)],
        'results': results, 'actualOriginalAndCompiledReturns': sum(row['actualOriginalAndCompiledReturns'] for row in results),
        'controls': controls, 'allSupportedFunctionalCasesPassed': True, 'sourceMatchedBytes': 0, 'acceptedSourceCredit': 0,
        'compiledHypothesisFunctions': len(results), 'nativeInitializedBytesExamined': sum(row['identity']['bytes'] for row in results),
        'originalCodeOrAddendPatches': False, 'originalCodeDelegation': False, 'physicalDeviceExecutionCredit': 0,
        'functionalContract': 'R0, callee-saved registers, SP/LR/mode, complete data buffer and guards, ordered nonstack writes, status/data/source read counts and input traces',
        'explicitlyUnmatched': ['Caller-scratch R1/R2/R3/R12, APSR result flags, internal stack layout and instruction offsets are recorded but are not functional equivalence claims',
            'No byte/module/ROM source credit, complete game scene/caller reachability, physical peripheral, storage device or legality claim'],
        'busBoundary': {'control': hex(native.CONTROL), 'data': hex(native.DATA), 'width': 2,
            'suppliedInputs': 'Synthetic finite0/2-set-mask reads per polling group and independent received16-bit words; permanent-mask cases are bounded no-return controls'},
        'widthCorrection': 'Widened32-bit address requires explicit native low-byte masks for page remainder and command[2]; old typed writers remain preserved and fail controlled native-model comparisons'}
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': sha256(REPORT),
        'returns': report['actualOriginalAndCompiledReturns'], 'functions': len(results), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
