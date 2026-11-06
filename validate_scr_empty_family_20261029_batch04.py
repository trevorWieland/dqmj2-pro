import argparse
import ast
import hashlib
import importlib.util
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MATCHER = 'match_scr_empty_family_20261029_batch04.py'
MATCHER_HASH = 'fbf1ac2bd718178b3dcc7d8d50c650a8ac11e7d23ddd2f044d2315146ac54f3c'
REPORT = 'evidence/matches/scripts-20261029-empty-family.json'
FAMILY = 'empty-void-SCR-entry'
SOURCE = 'src/scripts/20261029/batch02/before_primary_flag_reset.c'


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def local(root, name):
    path = (root / name).resolve()
    require(path.is_relative_to(root), 'Path escapes repository: ' + str(name))
    return path


def checked(root, item):
    path = local(root, item['path'])
    data = path.read_bytes()
    require(digest(data) == item['sha256'], 'Artifact hash: ' + str(path))
    if 'bytes' in item:
        require(len(data) == item['bytes'], 'Artifact length: ' + str(path))
    return path


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pins_from_matcher(root):
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets):
            pins = ast.literal_eval(node.value)
            for name, sha in pins.items():
                checked(root, {'path': name, 'sha256': sha})
            return pins
    raise ValueError('Missing frozen matcher pins')


def source_products(root, report):
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only command')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['inputClosure']}
    expected = {'build_scr_empty_family_20261029.py', 'scr_c_compiler_20261029.py',
                'scr_c_compiler_20261029_v3.py', 'before_primary_flag_reset.c', 'scr_flags.h'}
    require(set(inputs) == expected and len(build['inputClosure']) == 5, 'Exact source-only closure')
    pins = {item['path']: item['sha256'] for item in report['sourceClosure']}
    aliases = {'before_primary_flag_reset.c': SOURCE, 'scr_flags.h': 'src/scripts/20261029/batch03/scr_decision.h'}
    for name, path in inputs.items():
        require(digest(path.read_bytes()) == pins[aliases.get(name, name)], 'Copied source input')
    target_path = checked(root, build['targets'])
    generated_path = checked(root, build['generatedArtifact'])
    generated = json.loads(generated_path.read_text())
    require(generated['sourceClosure'] == build['build'], 'Recorded compiler closure')
    require(digest(canonical(build['build'])) == build['sourceClosureId'], 'Source closure identity')
    require(generated['originalBytecodeCompilerInput'] is False, 'Generated source-only identity')
    require(generated['newAuthoredImplementationFamilies'] == 0, 'Family novelty')
    require(generated['generatorSha256'] == pins['build_scr_empty_family_20261029.py'], 'Build driver identity')
    require(generated['targetsSha256'] == digest(target_path.read_bytes()), 'Layout input hash')
    closure = generated['sourceClosure']
    require(closure['sourceSha256'] == pins[SOURCE], 'Source definition identity')
    require(closure['includeSha256'] == pins[aliases['scr_flags.h']], 'Header identity')
    require(closure['compilerSha256'] == pins['scr_c_compiler_20261029_v3.py'], 'Compiler identity')
    require(closure['parserDependency']['sha256'] == pins['scr_c_compiler_20261029.py'], 'Parser identity')
    stage = root / 'work/script-source/20261029/batch04/empty-validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        shutil.copyfile(target_path, directory / 'targets.json')
        command = [sys.executable, 'build_scr_empty_family_20261029.py', '--source',
                   'before_primary_flag_reset.c', '--targets', 'targets.json', '--output', 'generated.json']
        subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=90, check=True)
        fresh = json.loads((directory / 'generated.json').read_text())
    require(fresh['compiledInstances'] == generated['compiledInstances'], 'Fresh source-only re-emission')
    products = {}
    for item in generated['compiledInstances']:
        key = item['scriptSha256'], item['startPc']
        require(key not in products, 'Duplicate emitted identity')
        body = bytes.fromhex(item['bodyHex'])
        require(len(body) == item['bytes'] == 16 and digest(body) == item['sha256'], 'Emitted body product')
        require(item['sourceFunction'] == 'before_primary_flag_reset' and item['sourceDefinitionFamily'] == FAMILY,
                'Emitted source definition')
        products[key] = body
    targets = json.loads(target_path.read_text())
    require(len(targets) == len(products) == 1109, 'Complete target/product population')
    require({(item['scriptSha256'], item['startPc']) for item in targets} == set(products), 'Layout/product identities')
    return products, build['sourceClosureId']


def native_case(case, row, ordinal):
    thread = ordinal % 4
    require(case['seed'] == 2026103020000 + ordinal and case['thread'] == thread, 'Fixture seed/thread')
    require(case['startPc'] == row['startPc'] and case['entryAliases'] == row['entryAliases'], 'Fixture range')
    require(case['launch'] == ('native-entry' if row['entryAliases'] else 'native-fork'), 'Native launch')
    require(case['scriptSteps'] == 2 and case['completeFunctionTerminated'] is True, 'Complete routine termination')
    require(case['persistentAndVmScratchUnchanged'] is True, 'Persistent and scratch effects')
    require(case['instructionCapPerNativeCall'] == 20000 and case['timeoutMicrosecondsPerNativeCall'] == 1000000,
            'Native fixture bounds')
    observations = case['observations']
    expected = [('0x204bc08', 1)]
    if row['entryAliases']:
        expected += [('0x204bd00', 1)] + [('0x204bed0', i) for i in range(1, thread + 1)]
    else:
        expected += [('0x204bed0', i) for i in range(thread + 1)]
    expected += [('0x204c5a0', 1), ('0x204c5a0', 1)]
    require(len(observations) == case['actualReturningCalls'] == thread + 4, 'Actual call population')
    for observation, (entry, result) in zip(observations, expected):
        require(observation['entry'] == entry and observation['resultWord'] == result, 'Native call ordering/result')
        require(observation['actualReturn'] is True and 0 < observation['instructions'] <= 20000, 'Actual bounded return')
        for field in ('registersSha256', 'orderedCpuStoresSha256', 'vmContextSha256',
                      'globalVmContextSha256', 'persistentSha256'):
            require(re.fullmatch('[0-9a-f]{64}', observation[field]) is not None, 'Native state digest')
    return digest(canonical(case))


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(sys.version_info[:3] == (3, 13, 5), 'Pinned Python version')
    pins = pins_from_matcher(root)
    native_inputs = {
        'extract/arm9/arm9.bin': 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f',
        'extract/arm9_overlays/ov000.bin': '783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6',
        'extract/arm9/itcm.bin': '69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb',
    }
    for name, sha in native_inputs.items():
        checked(root, {'path': name, 'sha256': sha})
    path = local(root, REPORT if report_path is None else report_path)
    report = json.loads(path.read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH, 'Frozen evidence generator')
    require(report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Frozen closure')
    require(report['sourceDefinitionUsed'] == SOURCE and report['sourceDefinitionSha256'] == pins[SOURCE], 'Shared C definition')
    for key in ('newAuthoredDefinitions', 'newImplementationFamilies', 'newSubstantiveDecisionLogicBytes',
                'completeImagesRecovered', 'ordinaryNativeExecutableByteCredit'):
        require(report[key] == 0, 'Credit scope: ' + key)
    require(report['nativeFunctionStubs'] == 0 and report['postFaultStateUsedForProof'] is False, 'Native proof scope')
    require(report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'State comparison scope')
    products, closure_id = source_products(root, report)
    auditor = load_module(root / 'audit_scr_v3_20261029_batch04.py', '_scr_empty_current_auditor')
    audit = auditor.audit()
    require(audit == report['frozenV3ExhaustionAudit'], 'Current inventory/direct-boundary audit')
    targets = {(item['asset'], item['startPc']): item for item in audit['newEmptyFunctionInstances']}
    assets = load_module(root / 'evidence/encounter/script_assets_20261029.py', '_scr_empty_current_assets')
    require(report['romSha256'] == assets.ROM_HASH, 'ROM identity')
    rom, files = assets.original_files()
    units, seen_products, seen_assets, ordinal, total_calls = {}, set(), set(), 0, 0
    definition = {'path': SOURCE, 'sha256': pins[SOURCE], 'function': 'before_primary_flag_reset', 'family': FAMILY}
    for module in report['modules']:
        asset = module['asset']
        require(asset not in seen_assets, 'Duplicate image')
        seen_assets.add(asset)
        data = assets.load(local(root, asset))
        for field in ('archiveSha256', 'scriptSha256'):
            require(module[field] == data['assetSha256' if field == 'archiveSha256' else field], 'Image identity')
        require(module['codeSha256'] == digest(data['code']), 'Code identity')
        require(module['entryTableSha256'] == digest(data['script'][4:4100]), 'Entry table identity')
        interval = files[Path(asset).name]
        require(module['romFileRange'] == list(interval), 'ROM interval')
        raw = local(root, asset).read_bytes()
        require(raw == rom[interval[0]:interval[1]], 'ROM-backed archive')
        require(len(module['members']) == assets.u32(raw, 4), 'Archive member population')
        for index, member in enumerate(module['members']):
            offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
            stored = raw[offset:offset + length]
            require(member == {'index': index, 'storedOffset': offset, 'storedBytes': length,
                    'storedSha256': digest(stored), 'scriptSha256': digest(data['script'])}, 'Member identity')
            require(assets.ash(stored) == data['script'], 'Member alias decoded bytes')
        ranges, cases = module['matchedRanges'], module['nativeDifferentialCases']
        require(len(ranges) == len(cases), 'Per-unit proof population')
        require(module['matchedBytes'] == len(ranges) * 16, 'Per-image matched bytes')
        require(module['originalScaffoldingBytes'] == len(data['script']) - len(ranges) * 16, 'Scaffolding accounting')
        require(module['scaffoldingSourceCredit'] == 0 and module['wholeImageReconstructed'] is False, 'Image credit scope')
        require(module['rebuiltDecodedImageEqualsOriginal'] is True, 'Decoded image equality record')
        for index, (row, case) in enumerate(zip(ranges, cases)):
            ordinal += 1
            base = row['startPc']
            target = targets[(asset, base)]
            key = module['codeSha256'], base
            product_key = data['scriptSha256'], base
            require(key not in units and product_key not in seen_products, 'Duplicate qualified range')
            seen_products.add(product_key)
            body = products[product_key]
            require(body == data['code'][base:base + 16] == struct.pack('<4I', 1036, 12, base + 12, 1026), 'Exact source bytes')
            require(row['endExclusivePc'] == base + 16 and row['bytes'] == 16 and row['sha256'] == digest(body), 'Range extent/hash')
            require(row['emittedBodyHex'] == body.hex() and row['scriptSha256'] == data['scriptSha256'], 'Qualified emitted body')
            require(row['mode'] == 'SCR' and row['vmHostProcessor'] == 'ARM9', 'Execution identity')
            require(row['sourceClosureId'] == closure_id and row['sourceImplementationFamily'] == FAMILY, 'Shared source identity')
            require(row['entryAliases'] == target['entryAliases'] and row['externalInteriorEntries'] == 0
                    and row['sharedReturnTailDetected'] is False, 'Complete private boundary')
            require(row['adjacentUnexecutedBytesSourceCredit'] == 0
                    and row['adjacentUnexecutedBytesSha256'] == digest(data['code'][base + 16:base + 24]), 'Adjacent scaffolding')
            observation_hash = native_case(case, row, ordinal)
            proof = row['nativeReturnEvidence']
            require(proof == {'moduleCaseIndex': index, 'seed': case['seed'], 'thread': case['thread'],
                    'actualReturningCalls': case['actualReturningCalls'], 'originalObservationSha256': observation_hash,
                    'rebuiltObservationSha256': observation_hash,
                    'comparisonRequiresAllObservedRegistersStoresAndStates': True}, 'Per-unit original/rebuilt proof')
            total_calls += case['actualReturningCalls']
            units[key] = {'codeSha256': key[0], 'startPc': base, 'endExclusivePc': base + 16,
                'bytes': 16, 'sha256': digest(body), 'scriptSha256': data['scriptSha256'], 'asset': asset,
                'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'entryAliases': row['entryAliases'],
                'sourceDefinition': definition, 'sourceClosureId': closure_id, 'newDefinitionCredit': 0,
                'newImplementationFamilyCredit': 0, 'substantiveDecisionLogicBytes': 0,
                'nativeReturnEvidence': proof, 'wholeImageReconstructed': False}
    require(set(products) == seen_products and len(units) == 1109 and len(seen_assets) == 113, 'Current qualified coverage')
    require(ordinal == report['completeFunctionInstances'] == report['freshMachinesPerImplementation'], 'Function population')
    require(total_calls == report['actualReturningCallsPerImplementation'] and total_calls * 2 == report['actualReturningCallsTotal'],
            'Total actual returns')
    require(report['qualifiedScriptRangeBytes'] == len(units) * 16, 'Total physical bytes')
    return units


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--report')
    options = parser.parse_args()
    units = validate(options.root, options.report)
    print(json.dumps({'validatedUnits': len(units), 'qualifiedBytes': sum(unit['bytes'] for unit in units.values()),
                      'sharedSourceDefinition': SOURCE, 'newAuthoredDefinitions': 0, 'newSubstantiveLogicBytes': 0}))


if __name__ == '__main__':
    main()
