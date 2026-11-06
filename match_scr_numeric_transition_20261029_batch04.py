import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261029/batch04'
WORK = ROOT / 'work/script-source/20261029/batch04/numeric-transition'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-numeric-transition.json'
PINS = {
    'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
    'scr_c_compiler_20261029_v2.py': 'e88ddd56f388e97852293942d7f49cc8fab2f89c8bd4d19683c33811de565f2e',
    'scr_c_compiler_20261029_v3.py': '6b26e8a8639ff9cb1b43a37606577dcf80ec0b43aee2d636739c9ee7f6e30c9f',
    'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
    'src/scripts/20261029/batch04/scr_numeric.h': 'dd9083a3b944895fa04c96a6dc41900e7d9d1923842f1f420ea253ff854a3bcf',
    'src/scripts/20261029/batch04/advance_numeric_nine.c': '5d92cace3f73a28d0f93be17709c410c41154789525d67698f28902bb3bcbddb',
    'src/scripts/20261029/batch04/numeric_nine.locals.json': '41373da4b45c7ac0fdbd056165460b705fccc4fe8fcbefceda466c1924fc657a',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
    'nonmatching/script-source/20261029/native_scr_numeric_20261029.py': 'd6e22c9055991030d0cd2f9a1667ed3d31236ffa07522cac0bf0a7ebf8b23fcd',
    'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
    'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_numeric_20261029 as fixtures
import scr_c_compiler_20261029_v4 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
            'sha256': digest(path.read_bytes())}


def input_image():
    data = assets.load(ROOT / 'extract/files/s07e01.e')
    assert data['assetSha256'] == '0eea1755d720f4544d974fa8bcaa66ba0d094ca92c72a1c1da5fc7218aef83ae'
    assert data['scriptSha256'] == 'f9aa89801c68b6f8c765a4162caa1540bace68c5928738621fd7890e41a050db'
    assert data['entries'][102] == fixtures.BASE
    raw = (ROOT / data['asset']).read_bytes()
    members = []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'offset': offset, 'bytes': length,
                        'storedSha256': digest(stored), 'scriptSha256': digest(data['script'])})
    return data, members


def boundaries_and_slots(data, allocation):
    base, end = fixtures.BASE, fixtures.BASE + 352
    owned = [row for row in data['instructions'] if base <= row['pc'] < end]
    expected = [1036, 1045, 1045, 39, 1045, 1045, 39, 1045, 1039, 1038,
                1039, 1038, 1039, 1038, 1045, 1045, 40, 1036, 1036, 1036, 1026]
    assert [row['opcode'] for row in owned] == expected and sum(row['bytes'] for row in owned) == 352
    assert [entry for entry, pc in data['entries'].items() if pc == base] == [102]
    assert not any(base < pc < end for pc in data['entries'].values())
    incoming, references = [], {slot: [] for slot in allocation.values()}
    bits = {compiler.fword(slot): slot for slot in allocation.values()}
    for row in data['instructions']:
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
            if mode == 0 and value in bits:
                references[bits[value]].append({'pc': row['pc'], 'access': access,
                                                'inside': base <= row['pc'] < end})
    for slot, rows in references.items():
        inside = [row for row in rows if row['inside']]
        outside = [row for row in rows if not row['inside']]
        assert [row['access'] for row in inside] == ['write', 'read']
        assert all(row['access'] == 'write' for row in outside)
        assert inside[0]['pc'] < base + 148
    return {'entry': 102, 'startPc': base, 'endExclusivePc': end, 'records': 21,
            'privateReturnPc': end - 4, 'knownDirectIncomingReferences': incoming,
            'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
            'namedScratchProfile': allocation, 'knownSlotReferences': references,
            'outsideWritesReconciled': 'Slots126/127 are reused by other procedures; this unit unconditionally overwrites every slot before any read',
            'knownOutsideReads': 0, 'opaqueSysIndirectSlotAccessCoverageClaimed': False,
            'interleavedOrReentrantABIClaimed': False,
            'adjacentUnexecutedBytesSha256': digest(data['code'][end:end + 8]), 'adjacentByteSourceCredit': 0}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py'),
             ('scr_c_compiler_20261029_v4.py', 'compiler_v4.py')]
    files += [('src/scripts/20261029/batch04/' + name, name) for name in
              ('advance_numeric_nine.c', 'scr_numeric.h', 'numeric_nine.locals.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, str(directory / 'compiler_v4.py'), '--source', 'advance_numeric_nine.c',
               '--base', hex(fixtures.BASE), '--locals', 'numeric_nine.locals.json',
               '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    report = json.loads((directory / 'build.json').read_text())
    assert len(body) == 352 and body == data['code'][fixtures.BASE:fixtures.BASE + 352]
    assert digest(body) == '05fb2c6b3e087b6c6e32ead277dc644ad3b3127764853eba394237a7d60161cd'
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.BASE + 352:]
    assert rebuilt == data['script']
    output = WORK / 's07e01.rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, report, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
                            'stdout': result.stdout.strip(), 'sourceOnlyInputClosure': [artifact(directory / name) for unused, name in files],
                            'originalBytecodeCompilerInput': False}, artifact(output)


def synthetic_numeric(body, initial, seed):
    entries = [-1] * 1024
    entries[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *entries) + body
    o = fixtures.Oracle(seed)
    state = o.persistent()
    state[fixtures.native.NUMERIC + 9 - fixtures.native.PERSIST] = initial
    expected = bytearray(state)
    expected[fixtures.native.NUMERIC + 9 - fixtures.native.PERSIST] = 3 if initial == 2 else 2
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
        raise AssertionError('Generated numeric if/else did not terminate')
    assert trace[-1]['opcode'] == 1026 and bytes(o.persistent()) == expected and len(o.numeric_writes) == 1
    return {'initialNumericNine': initial, 'finalNumericNine': expected[fixtures.native.NUMERIC + 9 - fixtures.native.PERSIST],
            'trace': trace, 'actualReturningCalls': o.returning_calls,
            'originalBytecodeInput': False, 'originalSourceCredit': 0}


def controls(allocation):
    directory = ROOT / 'nonmatching/script-source/20261029/batch04-numeric-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_numeric.h', directory / 'scr_numeric.h')
    text = (SOURCE / 'advance_numeric_nine.c').read_text()
    variants = {
        'invalid_context_index': text.replace('get_context_value(0)', 'get_context_value(8)'),
        'invalid_numeric_index': text.replace('get_numeric_state(0)', 'get_numeric_state(88)'),
        'invalid_numeric_set_index': text.replace('set_numeric_state(9, 3)', 'set_numeric_state(88, 3)'),
        'invalid_numeric_byte': text.replace('set_numeric_state(9, 3)', 'set_numeric_state(9, 256)'),
        'negative_numeric_byte': text.replace('set_numeric_state(9, 3)', 'set_numeric_state(9, -1)'),
        'wrong_getter_type': text.replace('float context_value', 'bool context_value'),
        'undeclared_variable': text.replace('context_value == 60', 'unknown == 60'),
        'nonexact_comparison_integer': text.replace('context_value == 60', 'context_value == 16777217'),
        'unsupported_arithmetic': text.replace('state_nine == 2', 'state_nine + 1 == 2'),
        'unsupported_api': text.replace('set_numeric_state', 'emit_opcode'),
        'escaping_include': text.replace('"scr_numeric.h"', '"../scr_numeric.h"'),
        'runtime_shadow': text.replace('float context_value', 'float get_context_value'),
        'uninitialized_runtime_if': text.replace('float context_value = get_context_value(0);', ''),
    }
    tests = [(name, value, dict(allocation)) for name, value in variants.items()]
    missing = dict(allocation)
    missing.pop('state_nine')
    duplicate = dict(allocation, state_nine=126)
    tests += [('missing_named_local', text, missing), ('duplicate_named_slots', text, duplicate),
              ('out_of_range_slot', text, dict(allocation, state_nine=256)),
              ('boolean_slot', text, dict(allocation, state_nine=False)),
              ('unused_named_slot', text, dict(allocation, unused=3))]
    rejected = []
    for name, value, profile in tests:
        path = directory / (name + '.c')
        path.write_text(value, encoding='utf-8', newline='\n')
        try:
            compiler.compile_source(path, fixtures.BASE, profile)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'profile': profile,
                             'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid scalar source/profile accepted: ' + name)
    synthetic = directory / 'numeric_else.c'
    synthetic.write_text('#include "scr_numeric.h"\nvoid numeric_else(void)\n{\n    float value = get_numeric_state(9);\n    if (value == 2) { set_numeric_state(9, 3); } else { set_numeric_state(9, 2); }\n}\n',
                         encoding='utf-8', newline='\n')
    body, build_report = compiler.compile_source(synthetic, 0, {'value': 5})
    assert len(body) == 232
    positive = [synthetic_numeric(body, value, 2026103025000 + value) for value in (0, 2, 3, 255)]
    valid = SOURCE / 'advance_numeric_nine.c'
    original, unused = compiler.compile_source(valid, fixtures.BASE, allocation)
    wrong, unused = compiler.compile_source(valid, fixtures.BASE, dict(allocation, context_value=134))
    assert len(original) == len(wrong) == 352 and original != wrong
    sentinel, report_path = WORK / 'negative-cli.bin', WORK / 'negative-cli.json'
    sentinel.write_bytes(b'unchanged-v4-output')
    report_path.write_bytes(b'unchanged-v4-report')
    invalid = directory / 'invalid-profile.json'
    invalid.write_text(json.dumps(missing))
    command = [sys.executable, str(ROOT / 'scr_c_compiler_20261029_v4.py'), '--source', str(valid),
               '--base', hex(fixtures.BASE), '--locals', str(invalid), '--output', str(sentinel), '--report', str(report_path)]
    result = subprocess.run(command, cwd=WORK, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0 and sentinel.read_bytes() == b'unchanged-v4-output'
    assert report_path.read_bytes() == b'unchanged-v4-report'
    return {'negativeSourcesOrProfiles': rejected, 'wrongNamedAllocationDoesNotMatchOriginal': True,
            'syntheticNumericElseSource': artifact(synthetic), 'syntheticNumericElseBuild': build_report,
            'syntheticNumericElseNativeCases': positive, 'controlSourceCredit': 0,
            'failedCliPreservesExistingOutputAndReport': True, 'failedCliExitCode': result.returncode}


def named_links():
    result = {'get_context_value': {'vmValueSourceKind': 3, 'bankByteOffset': '0x450', 'bankValues': 8,
              'nativeOperandReader': '0x0204bde0', 'representation': 'Unchanged input binary32 word', 'nativeSourceCredit': 0}}
    image = fixtures.native.MAIN
    for name, opcode in (('get_numeric_state', 39), ('set_numeric_state', 40)):
        address = 0x0205A68C + opcode * 4
        value = struct.unpack_from('<I', image, address - 0x02000000)[0] & 0xFFFFFF
        if value & 0x800000:
            value -= 0x1000000
        case = address + 8 + value * 4
        calls = []
        for pc in range(case, case + 28, 4):
            word = struct.unpack_from('<I', image, pc - 0x02000000)[0]
            if word >> 24 == 0xEA:
                break
            if word >> 24 == 0xEB:
                displacement = word & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 0x1000000
                calls.append(hex(pc + 8 + displacement * 4))
        assert len(calls) == 1
        result[name] = {'systemOpcode': opcode, 'nativeCasePc': hex(case), 'nativeWrapper': calls[0],
                        'nativeModuleSha256': fixtures.native.MAIN_HASH, 'nativeSourceCredit': 0,
                        'indices': '0..87', 'byteValues': '0..255 represented exactly as binary32'}
    return result


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                            (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    allocation = json.loads((SOURCE / 'numeric_nine.locals.json').read_text())
    data, members = input_image()
    boundary = boundaries_and_slots(data, allocation)
    rebuilt, source_report, command, output = build(data)
    control = controls(allocation)
    original = fixtures.run(data['script'])
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'evidenceClass': 'ordinary-C-complete-nested-numeric-state-transition-SCR-match',
              'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
              'reproductionCommand': 'python match_scr_numeric_transition_20261029_batch04.py',
              'sourceClosure': [{'path': path, 'sha256': expected} for path, expected in PINS.items()],
              'romSha256': assets.ROM_HASH, 'asset': data['asset'], 'archiveSha256': data['assetSha256'],
              'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
              'romFileRange': list(files['s07e01.e']), 'members': members,
              'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 352,
              'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.BASE + 352,
                               'bytes': 352, 'sha256': source_report['outputSha256']},
              'boundariesAndLocalStorage': boundary, 'sourceOnlyBuild': source_report, 'buildCommand': command,
              'namedRuntimeApiLinks': named_links(), 'compilerControls': control,
              'rebuiltDecodedImage': output, 'rebuiltDecodedImageEqualsOriginal': True,
              'originalScaffoldingBytes': len(rebuilt) - 352, 'scaffoldingSourceCredit': 0,
              'completeImagesRecovered': 0, 'ordinaryNativeExecutableByteCredit': 0,
              'actualReturningCallsPerImplementation': original['actualReturningCalls'],
              'actualReturningCallsTotal': original['actualReturningCalls'] * 2,
              'freshMachinesPerImplementation': original['freshMachines'], 'nativeFunctionStubs': 0,
              'allNestedBranchOutcomesTested': True, 'postFaultStateUsedForProof': False,
              'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
              'differential': original, 'wholeRomSourceMatch': False,
              'limitations': ['Only this complete352-byte procedure is reconstructed; other script/data/native/container bytes remain zero-credit scaffolding',
                  'Context0 is provided explicitly; no natural game producer/reachability for value60 or story/world meanings are established',
                  'Numeric state0 and9 are raw byte-plane indices, without labels imported from application assumptions',
                  'The source declares nonreentrant fixed-slot VM scratch; outside writes to126/127 are reconciled by unconditional initialization before reads',
                  'Opaque indirect slot access or interleaved invocation semantics remain uncertified',
                  'The restricted v4 supports typed getter declarations, exact-integer float comparisons, nested if/else and constant byte/Boolean setters',
                  'General C/C++, runtime arithmetic/reassignment, arbitrary APIs and malformed native index behavior are unsupported',
                  'No complete image, scene, access condition, battle eligibility, travel path or encounter renewability is certified']}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': OUTPUT.relative_to(ROOT).as_posix(), 'scriptBytes': 352,
                      'actualReturns': report['actualReturningCallsTotal'], 'freshMachinesPerImplementation': original['freshMachines'],
                      'negativeCompilerCases': len(control['negativeSourcesOrProfiles']), 'completeImages': 0}))


if __name__ == '__main__':
    main()
