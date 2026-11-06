import ast
import hashlib
import importlib.util
import json
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / 'validate_scr_numeric_transition_20261029_batch04.py'
if hashlib.sha256(SHARED.read_bytes()).hexdigest() != 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020':
    raise ValueError('Frozen numeric validation helper')
spec = importlib.util.spec_from_file_location('_captures_validation_helpers', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_captures_20261029_batch06.py'
MATCHER_HASH = 'ae04eacaea7ad4c626bf028b84079d163b3065365d6ac18420ce4d8dc9164193'
REPORT = 'evidence/matches/scripts-20261029-captures.json'


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def native_case(case, unit, data, ordinal):
    thread, variant = case['thread'], case['variant']
    seed = 2026103036000 + ordinal
    require(case['seed'] == seed and case['startPc'] == unit['startPc'] and case['entryAliases'] == unit['entryAliases'], 'Native unit identity')
    state = bytearray(random.Random(seed).randbytes(0x7040))
    numeric_offset = 0x021C0DC8 - 0x021B9EB4
    for index in range(88):
        state[numeric_offset + index] = 0 if variant == 0 else 255 if variant == 1 else (index * 19 + 37) & 255
    contexts = [0x7FC12345, 0x80000000, 0x7F800000, 0xFF800000, 0, word(1), word(-1), 0xFFC54321]
    if variant == 1:
        contexts = [0xFFC45678, 0x3F800000, 0x80000000, 0x7FC00001, word(16777216), 0, word(255), word(60)]
    elif variant == 2:
        contexts = [word(60), 0xFF800000, word(-1), 0x7F800000, 0xFFC00001, 0x80000000, word(255), 0]
    require(case['rawContextWords'] == contexts, 'Raw binary32 signed-zero/NaN/infinity/finite profile')
    registers = bytearray(random.Random(seed ^ 0x736).randbytes(1024))
    for slot, (api, index) in zip(unit['namedAllocation'].values(), unit['apis']):
        value = contexts[index] if api == 'get_context_value' else word(state[numeric_offset + index])
        struct.pack_into('<I', registers, slot * 4, value)
    require(case['expectedVmRegisterFileSha256'] == digest(registers) and case['persistentSha256'] == digest(state),
            'All256 register slots and persistent-byte expectation')
    require(case['fixedSlotOutputsRemainAfterReturn'] is True and case['otherSlotsAndConditionPreserved'] is True
            and case['completeFunctionTerminated'] is True, 'Fixed-slot output and complete-return scope')
    require(case['nativeInstructionCap'] == 20000 and case['nativeTimeoutMicroseconds'] == 1000000, 'Native bounds')
    records = {row['pc']: row for row in data['instructions']}
    trace, pc = [], unit['startPc']
    while True:
        row = records[pc]
        require(row['opcode'] in (1036, 1045, 39, 1026), 'Straight capture instruction family')
        target = row['argumentsRaw'][1] if row['opcode'] == 1036 else pc if row['opcode'] == 1026 else pc + row['bytes']
        trace.append({'pc': pc, 'opcode': row['opcode'], 'nextPc': target})
        if row['opcode'] == 1026:
            break
        require(len(trace) < 16, 'Bounded complete capture')
        pc = target
    require(trace == case['trace'] and trace[-1]['pc'] == unit['endExclusivePc'] - 4, 'Full private-RET trace')
    expected = [('0x204bc08', 1)]
    if unit['entryAliases']:
        expected += [('0x204bd00', 1)] + [('0x204bed0', index) for index in range(1, thread + 1)]
    else:
        expected += [('0x204bed0', index) for index in range(thread + 1)]
    expected += [('0x205a65c' if row['opcode'] < 1024 else '0x204c5a0', 1) for row in trace]
    observed = case['observations']
    require(len(observed) == case['actualReturningCalls'] == len(expected), 'True native call population')
    shared.observations(observed)
    require([(item['entry'], item['resultWord']) for item in observed] == expected, 'Native call ordering/results')
    require(all(item['persistentSha256'] == digest(state) for item in observed), 'Read-only persistent ABI')
    return len(observed)


def source_products(root, report, manifest, pins):
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only build scope')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['sourceOnlyInputs']}
    aliases = {'scr_numeric.h': 'src/scripts/20261029/batch06/scr_numeric.h'}
    aliases.update({Path(family['source']).name: family['source'] for family in manifest['families']})
    require(len(inputs) == len(build['sourceOnlyInputs']) == 14, 'Complete source-only input closure')
    for name, path in inputs.items():
        require(digest(path.read_bytes()) == pins[aliases.get(name, name)], 'Copied source/compiler/header closure')
    layout_path, product_path = checked(root, build['layout']), checked(root, build['products'])
    products = json.loads(product_path.read_text())
    require(products['originalBytecodeCompilerInput'] is False and products['layoutSha256'] == digest(layout_path.read_bytes()),
            'Source-only layout/product identity')
    expected_layout = [{'scriptSha256': unit['scriptSha256'], 'startPc': unit['startPc'],
        'sourceName': Path(unit['source']).name, 'allocation': unit['namedAllocation']} for unit in manifest['units']]
    require(json.loads(layout_path.read_text()) == expected_layout, 'Exact qualified layout')
    stage = root / 'work/script-source/20261029/batch06/capture-validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        shutil.copyfile(layout_path, directory / 'layout.json')
        command = [sys.executable, 'build_scr_captures_20261029_batch06.py', '--layout', 'layout.json', '--output', 'fresh.json']
        subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=90, check=True)
        fresh = json.loads((directory / 'fresh.json').read_text())
    require(len(products['products']) == len(fresh['products']) == 115, 'Complete source product population')
    selected = {}
    for product, new in zip(products['products'], fresh['products']):
        for field in ('scriptSha256', 'startPc', 'sourceName', 'bodyHex', 'sha256', 'bytes'):
            require(product[field] == new[field], 'Fresh emitted product: ' + field)
        for field in ('sourceSha256', 'includeSha256', 'compilerSha256', 'function', 'functionBase',
                      'namedAllocationProfile', 'variableAllocations', 'namedApiCalls', 'generatedBranches', 'parsedAst',
                      'outputBytes', 'outputSha256'):
            require(product['compilerReport'][field] == new['compilerReport'][field], 'Fresh compiler evidence: ' + field)
        key = product['scriptSha256'], product['startPc']
        require(key not in selected, 'Duplicate source product')
        selected[key] = product
    return selected


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(sys.version_info[:3] == (3, 13, 5), 'Pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_captures_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Repository-local dependencies')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
                      ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Frozen proof closure')
    manifest = json.loads(checked(root, report['manifest']).read_text())
    current = json.loads(json.dumps(matcher.auditor.audit()))
    require(report['currentOutsideReferenceAudit'] == current, 'Current full reference/dominance inventory')
    approved = {(row['scriptSha256'], row['startPc']): row for row in current['instances'] if not row['unresolvedOutsideReads']}
    require(len(approved) == len(manifest['units']) == 115, 'Qualified current unit population')
    require(len(manifest['heldUnits']) == 1 and manifest['heldUnits'][0]['bytes'] == 128
            and len(manifest['heldUnits'][0]['unresolvedOutsideReads']) == 3, 'Held live-in unit remains excluded')
    require(report['heldUnits'] == manifest['heldUnits'] and report['heldUnitSourceCredit'] == 0, 'No held-unit credit')
    require(report['sourceDefinitionFamilies'] == manifest['families'] and report['newAuthoredDefinitions'] == 10
            and report['uniqueApiShapeFamilies'] == 6 and report['fixedSlotAbi'] == manifest['abi'], 'Copy-only family/ABI scope')
    products = source_products(root, report, manifest, pins)
    definitions = {family['name']: family for family in manifest['families']}
    manifest_units = {(unit['scriptSha256'], unit['startPc']): unit for unit in manifest['units']}
    require(set(products) == set(manifest_units) == set(approved), 'Exact source/inventory/range identities')
    rom, files = matcher.assets.original_files()
    require(report['romSha256'] == matcher.assets.ROM_HASH, 'Original ROM hash')
    result, seen_assets, calls, ordinal = {}, set(), 0, 0
    for module in report['modules']:
        asset = module['asset']
        require(asset not in seen_assets, 'Duplicate decoded image')
        seen_assets.add(asset)
        data = matcher.assets.load(root / asset)
        require(module['archiveSha256'] == data['assetSha256'] and module['scriptSha256'] == data['scriptSha256']
                and module['codeSha256'] == digest(data['code']) and module['entryTableSha256'] == digest(data['script'][4:4100]), 'Image hashes')
        interval = files[Path(asset).name]
        raw = (root / asset).read_bytes()
        require(module['romFileRange'] == list(interval) and raw == rom[interval[0]:interval[1]], 'ROM-backed archive')
        members = []
        for index in range(matcher.assets.u32(raw, 4)):
            offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
            stored = raw[offset:offset + length]
            require(matcher.assets.ash(stored) == data['script'], 'Member alias decoded bytes')
            members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                            'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
        require(module['members'] == members, 'Complete member alias population')
        measured_bytes = 0
        for row in module['matchedRanges']:
            identity = data['scriptSha256'], row['startPc']
            unit, qualified, product = manifest_units[identity], approved[identity], products[identity]
            base, end = row['startPc'], row['endExclusivePc']
            body = bytes.fromhex(product['bodyHex'])
            key = digest(data['code']), base
            require(key not in result and body == data['code'][base:end] and row['emittedBodyHex'] == body.hex()
                    and row['sha256'] == digest(body) == product['sha256'] and row['bytes'] == len(body), 'Exact current source body')
            require(end == unit['endExclusivePc'] and row['privateReturnPc'] == end - 4
                    and row['externalInteriorEntries'] == 0 and row['sharedReturnTailDetected'] is False, 'Full private boundary')
            aliases = [slot for slot, pc in data['entries'].items() if pc == base]
            require(row['entryAliases'] == aliases == unit['entryAliases'] and not any(base < pc < end for pc in data['entries'].values()), 'Direct table boundaries')
            for record in data['instructions']:
                if record['opcode'] in (1033, 1034, 1036, 1037, 1038):
                    require(not (base < record['argumentsRaw'][1] < end and not base <= record['pc'] < end), 'External interior transfer')
            require(row['mode'] == 'SCR' and row['vmHostProcessor'] == 'ARM9' and row['allocation'] == unit['namedAllocation']
                    and row['apis'] == unit['apis'] and row['source'] == unit['source'] and row['family'] == unit['family'], 'Source ABI identity')
            require(row['slotReferences'] == unit['slotReferences'] == qualified['slotReferences']
                    and row['unresolvedOutsideReads'] == [], 'Every known outside slot reference')
            for refs in row['slotReferences'].values():
                for ref in refs:
                    if ref['access'] == 'read' and not ref['inside']:
                        q = ref['outsideReadQualification']
                        require(q['allKnownReachingRootsInitializeBeforeRead'] is True and q['knownRootPaths']
                                and not any(path['hasPathWithoutKnownInitialization'] for path in q['knownRootPaths']), 'Outside-read initialization dominance')
            require([(case['thread'], case['variant']) for case in row['nativeCases']] ==
                    [(thread, variant) for thread in range(4) for variant in range(3)], 'All four threads/three profiles')
            for case in row['nativeCases']:
                ordinal += 1
                calls += native_case(case, unit, data, ordinal)
            definition = definitions[row['family']]
            result[key] = {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': asset,
                'startPc': base, 'endExclusivePc': end, 'bytes': len(body), 'sha256': digest(body), 'mode': 'SCR',
                'vmHostProcessor': 'ARM9', 'sourceDefinition': definition, 'source': row['source'], 'sourceFamily': row['family'],
                'entryAliases': aliases, 'substantiveDecisionLogicBytes': 0, 'copyOnly': True,
                'nativeScenarios': 12, 'wholeImageReconstructed': False}
            measured_bytes += len(body)
        require(module['originalScaffoldingBytes'] == len(data['script']) - measured_bytes and module['scaffoldingSourceCredit'] == 0
                and module['rebuiltDecodedImageEqualsOriginal'] is True and module['wholeImageReconstructed'] is False, 'Per-image source scope')
    require(len(result) == report['completeFunctionInstances'] == 115 and sum(row['bytes'] for row in result.values()) == report['qualifiedScriptRangeBytes'] == 7368,
            'Qualified capture totals')
    require(ordinal == report['freshMachinesPerImplementation'] == 1380 and calls == report['actualReturningCallsPerImplementation'] == 10482
            and report['actualReturningCallsTotal'] == 20964, 'Actual native return/machine totals')
    for key in ('newSubstantiveDecisionLogicBytes', 'nativeFunctionStubs', 'completeImagesRecovered', 'ordinaryNativeExecutableByteCredit'):
        require(report[key] == 0, 'Copy-only credit scope: ' + key)
    require(report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Native comparison scope')
    return result


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(unit['bytes'] for unit in units.values()),
                      'copyDefinitions': 10, 'apiShapes': 6, 'substantiveDecisionBytes': 0}))
