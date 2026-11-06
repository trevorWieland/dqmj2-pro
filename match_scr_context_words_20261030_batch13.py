import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch13'
WORK = ROOT / 'work/script-source/20261030/batch13/context-words'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-context-words.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
    'scr_c_compiler_20261030_v11.py', 'nonmatching/script-source/20261029/native_scr_flags_20261029.py',
    'nonmatching/script-source/20261030/native_scr_context_words_20261030.py', 'evidence/encounter/script_assets_20261029.py',
    'evidence/encounter/vm_state_20261029.py', 'src/scripts/20261030/batch13/refresh_context_words.c',
    'src/scripts/20261030/batch13/scr_context_words.h', 'src/scripts/20261030/batch13/context.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v11.py': 'c30f671b25323f474b5aebd9a0b6fcd8a02055a5914ab850a51d430291d59af3',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_context_words_20261030.py': 'e23893d52266475830e7ec3e87db9558a8b311e895da2501dc6e728b13b90be9',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch13/refresh_context_words.c': '2b262d8bdaef29c941711ef7ddb2fdcdab3ebd0bd1d98788f7b17f0d42c815aa',
 'src/scripts/20261030/batch13/scr_context_words.h': 'b3387270855d7fddb3bdbdbd717ee6014118eafa471de6e9d7a7bc75945f6b9f',
 'src/scripts/20261030/batch13/context.bindings.json': '1f9e88013763ccc7f1f28917457278f1320782e56ee05cf73083b6a094b0a3db'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_context_words_20261030 as fixtures
import scr_c_compiler_20261030_v11 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    base, end = fixtures.BASE, fixtures.END
    aliases = [slot for slot, pc in data['entries'].items() if pc == base]
    assert aliases == [272] and not any(base < pc < end for pc in data['entries'].values())
    own = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in own) == 1280 and own[-1]['pc'] == end - 4 and own[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in own) == 1
    incoming, refs = [], []
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
            value = struct.unpack('<f', struct.pack('<I', raw))[0]
            assert value == int(value) and 0 <= value < 256
            if int(value) in (67, 68):
                assert base <= row['pc'] < end
                refs.append({'pc': row['pc'], 'slot': int(value), 'access': access})
    return {'entry': 272, 'startPc': base, 'endExclusivePc': end, 'bytes': 1280, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownSlotReferences': refs, 'knownOutsideSlotReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'reachableOwnRecordPcs': [row['pc'] for row in own], 'serializedCompleteEntryDomainOnly': True,
        'opaqueNativeOrComputedSlotReferenceCoverageComplete': False, 'lexicalBlockHeaderPc': 44244}


def native_contracts():
    result, image = {}, fixtures.native.MAIN
    for name, opcode in (('reset_context_words', 162), ('set_context_word', 161),
                         ('get_numeric_state', 39), ('get_primary_flag', 41)):
        pc = 0x0205A68C + opcode * 4
        delta = struct.unpack_from('<I', image, pc - 0x02000000)[0] & 0xFFFFFF
        delta -= 0x1000000 if delta & 0x800000 else 0
        target = pc + 8 + delta * 4
        word = struct.unpack_from('<I', image, target - 0x02000000 + 4)[0]
        assert word >> 24 == 0xEB
        delta = word & 0xFFFFFF
        delta -= 0x1000000 if delta & 0x800000 else 0
        result[name] = {'systemOpcode': opcode, 'casePc': hex(target), 'nativeWrapper': hex(target + 12 + delta * 4),
            'module': 'main', 'processor': 'ARM9', 'mode': 'ARM', 'moduleSha256': fixtures.native.MAIN_HASH, 'sourceCredit': 0}
    result['contextWordSetter'] = {'processor': 'ARM9', 'module': 'main', 'mode': 'ARM', 'address': '0x20725c8',
        'moduleSha256': fixtures.native.MAIN_HASH, 'storageAddress': hex(fixtures.WORDS), 'words': 16,
        'resetRawValueAddress': hex(fixtures.native.PERSIST + 4), 'sourceCredit': 0}
    return result


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in PIN_PATHS[:4]] + [
        ('src/scripts/20261030/batch13/' + name, name) for name in
        ('refresh_context_words.c', 'scr_context_words.h', 'context.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v11.py', '--source', 'refresh_context_words.c',
        '--base', hex(fixtures.BASE), '--bindings', 'context.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END] and len(body) == 1280
    rebuilt = bytearray(data['script'])
    rebuilt[4100 + fixtures.BASE:4100 + fixtures.END] = body
    assert bytes(rebuilt) == data['script']
    output = WORK / 'world.source-context-words.scr'
    output.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / target) for unused, target in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(output), 'originalBytecodeCompilerInput': False}


def byte_control(body, value):
    table = [-1] * 1024
    table[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *table) + body
    o = fixtures.Oracle(2026103021000 + value)
    state = o.persistent()
    state[fixtures.native.NUMERIC + 3 - fixtures.native.PERSIST] = value
    o.u.mem_write(fixtures.native.PERSIST, bytes(state))
    o.u.mem_write(fixtures.WORDS - 4, bytes([0xA5]) * 72)
    o.u.mem_write(fixtures.native.CODE - 4100, script)
    assert o.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert o.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    trace = []
    for unused in range(48):
        pc = o.read(fixtures.native.CTX + 0x470)
        op = struct.unpack_from('<I', body, pc)[0]
        assert o.call(0x0204C5A0 if op >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': op, 'nextPc': o.read(fixtures.native.CTX + 0x470)})
        if not o.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise ValueError('Synthetic <= control failed to return')
    expected = [0xA5A5A5A5] * 16
    if value <= 6:
        expected[2] = 1
    if value <= 28:
        expected[3] = 1
    assert list(struct.unpack('<16I', o.u.mem_read(fixtures.WORDS, 64))) == expected
    assert bytes(o.persistent()) == state
    assert o.u.mem_read(fixtures.WORDS - 4, 4) == bytes([0xA5]) * 4 and o.u.mem_read(fixtures.WORDS + 64, 4) == bytes([0xA5]) * 4
    return {'numeric3': value, 'expectedContextWords': expected, 'trace': trace,
        'actualReturningCalls': o.returning_calls, 'observations': o.observations,
        'completeControlReturned': True, 'sourceCredit': 0}


def controls(profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch13-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_context_words.h', directory / 'scr_context_words.h')
    text = (SOURCE / 'refresh_context_words.c').read_text()
    tests = [('index16', text.replace('set_context_word(2, 0)', 'set_context_word(16, 0)'), profile),
        ('negative_value', text.replace('set_context_word(2, 0)', 'set_context_word(2, -1)'), profile),
        ('inexact_value', text.replace('set_context_word(2, 0)', 'set_context_word(2, 16777217)'), profile),
        ('reset_argument', text.replace('reset_context_words()', 'reset_context_words(1)'), profile),
        ('wrong_setter_arity', text.replace('set_context_word(2, 0)', 'set_context_word(2)'), profile),
        ('read_before_declaration', text.replace('float state = get_numeric_state(0);', 'state = get_numeric_state(0);'), profile),
        ('context_ordering', text.replace('state = get_numeric_state(3)', 'state = get_context_value(3)'), profile),
        ('slot_alias', text, {'locals': {'state': 67, 'enabled': 67}, 'globals': {}}),
        ('slot256', text, {'locals': {'state': 256, 'enabled': 68}, 'globals': {}}),
        ('numeric88', text.replace('get_numeric_state(20)', 'get_numeric_state(88)'), profile)]
    rejected = []
    for name, source, bindings in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, bindings)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported context-word source accepted: ' + name)
    source = directory / 'byte_relation_control.c'
    source.write_text('#include "scr_context_words.h"\nvoid byte_relation_control(void)\n{\n    float value = get_numeric_state(3);\n    if (value <= 6) { set_context_word(2, 1); }\n    if (value <= 28) { set_context_word(3, 1); }\n}\n')
    body, evidence = compiler.compile_source(source, 0, {'locals': {'value': 96}, 'globals': {}})
    cases = [byte_control(body, value) for value in range(256)]
    return {'rejectedSourceProfiles': rejected, 'byteRelationSource': artifact(source), 'byteRelationBuild': evidence,
        'all256ByteRelationCases': cases, 'byteRelationActualReturningCalls': sum(case['actualReturningCalls'] for case in cases),
        'controlSourceCredit': 0, 'arbitraryContextFloatOrderingSupportClaimed': False}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS)
    for path, pin in PINS.items():
        assert digest((ROOT / path).read_bytes()) == pin, path
    data = assets.load(ROOT / 'extract/files/world.e')
    bounds = boundary(data)
    rebuilt, source_build = build(data)
    negative = controls(json.loads((SOURCE / 'context.bindings.json').read_text()))
    print(json.dumps({'stage': 'source-only/control proof passed', 'bytes': 1280}), flush=True)
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original complete', 'returns': original['actualReturningCalls']}), flush=True)
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled and original['executedOwnRecordPcs'] == bounds['reachableOwnRecordPcs']
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-numeric-primary-context-word-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': path, 'sha256': pin} for path, pin in PINS.items()],
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END,
        'bytes': 1280, 'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds,
        'sourceOnlyBuild': source_build, 'nativeContracts': native_contracts(), 'compilerControls': negative, 'differential': original,
        'pairedCompleteOwnEntryExecutions': original['completeEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
        'separateByteControlNativeReturns': negative['byteRelationActualReturningCalls'],
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 1280,
        'originalScaffoldingBytes': len(rebuilt) - 1280, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0,
        'nativeExecutableByteCredit': 0, 'nativeFunctionStubs': 0, 'wholeRomSourceMatch': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False,
        'limitations': ['Complete1280B entry272 only', 'Actual native context-word APIs remain zero-source-credit dependencies',
            'Known encoded slot/direct entry scope only; computed/opaque global program transfers unproved',
            'Raw context words and numeric/primary IDs have no assigned area/story/access/renewability meanings',
            'Restricted C compiler; explicit compound-block layout generated from ordinary C syntax']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'sourceBytes': 1280, 'completeEntries': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'controls': report['separateByteControlNativeReturns']}), flush=True)


if __name__ == '__main__':
    main()
