from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local

KIND = 'source-linked-SCR-ranges-v2'


def require(value, message):
    if not value:
        raise ValueError(message)


def native_hashes():
    modules = {row['name']: row['sha256'] for row in read_json(ROOT / 'provenance/seed-manifest.json')['modules']}
    return {key: modules[key] for key in ('main', 'ov000', 'itcm')}


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    rows = []
    for module in report['modules']:
        for region in module['matchedRanges']:
            boundary = next(row for row in module['boundaries'] if row['startPc'] == region['startPc'])
            rows.append({'report': relative, 'reproduce': reproduction, 'proofKind': KIND,
                         'identity': {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
                         'range': {'entrySlots': [boundary['entry']], **{key: region[key] for key in
                                   ('startPc', 'endExclusivePc', 'bytes', 'sha256')}},
                         'sourceFunction': region['sourceFunction'], 'sourceHashes': hashes,
                         'nativeModuleHashes': native_hashes()})
    return rows


def check_report(report, batch):
    require(report['evidenceClass'] == 'ordinary-C-SCR-flag-resets-with-source-linked-empty-hooks',
            'Unsupported linked SCR source evidence class')
    require(report['romSha256'] == configuration()['romSha256'], 'Linked SCR source ROM differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Linked SCR native VM namespace differs')
    flags = ('archiveMemberAliasesGiveNoDuplicateCredit', 'allGeneralRegistersCpsrAndOrderedCpuStoresCompared',
             'persistentAndVmStateCompared', 'nativeVmAndItsCalleesExecuteUnmodified', 'newHeaderIsSeparateFromFrozenV1Header')
    require(all(report[key] is True for key in flags), 'Linked SCR execution proof is incomplete')
    require(not any(report[key] for key in ('nativeFunctionStubs', 'postFaultStateUsedForProof',
                'completeImagesRecovered', 'ordinaryNativeExecutableByteCredit', 'wholeRomSourceMatch')),
            'Linked SCR proof claims unsupported execution or source credit')
    expected = {row['path']: row['sha256'] for row in report['sourceClosure']}
    expected[report['generator']] = report['generatorSha256']
    require(expected == batch['sourceHashes'], 'Linked SCR proof closure differs from the frozen registry')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in expected.items()),
            'Frozen linked SCR source/compiler changed')
    modules = report['modules']
    require(len({row['codeSha256'] for row in modules}) == len(modules), 'Linked SCR image aliases inflate coverage')
    ranges = [region for module in modules for region in module['matchedRanges']]
    builds = [build['build'] for module in modules for build in module['sourceOnlyBuilds']]
    definitions = {(build['function'], build['sourceSha256']) for build in builds}
    require(report['sourceFunctionDefinitions'] == len(definitions), 'Authored SCR definition count differs')
    require(report['completeFunctionInstances'] == len(ranges), 'Linked SCR function-instance count differs')
    require(report['qualifiedRangeBytes'] == sum(row['bytes'] for row in ranges), 'Linked SCR qualified byte count differs')
    require(report['uniqueDecodedImagesWithRecoveredRanges'] == len(modules), 'Linked SCR image count differs')
    require(report['distinctEmittedBodyHashes'] == len({row['sha256'] for row in ranges}), 'Linked SCR body identities differ')
    calls = sum(module['differential']['actualReturningCalls'] for module in modules)
    require(report['actualReturningCallsPerImplementation'] == calls and report['actualReturningCallsTotal'] == 2 * calls,
            'Linked SCR return counts differ')
    require(report['freshMachinesPerImplementation'] == sum(module['differential']['freshMachines'] for module in modules),
            'Linked SCR machine counts differ')
    controls = report['compilerControls']
    require(controls['controlSourceCredit'] == 0 and len(controls['negativeCases']) >= 19,
            'Linked SCR compiler controls are incomplete')
    require(all(row['rejectedBeforeOutput'] for row in controls['negativeCases']), 'Invalid SCR source/link accepted')
    require(all(controls[key] is True for key in ('wrongAlignedBindingDoesNotMatchOriginal',
                'onlyCallTargetWordChangesWithBinding', 'frozenV1RejectsTheBroaderABI')), 'Linked SCR binding controls failed')


def check_build(build, region, batch):
    compiled = build['build']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False,
            'Linked SCR compilation failed or consumes original bytecode')
    require(compiled['function'] == region['sourceFunction'] and compiled['functionBase'] == region['startPc'],
            'Linked SCR compiler function/base differs')
    require(compiled['outputBytes'] == region['bytes'] and compiled['outputSha256'] == region['sha256'],
            'Linked SCR compiler product differs')
    require(compiled['pythonVersion'].startswith('3.13.5 ') and
            compiled['pythonExecutableSha256'] == sha256(Path(sys.executable)), 'Linked SCR Python identity differs')
    require(compiled['generalCCompilerClaimed'] is False and compiled['runtimeVariablesSupported'] is False,
            'Linked SCR backend support differs')
    inputs = build['sourceOnlyInputs']
    expected_names = {'compiler_v1.py', 'compiler_v2.py', 'before_primary_flag_reset.c',
                      'clear_primary_flags_after_hook.c', 'scr_flags.h', 'scr_calls.h'}
    require(len(inputs) == 6 and {local(row['path']).name for row in inputs} == expected_names,
            'Linked SCR compiler has unexpected input files')
    require(all(row['sha256'] in batch['sourceHashes'].values() for row in inputs),
            'Linked SCR compiler input is not frozen source')
    inputs_by_path = {local(row['path']): row for row in inputs}
    for path_key, hash_key in (('sourcePath', 'sourceSha256'), ('includePath', 'includeSha256'), ('compilerPath', 'compilerSha256')):
        path = local(compiled[path_key])
        require(path in inputs_by_path and inputs_by_path[path]['sha256'] == compiled[hash_key],
                'Linked SCR selected compiler/source/header is outside its source-only closure')
    cwd = local(build['cwd'])
    require(all(local(row['path']).parent == cwd for row in inputs), 'Linked SCR input copies escape their build directory')
    available = True
    for row in inputs:
        path = local(row['path'])
        if not path.is_file():
            available = False
        else:
            require(path.stat().st_size == row['bytes'] and sha256(path) == row['sha256'], 'Linked SCR copied input changed')
    command = build['command']
    require(command[0] == str(Path(sys.executable)) and local(command[1]) == local(compiled['compilerPath']),
            'Linked SCR compiler command differs')
    require(local(cwd / command[command.index('--source') + 1]) == local(compiled['sourcePath']),
            'Linked SCR compiler command selects different source')
    require(int(command[command.index('--base') + 1], 0) == region['startPc'], 'Linked SCR command base differs')
    output = local(cwd / command[command.index('--output') + 1])
    require(output.parent == cwd, 'Linked SCR product escapes its source-only build')
    if not output.is_file():
        available = False
    else:
        require(output.stat().st_size == region['bytes'] and sha256(output) == region['sha256'], 'Linked SCR emitted body is stale')
    return available, output


def validated(report, image, batch):
    check_report(report, batch)
    identity = batch['identity']
    require(all(image[key] == value for key, value in identity.items()), 'Linked SCR inventoried image identity differs')
    modules = [row for row in report['modules'] if all(row[key] == value for key, value in identity.items())]
    require(len(modules) == 1, 'Linked SCR unit image is missing or ambiguous')
    module = modules[0]
    regions = module['matchedRanges']
    require(module['matchedBytes'] == sum(row['bytes'] for row in regions), 'Linked SCR module range sum differs')
    require(module['originalScaffoldBytes'] == image['decodedBytes'] - module['matchedBytes'] and
            module['scaffoldingSourceCredit'] == 0 and module['completeImageReconstructed'] is False,
            'Linked SCR scaffolding accounting differs')
    require(module['rebuiltDecodedImageEqualsOriginal'] is True, 'Linked SCR reconstructed container differs')
    spans = sorted((row['startPc'], row['endExclusivePc']) for row in regions)
    require(all(0 <= start < end <= image['codeBytes'] for start, end in spans) and
            all(left[1] <= right[0] for left, right in zip(spans, spans[1:])), 'Linked SCR owned ranges overlap or escape code')
    builds = module['sourceOnlyBuilds']
    require(len(builds) == len(regions), 'Linked SCR source build count differs')
    available = True
    outputs = {}
    for region in regions:
        boundary = next(row for row in module['boundaries'] if row['startPc'] == region['startPc'])
        require(boundary['endExclusivePc'] == region['endExclusivePc'] and boundary['privateReturnPc'] == region['endExclusivePc'] - 4,
                'Linked SCR complete-function boundary differs')
        require(not boundary['externalInteriorEntries'] and not boundary['sharedReturnTailDetected'] and
                boundary['adjacentEightBytesSourceCredit'] == 0 and not boundary['indirectOrOpaqueOutsideControlFlowCoverageClaimed'],
                'Linked SCR boundary sharing or coverage claims are unresolved')
        require(not any(region['startPc'] < row['targetPc'] < region['endExclusivePc'] and
                        not region['startPc'] <= row['sourcePc'] < region['endExclusivePc']
                        for row in boundary['knownIncomingDirectReferences']), 'Linked SCR external branch enters a function interior')
        build = next(row for row in builds if row['build']['functionBase'] == region['startPc'])
        present, output = check_build(build, region, batch)
        outputs[region['startPc']] = output
        available = available and present
        if build['version'] == 'v2':
            binding = build['bindingInput']
            require('--bindings' in build['command'] and local(build['cwd']) / build['command'][build['command'].index('--bindings') + 1] == local(binding['path']),
                    'Linked SCR binding command differs')
            require(build['build']['bindingInput']['sha256'] == binding['sha256'], 'Linked SCR binding identity differs')
            for name, target in build['build']['scriptBindings'].items():
                require(any(row['sourceFunction'] == name and row['startPc'] == target for row in regions),
                        'Linked SCR named target has no reconstructed source unit')
            path = local(binding['path'])
            if not path.is_file():
                available = False
            else:
                require(sha256(path) == binding['sha256'] and read_json(path) == build['build']['scriptBindings'],
                        'Linked SCR binding file differs from its source links')
    differential = module['differential']
    cases, errors = differential['cases'], differential['supportedErrors']
    require(cases and all(case['completeSourceCallTreeTerminated'] for case in cases), 'Linked SCR function did not return')
    observed = [row for case in cases + errors for row in case['observations']]
    require(len(observed) == differential['actualReturningCalls'] and all(row['actualReturn'] for row in observed),
            'Linked SCR return evidence contains incomplete calls')
    require(all(case['trace'][-1]['depthAfter'] == 0 and
                sum(row['opcode'] == 1033 for row in case['trace']) == case['scriptCallReturnPairs'] for case in cases),
            'Linked SCR CALL/RET stack proof differs')
    decoded_path = local(module['rebuiltDecodedImage']['path'])
    if not decoded_path.is_file():
        available = False
    elif available:
        require(decoded_path.stat().st_size == image['decodedBytes'] and sha256(decoded_path) == image['scriptSha256'],
                'Linked SCR decoded product is stale')
        decoded = decoded_path.read_bytes()
        header_bytes = image['decodedBytes'] - image['codeBytes']
        require(all(decoded[header_bytes + row['startPc']:header_bytes + row['endExclusivePc']] ==
                    outputs[row['startPc']].read_bytes() for row in regions), 'Linked SCR emitted bodies were not linked into the image')
    require(available or not all(path.is_file() for path in outputs.values()) or not decoded_path.is_file() or
            any(not local(row['path']).is_file() for build in builds for row in build['sourceOnlyInputs']) or
            any(not local(build['bindingInput']['path']).is_file() for build in builds), 'Linked SCR evidence availability is inconsistent')
    region = next(row for row in regions if row['startPc'] == batch['range']['startPc'])
    boundary = next(row for row in module['boundaries'] if row['startPc'] == region['startPc'])
    expected_range = {'entrySlots': [boundary['entry']], **{key: region[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(expected_range == batch['range'] and region['sourceFunction'] == batch['sourceFunction'], 'Frozen linked SCR unit changed')
    if not available:
        return None
    build = next(row['build'] for row in builds if row['build']['functionBase'] == region['startPc'])
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(region['startPc']),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
            'sourceHashes': batch['sourceHashes'], 'range': expected_range, 'sourceLanguage': 'restricted C99',
            'function': build['function'], 'sourceDefinitionId': build['sourceSha256'] + '/' + build['function'],
            'sourceByteCredit': region['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0,
            'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False}
