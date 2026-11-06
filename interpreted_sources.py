from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256

REGISTRY = ROOT / 'interpreted-recovery.json'


def local(path):
    result = (ROOT / path).resolve()
    if not result.is_relative_to(ROOT.resolve()):
        raise ValueError('Interpreted source evidence escapes the private repository')
    return result


def validated(report, image, batch):
    if report['romSha256'] != configuration()['romSha256']:
        raise ValueError('Interpreted source belongs to a different ROM')
    identity = {'scriptSha256': report['inputScriptSha256'], 'codeSha256': report['inputCodeSha256'],
                'entryTableSha256': report['entryTableSha256']}
    if identity != batch['identity'] or any(image[key] != value for key, value in identity.items()):
        raise ValueError('Interpreted source identity differs from its inventoried program')
    for path, expected in batch['sourceHashes'].items():
        if not local(path).is_file() or sha256(local(path)) != expected:
            raise ValueError('Frozen interpreted source/compiler changed: ' + path)
    for item in report['sourceClosure']:
        if not local(item['path']).is_file() or sha256(local(item['path'])) != item['sha256']:
            raise ValueError('Interpreted source proof closure is stale')
    boundary, region = report['boundaries'], report['matchedRange']
    start, end = region['startPc'], region['endExclusivePc']
    size = end - start
    if not 0 <= start < end <= image['codeBytes'] or size != region['bytes']:
        raise ValueError('Interpreted source range lies outside measured code')
    expected_range = {'entrySlots': boundary['entrySlots'], 'startPc': start, 'endExclusivePc': end,
                      'bytes': size, 'sha256': region['sha256']}
    if expected_range != batch['range']:
        raise ValueError('Interpreted source range differs from its accepted unit')
    if boundary['startPc'] != start or boundary['endExclusivePc'] != end or boundary['completeRoutineBytes'] != size:
        raise ValueError('Interpreted function boundaries do not cover the complete unit')
    if boundary['externalDirectInteriorEntries'] or boundary['sharedTailDetected'] or boundary['embeddedDataInOwnedRange']:
        raise ValueError('Interpreted source boundary has unresolved direct sharing or embedded data')
    flags = ['memberAliasesAreNotSeparateSourceCredit', 'generatedBytecodeIsOutputOnly',
             'sourceExpressesLoopAndNamedCalls', 'rebuiltDecodedImageEqualsOriginal',
             'allGeneralRegistersAndCpsrCompared', 'orderedCpuStoresCompared', 'fullPersistentAndVmStateCompared']
    if not all(report.get(key) is True for key in flags):
        raise ValueError('Interpreted source proof does not satisfy its acceptance contract')
    if report['sourceLanguage'] not in ('C', 'C++', 'restricted C99') or report['nativeFunctionStubs'] or report['postFaultStateUsedForProof']:
        raise ValueError('Interpreted source language/execution evidence is unsupported')
    zeros = ['ordinaryNativeExecutableByteCredit', 'sourceCreditForScaffolding', 'scriptHeaderOrEntryTableSourceCredit',
             'completeImagesRecovered']
    if any(report.get(key) != 0 for key in zeros) or report['wholeImageDecompiled'] or report['wholeRomSourceMatch']:
        raise ValueError('Partial interpreted source claims scaffolding or complete-image credit')
    if report['originalScaffoldingBytes'] != image['decodedBytes'] - size or report['originalCodeScaffoldingBytes'] != image['codeBytes'] - size:
        raise ValueError('Interpreted scaffolding accounting differs from measured ranges')
    if report['matchedScriptSourceUnits'] != 1 or report['matchedScriptSourceBytes'] != size:
        raise ValueError('Interpreted source counts disagree with measured unit bytes')
    build = report['compilerBuild']
    if build['exitCode'] or build['originalRomOrBytecodeInputToCompiler'] is not False:
        raise ValueError('Interpreted compiler requires original bytecode or did not succeed')
    compiled = build['build']
    if compiled['outputBytes'] != size or compiled['outputSha256'] != region['sha256'] or compiled['functionBase'] != start:
        raise ValueError('Interpreted compiler output differs from the accepted range')
    expected_inputs = {compiled['sourceSha256'], compiled['includeSha256'], compiled['compilerSha256']}
    if len(build['compilerInputClosure']) != 3 or {item['sha256'] for item in build['compilerInputClosure']} != expected_inputs:
        raise ValueError('Source-only compiler input closure is not the declared source/header/compiler')
    if not expected_inputs.issubset(set(batch['sourceHashes'].values())):
        raise ValueError('Compiler source input is not frozen in the accepted unit')
    modules = {row['name']: row['sha256'] for row in read_json(ROOT / 'provenance/seed-manifest.json')['modules']}
    if set(report['nativeModuleHashes']) != {'main', 'ov000', 'itcm'} or any(modules.get(name) != expected for name, expected in report['nativeModuleHashes'].items()):
        raise ValueError('Native VM evidence uses a different module identity')
    if not compiled['pythonVersion'].startswith('3.13.5 ') or compiled['pythonExecutableSha256'] != sha256(Path(sys.executable)):
        raise ValueError('Interpreted compiler Python identity differs')
    differential = report['differential']
    if not differential['allCountedCallsReachReturnSentinel'] or not differential['cases']:
        raise ValueError('Interpreted source has no complete returning native fixtures')
    if not all(case['completeFunctionTerminated'] for case in differential['cases']):
        raise ValueError('Interpreted source fixture stopped before the complete function returned')
    command = build['command']
    output = local(local(build['cwd']) / command[command.index('--output') + 1])
    product = local(report['rebuiltDecodedImage']['path'])
    if not output.is_file() or not product.is_file():
        return None
    emitted, decoded = output.read_bytes(), product.read_bytes()
    header_bytes = image['decodedBytes'] - image['codeBytes']
    if len(emitted) != size or sha256(output) != region['sha256']:
        raise ValueError('Interpreted generated output is stale')
    if len(decoded) != image['decodedBytes'] or sha256(product) != image['scriptSha256']:
        raise ValueError('Rebuilt decoded script differs from the measured image')
    if decoded[header_bytes + start:header_bytes + end] != emitted:
        raise ValueError('Interpreted compiler output was not used in the rebuilt image')
    for path in ('sourcePath', 'includePath', 'compilerPath'):
        expected = compiled[{'sourcePath': 'sourceSha256', 'includePath': 'includeSha256', 'compilerPath': 'compilerSha256'}[path]]
        if not local(compiled[path]).is_file():
            return None
        if sha256(local(compiled[path])) != expected:
            raise ValueError('Source-only compiler input copy changed')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(start),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
            'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': expected_range,
            'sourceLanguage': report['sourceLanguage'], 'function': compiled['function'],
            'sourceDefinitionId': compiled['sourceSha256'] + '/' + compiled['function'],
            'sourceByteCredit': size, 'sourceUnitCredit': 1, 'completeImageCredit': 0,
            'nativeByteCredit': 0, 'wholeImageControlFlowCertified': boundary['wholeImageControlFlowCertified'],
            'outsideIndirectTransfersExhaustivelyRuledOut': boundary['outsideOpaqueSysOrIndirectControlEffectsExhaustivelyRuledOut']}


def measure(inventory, registry=None):
    if registry is None and not REGISTRY.is_file():
        return [], []
    registry = read_json(REGISTRY) if registry is None else registry
    if registry['romSha256'] != inventory['romSha256']:
        raise ValueError('Interpreted source registry has a different ROM namespace')
    images = {image['codeSha256']: image for image in inventory['images']}
    units, unavailable, ranges, reports = [], [], {}, {}
    for batch in registry['batches']:
        if batch.get('proofKind') in ('grouped-empty-SCR-family-v4', 'grouped-context-captures-SCR-v4'):
            if batch['report'] not in reports:
                reports[batch['report']] = read_json(local(batch['report']))
            if batch['proofKind'] == 'grouped-empty-SCR-family-v4':
                from interpreted_empty_sources import measure as grouped_measure
            else:
                from interpreted_capture_sources import measure as grouped_measure
            grouped = grouped_measure(reports[batch['report']], inventory, batch)
            for unit in grouped:
                region = unit['range']
                spans = ranges.setdefault(unit['codeSha256'], [])
                if any(region['startPc'] < end and start < region['endExclusivePc'] for start, end in spans):
                    raise ValueError('Interpreted aliases or overlapping source units inflate coverage')
                spans.append((region['startPc'], region['endExclusivePc']))
                units.append(unit)
            continue
        image = images.get(batch['identity']['codeSha256'])
        if image is None:
            raise ValueError('Interpreted source registry references an uninventoried image')
        region = batch['range']
        spans = ranges.setdefault(image['codeSha256'], [])
        if any(region['startPc'] < end and start < region['endExclusivePc'] for start, end in spans):
            raise ValueError('Interpreted aliases or overlapping source units inflate coverage')
        spans.append((region['startPc'], region['endExclusivePc']))
        if batch['report'] not in reports:
            reports[batch['report']] = read_json(local(batch['report']))
        report = reports[batch['report']]
        if batch.get('proofKind') == 'source-linked-SCR-ranges-v2':
            from interpreted_linked_sources import validated as linked_validated
            unit = linked_validated(report, image, batch)
        elif batch.get('proofKind') == 'runtime-Boolean-SCR-v3':
            from interpreted_decision_sources import validated as decision_validated
            unit = decision_validated(report, image, batch)
        elif batch.get('proofKind') == 'nested-numeric-SCR-v4':
            from interpreted_numeric_sources import validated as numeric_validated
            unit = numeric_validated(report, image, batch)
        elif batch.get('proofKind') == 'nested-primary-SCR-v4':
            from interpreted_primary_sources import validated as primary_validated
            unit = primary_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-entry-original-calls-SCR-v5':
            from interpreted_entry_sources import validated as entry_validated
            unit = entry_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-world-state-SCR-v6':
            from interpreted_world_sources import validated as world_validated
            unit = world_validated(report, image, batch)
        elif batch.get('proofKind') == 'source-linked-world-reset-SCR-v7':
            from interpreted_reset_sources import validated as reset_validated
            unit = reset_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-primary24-formal-pair-SCR-v8':
            from interpreted_primary_pair_sources import validated as pair_validated
            unit = pair_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-bounded-selection-SCR-v9':
            from interpreted_bounded_selection_sources import validated as bounded_validated
            unit = bounded_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-runtime-primary-loop-SCR-v10':
            from interpreted_runtime_loop_sources import validated as loop_validated
            unit = loop_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-numeric-primary-context-words-SCR-v11':
            from interpreted_context_words_sources import validated as context_validated
            unit = context_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-primary-byte-modes-SCR-v12':
            from interpreted_byte_modes_sources import validated as modes_validated
            unit = modes_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-native-byte-row-configuration-SCR-v13':
            from interpreted_byte_rows_sources import validated as rows_validated
            unit = rows_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-registered-dynamic-primary-float-return-SCR-v14':
            from interpreted_registered_flags_sources import validated as registered_validated
            unit = registered_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-module-global-float-initializer-SCR-v15':
            from interpreted_registered_initializer_sources import validated as initializer_validated
            unit = initializer_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-shared-module-primary-configuration-SCR-v16':
            from interpreted_runtime_configuration_sources import validated as configuration_validated
            unit = configuration_validated(report, image, batch)
        elif batch.get('proofKind') == 'complete-native-record-capacity-decision-SCR-v17':
            from interpreted_record_capacity_sources import validated as capacity_validated
            unit = capacity_validated(report, image, batch)
        elif 'proofKind' in batch:
            raise ValueError('Unsupported interpreted source proof kind')
        else:
            unit = validated(report, image, batch)
        if unit is None:
            unavailable.append(batch['report'])
        else:
            units.append(unit)
    return units, unavailable
