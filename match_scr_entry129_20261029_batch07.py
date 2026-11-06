import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261029/batch07'
WORK = ROOT / 'work/script-source/20261029/batch07/entry129'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-entry129.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261029_v5.py': '4f117f078e0535630354229b96246adf0aa243257b40faf9c2992c4ccc9a6e89',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261029/native_scr_entry129_20261029.py': 'b08ce6ac978f66f4f4f6b580c374c4b30be1bad113b408bfc61324ec0cb78aaa',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261029/batch07/entry.links.json': 'ecec1251da4970d1f6318f3e6dd6dc140e46046b8b9199a041ae641594a7590a',
 'src/scripts/20261029/batch07/entry.locals.json': 'baac2d429bf1d89fbbb0ad83cbc96adb559e233b3bafd4cd3f5f761e48bb6fca',
 'src/scripts/20261029/batch07/process_context_entry.c': '9c5ef587a3a575df20d0c961750f58c4475414680e0fa6ea73202d60f615ce9a',
 'src/scripts/20261029/batch07/scr_typed_calls.h': '88fbcb7c7f582df57359a11283b19058d07638242b56ea3b6cbb18d374b343ac',
 'evidence/encounter/scr_entry129_bound_probe_20261029.py': '6c90f0a72f488728cf17a42c14d6de6327eb76f90b2be111a22e6872ceced8ee',
 'evidence/encounter/scr-entry129-native-bound-20261029.json': '8fe3c0a47f423ee3d064133c759018b3e86ea88e4b2b4495e8e170d3508344e5'}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_entry129_20261029 as fixtures
import scr_c_compiler_20261029_v5 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())}


def bindings(data, links):
    result = []
    for name, link in links.items():
        assert link['scriptSha256'] == data['scriptSha256'] and data['entries'][link['entryId']] == link['entryPc']
        base = link['entryPc']
        assert struct.unpack_from('<3I', data['code'], base) == (1036, 12, base + 12)
        if link['arity']:
            words = struct.unpack_from('<6I', data['code'], base + 12)
            assert words[:3] == (1045, 24, 0) and words[4:] == (1, 0)
            slot = struct.unpack('<f', struct.pack('<I', words[3]))[0]
            assert slot == int(slot) and 0 <= slot < 256
        result.append({'name': name, **link, 'first24CodeBytesSha256': digest(data['code'][base:base + 24]),
            'identity': {'processor': 'SCR-on-ARM9', 'scriptSha256': data['scriptSha256'], 'entryPc': base},
            'sourceLinkedCalleeClaimed': False, 'qualifiedOriginalCallee': True,
            'abi': 'Explicit float arguments overwrite only their register-bank cells; other VM state is retained'})
    return result


def boundary(data, allocation):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [129]
    assert not any(base < pc < end for pc in data['entries'].values())
    owned = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in owned) == 760 and owned[-1]['pc'] == end - 4 and owned[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in owned) == 1
    incoming = []
    refs = {slot: [] for slot in allocation.values()}
    bits = {compiler.prior.fword(slot): slot for slot in refs}
    for row in data['instructions']:
        opcode, args = row['opcode'], row['argumentsRaw']
        if opcode in (1033, 1034, 1036, 1037, 1038):
            if base <= args[1] < end:
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
        for mode, value, access in pairs:
            if mode == 0 and value in bits:
                refs[bits[value]].append({'pc': row['pc'], 'access': access, 'inside': base <= row['pc'] < end})
    assert all(row['inside'] for rows in refs.values() for row in rows)
    return {'entry': 129, 'startPc': base, 'endExclusivePc': end, 'bytes': 760, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'namedAllocation': allocation, 'knownSlotReferences': refs, 'knownOutsideSlotReferences': 0,
        'opaqueNativeComputedSlotCoverageComplete': False, 'serializedCompleteCallsOnly': True,
        'adjacentUnexecutedBytesSha256': digest(data['code'][end:end + 8]), 'adjacentByteSourceCredit': 0}


def named_apis():
    result = {}
    image = fixtures.native.MAIN
    for name, opcode in (('get_engine_state_code', 100), ('get_primary_flag', 41), ('set_primary_flag', 42),
                         ('set_numeric_state', 40), ('select_native_request', 261),
                         ('replace_native_request_scalar', 266), ('submit_native_request', 98)):
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
                        'nativeModuleSha256': fixtures.native.MAIN_HASH, 'nativeSourceCredit': 0}
    result['get_context_value'] = {'vmBankKind': 3, 'contextByteOffset': '0x450', 'rawBinary32': True, 'nativeSourceCredit': 0}
    return result


def build(data, allocation, links):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261029_v5.py')]
    files += [('src/scripts/20261029/batch07/' + name, name) for name in
              ('process_context_entry.c', 'scr_typed_calls.h', 'entry.locals.json', 'entry.links.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, str(directory / 'scr_c_compiler_20261029_v5.py'), '--source', 'process_context_entry.c',
        '--base', hex(fixtures.BASE), '--locals', 'entry.locals.json', '--links', 'entry.links.json',
        '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    source_report = json.loads((directory / 'build.json').read_text())
    assert len(body) == 760 and body == data['code'][fixtures.BASE:fixtures.END]
    assert digest(body) == 'bb36e768a527537832eb8f90eddb498f805f8d3115165d0b29cfd9c06dbf44a1'
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.END:]
    assert rebuilt == data['script']
    output = WORK / 's07e01.rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, source_report, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'stdout': result.stdout.strip(), 'inputs': [artifact(directory / name) for unused, name in files],
        'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
        'rebuiltImage': artifact(output), 'originalBytecodeCompilerInput': False}


def controls(data, allocation, links):
    directory = ROOT / 'nonmatching/script-source/20261029/batch07-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_typed_calls.h', directory / 'scr_typed_calls.h')
    text = (SOURCE / 'process_context_entry.c').read_text()
    tests = [('unknown_call', text.replace('process_imported_context(context_value)', 'unknown_context(context_value)'), allocation, links),
        ('missing_script_arg', text.replace('process_imported_context(context_value)', 'process_imported_context()'), allocation, links),
        ('extra_script_arg', text.replace('advance_numeric_nine_when_values_match()', 'advance_numeric_nine_when_values_match(1)'), allocation, links),
        ('missing_request_arg', text.replace('130, -38.97f, 0, 0, 90', '130, -38.97f, 0, 90'), allocation, links),
        ('float_overflow', text.replace('-38.97f', '1.0e500f'), allocation, links),
        ('wrong_bool_type', text.replace('bool primary_222', 'float primary_222'), allocation, links),
        ('missing_local', text, {name: slot for name, slot in allocation.items() if name != 'engine_state'}, links),
        ('duplicate_local', text, dict(allocation, engine_state=201), links),
        ('missing_link', text, allocation, {name: link for name, link in links.items() if name != 'process_imported_context'}),
        ('cross_image_link', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], scriptSha256='0' * 64))),
        ('bad_arity', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], arity=0))),
        ('bool_arity', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], arity=True))),
        ('bad_entry_id', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], entryId=1024))),
        ('unaligned_target', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], entryPc=138617))),
        ('false_callee_credit', text, allocation, dict(links, process_imported_context=dict(links['process_imported_context'], calleeSourceCredit=1)))]
    rejected = []
    for name, source, profile, bindings_value in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, profile, bindings_value)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'allocation': profile, 'links': bindings_value,
                             'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid typed-call control accepted: ' + name)
    wrong_link = dict(links, process_imported_context=dict(links['process_imported_context'], entryPc=138620))
    changed, unused = compiler.compile_source(SOURCE / 'process_context_entry.c', fixtures.BASE, allocation, wrong_link)
    assert changed != data['code'][fixtures.BASE:fixtures.END]
    try:
        bindings(data, wrong_link)
    except AssertionError:
        wrong_target_rejected = True
    else:
        raise AssertionError('Interior link accepted by current image qualification')
    sentinel, report_path = WORK / 'negative.bin', WORK / 'negative.json'
    sentinel.write_bytes(b'unchanged-v5-output')
    report_path.write_bytes(b'unchanged-v5-report')
    invalid = directory / 'invalid.links.json'
    invalid.write_text('{}\n')
    command = [sys.executable, str(ROOT / 'scr_c_compiler_20261029_v5.py'), '--source', str(SOURCE / 'process_context_entry.c'),
        '--base', hex(fixtures.BASE), '--locals', str(SOURCE / 'entry.locals.json'), '--links', str(invalid),
        '--output', str(sentinel), '--report', str(report_path)]
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0 and sentinel.read_bytes() == b'unchanged-v5-output' and report_path.read_bytes() == b'unchanged-v5-report'
    return {'rejectedSourceProfilesLinks': rejected, 'wrongAlignedTargetChangesBytes': True,
        'wrongAlignedTargetRejectedByImageQualification': wrong_target_rejected,
        'failedCliPreservesOutputAndReport': True, 'failedCliExitCode': result.returncode, 'controlSourceCredit': 0}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/s07e01.e')
    allocation = json.loads((SOURCE / 'entry.locals.json').read_text())
    links = json.loads((SOURCE / 'entry.links.json').read_text())
    qualified = bindings(data, links)
    bounds = boundary(data, allocation)
    rebuilt, source_report, command = build(data, allocation, links)
    control = controls(data, allocation, links)
    original = fixtures.run(data['script'])
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled
    raw = (ROOT / data['asset']).read_bytes()
    members = []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'offset': offset, 'bytes': length, 'storedSha256': digest(stored),
                        'scriptSha256': data['scriptSha256']})
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(),
        'generatorSha256': digest(Path(__file__).read_bytes()), 'evidenceClass': 'ordinary-C-complete-entry129-typed-script-call-SCR-match',
        'reproductionCommand': 'python match_scr_entry129_20261029_batch07.py',
        'sourceClosure': [{'path': path, 'sha256': sha} for path, sha in PINS.items()], 'romSha256': assets.ROM_HASH,
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
        'codeSha256': digest(data['code']), 'romFileRange': list(files['s07e01.e']), 'members': members,
        'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END, 'bytes': 760, 'sha256': source_report['outputSha256']},
        'boundariesAndLocalStorage': bounds, 'qualifiedOriginalScriptCallees': qualified,
        'namedNativeApiBindings': named_apis(), 'sourceOnlyBuild': source_report, 'buildCommand': command,
        'compilerControls': control, 'differential': original, 'sourceDefinitionCount': 1,
        'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 760,
        'originalScaffoldingBytes': len(rebuilt) - 760, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0,
        'nativeExecutableByteCredit': 0, 'originalScriptCalleeSourceCredit': 0,
        'actualReturningCallsPerImplementation': original['actualReturningCalls'],
        'actualReturningCallsTotal': original['actualReturningCalls'] * 2,
        'freshMachinesPerImplementation': original['freshMachines'], 'nativeFunctionStubs': 0,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False,
        'boundedPriorUnsupportedProof': artifact(ROOT / 'evidence/encounter/scr-entry129-native-bound-20261029.json'),
        'wholeRomSourceMatch': False,
        'limitations': ['Complete760B caller source only; original SCR callees are qualified zero-credit dependencies, not source-linked claims',
            'Positive native fixtures explicitly require syntheticu16 RAM021C0ECC=0; its semantics and save partition remain unchanged',
            'The preserved random0x5071 field case exceeds20,000 native instructions inside delegated SYS143; it is not a resource error or return',
            'All own branches and two serialized full returns per scenario are measured; broader control-field values and other engine contexts remain unsupported',
            'Reentry starts the same VM table entry with its unchanged context bank; a new native launcher import is a separate operation',
            'Native request API names describe measured request-field effects, with no area/story/access/renewability meanings',
            'New v5 is a restricted source backend; finite float literals and qualified script calls do not establish general C/C++ support']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 760, 'actualReturns': report['actualReturningCallsTotal'],
        'freshMachinesPerImplementation': original['freshMachines'], 'negativeControls': len(control['rejectedSourceProfilesLinks'])}))


if __name__ == '__main__':
    main()
