from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'runtime-Boolean-SCR-v3'


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    rows = []
    for module in report['modules']:
        rows.append({'report': relative, 'reproduce': reproduction, 'proofKind': KIND,
                     'identity': {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
                     'range': {'entrySlots': [module['boundaries']['entry']], **module['matchedRange']},
                     'sourceHashes': hashes, 'nativeModuleHashes': native_hashes()})
    return rows


def check_report(report, batch):
    require(report['evidenceClass'] == 'ordinary-C-runtime-Boolean-SCR-decision-source-match', 'Unsupported SCR decision evidence')
    require(report['romSha256'] == configuration()['romSha256'] and batch['nativeModuleHashes'] == native_hashes(),
            'SCR decision ROM/native namespace differs')
    expected = {row['path']: row['sha256'] for row in report['sourceClosure']}
    expected[report['generator']] = report['generatorSha256']
    require(expected == batch['sourceHashes'], 'SCR decision source closure differs from frozen registry')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in expected.items()),
            'SCR decision source/compiler changed')
    require(report['allSupportedOriginalBranchOutcomesTested'] is True and
            report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True,
            'SCR decision comparison/branch proof is incomplete')
    require(not any(report[key] for key in ('postFaultStateUsedForProof', 'ordinaryNativeExecutableByteCredit',
                'completeImagesRecovered', 'nativeFunctionStubs', 'wholeRomSourceMatch')), 'SCR decision claims unsupported credit')
    links = report['namedRuntimeApiLinks']
    require(set(links) == {'get_primary_flag', 'set_primary_flag'}, 'SCR decision has unqualified runtime APIs')
    for api, opcode, wrapper in (('get_primary_flag', 41, 0x02054980), ('set_primary_flag', 42, 0x020549D4)):
        row = links[api]
        require(row['systemOpcode'] == opcode and int(row['nativeWrapper'], 0) == wrapper and
                row['nativeModuleSha256'] == native_hashes()['main'] and row['nativeSourceCredit'] == 0,
                'SCR decision runtime API identity differs')
    modules = report['modules']
    require(len({row['codeSha256'] for row in modules}) == len(modules), 'SCR decision image aliases inflate counts')
    require(report['completeFunctionInstances'] == len(modules) == report['imagesWithRecoveredRanges'],
            'SCR decision instance/image count differs')
    require(report['matchedScriptSourceBytes'] == sum(row['matchedRange']['bytes'] for row in modules),
            'SCR decision qualified byte count differs')
    definitions = {(row['sourceOnlyBuild']['build']['function'], row['sourceOnlyBuild']['build']['sourceSha256']) for row in modules}
    require(report['sourceFunctionDefinitions'] == len(definitions), 'SCR decision authored-definition count differs')
    calls = sum(row['differential']['actualReturningCalls'] for row in modules)
    require(report['actualReturningCallsPerImplementation'] == calls and report['actualReturningCallsTotal'] == 2 * calls,
            'SCR decision return count differs')
    require(report['freshMachinesPerImplementation'] == sum(row['differential']['freshMachines'] for row in modules),
            'SCR decision machine count differs')
    controls = report['compilerControls']
    require(len(controls['rejectedSourcesOrProfiles']) >= 18 and all(row['rejectedBeforeOutput'] for row in controls['rejectedSourcesOrProfiles']),
            'SCR decision invalid source/profile control failed')
    require(controls['wrongAllocationProfileDoesNotMatchOriginal'] and controls['failedCliPreservesExistingOutputAndReport'] and
            controls['failedCliExitCode'] != 0 and controls['controlSourceCredit'] == 0, 'SCR decision allocation/CLI controls failed')
    for key in ('syntheticElseBothRuntimeBranches', 'syntheticInequalityBothRuntimeBranches'):
        require(len(controls[key]) == 2 and all(row['actualReturningCalls'] > 0 and not row['originalBytecodeInput'] and
                row['originalSourceCredit'] == 0 for row in controls[key]), 'SCR decision synthetic branches are not independently tested')


def validated(report, image, batch):
    check_report(report, batch)
    identity = batch['identity']
    require(all(image[key] == value for key, value in identity.items()), 'SCR decision image identity differs')
    module = next(row for row in report['modules'] if all(row[key] == value for key, value in identity.items()))
    region, boundary = module['matchedRange'], module['boundaries']
    start, end, size = region['startPc'], region['endExclusivePc'], region['bytes']
    require({'entrySlots': [boundary['entry']], **region} == batch['range'], 'SCR decision frozen range changed')
    require(0 <= start < end <= image['codeBytes'] and size == end - start == module['matchedSourceBytes'],
            'SCR decision owned range escapes code')
    require(boundary['startPc'] == start and boundary['endExclusivePc'] == end and boundary['privateReturnPc'] == end - 4,
            'SCR decision private boundary differs')
    require(boundary['externalInteriorEntries'] == 0 and boundary['sharedReturnTailDetected'] is False and
            boundary['unexecutedAdjacentBytes']['sourceCredit'] == 0 and boundary['indirectOrOpaqueOutsideControlFlowCoverageClaimed'] is False,
            'SCR decision has unresolved direct sharing or inflated coverage')
    require(not any(start < row['targetPc'] < end and not start <= row['sourcePc'] < end
                    for row in boundary['knownIncomingDirectReferences']), 'SCR decision external transfer enters an interior')
    require(module['originalScaffoldingBytes'] == image['decodedBytes'] - size and module['scaffoldingSourceCredit'] == 0 and
            module['completeImageReconstructed'] is False and module['rebuiltDecodedImageEqualsOriginal'] is True,
            'SCR decision scaffolding/image accounting differs')
    build, variable = module['sourceOnlyBuild'], boundary['runtimeVariable']
    compiled = build['build']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'SCR decision compiler failed or consumes bytecode')
    require(compiled['backend'] == 'restricted-C99-runtime-bool-SCR-v3' and compiled['outputBytes'] == size and
            compiled['outputSha256'] == region['sha256'] and compiled['functionBase'] == start, 'SCR decision compiler product differs')
    require(compiled['runtimeVariablesSupported'] == 'Boolean getter results only' and compiled['runtimeIfElseSupported'] is True and
            compiled['generalCCompilerClaimed'] is False and compiled['reentrantOrInterleavedInvocationSemanticsClaimed'] is False,
            'SCR decision compiler support/ABI claims differ')
    require(compiled['pythonVersion'].startswith('3.13.5 ') and compiled['pythonExecutableSha256'] == sha256(Path(sys.executable)),
            'SCR decision Python identity differs')
    allocations = compiled['variableAllocations']
    require(len(allocations) == 1 and allocations[0]['name'] == variable['name'] and
            allocations[0]['slot'] == compiled['localAllocationBase'] == variable['slot'] and
            allocations[0]['vmByteOffset'] == variable['vmByteOffset'] == 0x50 + 4 * variable['slot'],
            'SCR decision local allocation differs')
    references = variable['knownDirectSlotReferences']
    require(len(references) == 2 and {row['access'] for row in references} == {'write', 'read'} and
            all(start <= row['pc'] < end for row in references) and variable['opaqueNativeSysSlotEffectsExhaustivelyRuledOut'] is False,
            'SCR decision slot references or coverage differ')
    inputs = build['sourceOnlyInputClosure']
    require(len(inputs) == 4 and all(row['sha256'] in batch['sourceHashes'].values() for row in inputs),
            'SCR decision source-only closure has unexpected inputs')
    selected = [(compiled['sourcePath'], compiled['sourceSha256']), (compiled['includePath'], compiled['includeSha256']),
                (compiled['compilerPath'], compiled['compilerSha256']),
                (compiled['parserDependency']['path'], compiled['parserDependency']['sha256'])]
    require({(local(row['path']), row['sha256']) for row in inputs} == {(local(path), pin) for path, pin in selected},
            'SCR decision selected source/header/compiler/parser differs')
    cwd, command = local(build['cwd']), build['command']
    require(all(local(row['path']).parent == cwd for row in inputs), 'SCR decision input copies escape source-only build')
    require(command[0] == str(Path(sys.executable)) and local(command[1]) == local(compiled['compilerPath']) and
            local(cwd / command[command.index('--source') + 1]) == local(compiled['sourcePath']) and
            int(command[command.index('--base') + 1], 0) == start and
            int(command[command.index('--local-base') + 1], 0) == variable['slot'], 'SCR decision compile command differs')
    available = True
    for row in inputs:
        path = local(row['path'])
        if not path.is_file():
            available = False
        else:
            require(path.stat().st_size == row['bytes'] and sha256(path) == row['sha256'], 'SCR decision copied compiler input changed')
    output = local(cwd / command[command.index('--output') + 1])
    product = local(module['rebuiltDecodedImage']['path'])
    require(output.parent == cwd, 'SCR decision compiler output escapes build')
    if not output.is_file() or not product.is_file():
        available = False
    else:
        require(output.stat().st_size == size and sha256(output) == region['sha256'], 'SCR decision generated output is stale')
        require(product.stat().st_size == image['decodedBytes'] and sha256(product) == image['scriptSha256'], 'SCR decision decoded image differs')
        header = image['decodedBytes'] - image['codeBytes']
        require(product.read_bytes()[header + start:header + end] == output.read_bytes(), 'SCR decision emitted source was not used')
    differential = module['differential']
    require(differential['serializedCompleteCallsOnly'] is True and differential['interleavedOrReentrantScratchSemanticsCertified'] is False,
            'SCR decision scratch-call ABI differs')
    cases = differential['cases']
    require(cases and {row['thread'] for row in cases} == {0, 1, 2, 3} and {row['initialFlag'] for row in cases} == {0, 1},
            'SCR decision original branch/thread coverage differs')
    observed = [row for case in cases + differential['supportedErrors'] for row in case['observations']]
    require(len(observed) == differential['actualReturningCalls'] and all(row['actualReturn'] for row in observed),
            'SCR decision native return evidence is incomplete')
    for case in cases:
        require(case['independentSecondInvocationSeesClearedFlag'] is True, 'SCR decision repeated-state model differs')
        for index, key in enumerate(('first', 'second')):
            invocation = case[key]
            expected_flag = case['initialFlag'] if index == 0 else 0
            require(invocation['completeFunctionTerminated'] and invocation['initialFlag'] == expected_flag and
                    invocation['getterCalls'] == 1 and invocation['setterCalls'] == len(invocation['targetByteWrites']) == expected_flag and
                    invocation['runtimeBooleanSlotWord'] == (0x3F800000 if expected_flag else 0) and
                    invocation['trace'][-1]['pc'] == boundary['privateReturnPc'], 'SCR decision independent branch/effect model differs')
    if not available:
        return None
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(start),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
            'sourceHashes': batch['sourceHashes'], 'range': batch['range'], 'sourceLanguage': 'restricted C99',
            'function': compiled['function'], 'sourceDefinitionId': compiled['sourceSha256'] + '/' + compiled['function'],
            'sourceByteCredit': size, 'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0,
            'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
            'scratchCallAbi': 'serialized complete calls only'}
