import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch14'
WORK = ROOT / 'work/script-source/20261030/batch14/byte-modes'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-byte-modes.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
    'scr_c_compiler_20261030_v12.py', 'nonmatching/script-source/20261029/native_scr_flags_20261029.py',
    'nonmatching/script-source/20261030/native_scr_byte_modes_20261030.py', 'evidence/encounter/script_assets_20261029.py',
    'evidence/encounter/vm_state_20261029.py', 'src/scripts/20261030/batch14/apply_primary_byte_modes.c',
    'src/scripts/20261030/batch14/scr_byte_mode.h', 'src/scripts/20261030/batch14/modes.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v12.py': '0452b7c010993dea523cf92fda01d72fc83a7a0aea318f33886fdc836c0bb271',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_byte_modes_20261030.py': '08cc66f2c761202b49d4a17fe0ba83677e3e4a90985f0b1277234a5ba39d4a68',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch14/apply_primary_byte_modes.c': '14e7e5ec2ce98fc448163f869e65568a0eacf5e825aab2992344e7692f3578c9',
 'src/scripts/20261030/batch14/scr_byte_mode.h': '289cf01611ce83f1c668dbecf66b9235a2a92e4841d90f63b6ede80e1e612cbb',
 'src/scripts/20261030/batch14/modes.bindings.json': '8cc7865465d92a5334323c0862fc81c65ea6bb12d5565ee1b0a58f38759323d9'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_byte_modes_20261030 as fixtures
import scr_c_compiler_20261030_v12 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [12]
    assert not any(base < pc < end for pc in data['entries'].values())
    own = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in own) == 1000 and own[-1]['pc'] == end - 4 and own[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in own) == 1
    incoming, references = [], []
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and base <= args[1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': args[1], 'opcode': op})
            assert not (base < args[1] < end and not base <= row['pc'] < end)
        pairs = []
        if op == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif 1039 <= op <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= op <= 1053:
            pairs = [(args[i], args[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)]
        elif op == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode != 0:
                continue
            slot = assets.f32(raw)
            assert slot == int(slot) and 0 <= slot < 256
            if int(slot) in (81, 82):
                assert base <= row['pc'] < end
                references.append({'pc': row['pc'], 'slot': int(slot), 'access': access})
    return {'entry': 12, 'startPc': base, 'endExclusivePc': end, 'bytes': 1000, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownSlotReferences': references, 'knownOutsideSlotReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'reachableOwnRecordPcs': [row['pc'] for row in own], 'serializedCompleteEntryDomainOnly': True,
        'opaqueNativeOrComputedSlotReferenceCoverageComplete': False, 'formalCopiedBeforeArgumentRegistersReused': True,
        'formalUnusedByOwnLogicButAbiCaptureRetained': True}


def native_contracts():
    image = fixtures.native.MAIN
    result = {'logicalIndexToNativeRow': list(fixtures.MAPPING), 'tableAddress': hex(fixtures.TABLE), 'tableBytes': 64,
        'sourceCredit': 0, 'module': 'main', 'processor': 'ARM9', 'mode': 'ARM', 'moduleSha256': fixtures.native.MAIN_HASH,
        'systemOpcode': 103, 'nativeWrapper': '0x2054c1c', 'nativeIndexMapper': '0x20725e8', 'nativeByteCopier': '0x20c1fdc'}
    instruction = struct.unpack_from('<I', image, 0x0205B6FC - 0x02000000)[0]
    offset = instruction & 0xFFFFFF
    offset -= 0x1000000 if offset & 0x800000 else 0
    assert instruction >> 24 == 0xEB and 0x0205B6FC + 8 + offset * 4 == 0x02054C1C
    result['dispatchCasePc'] = '0x205b6f8'
    return result


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in PIN_PATHS[:4]] + [('src/scripts/20261030/batch14/' + name, name)
        for name in ('apply_primary_byte_modes.c', 'scr_byte_mode.h', 'modes.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v12.py', '--source', 'apply_primary_byte_modes.c', '--base', hex(fixtures.BASE),
        '--bindings', 'modes.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    outcome = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END] and len(body) == 1000
    rebuilt = bytearray(data['script'])
    rebuilt[4100 + fixtures.BASE:4100 + fixtures.END] = body
    assert bytes(rebuilt) == data['script']
    target = WORK / 'world.source-byte-modes.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': outcome.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(target), 'originalBytecodeCompilerInput': False}


def mode_control(body, logical, mode):
    entries = [-1] * 1024
    entries[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *entries) + body
    seed = 2026103023000 + logical * 4 + mode
    oracle = fixtures.Oracle(seed)
    initial = bytes([0xA5]) * 72
    oracle.u.mem_write(fixtures.TABLE - 4, initial)
    persistent = bytes(oracle.persistent())
    oracle.u.mem_write(fixtures.native.CODE - 4100, script)
    assert oracle.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert oracle.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    oracle.u.mem_write(fixtures.native.CTX + 0x10, struct.pack('<I', 0x7FC12345))
    trace = []
    for unused in range(20):
        pc = oracle.read(fixtures.native.CTX + 0x470)
        op = struct.unpack_from('<I', body, pc)[0]
        assert oracle.call(0x0204C5A0 if op >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': op, 'nextPc': oracle.read(fixtures.native.CTX + 0x470)})
        if not oracle.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise ValueError('Synthetic mode control failed to terminate')
    row = fixtures.MAPPING[logical]
    expected = bytearray(initial)
    expected[4 + row * 4:8 + row * 4] = bytes(100 if lane == mode else 0 for lane in range(4))
    assert bytes(oracle.u.mem_read(fixtures.TABLE - 4, 72)) == expected
    assert bytes(oracle.persistent()) == persistent
    assert oracle.read(fixtures.native.CTX + 0x50) == 0x7FC12345
    return {'logicalIndex': logical, 'mode': mode, 'nativeRow': row, 'expectedGuardedRowsHex': expected.hex(),
        'trace': trace, 'observations': oracle.observations, 'actualReturningCalls': oracle.returning_calls,
        'orderedNativeByteStores': oracle.byte_stores, 'completeControlReturned': True, 'sourceCredit': 0}


def controls(profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch14-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_byte_mode.h', directory / 'scr_byte_mode.h')
    text = (SOURCE / 'apply_primary_byte_modes.c').read_text()
    tests = [('logical19', text.replace('select_context_byte_mode(2, 0)', 'select_context_byte_mode(19, 0)'), profile),
        ('negative_logical', text.replace('select_context_byte_mode(2, 0)', 'select_context_byte_mode(-1, 0)'), profile),
        ('mode4', text.replace('select_context_byte_mode(2, 0)', 'select_context_byte_mode(2, 4)'), profile),
        ('negative_mode', text.replace('select_context_byte_mode(2, 0)', 'select_context_byte_mode(2, -1)'), profile),
        ('wrong_arity', text.replace('select_context_byte_mode(2, 0)', 'select_context_byte_mode(2)'), profile),
        ('formal_alias', text, {'locals': {'saved_input': 81, 'enabled': 81}, 'globals': {}}),
        ('formal_slot256', text, {'locals': {'saved_input': 256, 'enabled': 82}, 'globals': {}}),
        ('uninitialized_flag', text.replace('bool enabled = get_primary_flag(207);', 'bool enabled;'), profile)]
    rejected, modes = [], []
    for name, content, bindings in tests:
        source = directory / (name + '.c')
        source.write_text(content)
        try:
            compiler.compile_source(source, fixtures.BASE, bindings)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(source), 'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported byte-mode source accepted: ' + name)
    for logical in range(19):
        for mode in range(4):
            source = directory / ('mode_' + str(logical) + '_' + str(mode) + '.c')
            source.write_text('#include "scr_byte_mode.h"\nvoid mode_control(float input)\n{\n    select_context_byte_mode(' + str(logical) + ', ' + str(mode) + ');\n}\n')
            body, evidence = compiler.compile_source(source, 0, {'locals': {'input': 0}, 'globals': {}})
            modes.append({'source': artifact(source), 'compilerEvidence': evidence, **mode_control(body, logical, mode)})
    return {'rejectedSourceProfiles': rejected, 'all76LogicalModeCases': modes, 'controlSourceCredit': 0,
        'modeControlNativeReturns': sum(case['actualReturningCalls'] for case in modes)}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS)
    for name, pin in PINS.items():
        assert digest((ROOT / name).read_bytes()) == pin, name
    data = assets.load(ROOT / 'extract/files/world.e')
    bounds = boundary(data)
    rebuilt, source_build = build(data)
    negative = controls(json.loads((SOURCE / 'modes.bindings.json').read_text()))
    print(json.dumps({'stage': 'source-only and76 mode controls passed', 'bytes': 1000}), flush=True)
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original complete', 'returns': original['actualReturningCalls']}), flush=True)
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled and original['executedOwnRecordPcs'] == bounds['reachableOwnRecordPcs']
    unused, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-primary-conditional-byte-mode-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()],
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END,
        'bytes': 1000, 'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds,
        'sourceOnlyBuild': source_build, 'nativeContracts': native_contracts(), 'compilerControls': negative, 'differential': original,
        'pairedCompleteOwnEntryExecutions': original['completeEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
        'separateModeControlNativeReturns': negative['modeControlNativeReturns'], 'sourceDefinitionCount': 1,
        'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 1000, 'originalScaffoldingBytes': len(rebuilt) - 1000,
        'scaffoldingSourceCredit': 0, 'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False,
        'wholeRomSourceMatch': False, 'limitations': ['Complete1000B entry12 only', 'Original native byte-mode APIs remain zero-credit dependencies',
            'Serialized direct-entry domain only; opaque/computed global program references unproved',
            'Formal captured as raw binary32 bits before argument reuse, unused by own source logic',
            'Raw byte rows/modes and primary IDs have no assigned story/area/access/renewability meaning']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 1000, 'completeEntries': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'controls': report['separateModeControlNativeReturns']}), flush=True)


if __name__ == '__main__':
    main()
