import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261029/batch03'
SOURCE = ROOT / 'src/scripts/20261029/batch03'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-runtime-decisions.json'
PINS = {
    'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
    'scr_c_compiler_20261029_v2.py': 'e88ddd56f388e97852293942d7f49cc8fab2f89c8bd4d19683c33811de565f2e',
    'match_scr_flags_20261029.py': 'b24e7262a7a42ccd7954d68d366be2644e662e7aa24ac7528462bc5fd21ca6b7',
    'match_scr_resets_20261029_batch02.py': '4761dc295ef8ddd5b66cab45c52a105548b397132535486d63da96bdd5a362ac',
    'src/scripts/20261029/s07e04_reset_flags.c': '2c430637c1bfa51fbc34d55c6a4204c004b1821ec6f883242e3f67e9160556bf',
    'src/scripts/20261029/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
    'scr_c_compiler_20261029_v3.py': '6b26e8a8639ff9cb1b43a37606577dcf80ec0b43aee2d636739c9ee7f6e30c9f',
    'src/scripts/20261029/batch03/scr_decision.h': '476823583e462d2fc5a90d2d43abc25301a73f4a284550012b9aa3f9bca097c1',
    'src/scripts/20261029/batch03/clear_primary_4_if_set.c': '539a8d3521ec23269b569153c1a2c2c01f178d570a65b909a994e02d1c27cff0',
    'src/scripts/20261029/batch03/clear_primary_539_if_set.c': '892560cb65e462fe8dddd2f770e2473d308e8f5e135f0fc9b15d0b079aa9df4a',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
    'nonmatching/script-source/20261029/native_scr_decision_20261029.py': '296cedbde145a05d3ecc4ba9eaeb2c2435d974b436ac7ea92d133e14a2eb6d63',
    'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
    'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_decision_20261029 as fixtures
import scr_c_compiler_20261029_v3 as compiler
import unicorn

IMAGES = (
    ('s05e02.e', 102, 4, 94, 'ee077a4568167bc1565a5285e970400cb146857bb73354e335319ef28c9e77ef',
     'dc121e7d6ca9c32d4253f87fdbe81bd0ea9bf0a7975a7d1f301599d242887722'),
    ('s04e14.e', 103, 539, 134, '52c2336f908473c0cb6571d345de29d02186a869eea90e0fca99e9b188d6439e',
     'ff91a66f89c8820af24992d529b3cbfb712d0497ba22498b7fdf37425e8b1df8'),
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()),
            'bytes': path.stat().st_size}


def load(name, entry, archive_hash, script_hash):
    data = assets.load(ROOT / 'extract/files' / name)
    assert data['assetSha256'] == archive_hash and data['scriptSha256'] == script_hash
    raw = (ROOT / data['asset']).read_bytes()
    members = []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                        'storedSha256': digest(stored), 'decodedSha256': digest(data['script'])})
    return data, members, data['entries'][entry]


def boundaries_and_storage(data, base, entry, slot):
    end = base + 176
    rows = data['instructions']
    owned = [row for row in rows if base <= row['pc'] < end]
    assert [row['opcode'] for row in owned] == [1036, 1045, 41, 1045, 1039, 1038, 1045, 1045, 42, 1036, 1026]
    assert sum(row['bytes'] for row in owned) == 176
    assert owned[0]['pc'] == base and owned[-1]['pc'] + owned[-1]['bytes'] == end
    assert [i for i, target in data['entries'].items() if target == base] == [entry]
    assert not any(base < target < end for target in data['entries'].values())
    incoming, references = [], []
    slot_word = compiler.fword(slot)
    for row in rows:
        args = row['argumentsRaw']
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038):
            target = args[1]
            if base <= target < end:
                incoming.append({'sourcePc': row['pc'], 'targetPc': target, 'opcode': row['opcode']})
                assert not (base < target < end and not base <= row['pc'] < end)
        pairs = []
        if row['opcode'] == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif row['opcode'] in range(1039, 1045):
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif row['opcode'] in range(1046, 1054):
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read'), (args[5], args[6], 'read')]
        elif row['opcode'] == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, value, access in pairs:
            if mode == 0 and value == slot_word:
                references.append({'pc': row['pc'], 'opcode': row['opcode'], 'access': access})
                assert base <= row['pc'] < end
    assert references == [{'pc': base + 44, 'opcode': 1045, 'access': 'write'},
                          {'pc': base + 68, 'opcode': 1039, 'access': 'read'}]
    return {'entry': entry, 'startPc': base, 'endExclusivePc': end, 'recordCount': 11,
            'privateReturnPc': end - 4, 'knownIncomingDirectReferences': incoming,
            'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
            'runtimeVariable': {'name': 'was_set', 'slot': slot, 'vmByteOffset': 0x50 + slot * 4,
                                'knownDirectSlotReferences': references,
                                'opaqueNativeSysSlotEffectsExhaustivelyRuledOut': False},
            'unexecutedAdjacentBytes': {'bytes': 8, 'sha256': digest(data['code'][end:end + 8]), 'sourceCredit': 0},
            'indirectOrOpaqueOutsideControlFlowCoverageClaimed': False}


def build(data, base, flag, slot, name):
    directory = WORK / name / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    source_name = 'clear_primary_' + str(flag) + '_if_set.c'
    for source, target in ((ROOT / 'scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py'),
                           (ROOT / 'scr_c_compiler_20261029_v3.py', 'compiler_v3.py'),
                           (SOURCE / source_name, source_name), (SOURCE / 'scr_decision.h', 'scr_decision.h')):
        shutil.copyfile(source, directory / target)
    command = [sys.executable, str(directory / 'compiler_v3.py'), '--source', source_name, '--base', hex(base),
               '--local-base', str(slot), '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    report = json.loads((directory / 'build.json').read_text())
    assert len(body) == 176 and body == data['code'][base:base + 176]
    assert report['variableAllocations'] == [{'name': 'was_set', 'slot': slot, 'vmByteOffset': 0x50 + slot * 4,
                                             'sourceType': 'bool', 'vmRepresentation': 'binary32 zero or one'}]
    rebuilt = data['script'][:4100 + base] + body + data['script'][4100 + base + 176:]
    assert rebuilt == data['script']
    output = WORK / name / 'rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, body, {'command': command, 'cwd': str(directory), 'stdout': result.stdout.strip(),
                           'exitCode': result.returncode, 'build': report,
                           'sourceOnlyInputClosure': [artifact(directory / value) for value in
                               ('scr_c_compiler_20261029.py', 'compiler_v3.py', source_name, 'scr_decision.h')],
                           'originalBytecodeCompilerInput': False}, artifact(output)


def synthetic_else(body, initial_flag, seed):
    entries = [-1] * 1024
    entries[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *entries) + body
    o = fixtures.Oracle(seed, fixtures.native.PRIMARY)
    state = o.persistent()
    fixtures.native.bit_set(state, fixtures.native.PRIMARY, 4, bool(initial_flag))
    expected = bytearray(state)
    fixtures.native.bit_set(expected, fixtures.native.PRIMARY, 4, not initial_flag)
    o.u.mem_write(fixtures.native.PERSIST, bytes(state))
    o.u.mem_write(fixtures.native.CODE - 4100, script)
    assert o.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert o.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    o.u.mem_write(fixtures.native.CTX + 3, b'\0')
    trace = []
    for unused in range(20):
        pc = o.read(fixtures.native.CTX + 0x470)
        assert 0 <= pc < len(body)
        opcode = struct.unpack_from('<I', body, pc)[0]
        assert o.call(0x0204C5A0 if opcode >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': opcode, 'nextPc': o.read(fixtures.native.CTX + 0x470)})
        if not o.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise AssertionError('Synthetic structured else did not terminate')
    assert trace[-1]['opcode'] == 1026 and bytes(o.persistent()) == expected
    assert len(o.primary_writes) == 1
    return {'initialFlag': initial_flag, 'finalFlag': 1 - initial_flag, 'trace': trace,
            'actualReturningCalls': o.returning_calls, 'expectedPersistentSha256': digest(expected),
            'originalBytecodeInput': False, 'originalSourceCredit': 0}


def controls():
    directory = ROOT / 'nonmatching/script-source/20261029/batch03-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_decision.h', directory / 'scr_decision.h')
    text = (SOURCE / 'clear_primary_4_if_set.c').read_text()
    variants = {
        'invalid_get_index': text.replace('get_primary_flag(4)', 'get_primary_flag(1536)'),
        'invalid_set_boolean': text.replace('4, false', '4, 2'),
        'unknown_get_api': text.replace('get_primary_flag', 'unknown_getter'),
        'wrong_get_arity': text.replace('get_primary_flag(4)', 'get_primary_flag(4, 1)'),
        'undefined_runtime_condition': text.replace('if (was_set', 'if (unknown'),
        'invalid_runtime_constant': text.replace('was_set == true', 'was_set == 2'),
        'implicit_runtime_condition': text.replace('was_set == true', 'was_set'),
        'unsupported_runtime_arithmetic': text.replace('was_set == true', 'was_set + 1 == true'),
        'unknown_api_in_else': text.replace('    }\n}', '    } else { emit_opcode(42); }\n}'),
        'runtime_shadow': text.replace('bool was_set =', 'bool get_primary_flag ='),
        'unsupported_int_local': text.replace('bool was_set =', 'int was_set ='),
        'escaping_include': text.replace('"scr_decision.h"', '"../scr_decision.h"'),
        'duplicate_runtime_variable': text.replace('    if (', '    bool was_set = get_primary_flag(4);\n    if ('),
        'getter_entry_conflict': text.replace('clear_primary_4_if_set', 'get_primary_flag'),
    }
    tests = [(name, value, 57124, 94) for name, value in variants.items()]
    tests += [('invalid_local_base', text, 57124, 256), ('negative_local_base', text, 57124, -1),
              ('unaligned_function_base', text, 57126, 94),
              ('allocation_overflow', text.replace('    if (', '    bool other = get_primary_flag(4);\n    if ('), 57124, 255)]
    rejected = []
    for name, value, base, slot in tests:
        path = directory / (name + '.c')
        path.write_text(value, encoding='utf-8', newline='\n')
        try:
            compiler.compile_source(path, base, slot)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'base': base, 'localBase': slot,
                             'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported runtime source/profile accepted: ' + name)
    alternative = directory / 'explicit_else.c'
    alternative.write_text(text.replace('    }\n}', '    } else {\n        set_primary_flag(4, true);\n    }\n}'),
                           encoding='utf-8', newline='\n')
    body, report = compiler.compile_source(alternative, 0, 94)
    assert len(body) == 232
    positive = [synthetic_else(body, value, 2026103017000 + value) for value in (0, 1)]
    inverse = directory / 'inequality_else.c'
    inverse_text = text.replace('was_set == true', 'was_set != true').replace('4, false', '4, true')
    inverse.write_text(inverse_text.replace('    }\n}', '    } else {\n        set_primary_flag(4, false);\n    }\n}'),
                       encoding='utf-8', newline='\n')
    inverse_body, inverse_report = compiler.compile_source(inverse, 0, 94)
    assert len(inverse_body) == 232 and inverse_body != body
    inverse_cases = [synthetic_else(inverse_body, value, 2026103017100 + value) for value in (0, 1)]
    valid = SOURCE / 'clear_primary_4_if_set.c'
    original, unused = compiler.compile_source(valid, 57124, 94)
    wrong_slot, unused = compiler.compile_source(valid, 57124, 95)
    assert len(original) == len(wrong_slot) == 176 and original != wrong_slot
    sentinel = WORK / 'negative-cli.scrfunc'
    sentinel.write_bytes(b'unchanged-runtime-negative-output')
    report_path = WORK / 'negative-cli-report.json'
    report_path.write_bytes(b'unchanged-runtime-negative-report')
    command = [sys.executable, str(ROOT / 'scr_c_compiler_20261029_v3.py'), '--source', str(valid), '--base', '57124',
               '--local-base', '256', '--output', str(sentinel), '--report', str(report_path)]
    result = subprocess.run(command, cwd=WORK, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0 and sentinel.read_bytes() == b'unchanged-runtime-negative-output'
    assert report_path.read_bytes() == b'unchanged-runtime-negative-report'
    return {'rejectedSourcesOrProfiles': rejected, 'wrongAllocationProfileDoesNotMatchOriginal': True,
            'syntheticElseSource': artifact(alternative), 'syntheticElseBuild': report,
            'syntheticElseBothRuntimeBranches': positive, 'controlSourceCredit': 0,
            'syntheticInequalitySource': artifact(inverse), 'syntheticInequalityBuild': inverse_report,
            'syntheticInequalityBothRuntimeBranches': inverse_cases,
            'failedCliPreservesExistingOutputAndReport': True, 'failedCliExitCode': result.returncode}


def runtime_api_links():
    image = fixtures.native.MAIN
    result = {}
    for name, opcode in (('get_primary_flag', 41), ('set_primary_flag', 42)):
        address = 0x0205A68C + opcode * 4
        word = struct.unpack_from('<I', image, address - 0x02000000)[0]
        displacement = word & 0xFFFFFF
        if displacement & 0x800000:
            displacement -= 0x1000000
        case = address + 8 + displacement * 4
        calls = []
        for pc in range(case, case + 28, 4):
            instruction = struct.unpack_from('<I', image, pc - 0x02000000)[0]
            if instruction >> 24 == 0xEA:
                break
            if instruction >> 24 == 0xEB:
                value = instruction & 0xFFFFFF
                if value & 0x800000:
                    value -= 0x1000000
                calls.append(hex(pc + 8 + value * 4))
        assert len(calls) == 1
        result[name] = {'systemOpcode': opcode, 'nativeCasePc': hex(case), 'nativeWrapper': calls[0],
                        'nativeModuleSha256': fixtures.native.MAIN_HASH, 'nativeSourceCredit': 0,
                        'argument0': 'Exact binary32 index in0..1535',
                        'resultOrArgument1': 'Binary32 Boolean0/1; getter result is copied into the assigned VM scratch cell'}
    return result


def main():
    assert unicorn.__version__ == '2.1.4'
    for data, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                           (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                           (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(data) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    control = controls()
    modules, total_calls, total_machines = [], 0, 0
    rom, files = assets.original_files()
    for i, (name, entry, flag, slot, archive_hash, script_hash) in enumerate(IMAGES):
        data, members, base = load(name, entry, archive_hash, script_hash)
        boundary = boundaries_and_storage(data, base, entry, slot)
        rebuilt, body, source_build, output = build(data, base, flag, slot, name)
        original_result = fixtures.run(data['script'], base, entry, flag, slot, 2026103018000 + i * 1000)
        rebuilt_result = fixtures.run(rebuilt, base, entry, flag, slot, 2026103018000 + i * 1000)
        assert original_result == rebuilt_result
        total_calls += original_result['actualReturningCalls']
        total_machines += original_result['freshMachines']
        modules.append({'asset': data['asset'], 'archiveSha256': archive_hash, 'scriptSha256': script_hash,
                        'codeSha256': digest(data['code']), 'entryTableSha256': digest(data['script'][4:4100]),
                        'members': members, 'romFileRange': list(files[name]), 'boundaries': boundary,
                        'sourceOnlyBuild': source_build, 'matchedRange': {'startPc': base, 'endExclusivePc': base + 176,
                        'bytes': 176, 'sha256': digest(body)}, 'matchedSourceBytes': 176,
                        'originalScaffoldingBytes': len(rebuilt) - 176, 'scaffoldingSourceCredit': 0,
                        'rebuiltDecodedImage': output, 'rebuiltDecodedImageEqualsOriginal': True,
                        'completeImageReconstructed': False, 'differential': original_result})
    report = {'schemaVersion': 1, 'evidenceClass': 'ordinary-C-runtime-Boolean-SCR-decision-source-match',
              'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
              'reproductionCommand': 'python match_scr_decisions_20261029_batch03.py', 'romSha256': assets.ROM_HASH,
              'sourceClosure': [{'path': path, 'sha256': expected} for path, expected in PINS.items()],
              'sourceFunctionDefinitions': 2, 'completeFunctionInstances': 2, 'matchedScriptSourceBytes': 352,
              'imagesWithRecoveredRanges': 2, 'completeImagesRecovered': 0, 'ordinaryNativeExecutableByteCredit': 0,
              'actualReturningCallsPerImplementation': total_calls, 'actualReturningCallsTotal': total_calls * 2,
              'freshMachinesPerImplementation': total_machines, 'nativeFunctionStubs': 0,
              'namedRuntimeApiLinks': runtime_api_links(), 'allSupportedOriginalBranchOutcomesTested': True,
              'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
              'postFaultStateUsedForProof': False, 'modules': modules, 'compilerControls': control,
              'wholeRomSourceMatch': False,
              'limitations': ['Only two complete176-byte runtime decision routines receive source candidate credit',
                  'All other script/header/adjacent metadata, native VM/callees and archive compression remain zero-credit scaffolding',
                  'V3 supports Boolean getter-result declarations, Boolean-variable ==/!= constant conditions, structured if/else and constant flag setters only',
                  'Fixed VM scratch allocation is an explicit nonreentrant unit ABI; interleaved concurrent invocations and portable C thread-local semantics are not certified',
                  'Known direct slot accesses are local to each routine, without exhaustive opaque-SYS indirect access coverage',
                  'The native comparison ABI uses binary32 operands and VM predicate state, not a generic C integer-return helper binding',
                  'Synthetic else controls use generated fixture images and receive zero original recovered-byte credit',
                  'Runtime arithmetic, arbitrary C/C++/APIs and malformed native flag indices remain unsupported',
                  'No full image, story/quest meaning, live scene, travel, battle access or encounter renewability is inferred']}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': OUTPUT.relative_to(ROOT).as_posix(), 'completeFunctions': 2, 'scriptBytes': 352,
                      'actualReturns': total_calls * 2, 'freshMachinesPerImplementation': total_machines,
                      'negativeCompilerCases': len(control['rejectedSourcesOrProfiles']), 'completeImages': 0}))


if __name__ == '__main__':
    main()
