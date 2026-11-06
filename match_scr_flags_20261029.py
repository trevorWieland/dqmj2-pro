import hashlib
import importlib.util
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261029'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-flags.json'
PINS = {
    'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
    'src/scripts/20261029/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
    'src/scripts/20261029/s07e04_reset_flags.c': '2c430637c1bfa51fbc34d55c6a4204c004b1821ec6f883242e3f67e9160556bf',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
    'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
    'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
    'evidence/encounter/script-cfg-20261029/a3f0cd628f46485f8e4fdfcf3912b4c53457839e91f074eeb4ede2cb7bb2180e.json':
        '9ef967d4a32cab3f8d2a9ab9956d08f8f2e395736332c0008995ddd5d2559ac5',
}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_flags_20261029 as fixtures
import scr_c_compiler_20261029 as compiler
import unicorn

ASSET = 'extract/files/s07e04.e'
SOURCE = ROOT / 'src/scripts/20261029/s07e04_reset_flags.c'
BASE, END, ENTRY = fixtures.BASE, fixtures.END, fixtures.ENTRY


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
            'sha256': digest(path.read_bytes())}


def measured_input():
    assert unicorn.__version__ == '2.1.4'
    data = assets.load(ROOT / ASSET)
    assert data['assetSha256'] == '7444b8bd3eb9765f29ef3dffa2d924927a41f53f869539418a1201fbc714bc4f'
    assert data['scriptSha256'] == 'a3f0cd628f46485f8e4fdfcf3912b4c53457839e91f074eeb4ede2cb7bb2180e'
    assert data['entries'][ENTRY] == BASE
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                            (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    raw = (ROOT / ASSET).read_bytes()
    assert assets.u32(raw, 4) == 8
    members = []
    for index in range(8):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        decoded = assets.ash(stored)
        assert decoded == data['script']
        members.append({'memberIndex': index, 'storedOffset': offset, 'storedBytes': length,
                        'storedSha256': digest(stored), 'scriptSha256': digest(decoded)})
    return data, members


def boundaries(data):
    rows = data['instructions']
    owned = [row for row in rows if BASE <= row['pc'] < END]
    assert len(owned) == 14 and sum(row['bytes'] for row in owned) == END - BASE == 240
    assert owned[0]['pc'] == BASE and owned[-1]['pc'] + owned[-1]['bytes'] == END
    assert [row['opcode'] for row in owned] == [1036] + [1045, 1045, 42] * 4 + [1026]
    assert owned[0]['argumentsRaw'] == [12, BASE + 12]
    starts = {row['pc'] for row in rows}
    assert BASE in starts and END in starts
    assert [slot for slot, pc in data['entries'].items() if pc == BASE] == [ENTRY]
    assert not any(BASE < pc < END for pc in data['entries'].values())
    incoming, outgoing = [], []
    for row in rows:
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038):
            target = row['argumentsRaw'][1]
            if BASE <= target < END:
                incoming.append({'sourcePc': row['pc'], 'targetPc': target, 'opcode': row['opcode']})
                assert not (BASE < target < END and not BASE <= row['pc'] < END)
            if BASE <= row['pc'] < END:
                outgoing.append({'sourcePc': row['pc'], 'targetPc': target})
                assert BASE <= target < END
    assert incoming == [{'sourcePc': BASE, 'targetPc': BASE + 12, 'opcode': 1036}]
    return {'entrySlots': [ENTRY], 'startPc': BASE, 'endExclusivePc': END,
            'completeRoutineBytes': 240, 'instructionRecordCount': 14,
            'privateReturnPc': END - 4, 'entryTrampoline': outgoing[0],
            'knownIncomingDirectControlReferences': incoming, 'externalDirectInteriorEntries': 0,
            'sharedTailDetected': False, 'embeddedDataInOwnedRange': False,
            'operandLiteralsAreInstructionRecords': True,
            'wholeImageControlFlowCertified': False,
            'outsideOpaqueSysOrIndirectControlEffectsExhaustivelyRuledOut': False,
            'scope': 'Complete execution of entry129 in the measured valid-input native-VM context'}


def source_only_build():
    directory = WORK / 'source-only-build'
    directory.mkdir(parents=True, exist_ok=True)
    for source, name in ((ROOT / 'scr_c_compiler_20261029.py', 'compiler.py'),
                         (SOURCE, SOURCE.name), (SOURCE.parent / 'scr_flags.h', 'scr_flags.h')):
        shutil.copyfile(source, directory / name)
    command = [sys.executable, str(directory / 'compiler.py'), '--source', SOURCE.name,
               '--base', hex(BASE), '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    report = json.loads((directory / 'build.json').read_text())
    assert report['compilerSha256'] == PINS['scr_c_compiler_20261029.py']
    assert report['sourceSha256'] == PINS[SOURCE.relative_to(ROOT).as_posix()]
    assert report['includeSha256'] == PINS['src/scripts/20261029/scr_flags.h']
    assert report['outputBytes'] == 240
    return (directory / 'generated.scrfunc').read_bytes(), {'command': command, 'cwd': str(directory),
            'exitCode': result.returncode, 'stdout': result.stdout.strip(), 'build': report,
            'compilerInputClosure': [artifact(directory / name) for name in ('compiler.py', SOURCE.name, 'scr_flags.h')],
            'originalRomOrBytecodeInputToCompiler': False}


def compiler_controls(data, original_body):
    directory = ROOT / 'nonmatching/script-source/20261029/compiler-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE.parent / 'scr_flags.h', directory / 'scr_flags.h')
    text = SOURCE.read_text()
    variants = {
        'invalid_flag_index': text.replace('281; flag < 285', '1536; flag < 1537'),
        'non_boolean': text.replace('flag, false', 'flag, 2'),
        'unknown_api': text.replace('set_primary_flag', 'emit_opcode'),
        'undeclared_runtime_value': text.replace('flag < 285', 'flag < runtime_limit'),
        'unbounded_loop': text.replace('flag < 285', '1'),
        'signed_overflow': text.replace('int flag = 281', 'int flag = 2147483647 + 1'),
        'escaping_include': text.replace('"scr_flags.h"', '"../scr_flags.h"'),
        'dead_unknown_api': text.replace('    for (', '    if (false) { emit_opcode(42); }\n    for ('),
        'unsupported_octal_literal': text.replace('int flag = 281', 'int flag = 0431'),
        'api_shadow': text.replace('    for (', '    int set_primary_flag = 0;\n    for ('),
        'keyword_entry': text.replace('clear_primary_flags_281_through_284', 'auto'),
    }
    rejected = []
    for name, source in variants.items():
        path = directory / (name + '.c')
        path.write_text(source, encoding='utf-8', newline='\n')
        try:
            compiler.compile_source(path, BASE)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported C source was accepted: ' + name)
    altered = directory / 'conditional_flags.c'
    altered.write_text(text.replace('        set_primary_flag(flag, false);',
        '        if (flag == 282) {\n            set_primary_flag(flag, true);\n        } else {\n            set_primary_flag(flag, false);\n        }'), encoding='utf-8', newline='\n')
    changed, changed_report = compiler.compile_source(altered, BASE)
    assert len(changed) == 240 and changed != original_body
    mutated = data['script'][:4100 + BASE] + changed + data['script'][4100 + END:]
    expected = [fixtures.execute(mutated, 15, thread, 2026103010000 + thread, (0, 1, 0, 0)) for thread in range(4)]
    relocated, unused = compiler.compile_source(SOURCE, 0)
    assert relocated[:8] == original_body[:8] and relocated[12:] == original_body[12:]
    assert struct.unpack_from('<I', relocated, 8)[0] == 12
    shorter = directory / 'shorter_loop.c'
    shorter.write_text(text.replace('flag < 285', 'flag < 284'), encoding='utf-8', newline='\n')
    shorter_body, unused = compiler.compile_source(shorter, BASE)
    assert len(shorter_body) == 184 and shorter_body != original_body
    sentinel = WORK / 'rejected-build-output.bin'
    sentinel.write_bytes(b'unchanged-negative-build-sentinel')
    rejected_report = WORK / 'rejected-build-report.json'
    rejected_report.write_bytes(b'unchanged-negative-report-sentinel')
    command = [sys.executable, str(ROOT / 'scr_c_compiler_20261029.py'), '--source', str(directory / 'unknown_api.c'),
               '--base', hex(BASE), '--output', str(sentinel), '--report', str(rejected_report)]
    result = subprocess.run(command, cwd=WORK, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0 and sentinel.read_bytes() == b'unchanged-negative-build-sentinel'
    assert rejected_report.read_bytes() == b'unchanged-negative-report-sentinel'
    return {'rejectedSources': rejected, 'conditionalSource': artifact(altered), 'conditionalBuild': changed_report,
            'conditionalOriginalMatch': False, 'conditionalIndependentNativeCases': expected,
            'changedLoopBoundProducesBytes': len(shorter_body), 'baseRelocationOnlyChangesTrampolineTarget': True,
            'failedCliBuildPreservesExistingOutputs': True, 'negativeCliExitCode': result.returncode,
            'negativeCliCommand': command, 'additionalSourceCredit': 0}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    data, members = measured_input()
    boundary = boundaries(data)
    body, build = source_only_build()
    original = data['code'][BASE:END]
    assert len(body) == 240 and body == original
    assert digest(body) == '58c94f200124dba9227f4d21d3359bab5da54dafd2e0c1f5af362b9aaae6a741'
    rebuilt = data['script'][:4100 + BASE] + body + data['script'][4100 + END:]
    assert rebuilt == data['script']
    generated = WORK / 's07e04.rebuilt.scr'
    generated.write_bytes(rebuilt)
    controls = compiler_controls(data, body)
    native_result = fixtures.run(data['script'])
    rebuilt_result = fixtures.run(rebuilt)
    assert native_result == rebuilt_result
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'evidenceClass': 'high-level-C-source-to-SCR-complete-entry-byte-and-native-match',
              'reproductionCommand': 'python match_scr_flags_20261029.py',
              'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
              'sourceClosure': [{'path': path, 'sha256': expected} for path, expected in PINS.items()],
              'romSha256': assets.ROM_HASH, 'asset': ASSET, 'assetSha256': data['assetSha256'],
              'romFileRange': list(files['s07e04.e']), 'members': members,
              'inputScriptSha256': data['scriptSha256'], 'inputCodeSha256': digest(data['code']),
              'entryTableSha256': digest(data['script'][4:4100]), 'codeBytes': len(data['code']),
              'matchedScriptSourceUnits': 1, 'matchedScriptSourceBytes': 240,
              'uniqueDecodedImagesWithRecoveredRange': 1, 'completeImagesRecovered': 0,
              'memberAliasesAreNotSeparateSourceCredit': True,
              'matchedRange': {'startPc': BASE, 'endExclusivePc': END, 'bytes': 240, 'sha256': digest(body)},
              'generatedBytecodeIsOutputOnly': True, 'sourceLanguage': 'restricted C99',
              'sourceExpressesLoopAndNamedCalls': True, 'generalCCompilerClaimed': False,
              'ordinaryNativeExecutableByteCredit': 0, 'compilerBuild': build, 'boundaries': boundary,
              'rebuiltDecodedImage': artifact(generated), 'rebuiltDecodedImageEqualsOriginal': True,
              'originalScaffoldingBytes': len(rebuilt) - 240, 'originalCodeScaffoldingBytes': len(data['code']) - 240,
              'sourceCreditForScaffolding': 0, 'scriptHeaderOrEntryTableSourceCredit': 0,
              'actualReturningCallsPerImplementation': native_result['actualReturningCalls'],
              'actualReturningCallsTotal': native_result['actualReturningCalls'] * 2,
              'freshMachinesPerImplementation': native_result['freshMachines'], 'nativeFunctionStubs': 0,
              'allGeneralRegistersAndCpsrCompared': True, 'orderedCpuStoresCompared': True,
              'fullPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False,
              'nativeModuleHashes': {'main': fixtures.native.MAIN_HASH, 'ov000': fixtures.native.OVERLAY_HASH,
                                     'itcm': fixtures.native.ITCM_HASH},
              'differential': native_result, 'compilerControls': controls,
              'wholeRomSourceMatch': False, 'wholeImageDecompiled': False,
              'limitations': ['Only one complete entry129 routine and240 unique SCR bytes are reconstructed',
                  'The remaining original SCR bytes, native VM/callees and container are zero-credit scaffolding',
                  'No whole script-image, archive-compression or ROM source reconstruction is certified',
                  'The compiler accepts one void function, one verified ABI include, compile-time signed32 expressions, declarations, if and bounded constant loops',
                  'It supports only the set_primary_flag API, with exact finite float marshalling for indices0..1535 and booleans0/1',
                  'Runtime variables, runtime branches, parameters, general C/C++ and arbitrary script APIs remain unsupported',
                  'Four primary flag IDs have measured reset behavior without assigned story, quest or encounter meanings',
                  'Native threads are selected by controlled scheduler bytes; entry/fork creation and termination execute original native helpers',
                  'Whole-image indirect or opaque-SYS transfer coverage is not claimed',
                  'Conditional and shorter-loop controls demonstrate compilation behavior and receive zero additional recovered-byte credit']}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': OUTPUT.relative_to(ROOT).as_posix(), 'scriptSourceUnits': 1,
                      'scriptSourceBytes': 240, 'actualReturns': report['actualReturningCallsTotal'],
                      'freshMachinesPerImplementation': native_result['freshMachines'], 'completeImages': 0}))


if __name__ == '__main__':
    main()
