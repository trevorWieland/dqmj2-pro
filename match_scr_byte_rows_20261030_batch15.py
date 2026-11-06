import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch15'
WORK = ROOT / 'work/script-source/20261030/batch15/byte-rows'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-byte-rows.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v13.py',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py',
    'nonmatching/script-source/20261030/native_scr_byte_modes_20261030.py',
    'nonmatching/script-source/20261030/native_scr_byte_rows_20261030.py', 'evidence/encounter/script_assets_20261029.py',
    'evidence/encounter/vm_state_20261029.py', 'src/scripts/20261030/batch15/initialize_context_byte_rows.c',
    'src/scripts/20261030/batch15/scr_byte_rows.h')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v13.py': '1939e65b0a7cc49ea6c563e622f73713b032e427261380c83cb2e422a3a527d0',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_byte_modes_20261030.py': '08cc66f2c761202b49d4a17fe0ba83677e3e4a90985f0b1277234a5ba39d4a68',
 'nonmatching/script-source/20261030/native_scr_byte_rows_20261030.py': '27dcdb2bd239bb53449e4ab11a20ca612791b9c92b83fed95cc74e657b062f92',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch15/initialize_context_byte_rows.c': 'fa82be162b2dc89624e8c8204a5ee704a754b5b6eb1a59e2da78cfa284686364',
 'src/scripts/20261030/batch15/scr_byte_rows.h': '1bcb2ca3b8a33fb54da33d969ae2382efa788f0dd324004fcaac4157715ebf29'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_byte_rows_20261030 as fixtures
import scr_c_compiler_20261030_v13 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [11]
    assert not any(base < pc < end for pc in data['entries'].values())
    own = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in own) == 1552 and own[-1]['pc'] == end - 4 and own[-1]['opcode'] == 1026
    assert len(own) == 74 and sum(row['opcode'] == 1026 for row in own) == 1
    incoming = []
    for row in data['instructions']:
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038) and base <= row['argumentsRaw'][1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': row['argumentsRaw'][1], 'opcode': row['opcode']})
            assert not (base < row['argumentsRaw'][1] < end and not base <= row['pc'] < end)
    assert all(row['opcode'] in (102, 1026, 1036, 1045) for row in own)
    assert all(row['argumentsRaw'][1] == 1 and row['argumentsRaw'][3] == 2 for row in own if row['opcode'] == 1045)
    return {'entry': 11, 'startPc': base, 'endExclusivePc': end, 'bytes': 1552, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'reachableOwnRecordPcs': [row['pc'] for row in own], 'serializedCompleteEntryDomainOnly': True,
        'configurationOnly': True, 'branchDecisionLogicClaimed': False, 'vmVariableSlotsReadOrWritten': [],
        'opaqueNativeOrComputedGlobalReferenceCoverageComplete': False}


def native_contracts():
    image = fixtures.native.MAIN
    word = struct.unpack_from('<I', image, 0x0205B6F0 - 0x02000000)[0]
    delta = word & 0xFFFFFF
    delta -= 0x1000000 if delta & 0x800000 else 0
    assert word >> 24 == 0xEB and 0x0205B6F0 + 8 + delta * 4 == 0x02054B88
    return {'module': 'main', 'processor': 'ARM9', 'mode': 'ARM', 'moduleSha256': fixtures.native.MAIN_HASH,
        'systemOpcode': 102, 'casePc': '0x205b6ec', 'nativeWrapper': '0x2054b88', 'nativeIndexMapper': '0x20725e8',
        'nativeByteCopier': '0x20c1fdc', 'tableAddress': hex(fixtures.TABLE), 'tableBytes': 64,
        'logicalIndexToNativeRow': list(fixtures.MAPPING), 'argumentWordCount': 5, 'sourceCredit': 0}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in PIN_PATHS[:2]] + [('src/scripts/20261030/batch15/' + name, name)
        for name in ('initialize_context_byte_rows.c', 'scr_byte_rows.h')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v13.py', '--source', 'initialize_context_byte_rows.c',
        '--base', hex(fixtures.BASE), '--output', 'generated.scrfunc', '--report', 'build.json']
    outcome = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END] and len(body) == 1552
    rebuilt = bytearray(data['script'])
    rebuilt[4100 + fixtures.BASE:4100 + fixtures.END] = body
    assert bytes(rebuilt) == data['script']
    target = WORK / 'world.source-byte-rows.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': outcome.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(target), 'originalBytecodeCompilerInput': False}


def row_control(body, logical, values, ordinal):
    entries = [-1] * 1024
    entries[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *entries) + body
    oracle = fixtures.Oracle(2026103025000 + ordinal)
    guarded = bytes([0xA5]) * 72
    oracle.u.mem_write(fixtures.TABLE - 4, guarded)
    state = bytes(oracle.persistent())
    oracle.u.mem_write(fixtures.native.CODE - 4100, script)
    assert oracle.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert oracle.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    trace = []
    for unused in range(16):
        pc = oracle.read(fixtures.native.CTX + 0x470)
        op = struct.unpack_from('<I', body, pc)[0]
        assert oracle.call(0x0204C5A0 if op >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': op, 'nextPc': oracle.read(fixtures.native.CTX + 0x470)})
        if not oracle.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise ValueError('Synthetic byte-row control failed to return')
    row = fixtures.MAPPING[logical]
    expected = bytearray(guarded)
    expected[4 + row * 4:8 + row * 4] = bytes(values)
    stores = [{'address': hex(fixtures.TABLE + row * 4 + lane), 'bytes': 1, 'value': value} for lane, value in enumerate(values)]
    assert oracle.byte_stores == stores and bytes(oracle.u.mem_read(fixtures.TABLE - 4, 72)) == expected
    assert bytes(oracle.persistent()) == state
    return {'logicalIndex': logical, 'values': list(values), 'nativeRow': row, 'expectedGuardedRowsHex': expected.hex(),
        'trace': trace, 'observations': oracle.observations, 'actualReturningCalls': oracle.returning_calls,
        'orderedNativeByteStores': stores, 'completeControlReturned': True, 'sourceCredit': 0}


def controls():
    directory = ROOT / 'nonmatching/script-source/20261030/batch15-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_byte_rows.h', directory / 'scr_byte_rows.h')
    text = (SOURCE / 'initialize_context_byte_rows.c').read_text()
    tests = [('index19', text.replace('set_context_byte_row(0, 100,', 'set_context_byte_row(19, 100,')),
        ('index_negative', text.replace('set_context_byte_row(0, 100,', 'set_context_byte_row(-1, 100,')),
        ('byte256', text.replace('set_context_byte_row(0, 100,', 'set_context_byte_row(0, 256,')),
        ('byte_negative', text.replace('set_context_byte_row(0, 100,', 'set_context_byte_row(0, -1,')),
        ('wrong_arity', text.replace('set_context_byte_row(0, 100, 0, 0, 0)', 'set_context_byte_row(0, 100, 0, 0)')),
        ('api_shadow', text.replace('void initialize_context_byte_rows(void)', 'void set_context_byte_row(void)')),
        ('unknown_api', text.replace('set_context_byte_row(0, 100,', 'set_unknown_byte_row(0, 100,'))]
    rejected, cases = [], []
    for name, content in tests:
        source = directory / (name + '.c')
        source.write_text(content)
        try:
            compiler.compile_source(source, fixtures.BASE)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(source), 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported byte-row configuration accepted: ' + name)
    for logical in range(19):
        for values in ((0, 0, 0, 0), (255, 255, 255, 255), (0, 1, 128, 255), (255, 128, 1, 0), (1, 2, 3, 4)):
            source = directory / ('row_' + str(len(cases)) + '.c')
            source.write_text('#include "scr_byte_rows.h"\nvoid row_control(void)\n{\n    set_context_byte_row(' +
                ', '.join(map(str, (logical, *values))) + ');\n}\n')
            body, evidence = compiler.compile_source(source, 0)
            cases.append({'source': artifact(source), 'compilerEvidence': evidence, **row_control(body, logical, values, len(cases))})
    return {'rejectedSourceProfiles': rejected, 'all95LogicalByteCases': cases, 'controlSourceCredit': 0,
        'rowControlNativeReturns': sum(case['actualReturningCalls'] for case in cases)}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS)
    for name, pin in PINS.items():
        assert digest((ROOT / name).read_bytes()) == pin, name
    data = assets.load(ROOT / 'extract/files/world.e')
    bounds = boundary(data)
    rebuilt, source_build = build(data)
    negative = controls()
    print(json.dumps({'stage': 'source-only and95 byte controls passed', 'bytes': 1552}), flush=True)
    original, recompiled = fixtures.run(data['script']), fixtures.run(rebuilt)
    assert original == recompiled and original['executedOwnRecordPcs'] == bounds['reachableOwnRecordPcs']
    unused, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-native-byte-row-configuration-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()], 'asset': data['asset'],
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END,
        'bytes': 1552, 'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds,
        'sourceOnlyBuild': source_build, 'nativeContracts': native_contracts(), 'compilerControls': negative, 'differential': original,
        'pairedCompleteOwnEntryExecutions': original['completeEntryExecutions'] * 2, 'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
        'separateRowControlNativeReturns': negative['rowControlNativeReturns'], 'configurationOnly': True, 'branchDecisionLogicClaimed': False,
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 1552,
        'originalScaffoldingBytes': len(rebuilt) - 1552, 'scaffoldingSourceCredit': 0, 'nativeExecutableByteCredit': 0,
        'completeImagesRecovered': 0, 'nativeFunctionStubs': 0, 'wholeRomSourceMatch': False, 'postFaultStateUsedForProof': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'limitations': ['Complete1552B configuration function only; not decision-logic novelty', 'Actual native byte-row APIs remain zero-credit dependencies',
            'Serialized direct-entry domain only; opaque/computed global references unproved', 'Raw byte rows have no assigned gameplay meanings']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 1552, 'configurationOnly': True, 'completeEntries': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'controls': report['separateRowControlNativeReturns']}), flush=True)


if __name__ == '__main__':
    main()
