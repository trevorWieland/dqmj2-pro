import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261029/batch02'
SOURCE = ROOT / 'src/scripts/20261029/batch02'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-reset-calls.json'
PINS = {
    'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
    'match_scr_flags_20261029.py': 'b24e7262a7a42ccd7954d68d366be2644e662e7aa24ac7528462bc5fd21ca6b7',
    'src/scripts/20261029/s07e04_reset_flags.c': '2c430637c1bfa51fbc34d55c6a4204c004b1821ec6f883242e3f67e9160556bf',
    'src/scripts/20261029/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
    'scr_c_compiler_20261029_v2.py': 'e88ddd56f388e97852293942d7f49cc8fab2f89c8bd4d19683c33811de565f2e',
    'src/scripts/20261029/batch02/before_primary_flag_reset.c': 'c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d',
    'src/scripts/20261029/batch02/clear_primary_flags_after_hook.c': '4e4c6390073a68d904f0667bdd983bbebd69e4ed1a3df7ae7e24fa182be72d5e',
    'src/scripts/20261029/batch02/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
    'src/scripts/20261029/batch02/scr_calls.h': '9ac1d6c5c6e50340b690e50f657fca26850c845e459ec6579cfb3123214a5599',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
    'nonmatching/script-source/20261029/native_scr_calls_20261029.py': '5f1ef9f313c12ae39eee9ee731ca2036f1f5140ff23a71b3f877cd24da95df24',
    'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
    'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_calls_20261029 as fixtures
import scr_c_compiler_20261029 as v1
import scr_c_compiler_20261029_v2 as v2
import unicorn

IMAGES = (
    ('s07e05.e', 0x16608, '95c9ef238cb1a1d5836396e98e836ba97fcfc4b5e2b396c0b9516af679d96e1e',
     '4a0af687456cdfd4297badecc8cb05578cc410adfcb152082361675939dbcc66'),
    ('s07e11.e', 0xE158, '8d538729550779610edda531f8bcd16d3a15bce668100b226999b57d4a8a0661',
     'bb7bc3a54c93e3a774cb8c918b194eabbdf76b2aa92437fb3fc1b334f89dbda7'),
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
            'sha256': digest(path.read_bytes())}


def load(name, wrapper, archive_hash, script_hash):
    path = ROOT / 'extract/files' / name
    data = assets.load(path)
    assert data['assetSha256'] == archive_hash and data['scriptSha256'] == script_hash
    assert data['entries'][102] == fixtures.HOOK and data['entries'][129] == wrapper
    raw = path.read_bytes()
    members = []
    for index in range(assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        assert assets.ash(stored) == data['script']
        members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                        'storedSha256': digest(stored), 'decodedSha256': digest(data['script'])})
    return data, members


def boundaries(data, wrapper):
    ranges = ((fixtures.HOOK, fixtures.HOOK + 16, 102), (wrapper, wrapper + 252, 129))
    evidence = []
    for base, end, entry in ranges:
        owned = [row for row in data['instructions'] if base <= row['pc'] < end]
        expected = [1036, 1026] if entry == 102 else [1036, 1033] + [1045, 1045, 42] * 4 + [1026]
        assert [row['opcode'] for row in owned] == expected
        assert sum(row['bytes'] for row in owned) == end - base
        assert owned[0]['pc'] == base and owned[-1]['pc'] + owned[-1]['bytes'] == end
        assert owned[0]['argumentsRaw'] == [12, base + 12]
        assert [slot for slot, target in data['entries'].items() if target == base] == [entry]
        assert not any(base < target < end for target in data['entries'].values())
        incoming = []
        for row in data['instructions']:
            if row['opcode'] in (1033, 1034, 1036, 1037, 1038):
                target = row['argumentsRaw'][1]
                if base <= target < end:
                    incoming.append({'sourcePc': row['pc'], 'targetPc': target, 'opcode': row['opcode']})
                    assert not (base < target < end and not base <= row['pc'] < end)
        trailer = data['code'][end:end + 8]
        evidence.append({'entry': entry, 'startPc': base, 'endExclusivePc': end,
                         'recordCount': len(owned), 'privateReturnPc': end - 4,
                         'knownIncomingDirectReferences': incoming, 'externalInteriorEntries': 0,
                         'adjacentEightBytesSha256': digest(trailer), 'adjacentEightBytesSourceCredit': 0,
                         'adjacentBytesClassification': 'Unexecuted original metadata/scaffolding, not part of accepted executable range',
                         'indirectOrOpaqueOutsideControlFlowCoverageClaimed': False, 'sharedReturnTailDetected': False})
    return evidence


def compile_pair(data, wrapper, name):
    directory = WORK / name / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(ROOT / 'scr_c_compiler_20261029.py', 'compiler_v1.py'),
             (ROOT / 'scr_c_compiler_20261029_v2.py', 'compiler_v2.py')]
    files += [(SOURCE / name, name) for name in ('before_primary_flag_reset.c',
               'clear_primary_flags_after_hook.c', 'scr_flags.h', 'scr_calls.h')]
    for source, target in files:
        shutil.copyfile(source, directory / target)
    binding = {'before_primary_flag_reset': data['entries'][102]}
    (directory / 'bindings.json').write_text(json.dumps(binding, sort_keys=True) + '\n')
    builds, bodies = [], []
    for version, source, base, output in (('v1', 'before_primary_flag_reset.c', fixtures.HOOK, 'hook'),
                                        ('v2', 'clear_primary_flags_after_hook.c', wrapper, 'wrapper')):
        command = [sys.executable, str(directory / ('compiler_' + version + '.py')), '--source', source,
                   '--base', hex(base), '--output', output + '.scrfunc', '--report', output + '.json']
        if version == 'v2':
            command += ['--bindings', 'bindings.json']
        result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        body = (directory / (output + '.scrfunc')).read_bytes()
        report = json.loads((directory / (output + '.json')).read_text())
        assert body == data['code'][base:base + len(body)]
        bodies.append((base, body))
        builds.append({'version': version, 'command': command, 'cwd': str(directory),
                       'exitCode': result.returncode, 'stdout': result.stdout.strip(), 'build': report,
                       'sourceOnlyInputs': [artifact(directory / target) for unused, target in files],
                       'bindingInput': artifact(directory / 'bindings.json'), 'originalBytecodeCompilerInput': False})
    assert len(bodies[0][1]) == 16 and len(bodies[1][1]) == 252
    rebuilt = bytearray(data['script'])
    for base, body in bodies:
        rebuilt[4100 + base:4100 + base + len(body)] = body
    assert bytes(rebuilt) == data['script']
    path = WORK / name / 'rebuilt.scr'
    path.write_bytes(rebuilt)
    return bytes(rebuilt), builds, bodies, artifact(path)


def controls():
    directory = ROOT / 'nonmatching/script-source/20261029/batch02-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_calls.h', directory / 'scr_calls.h')
    text = (SOURCE / 'clear_primary_flags_after_hook.c').read_text()
    source = directory / 'valid.c'
    source.write_text(text, encoding='utf-8', newline='\n')
    binding = {'before_primary_flag_reset': fixtures.HOOK}
    cases = []
    variants = {
        'unknown_api': text.replace('set_primary_flag', 'emit_opcode'),
        'undeclared_value': text.replace('flag < 285', 'flag < runtime_limit'),
        'unbounded_loop': text.replace('flag < 285', '1'),
        'invalid_flag': text.replace('281; flag < 285', '1536; flag < 1537'),
        'invalid_boolean': text.replace('flag, false', 'flag, 2'),
        'signed_overflow': text.replace('int flag = 281', 'int flag = 2147483647 + 1'),
        'escaping_include': text.replace('"scr_calls.h"', '"../scr_calls.h"'),
        'dead_unknown_api': text.replace('    for (', '    if (false) { emit_opcode(42); }\n    for ('),
        'octal_literal': text.replace('int flag = 281', 'int flag = 0431'),
        'api_shadow': text.replace('    for (', '    int before_primary_flag_reset = 0;\n    for ('),
        'keyword_entry': text.replace('clear_primary_flags_after_hook', 'auto'),
        'wrong_call_arity': text.replace('before_primary_flag_reset();', 'before_primary_flag_reset(1);'),
        'excess_script_calls': text.replace('    before_primary_flag_reset();',
            '    for (int call = 0; call < 1024; ++call) { before_primary_flag_reset(); before_primary_flag_reset(); }'),
    }
    tests = [(name, value, binding) for name, value in variants.items()]
    tests += [('missing_binding', text, {}), ('unaligned_binding', text, {'before_primary_flag_reset': fixtures.HOOK + 2}),
              ('negative_binding', text, {'before_primary_flag_reset': -4}),
              ('out_of_range_binding', text, {'before_primary_flag_reset': 0x80000000}),
              ('boolean_binding', text, {'before_primary_flag_reset': False}),
              ('unknown_symbol_binding', text, {'emit_opcode': fixtures.HOOK})]
    for name, value, bindings in tests:
        path = directory / (name + '.c')
        path.write_text(value, encoding='utf-8', newline='\n')
        try:
            v2.compile_source(path, 0x16608, bindings)
        except ValueError as error:
            cases.append({'name': name, 'source': artifact(path), 'bindings': bindings,
                          'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid v2 source or binding accepted: ' + name)
    correct, unused = v2.compile_source(source, 0x16608, binding)
    relocated, unused = v2.compile_source(source, 0x16608, {'before_primary_flag_reset': fixtures.HOOK + 24})
    assert len(relocated) == len(correct) == 252 and relocated != correct
    assert correct[:20] == relocated[:20] and correct[24:] == relocated[24:]
    try:
        v1.compile_source(source, 0x16608)
    except ValueError:
        pass
    else:
        raise AssertionError('Frozen v1 unexpectedly accepts the v2 ABI header')
    return {'negativeCases': cases, 'wrongAlignedBindingDoesNotMatchOriginal': True,
            'onlyCallTargetWordChangesWithBinding': True, 'frozenV1RejectsTheBroaderABI': True,
            'controlSourceCredit': 0}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                            (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    control = controls()
    modules, emitted_hashes = [], set()
    total_calls, total_machines = 0, 0
    rom, files = assets.original_files()
    for image_index, (name, wrapper, archive_hash, script_hash) in enumerate(IMAGES):
        data, members = load(name, wrapper, archive_hash, script_hash)
        boundary = boundaries(data, wrapper)
        rebuilt, builds, bodies, output = compile_pair(data, wrapper, name)
        original_result = fixtures.run(data['script'], wrapper, 2026103012000 + image_index * 1000)
        rebuilt_result = fixtures.run(rebuilt, wrapper, 2026103012000 + image_index * 1000)
        assert original_result == rebuilt_result
        total_calls += original_result['actualReturningCalls']
        total_machines += original_result['freshMachines']
        ranges = [{'startPc': base, 'endExclusivePc': base + len(body), 'bytes': len(body), 'sha256': digest(body),
                   'sourceFunction': 'before_primary_flag_reset' if len(body) == 16 else 'clear_primary_flags_after_hook'}
                  for base, body in bodies]
        emitted_hashes.update(row['sha256'] for row in ranges)
        modules.append({'asset': data['asset'], 'archiveSha256': archive_hash, 'scriptSha256': script_hash,
                        'codeSha256': digest(data['code']), 'entryTableSha256': digest(data['script'][4:4100]),
                        'romFileRange': list(files[name]), 'members': members, 'boundaries': boundary,
                        'sourceOnlyBuilds': builds, 'matchedRanges': ranges, 'matchedBytes': 268,
                        'originalScaffoldBytes': len(rebuilt) - 268, 'scaffoldingSourceCredit': 0,
                        'rebuiltDecodedImage': output, 'rebuiltDecodedImageEqualsOriginal': True,
                        'completeImageReconstructed': False, 'differential': original_result})
    report = {'schemaVersion': 1, 'evidenceClass': 'ordinary-C-SCR-flag-resets-with-source-linked-empty-hooks',
              'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
              'reproductionCommand': 'python match_scr_resets_20261029_batch02.py', 'romSha256': assets.ROM_HASH,
              'sourceClosure': [{'path': path, 'sha256': expected} for path, expected in PINS.items()],
              'sourceFunctionDefinitions': 2, 'completeFunctionInstances': 4, 'qualifiedRangeBytes': 536,
              'uniqueDecodedImagesWithRecoveredRanges': 2, 'distinctEmittedBodyHashes': len(emitted_hashes),
              'identicalEmptyHookBodyCopiesAcrossImages': 2, 'archiveMemberAliasesGiveNoDuplicateCredit': True,
              'completeImagesRecovered': 0, 'ordinaryNativeExecutableByteCredit': 0,
              'actualReturningCallsPerImplementation': total_calls, 'actualReturningCallsTotal': total_calls * 2,
              'freshMachinesPerImplementation': total_machines, 'nativeFunctionStubs': 0,
              'allGeneralRegistersCpsrAndOrderedCpuStoresCompared': True, 'persistentAndVmStateCompared': True,
              'nativeVmAndItsCalleesExecuteUnmodified': True, 'nativeFilesystemLoaderExecuted': False,
              'newHeaderIsSeparateFromFrozenV1Header': True,
              'postFaultStateUsedForProof': False, 'modules': modules, 'compilerControls': control,
              'wholeRomSourceMatch': False,
              'limitations': ['Only two source definitions instantiated as four complete routine ranges across two images are reconstructed',
                  'The16-byte hook is empty; it is reported separately from the meaningful252-byte flag-reset wrapper',
                  'Identical member/image body reuse is explicit and not treated as independent authored logic',
                  'Original headers, adjacent unexecuted metadata, other script/native code and archive compression remain zero-credit scaffolding',
                  'V2 extends the frozen restricted backend only with a declared zero-argument script call and explicit named binding',
                  'Runtime variables/branches, general C/C++, arbitrary APIs and full preprocessing remain unsupported',
                  'Known direct boundaries and call/return stacks are certified for these complete entry executions; indirect or opaque outside transfers are not exhaustively covered',
                  'Flags281..284 have measured clearing behavior without assigned story/quest/encounter meanings',
                  'No full image, live scene, travel, battle access or encounter renewability claim is made']}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': OUTPUT.relative_to(ROOT).as_posix(), 'functionInstances': 4, 'rangeBytes': 536,
                      'actualReturns': total_calls * 2, 'freshMachinesPerImplementation': total_machines,
                      'completeImages': 0, 'negativeCompilerCases': len(control['negativeCases'])}))


if __name__ == '__main__':
    main()
