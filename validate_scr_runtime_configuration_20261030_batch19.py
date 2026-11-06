import ast
import hashlib
import importlib.util
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / 'validate_scr_numeric_transition_20261029_batch04.py'
assert hashlib.sha256(SHARED.read_bytes()).hexdigest() == 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020'
SPEC = importlib.util.spec_from_file_location('_runtime_configuration_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_runtime_configuration_20261030_batch19.py'
MATCHER_HASH = '0311afc386e8fd86a2a3685fd82b3a2b136f4dbb9f86961e703d5d5167cd90e8'
REPORT = 'evidence/matches/scripts-20261030-runtime-configuration.json'


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def number(raw):
    return struct.unpack('<f', struct.pack('<I', raw))[0]


def conversion(raw):
    value = number(raw)
    require(math.isfinite(value) and abs(value) <= 4096, 'Qualified finite coordinate conversion domain')
    product = number(fword(value * 4096))
    return int(number(fword(product + (0.5 if value > 0 else -0.5)))) & 0xFFFFFFFF


def native_proof(report, matcher, data):
    proof, native = report['differential'], matcher.fixtures.native
    require(proof['freshMachines'] == len(proof['cases']) == 64 and proof['scriptStepCap'] == 40 and proof['nativeInstructionCap'] == 20000
        and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['providerCount'] == 0 and proof['originalConstructorRetained'] is True
        and proof['all16PoolRecordsNonzeroActiveRequired'] is True and proof['constructorCapacityExhaustedReturnOnly'] is True
        and proof['freePoolSuccessOrNaturalSceneReachabilityProven'] is False and proof['coordinateDomain'] == 'finite binary32 values with absolute value <=4096'
        and proof['primaryIndexDomain'] == [0, 1535] and proof['opaqueGlobalProgramReferenceCoverageComplete'] is False, 'Qualified full-pool/provider-free native domain')
    coordinates = ((0, 1, -1, 1.5), (0.125, -0.125, 0.0001, -0.0001),
        (0.0001220703125, -0.0001220703125, 4096, -4096), (-0.0, 0.0, 0.5, -0.5))
    outcomes, covered, counts = {}, {}, {261: 0, 273: 0}
    for ordinal, case in enumerate(proof['cases']):
        group, within = divmod(ordinal, 32)
        thread, profile_id = divmod(within, 8)
        unit = matcher.fixtures.UNITS[group]
        entry, base, end, category, selected_slot = unit
        seed = 2026103032000 + ordinal
        profile = {'coordinates': [fword(value) for value in coordinates[profile_id // 2]], 'primaryIndex': (0, 1535, 31, 32)[profile_id // 2],
            'enabled': bool(profile_id % 2)}
        require((case['entry'], case['thread'], case['seed']) == (entry, thread, seed) and case['profile'] == profile, 'Independent native category/branch/scalar profile')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        native.bit_set(state, native.PRIMARY, profile['primaryIndex'], profile['enabled'])
        persistent = digest(state)
        pool = bytearray(random.Random(seed ^ 0xB33).randbytes(16 * 0x10C))
        for index in range(16):
            pool[index * 0x10C + 0x105] = (1, 255, 128, 2)[index % 4]
        pool_hash = digest(pool)
        registers = bytearray(random.Random(seed ^ 0xC17).randbytes(1024))
        require(case['initialRegisterFileHex'] == registers.hex(), 'Random full module register-file live-in')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Actual original native start/forks')
        cursor = len(startup)
        instructions = {row['pc']: row for row in data['instructions'] if base <= row['pc'] < end}
        for iteration, name in enumerate(('first', 'second')):
            if iteration:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Actual original native reentry')
                cursor += 1
            part, pc, trace = case[name], base, []
            while True:
                row = instructions[pc]
                opcode, raw = row['opcode'], row['argumentsRaw']
                following = raw[1] if opcode == 1036 else (raw[1] if opcode == 1038 and profile['enabled'] else pc + row['bytes'])
                if opcode == 1026:
                    following = pc
                trace.append({'pc': pc, 'opcode': opcode, 'nextPc': following})
                if opcode == 1038:
                    outcomes.setdefault(pc, set()).add(bool(profile['enabled']))
                require(len(trace) <= 40, 'Complete independent configuration trace cap')
                if opcode == 1026:
                    break
                pc = following
            require(part['initialRegisterFileHex'] == registers.hex() and part['trace'] == trace and part['completeOwnEntryReturned'] is True
                and part['privateReturnPc'] == end - 4, 'Complete source-range private configuration return')
            words = [category, *[conversion(raw) for raw in profile['coordinates']], 2 if profile['enabled'] else 0, 0, 0xFFFFFFFF]
            require(part['constructorCalls'] == [{'entry': '0x2212c94', 'words': words}], 'Actual eight-word original constructor/scaled signed-coordinate ABI')
            stores = [{'address': hex(native.CTX + 0x50 + slot * 4), 'bytes': 4, 'value': raw} for slot, raw in
                list(zip((23, 24, 25, 26), profile['coordinates'])) + [(selected_slot, fword(profile['primaryIndex'])), (selected_slot, fword(profile['enabled']))]]
            registers[92:108] = struct.pack('<4I', *profile['coordinates'])
            struct.pack_into('<I', registers, selected_slot * 4, fword(profile['enabled']))
            args = struct.pack('<7I', fword(-1), *profile['coordinates'], fword(2 if profile['enabled'] else 0), fword(-1)) + bytes(36)
            require(part['orderedGlobalWordStores'] == stores and part['finalRegisterFileSha256'] == digest(registers)
                and part['allOther251SlotsPreserved'] is True and part['persistentSha256'] == persistent and part['unchangedFullPoolSha256'] == pool_hash,
                'Exact ordered shared-global/251-neighbor/persistent/full-pool effects')
            require(part['finalArgumentBankSha256'] == digest(args) and part['configurationResultRawWord'] == fword(-1), 'Actual capacity failure float return/argument clobbers')
            for row, expectation in zip(observed[cursor:cursor + len(trace)], trace):
                require(row['entry'] == ('0x204c5a0' if expectation['opcode'] >= 1024 else '0x205a65c') and row['resultWord'] == 1
                    and row['persistentSha256'] == persistent, 'Every actual native VM return/persistent state')
            covered.setdefault(entry, set()).update(row['pc'] for row in trace)
            cursor += len(trace)
        require(cursor == len(observed) == case['actualReturningCalls'] == (49 if profile['enabled'] else 45) + thread, 'Separate native startup/fork/reentry/record returns')
        counts[entry] += cursor
    require(all(values == {False, True} for values in outcomes.values()) and len(outcomes) == 2, 'Both outcomes of each primary decision')
    for unit in matcher.fixtures.UNITS:
        require(sorted(covered[unit[0]]) == matcher.boundary(data, unit)['allOwnRecordPcs'] and counts[unit[0]] == 1552, 'Full records and per-unit native counts')
    require(proof['actualReturningCalls'] == sum(counts.values()) == 3104 and proof['completeOwnEntryExecutions'] == 128
        and report['pairedCompleteOwnEntryExecutions'] == 256 and report['pairedNativeReturningCalls'] == 6208, 'Separate paired SCR/native execution totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_runtime_configuration_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH), ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
            ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-shared-module-primary-configuration-SCR-source-match' and report['generator'] == MATCHER
        and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] == [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen shared-configuration source closure')
    unused, files = matcher.assets.original_files()
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(files['world.e']) and report['archiveSha256'] == data['assetSha256']
        and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current original ROM/archive/image identity')
    require(report['boundariesAndStorage'] == [matcher.boundary(data, unit) for unit in matcher.fixtures.UNITS], 'Current complete/direct/shared module/argument boundaries')
    build = report['sourceOnlyBuild']
    require(build['originalBytecodeCompilerInput'] is False and len(build['units']) == 2 and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Two complete source ranges/current image')
    units = {}
    for unit, product in zip(matcher.fixtures.UNITS, build['units']):
        entry, base, end, category, slot = unit
        require(product['entry'] == entry and product['exitCode'] == 0 and product['originalBytecodeCompilerInput'] is False and product['cwd'] ==
            str(root / 'work/script-source/20261030/batch19/runtime-configuration' / ('source-only-' + str(category))) and product['command'] ==
            [sys.executable, 'scr_c_compiler_20261030_v16.py', '--source', 'configure_primary_object' + str(category) + '.c', '--base', str(base),
            '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only per-unit invocation')
        inputs = {Path(row['path']).name: checked(root, row) for row in product['inputs']}
        require(len(inputs) == len(product['inputs']) == 5, 'Five source-only configuration inputs')
        for name, copied in inputs.items():
            origin = name if name.endswith('.py') else 'src/scripts/20261030/batch19/object' + str(category) + '/' + name
            require(digest(copied.read_bytes()) == pins[origin], 'Copied frozen configuration input')
        body = checked(root, product['emittedBody']).read_bytes()
        compiled = json.loads(checked(root, product['compilerReport']).read_text())
        require(body == data['code'][base:end] and compiled == product['compilerEvidence'] and product['range'] ==
            {'startPc': base, 'endExclusivePc': end, 'bytes': 624, 'sha256': digest(body)}, 'Full624B source-only product')
        stage = root / 'work/script-source/20261030/batch19/validator'
        stage.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
            directory = Path(temporary)
            for name, copied in inputs.items():
                shutil.copyfile(copied, directory / name)
            subprocess.run(product['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
            require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
                'Fresh isolated configuration source-only rebuild')
        require(compiled['generalCCompilerClaimed'] is False and compiled['moduleAndArgumentObjectsAreNotPrivateLocals'] is True
            and compiled['dynamicPrimaryIndexRequiresQualifiedFiniteIntegerDomain'] == [0, 1535] and compiled['opaqueGlobalDomainProofClaimed'] is False,
            'Explicit shared/argument and qualified native language domain')
        instructions = {row['pc']: row for row in data['instructions'] if base <= row['pc'] < end}
        for access in compiled['objectAccesses']:
            row = instructions[access['instructionPc']]
            raw, opcode = row['argumentsRaw'], row['opcode']
            if access['access'] == 'write':
                require(opcode == 1045 and (raw[1], raw[2]) == (access['bank'], fword(access['slot'])), 'Actual compiler object write-PC qualification')
            else:
                operands = [(raw[3], raw[4])] if opcode == 1045 else [(raw[1], raw[2]), (raw[3], raw[4])] if opcode in (1039, 1040) else []
                require((access['bank'], fword(access['slot'])) in operands, 'Actual compiler object read-PC qualification')
        units[(digest(data['code']), base)] = {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'startPc': base,
            'endExclusivePc': end, 'bytes': 624, 'sha256': digest(body), 'entryAliases': [entry], 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
            'sourceSha256': compiled['sourceSha256'], 'function': compiled['function'], 'source': 'src/scripts/20261030/batch19/object' + str(category) + '/configure_primary_object' + str(category) + '.c',
            'pairedCompleteOwnEntryExecutions': 128, 'pairedNativeReturningCalls': 3104, 'wholeImageReconstructed': False,
            'moduleGlobalSlots': [23, 24, 25, 26, slot], 'argumentBankLiveIns': [0, 1, 2, 3, 4], 'argumentBankCallClobbers': list(range(7))}
    require(len(report['compilerControls']) == 10, 'Ten source/type/ABI/storage controls')
    for row in report['compilerControls']:
        source, header = checked(root, row['source']), checked(root, row['header'])
        require(header == source.parent / 'scr_runtime_configuration.h', 'Control include closure')
        try:
            matcher.compiler.compile_source(source, 11912, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source/type/ABI/storage rejection')
        else:
            raise ValueError('Unsupported configuration source compiled')
    native_proof(report, matcher, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 2 and report['implementationFamilyCount'] == 1
        and report['qualifiedScriptRangeBytes'] == 1248 and report['originalScaffoldingBytes'] == len(data['script']) - 1248, 'Two definitions/ranges with one implementation family')
    require(all(report[name] == 0 for name in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False and report['originalConstructorRetained'] is True
        and report['constructorCapacityExhaustedReturnOnly'] is True and report['freePoolSuccessOrNaturalSceneReachabilityProven'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Zero excess/provider/free-pool/post-fault credit')
    return units


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
