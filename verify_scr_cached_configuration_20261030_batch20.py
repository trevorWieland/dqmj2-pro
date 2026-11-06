import ast
import copy
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
BASE = ROOT / 'validate_scr_runtime_configuration_20261030_batch19.py'
assert hashlib.sha256(BASE.read_bytes()).hexdigest() == '87d2bdf6c79dbc0fad5754d6c63426ab834545fe04203899e2ff4082959b70ab'
spec = importlib.util.spec_from_file_location('_cached_configuration_base', BASE)
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
require, checked, digest, local = legacy.require, legacy.checked, legacy.digest, legacy.local
MATCHER = 'match_scr_cached_configuration_20261030_batch20.py'
MATCHER_HASH = 'f56de7696bb9ae722aa929ae588587db20c567269eb508f3cdce47128ba08f52'
REPORT = 'evidence/encounter/scripts-cached-configuration-contexts-20261030.json'


def proof(report, module, data):
    native, fixture = module.fixtures.native, module.fixtures
    measured = report['differential']
    require(measured['freshMachines'] == len(measured['cases']) == 72 and measured['nativeInstructionCap'] == 20000
        and measured['nativeTimeoutMicroseconds'] == 1000000 and measured['scriptStepCap'] == 40 and measured['providerCount'] == 0
        and measured['originalConstructorAndResourceHelpersRetained'] is True and measured['cachedIdSyntheticContextOnly'] is True
        and measured['assetReadinessOrNaturalSceneReachabilityProven'] is False and measured['newSourceByteCredit'] == measured['newSourceDefinitionCredit'] == 0,
        'Qualified synthetic cache/retained-native scope')
    rows_seen, resource_results, calls, nested = set(), set(), 0, 0
    for ordinal, case in enumerate(measured['cases']):
        group, rest = divmod(ordinal, 36)
        thread_id, rest = divmod(rest, 18)
        free_index, rest = divmod(rest, 6)
        cache_index, enabled = divmod(rest, 2)
        thread, seed = (0, 3)[thread_id], 2026103035000 + ordinal
        unit = fixture.frozen.UNITS[group]
        entry, base, end, category, selected_slot = unit
        mode, free_rows = ('hit-first', 'hit-last', 'full-no-match')[cache_index], ((0,), (15,), (0, 1))[free_index]
        profile = fixture.frozen.profiles()[((free_index + cache_index) % 4) * 2 + enabled]
        require((case['entry'], case['thread'], case['seed'], case['cacheMode']) == (entry, thread, seed, mode)
            and case['profile'] == profile and case['freeRows'] == list(free_rows), 'Independent native cache/free-row profile')
        pool = bytearray(random.Random(seed ^ 0xB33).randbytes(16 * 0x10C))
        for index in range(16):
            pool[index * 0x10C + 0x105] = 0 if index in free_rows else (1, 255, 128, 2)[index % 4]
        cache = bytearray(random.Random(seed ^ 0xCA53).randbytes(16 * 0x30))
        for index in range(16):
            struct.pack_into('<I', cache, index * 0x30, 1000 + index if mode == 'full-no-match' else 0)
        if mode != 'full-no-match':
            struct.pack_into('<I', cache, (0 if mode == 'hit-first' else 15) * 0x30, (119, 190)[group])
        state = bytearray(random.Random(seed).randbytes(0x7040))
        native.bit_set(state, native.PRIMARY, profile['primaryIndex'], profile['enabled'])
        registers = bytearray(random.Random(seed ^ 0xC17).randbytes(1024))
        require(case['initialPoolSha256'] == digest(pool) and case['initialCacheSha256'] == digest(cache)
            and case['initialRegisterFileHex'] == registers.hex(), 'Exact independent randomized inputs')
        observed = case['observations']
        legacy.shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Natural native launch/forks')
        cursor = len(startup)
        instructions = {row['pc']: row for row in data['instructions'] if base <= row['pc'] < end}
        for iteration, name in enumerate(('first', 'second')):
            if iteration:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            part = case[name]
            chosen = next((index for index in range(16) if pool[index * 0x10C + 0x105] == 0), -1)
            require(part['poolBeforeHex'] == pool.hex() and part['chosenFirstFreeRow'] == chosen and part['rawResultWord'] == legacy.fword(chosen),
                'Actual first-free allocation and carried capacity exhaustion')
            raw_coordinates = profile['coordinates']
            coordinates = [legacy.conversion(raw) for raw in raw_coordinates]
            expected = [(0x70, 4, coordinates[0]), (0x74, 4, coordinates[1]), (0x78, 4, coordinates[2]), (0x88, 4, 0),
                (0x8C, 4, coordinates[3]), (0x90, 4, 0), (0x7C, 4, 4096), (0x80, 4, 4096), (0x84, 4, 4096), (0x106, 1, category),
                (0x107, 1, 2 if enabled else 0), (0x100, 2, 0xFFFF), (0x108, 1, 0), (0x105, 1, 1)] if chosen >= 0 else []
            stores = []
            for offset, size, value in expected:
                at = chosen * 0x10C + offset
                pool[at:at + size] = value.to_bytes(size, 'little')
                stores.append({'address': hex(fixture.POOL + at), 'bytes': size, 'value': value})
            resources = [] if chosen < 0 else [{'entry': '0x21df950', 'resourceId': (119, 190)[group], 'nativeReturnAddress': '0x2212d44',
                'actualNativeNestedReturn': True, 'resultWord': int(mode != 'full-no-match')}]
            require(part['orderedPoolStores'] == stores and part['poolAfterSha256'] == digest(pool) and part['cacheSha256'] == digest(cache)
                and part['resourceDataPointerWord'] == 0, 'Exact14-field pool writes/cache preservation/data-pointer qualification')
            require(part['resourceCalls'] == resources and part['constructorCalls'] == [{'entry': '0x2212c94',
                'words': [category, *coordinates, 2 if enabled else 0, 0, 0xFFFFFFFF]}], 'Real constructor and nested resource-return ABI')
            rows_seen.add(chosen)
            resource_results.update(row['resultWord'] for row in resources)
            nested += len(resources)
            require(part['initialRegisterFileHex'] == registers.hex(), 'Shared register-file carry')
            registers[92:108] = struct.pack('<4I', *raw_coordinates)
            struct.pack_into('<I', registers, selected_slot * 4, legacy.fword(enabled))
            module_stores = [{'address': hex(native.CTX + 0x50 + slot * 4), 'bytes': 4, 'value': value} for slot, value in
                list(zip((23, 24, 25, 26), raw_coordinates)) + [(selected_slot, legacy.fword(profile['primaryIndex'])), (selected_slot, legacy.fword(enabled))]]
            arguments = struct.pack('<7I', legacy.fword(chosen), *raw_coordinates, legacy.fword(2 if enabled else 0), legacy.fword(-1)) + bytes(36)
            require(part['finalRegisterFileSha256'] == digest(registers) and part['orderedModuleStores'] == module_stores
                and part['finalArgumentBankSha256'] == digest(arguments) and part['persistentSha256'] == digest(state)
                and part['allOther251SlotsPreserved'] is True and part['actualAssetReadinessProven'] is False, 'Exact shared/argument/persistent state with no asset claim')
            pc, trace = base, []
            while True:
                row = instructions[pc]
                op, raw = row['opcode'], row['argumentsRaw']
                following = raw[1] if op == 1036 or op == 1038 and enabled else pc + row['bytes']
                if op == 1026:
                    following = pc
                trace.append({'pc': pc, 'opcode': op, 'nextPc': following})
                require(len(trace) <= 40, 'Bounded full script trace')
                if op == 1026:
                    break
                pc = following
            require(part['trace'] == trace and part['completeOwnEntryReturned'] is True and part['privateReturnPc'] == end - 4
                and part['iteration'] == iteration, 'Whole private entry completion')
            for row, expected_trace in zip(observed[cursor:cursor + len(trace)], trace):
                require(row['entry'] == ('0x204c5a0' if expected_trace['opcode'] >= 1024 else '0x205a65c')
                    and row['resultWord'] == 1 and row['persistentSha256'] == digest(state), 'Actual bounded native VM returns')
            cursor += len(trace)
        require(cursor == len(observed) == case['actualReturningCalls'] == (49 if enabled else 45) + thread, 'Native root/fork/reentry accounting')
        calls += cursor
    require(measured['actualReturningCalls'] == calls == 3492 and measured['completeOwnEntryExecutions'] == 144
        and report['pairedNativeReturningCalls'] == 6984 and report['pairedCompleteOwnEntryExecutions'] == 288
        and report['pairedActualNestedResourceReturns'] == nested * 2 == 192, 'Separate root/complete/nested return counts')
    require(report['chosenRowCoverage'] == sorted(rows_seen) == [-1, 0, 1, 15] and report['nativeResourceReturnCoverage'] == sorted(resource_results) == [0, 1],
        'Record-allocation and real resource-return breadth')


def validate(report_path=REPORT):
    path = checked(ROOT, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(ROOT, {'path': name, 'sha256': pin})
    module = legacy.shared.helpers.load_module(path, '_cached_configuration_matcher')
    for filename, value in (('extract/arm9/arm9.bin', module.fixtures.native.MAIN_HASH), ('extract/arm9_overlays/ov000.bin', module.fixtures.native.OVERLAY_HASH),
            ('extract/arm9/itcm.bin', module.fixtures.native.ITCM_HASH)):
        checked(ROOT, {'path': filename, 'sha256': value})
    module.assets.original_files.cache_clear()
    data = module.assets.load(ROOT / 'extract/files/world.e')
    report = json.loads(local(ROOT, report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()] and report['evidenceClass'] ==
        'fresh-source-linked-existing-SCR-positive-record-allocation-cache-context-extension', 'Frozen source/context generator identity')
    require(report['romSha256'] == module.assets.ROM_HASH and report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
        and report['codeSha256'] == digest(data['code']) and report['nativeSourceRoot'] == str(ROOT) == str(module.fixtures.native.ROOT), 'Current original image/native-root provenance')
    require(report['nativeModuleHashes'] == {'main': module.fixtures.native.MAIN_HASH, 'overlay000': module.fixtures.native.OVERLAY_HASH, 'itcm': module.fixtures.native.ITCM_HASH},
        'Qualified current executable module namespace')
    require(report['boundariesAndStorage'] == [module.frozen.boundary(data, unit) for unit in module.fixtures.frozen.UNITS], 'Current bounded/shared source identities')
    build = report['sourceOnlyBuild']
    require(build['reusedSourceBytes'] == 1248 and build['newSourceByteCredit'] == build['newSourceDefinitionCredit'] == 0 and len(build['units']) == 2
        and checked(ROOT, build['rebuiltImage']).read_bytes() == data['script'], 'Reused source-only ranges/zero new credit')
    for unit, product in zip(module.fixtures.frozen.UNITS, build['units']):
        entry, base, end, category, unused = unit
        inputs = {Path(row['path']).name: checked(ROOT, row) for row in product['inputs']}
        require(len(inputs) == len(product['inputs']) == 5 and product['entry'] == entry and product['startPc'] == base and product['endExclusivePc'] == end
            and product['bytes'] == 624 and product['exitCode'] == 0 and product['originalBytecodeCompilerInput'] is False, 'Actual source-only closure/range')
        body = checked(ROOT, product['emittedBody']).read_bytes()
        compiled = json.loads(checked(ROOT, product['compilerReport']).read_text())
        require(body == data['code'][base:end] and product['sha256'] == digest(body) and compiled == product['compilerEvidence'], 'Complete freshly emitted body/report')
        for name, copied in inputs.items():
            origin = name if name.endswith('.py') else 'src/scripts/20261030/batch19/object' + str(category) + '/' + name
            require(digest(copied.read_bytes()) == pins[origin], 'Frozen reused source-only input')
        require(product['cwd'] == str(ROOT / 'work/script-source/20261030/batch20/cached-configuration' / ('source-only-' + str(category)))
            and product['command'] == [sys.executable, 'scr_c_compiler_20261030_v16.py', '--source', 'configure_primary_object' + str(category) + '.c',
            '--base', str(base), '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Explicit source-only command/CWD')
        stage = ROOT / 'work/script-source/20261030/batch20/validator'
        stage.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=stage) as temporary:
            directory = Path(temporary)
            for name, copied in inputs.items():
                shutil.copyfile(copied, directory / name)
            subprocess.run(product['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
            require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
                'Fresh independent source-only replay')
    proof(report, module, data)
    error = report['unsupportedControls'][0]
    require(len(report['unsupportedControls']) == 1 and error['diagnosticNativePc'] == '0x21df9a4' and error['errno'] == 6
        and error['completeEntryReturnCredit'] == error['postFaultStateCredit'] == error['sourceCredit'] == 0, 'Unsupported resource miss remains a failure')
    require(report['originalConstructorAndResourceHelpersRetained'] is True and report['providerCount'] == 0
        and report['recordAllocationDespiteResourceReturn0Observed'] is True and report['nativeAssetReadinessProven'] is False
        and report['naturalSceneOrAccessRenewalMeaningProven'] is False and report['wholeRomSourceMatch'] is False
        and all(report[key] == 0 for key in ('newSourceByteCredit', 'newSourceDefinitionCredit', 'newNativeByteCredit', 'completeImageCredit', 'postFaultStateCredit')),
        'Zero new source/native/asset/scene/post-fault credit')
    return report


def main():
    original = validate()
    directory = ROOT / 'work/script-source/20261030/batch20/negative-controls'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []
    tests = [('false-private-return', lambda r: r['differential']['cases'][0]['first'].update(completeOwnEntryReturned=False), 'Whole private entry completion'),
        ('wrong-first-row', lambda r: r['differential']['cases'][0]['first'].update(chosenFirstFreeRow=15), 'Actual first-free allocation'),
        ('wrong-record-byte', lambda r: r['differential']['cases'][0]['first']['orderedPoolStores'][0].update(value=1), 'Exact14-field pool writes'),
        ('factory-zero-as-failure-to-allocate', lambda r: r.update(recordAllocationDespiteResourceReturn0Observed=False), 'Zero new source/native/asset'),
        ('cached-ID-as-asset-proof', lambda r: r.update(nativeAssetReadinessProven=True), 'Zero new source/native/asset'),
        ('lost-nested-return', lambda r: r['differential']['cases'][0]['first']['resourceCalls'][0].update(actualNativeNestedReturn=False), 'Real constructor and nested resource-return ABI'),
        ('counter-as-complete-entry', lambda r: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate root/complete/nested return counts'),
        ('duplicate-source-credit', lambda r: r.update(newSourceByteCredit=1248), 'Zero new source/native/asset'),
        ('unsupported-post-fault-credit', lambda r: r['unsupportedControls'][0].update(postFaultStateCredit=1), 'Unsupported resource miss remains a failure'),
        ('cross-root-native-provenance', lambda r: r.update(nativeSourceRoot=str(ROOT.parent)), 'Current original image/native-root provenance')]
    for name, mutate, reason in tests:
        report = copy.deepcopy(original)
        mutate(report)
        path = directory / 'candidate.json'
        path.write_text(json.dumps(report))
        try:
            validate(path.relative_to(ROOT).as_posix())
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            require(reason in str(error), 'Unexpected control rejection: ' + str(error))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise AssertionError('Invalid cached configuration proof accepted')
    output = {'passed': True, 'controls': controls, 'completeEntries': 288, 'nativeReturns': 6984, 'nestedResourceReturns': 192,
        'newSourceByteCredit': 0, 'newSourceDefinitionCredit': 0, 'assetReadinessProven': False}
    target = ROOT / 'evidence/verification/scr-cached-configuration-contexts-20261030.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
