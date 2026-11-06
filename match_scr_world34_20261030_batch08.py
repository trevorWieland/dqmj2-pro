import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch08'
WORK = ROOT / 'work/script-source/20261030/batch08/world34'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-world34.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_world34_20261030.py': '4dfb558f72ade785f2bc1cb15988f19b56d836943fa49ccef1854c6d0359e304',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch08/advance_world_state.c': 'a37916359e3cd70b6df1813b7dc1e597f910d6e90691ccca38f81f31d3476259',
 'src/scripts/20261030/batch08/scr_world_state.h': '1925a586fd944285694802df3d149355be853f4a81cadb17828550bf11658b2b',
 'src/scripts/20261030/batch08/world.bindings.json': 'ed204331ed62ff1d1ac7a927758f7108607701704463f277cd3e448d576169a5'}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261030'))
import script_assets_20261029 as assets
import native_scr_world34_20261030 as fixtures
import scr_c_compiler_20261030_v6 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())}


def boundary(data, profile):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [34]
    assert not any(base < pc < end for pc in data['entries'].values())
    owned = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in owned) == 1352 and owned[-1]['pc'] == end - 4 and owned[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in owned) == 1
    objects = {name: {'slot': slot, 'scope': scope, 'references': []} for scope, section in
               (('module-global', 'globals'), ('local', 'locals')) for name, slot in profile[section].items()}
    by_slot = {value['slot']: value for value in objects.values()}
    incoming, noncanonical, parsed_operands = [], [], 0
    for row in data['instructions']:
        opcode, args = row['opcode'], row['argumentsRaw']
        if opcode in (1033, 1034, 1036, 1037, 1038) and base <= args[1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': args[1], 'opcode': opcode})
            assert not (base < args[1] < end and not base <= row['pc'] < end)
        pairs = []
        if opcode == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif 1039 <= opcode <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= opcode <= 1053:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read'), (args[5], args[6], 'read')]
        elif opcode == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode != 0:
                continue
            parsed_operands += 1
            value = struct.unpack('<f', struct.pack('<I', raw))[0]
            if not math.isfinite(value) or value != int(value) or not 0 <= value < 256:
                noncanonical.append({'pc': row['pc'], 'rawWord': raw})
                continue
            if int(value) in by_slot:
                by_slot[int(value)]['references'].append({'pc': row['pc'], 'access': access,
                    'inside': base <= row['pc'] < end, 'scope': by_slot[int(value)]['scope']})
    assert not noncanonical
    assert all(ref['inside'] for value in objects.values() for ref in value['references'])
    assert {name for name, value in objects.items() if value['scope'] == 'module-global'} == {
        'cached_numeric_twenty', 'cached_numeric_twenty_eight', 'cached_primary_236'}
    return {'entry': 34, 'startPc': base, 'endExclusivePc': end, 'bytes': 1352, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'objects': objects, 'knownOutsideObjectReferences': 0,
        'moduleGlobalObjectsAreNotPrivateLocals': True, 'moduleLifetime': 'Per-world.e-program VM state across entry calls',
        'allKnownEncodedMode0IndicesCanonical': True, 'mode0OperandsInspectedAcrossImage': parsed_operands,
        'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'opaqueNativeOrComputedObjectReferenceCoverageComplete': False, 'serializedCompleteCallsOnly': True,
        'adjacentUnexecutedBytesSha256': digest(data['code'][end:end + 8]), 'adjacentByteSourceCredit': 0}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py')]
    files += [('src/scripts/20261030/batch08/' + name, name) for name in
              ('advance_world_state.c', 'scr_world_state.h', 'world.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, str(directory / 'scr_c_compiler_20261030_v6.py'), '--source', 'advance_world_state.c',
        '--base', hex(fixtures.BASE), '--bindings', 'world.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    report = json.loads((directory / 'build.json').read_text())
    assert len(body) == 1352 and body == data['code'][fixtures.BASE:fixtures.END]
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.END:]
    assert rebuilt == data['script']
    output = WORK / 'world.rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, report, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'stdout': result.stdout.strip(), 'inputs': [artifact(directory / name) for unused, name in files],
        'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
        'rebuiltImage': artifact(output), 'originalBytecodeCompilerInput': False}


def named_native_apis():
    result, image = {}, fixtures.native.MAIN
    for name, opcode in (('get_numeric_state', 39), ('set_numeric_state', 40),
                         ('get_primary_flag', 41), ('set_primary_flag', 42)):
        address = 0x0205A68C + opcode * 4
        displacement = struct.unpack_from('<I', image, address - 0x02000000)[0] & 0xFFFFFF
        if displacement & 0x800000:
            displacement -= 0x1000000
        case = address + 8 + displacement * 4
        calls = []
        for pc in range(case, case + 40, 4):
            word = struct.unpack_from('<I', image, pc - 0x02000000)[0]
            if word >> 24 == 0xEA:
                break
            if word >> 24 == 0xEB:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                calls.append(hex(pc + 8 + delta * 4))
        assert len(calls) == 1
        result[name] = {'systemOpcode': opcode, 'nativeCasePc': hex(case), 'nativeWrapper': calls[0],
            'nativeModuleSha256': fixtures.native.MAIN_HASH, 'processor': 'ARM9', 'module': 'main', 'mode': 'ARM',
            'nativeSourceCredit': 0}
    return result


def ordered_case(body, value, seed):
    header = [-1] * 1024
    header[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *header) + body
    o = fixtures.Oracle(seed)
    state = o.persistent()
    state[fixtures.native.NUMERIC + 20 - fixtures.native.PERSIST] = value
    fixtures.native.bit_set(state, fixtures.native.PRIMARY, 0, False)
    expected = bytearray(state)
    fixtures.native.bit_set(expected, fixtures.native.PRIMARY, 0, value >= 28)
    o.u.mem_write(fixtures.native.PERSIST, bytes(state))
    o.u.mem_write(fixtures.native.CODE - 4100, script)
    assert o.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert o.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    o.u.mem_write(fixtures.native.CTX + 3, b'\0')
    trace = []
    for unused in range(16):
        pc = o.read(fixtures.native.CTX + 0x470)
        opcode = struct.unpack_from('<I', body, pc)[0]
        assert o.call(0x0204C5A0 if opcode >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': opcode, 'nextPc': o.read(fixtures.native.CTX + 0x470)})
        if not o.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise AssertionError('Generated ordered control did not terminate')
    assert bytes(o.persistent()) == expected
    return {'numeric20': value, 'predicate': value >= 28, 'trace': trace,
        'actualReturningCalls': o.returning_calls, 'observations': o.observations,
        'sourceCredit': 0, 'originalBytecodeInput': False, 'completeControlReturned': True}


def controls(profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch08-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_world_state.h', directory / 'scr_world_state.h')
    text = (SOURCE / 'advance_world_state.c').read_text()
    wrong_scope = {'locals': dict(profile['locals'], **profile['globals']), 'globals': {}}
    aliased = json.loads(json.dumps(profile))
    aliased['globals']['cached_numeric_twenty'] = 105
    tests = [('globals_as_locals', text, wrong_scope), ('aliased_storage', text, aliased),
        ('wrong_global_type', text.replace('extern bool cached_primary_236', 'extern float cached_primary_236'), profile),
        ('missing_global_declaration', text.replace('extern float cached_numeric_twenty;\n', ''), profile),
        ('uninitialized_ordered_global', text.replace('cached_numeric_twenty = get_numeric_state(20);', ''), profile),
        ('context_ordered_relation', text.replace('cached_numeric_twenty = get_numeric_state(20);', 'cached_numeric_twenty = get_context_value(0);'), profile),
        ('provenance_change', text.replace('state = get_numeric_state(4);', 'state = get_context_value(0);'), profile),
        ('unknown_assignment', text.replace('state = get_numeric_state(4);', 'missing = get_numeric_state(4);'), profile),
        ('bad_numeric_index', text.replace('get_numeric_state(28)', 'get_numeric_state(88)'), profile),
        ('bad_primary_index', text.replace('get_primary_flag(236)', 'get_primary_flag(1536)'), profile),
        ('unqualified_relation', text.replace('cached_numeric_twenty >= 28', 'cached_numeric_twenty > 28'), profile),
        ('setter_overflow', text.replace('set_numeric_state(5, 8)', 'set_numeric_state(5, 256)'), profile)]
    rejected = []
    for name, source, bindings in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, bindings)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid scalar-state source accepted: ' + name)
    synthetic = directory / 'ordered_byte_control.c'
    synthetic.write_text('#include "scr_world_state.h"\nvoid ordered_byte_control(void)\n{\n    float state = get_numeric_state(20);\n    if (state >= 28) {\n        set_primary_flag(0, true);\n    }\n}\n')
    body, report = compiler.compile_source(synthetic, 0, {'locals': {'state': 105}, 'globals': {}})
    assert len(body) == 176
    cases = [ordered_case(body, value, 2026103009000 + value) for value in range(256)]
    assert {case['predicate'] for case in cases} == {False, True}
    return {'rejectedSourceProfiles': rejected, 'syntheticOrderedSource': artifact(synthetic), 'syntheticOrderedBuild': report,
        'all256ByteValues': cases, 'orderedControlActualReturns': sum(case['actualReturningCalls'] for case in cases),
        'syntheticControlSourceCredit': 0, 'orderedArbitraryContextFloatSupportClaimed': False}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/world.e')
    assert data['assetSha256'] == '516ee5fa9061712ec2593d8d385ff61e1c3d54c31d3b291246366bfd891e3923'
    assert data['scriptSha256'] == '9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8'
    profile = json.loads((SOURCE / 'world.bindings.json').read_text())
    bound = boundary(data, profile)
    rebuilt, source_report, command = build(data)
    control = controls(profile)
    original = fixtures.run(data['script'])
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled
    covered = {step['pc'] for case in original['cases'] for result in (case['first'], case['second']) for step in result['trace']}
    assert covered == {row['pc'] for row in data['instructions'] if fixtures.BASE <= row['pc'] < fixtures.END}
    raw, members = (ROOT / data['asset']).read_bytes(), []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'offset': offset, 'bytes': length, 'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(),
        'generatorSha256': digest(Path(__file__).read_bytes()), 'evidenceClass': 'ordinary-C-complete-world-state-progression-reset-SCR-match',
        'reproductionCommand': 'python match_scr_world34_20261030_batch08.py',
        'sourceClosure': [{'path': path, 'sha256': sha} for path, sha in PINS.items()], 'romSha256': assets.ROM_HASH,
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
        'codeSha256': digest(data['code']), 'romFileRange': list(files['world.e']), 'members': members,
        'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END, 'bytes': 1352, 'sha256': source_report['outputSha256']},
        'boundariesAndModuleObjects': bound, 'sourceOnlyBuild': source_report, 'buildCommand': command,
        'namedNativeApiBindings': named_native_apis(),
        'compilerControls': control, 'differential': original, 'allOwnRecordsExecuted': True, 'executedRecordPcs': sorted(covered),
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 1352,
        'originalScaffoldingBytes': len(rebuilt) - 1352, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0,
        'nativeExecutableByteCredit': 0, 'actualReturningCallsPerImplementation': original['actualReturningCalls'],
        'actualReturningCallsTotal': original['actualReturningCalls'] * 2, 'freshMachinesPerImplementation': original['freshMachines'],
        'independentCompilerControlReturns': control['orderedControlActualReturns'], 'nativeFunctionStubs': 0,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False,
        'wholeRomSourceMatch': False,
        'limitations': ['Complete1352B world entry34 only; all other code/assets/native routines remain zero-credit scaffolding',
            'Numeric20/28/primary236 captures are genuine module-global objects under the explicit per-VM-module slot ABI',
            'Known cross-entry encoded object references are fully scanned and currently absent; opaque/computed native access remains incomplete',
            'Source localstate supports imperative reassignment; ordered>= is qualified only for initialized numeric-byte getter provenance',
            'Synthetic256-value compiler controls have no original-source credit and are separate from paired full-routine returns',
            'No area/story meaning, ordinary world entry, acquisition eligibility or encounter renewability is inferred from raw state/flag IDs',
            'Reentry is serialized; state advances can stop their own first-phase writes, while a still-true final gate repeats the237/203 setters']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 1352, 'actualReturns': report['actualReturningCallsTotal'],
        'freshMachinesPerImplementation': original['freshMachines'], 'compilerControlReturns': report['independentCompilerControlReturns'],
        'negativeControls': len(control['rejectedSourceProfiles'])}))


if __name__ == '__main__':
    main()
