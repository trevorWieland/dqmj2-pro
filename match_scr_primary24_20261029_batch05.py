import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261029/batch05'
WORK = ROOT / 'work/script-source/20261029/batch05/primary24'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-primary24.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'src/scripts/20261029/batch05/scr_numeric.h': 'dd9083a3b944895fa04c96a6dc41900e7d9d1923842f1f420ea253ff854a3bcf',
 'src/scripts/20261029/batch05/set_primary_24.c': '9b4fda3074d5326c26642eaac79eb1aaf1072af821e56523c13d3c3a66495506',
 'src/scripts/20261029/batch05/primary24.locals.json': '8e6f6807531deefcc20adfb035ba71ea2416925a91baf11dfea03449e034669f',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261029/native_scr_primary24_20261029.py': '245b0b963e2bc453f0c2ff72040d2c4489759fec0d3d06bc35d921a12e14eb98',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5'}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_primary24_20261029 as fixtures
import scr_c_compiler_20261029_v4 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())}


def boundaries(data, allocation):
    base, end = fixtures.BASE, fixtures.BASE + 352
    owned = [row for row in data['instructions'] if base <= row['pc'] < end]
    expected = [1036, 1045, 1045, 39, 1045, 1045, 39, 1045, 1039, 1038,
                1039, 1038, 1039, 1038, 1045, 1045, 42, 1036, 1036, 1036, 1026]
    assert [row['opcode'] for row in owned] == expected and sum(row['bytes'] for row in owned) == 352
    assert [entry for entry, pc in data['entries'].items() if pc == base] == [102]
    assert not any(base < pc < end for pc in data['entries'].values())
    incoming, references = [], {slot: [] for slot in allocation.values()}
    bits = {compiler.fword(slot): slot for slot in allocation.values()}
    for row in data['instructions']:
        args = row['argumentsRaw']
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038) and base <= args[1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': args[1], 'opcode': row['opcode']})
            assert not (base < args[1] < end and not base <= row['pc'] < end)
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
                references[bits[value]].append({'pc': row['pc'], 'access': access, 'inside': base <= row['pc'] < end})
    for slot, rows in references.items():
        inside = [row for row in rows if row['inside']]
        outside = [row for row in rows if not row['inside']]
        assert [row['access'] for row in inside] == ['write', 'read']
        assert inside[0]['pc'] < base + 148
    outside_reads = [(slot, row['pc']) for slot, rows in references.items() for row in rows
                     if not row['inside'] and row['access'] == 'read']
    assert outside_reads == [(138, 74100), (138, 75088), (139, 74136)]
    assert data['entries'][100] == 73888
    assert not any(73888 < pc < 75160 for pc in data['entries'].values())
    for row in data['instructions']:
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038):
            assert not (73888 < row['argumentsRaw'][1] < 75160 and not 73888 <= row['pc'] < 75160)
    prefix = [row for row in data['instructions'] if 73888 <= row['pc'] < 74100]
    assert [row['pc'] for row in prefix] == [73888, 73900, 73924, 73932, 73956, 73964,
        73988, 74012, 74020, 74044, 74068, 74076]
    assert [row['opcode'] for row in prefix] == [1036, 1045, 47, 1045, 48, 1045, 1045, 39, 1045, 1045, 39, 1045]
    assert prefix[0]['argumentsRaw'][1] == 73900
    return {'entry': 102, 'startPc': base, 'endExclusivePc': end, 'records': 21, 'privateReturnPc': end - 4,
            'knownDirectIncomingReferences': incoming, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
            'namedScratchProfile': allocation, 'knownSlotReferences': references, 'knownOutsideReads': len(outside_reads),
            'outsideReadQualification': {'owningEntry': 100, 'owningRange': [73888, 75160],
                'unconditionalInitializationPc': {'138': 74020, '139': 74076},
                'firstConditionalPc': 74124, 'firstReadPc': 74100,
                'noKnownExternalInteriorEntry': True, 'allThreeReadsDominatedByOwnPrefixWrites': True,
                'prefixNativeReplayRequired': True, 'wholeOwnerRecoveredOrTested': False},
            'outsideWritesReconciledByUnconditionalInitializationBeforeReads': True,
            'opaqueSysIndirectSlotAccessCoverageClaimed': False, 'interleavedOrReentrantABIClaimed': False,
            'adjacentUnexecutedBytesSha256': digest(data['code'][end:end + 8]), 'adjacentByteSourceCredit': 0}


def named_links():
    result = {'get_context_value': {'vmValueSourceKind': 3, 'bankByteOffset': '0x450', 'bankValues': 8,
              'nativeOperandReader': '0x0204bde0', 'rawBinary32Preserved': True, 'nativeSourceCredit': 0}}
    image = fixtures.native.MAIN
    for name, opcode in (('get_numeric_state', 39), ('set_primary_flag', 42)):
        address = 0x0205A68C + opcode * 4
        offset = struct.unpack_from('<I', image, address - 0x02000000)[0] & 0xFFFFFF
        if offset & 0x800000:
            offset -= 0x1000000
        case = address + 8 + offset * 4
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
                        'nativeModuleSha256': fixtures.native.MAIN_HASH, 'nativeSourceCredit': 0}
    return result


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py'),
             ('scr_c_compiler_20261029_v4.py', 'compiler_v4.py')]
    files += [('src/scripts/20261029/batch05/' + name, name) for name in
              ('set_primary_24.c', 'scr_numeric.h', 'primary24.locals.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, str(directory / 'compiler_v4.py'), '--source', 'set_primary_24.c',
               '--base', hex(fixtures.BASE), '--locals', 'primary24.locals.json',
               '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    source_report = json.loads((directory / 'build.json').read_text())
    assert len(body) == 352 and body == data['code'][fixtures.BASE:fixtures.BASE + 352]
    assert digest(body) == '5656f43fe8369e71cdce73ff171712f2e3e26d165734a2aee94d6c304838ed96'
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.BASE + 352:]
    assert rebuilt == data['script']
    output = WORK / 's02e10.rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, source_report, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'stdout': result.stdout.strip(), 'sourceOnlyInputClosure': [artifact(directory / name) for unused, name in files],
        'originalBytecodeCompilerInput': False, 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json')}, artifact(output)


def controls(allocation):
    directory = ROOT / 'nonmatching/script-source/20261029/batch05-primary24-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_numeric.h', directory / 'scr_numeric.h')
    text = (SOURCE / 'set_primary_24.c').read_text()
    tests = [('invalid_context', text.replace('get_context_value(0)', 'get_context_value(8)'), allocation),
             ('invalid_numeric', text.replace('get_numeric_state(3)', 'get_numeric_state(88)'), allocation),
             ('invalid_flag', text.replace('set_primary_flag(24, true)', 'set_primary_flag(1536, true)'), allocation),
             ('invalid_boolean', text.replace('set_primary_flag(24, true)', 'set_primary_flag(24, 2)'), allocation),
             ('wrong_getter_type', text.replace('float state_three', 'bool state_three'), allocation),
             ('missing_local', text, {name: slot for name, slot in allocation.items() if name != 'state_three'}),
             ('duplicate_local', text, dict(allocation, state_three=138)),
             ('bad_local', text, dict(allocation, state_three=256)),
             ('unused_local', text, dict(allocation, unused=1)),
             ('arithmetic', text.replace('state_three == 1', 'state_three + 1 == 2'), allocation)]
    rejected = []
    for name, source, profile in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, profile)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'profile': profile,
                             'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid primary24 source/profile accepted: ' + name)
    body, unused = compiler.compile_source(SOURCE / 'set_primary_24.c', fixtures.BASE, allocation)
    wrong, unused = compiler.compile_source(SOURCE / 'set_primary_24.c', fixtures.BASE, dict(allocation, context_value=147))
    assert len(body) == len(wrong) == 352 and body != wrong
    return {'rejectedSourceProfiles': rejected, 'wrongValidAllocationChangesBytes': True,
            'backendUnchanged': 'Frozen v4; broader ABI/else/CLI controls remain separately versioned in batch04', 'sourceCredit': 0}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/s02e10.e')
    assert data['assetSha256'] == '74d48a6935dd26ed80407785750aa5e976a5517727301ac0c00a7b09f661aa14'
    assert data['scriptSha256'] == '39a6d7add5e43f7bc403b50cc9ac6a22c17f10c826f6b95760634f2fff65a906'
    raw = (ROOT / data['asset']).read_bytes()
    members = []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                        'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
    allocation = json.loads((SOURCE / 'primary24.locals.json').read_text())
    bound = boundaries(data, allocation)
    rebuilt, source_report, command, output = build(data)
    control = controls(allocation)
    original, recompiled = fixtures.run(data['script']), fixtures.run(rebuilt)
    assert original == recompiled
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(),
        'generatorSha256': digest(Path(__file__).read_bytes()), 'evidenceClass': 'ordinary-C-complete-nested-primary24-SCR-match',
        'reproductionCommand': 'python match_scr_primary24_20261029_batch05.py',
        'sourceClosure': [{'path': path, 'sha256': sha} for path, sha in PINS.items()], 'romSha256': assets.ROM_HASH,
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
        'codeSha256': digest(data['code']), 'romFileRange': list(files['s02e10.e']), 'members': members,
        'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.BASE + 352,
                         'bytes': 352, 'sha256': source_report['outputSha256']},
        'boundariesAndLocalStorage': bound, 'sourceOnlyBuild': source_report, 'buildCommand': command,
        'namedRuntimeApiLinks': named_links(), 'compilerControls': control,
        'rebuiltDecodedImage': output, 'rebuiltDecodedImageEqualsOriginal': True,
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 352,
        'originalScaffoldingBytes': len(rebuilt) - 352, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0,
        'ordinaryNativeExecutableByteCredit': 0, 'differential': original,
        'actualReturningCallsPerImplementation': original['actualReturningCalls'],
        'actualReturningCallsTotal': original['actualReturningCalls'] * 2,
        'freshMachinesPerImplementation': original['freshMachines'], 'nativeFunctionStubs': 0,
        'postFaultStateUsedForProof': False, 'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'wholeRomSourceMatch': False,
        'limitations': ['Only this352B full routine is reconstructed; remaining image/native/container bytes are zero-credit scaffolding',
            'No natural context0 value12 producer, area/story meaning or access/renewability interpretation is established',
            'Primary24 stores use a32-bit RMW; a repeated matching call repeats that store even after the flag is set',
            'Three known outside reads belong to entry100 and are dominated by its own initialization; opaque reads/reentrancy remain uncertified',
            'Frozen restricted-v4 ABI and full native bounds apply; malformed native indices are unsupported']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'scriptBytes': 352, 'actualReturns': report['actualReturningCallsTotal'],
                      'freshMachinesPerImplementation': original['freshMachines'], 'rejectedControls': len(control['rejectedSourceProfiles'])}))


if __name__ == '__main__':
    main()
