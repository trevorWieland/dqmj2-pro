import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from source_dependencies import dependencies_current

ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
SAVE_SHA = '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0'
MAIN_SHA = 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
SPECS = [('record33_zero_exact_fixtures_20261029.py', 'record33-zero-exact-fixtures-20261029.json',
          'src/mechanics_save/20261029_record33_zero_value.c'),
         ('record33_reader_fixtures_20261029.py', 'record33-reader-fixtures-20261029.json',
          'src/mechanics_save/20261029_record33_reader.c')]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def file_identity(relative):
    return {'path': str(relative).replace('\\', '/'), 'sha256': sha((ROOT / relative).read_bytes())}


def verify_inputs():
    for relative, digest in [('inputs/game.nds', ROM_SHA), ('inputs/save.sav', SAVE_SHA),
                             ('extract/arm9/arm9.bin', MAIN_SHA)]:
        if sha((ROOT / relative).read_bytes()) != digest:
            raise AssertionError('Record33 matcher input pin changed')


def native_entry(module, address, cache):
    if module not in cache:
        seed = json.loads((ROOT / 'provenance/seed-manifest.json').read_text())
        metadata = next(item for item in seed['modules'] if item['name'] == module)
        body = (ROOT / metadata['binary']).read_bytes()
        if sha(body) != metadata['sha256']:
            raise AssertionError('Record33 native module pin changed')
        text = (ROOT / metadata['symbolsFile']).read_text()
        functions = {}
        for name, mode, size, point in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', text, re.M):
            functions[int(point, 0)] = (name, mode, int(size, 0))
        cache[module] = (metadata, body, functions)
    metadata, body, functions = cache[module]
    if address not in functions:
        raise AssertionError(('Binding is not a declared native function start', module, hex(address)))
    name, mode, length = functions[address]
    start = address - int(metadata['base'], 0)
    span = body[start:start + length]
    if len(span) != length or mode != 'arm':
        raise AssertionError('Record33 native function span/mode mismatch')
    return {'address': hex(address), 'mode': mode, 'module': module, 'processor': 'arm9',
            'kind': 'function', 'nativeAlias': name, 'bytes': length,
            'nativeSpanSha256': sha(span), 'nativeModuleSha256': metadata['sha256'],
            'verification': 'Declared native function start and measured complete module/span hashes'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--writer-source', default=SPECS[0][2])
    parser.add_argument('--reader-source', default=SPECS[1][2])
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 13, 5):
        raise AssertionError('Pinned Python3.13.5 is required')
    import unicorn
    if unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Unicorn2.1.4 is required')
    verify_inputs()
    matches, reports, dependencies = [], [], []
    entries, modules = {}, {}
    for (script, report_name, default_source), source in zip(SPECS, [args.writer_source, args.reader_source]):
        relative_script = 'evidence/application/' + script
        command = [sys.executable, str(ROOT / relative_script), '--source', source]
        process = subprocess.run(command, capture_output=True, text=True, timeout=90)
        if process.returncode:
            raise AssertionError(process.stdout + process.stderr)
        relative_report = 'evidence/application/' + report_name
        report = json.loads((ROOT / relative_report).read_text())
        row = dict(report['source'])
        row.pop('sourceCredit', None)
        row.pop('registered', None)
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
            raise AssertionError('Fixture did not prove the complete function')
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
                    'sourceDependencies': [], 'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
                    'oracle': {'supported': True, 'cases': report['cases'], 'actualReturns': report['actualReturns'],
                               'report': relative_report, 'reportSha256': sha((ROOT / relative_report).read_bytes()),
                               'providerQualification': report['limits']}})
        if not dependencies_current(row):
            raise AssertionError('Source/include closure is not current')
        for field, digest_field in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                    ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                    ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[field]).read_bytes()) != row[digest_field]:
                raise AssertionError('Record33 source/object/link artifact hash changed')
        for relocation in row['relocations']:
            symbol = relocation['symbol']
            verified = native_entry(relocation['targetModule'], int(relocation['target'], 0), modules)
            if symbol in entries and entries[symbol] != verified:
                raise AssertionError('Conflicting qualified native bindings')
            entries[symbol] = verified
        entries[row['name']] = native_entry(row['module'], int(row['address'], 0), modules)
        row['oracle']['routineReturns'] = report.get('routineReturns', report['actualReturns'])
        row['oracle']['setupGetterReturns'] = report.get('setupGetterReturns', 0)
        row['oracle']['sourceSemantics'] = 'Operational record-byte behavior; status/ownership meanings unproved'
        matches.append(row)
        reports.append({'path': relative_report, 'sha256': sha((ROOT / relative_report).read_bytes()),
                        'cases': report['cases'], 'actualReturns': report['actualReturns'],
                        'reproductionCommand': command, 'childSummary': process.stdout.strip()})
        dependencies.append(file_identity(relative_script))
    replay_paths = ['evidence/application/record33_zero_build_20261029.py',
                    'evidence/application/record33_reader_build_20261029.py',
                    'evidence/application/preparation_machine_20261029.py',
                    'preparation_build_20261029.py', 'link_runtime_unit.py', 'save_link_snapshots.py',
                    'source_dependencies.py', 'match_mechanics_save_20261029_record33.py']
    dependencies.extend(file_identity(path) for path in replay_paths)
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': matches[0]['compilerSha256'], 'sourceDependencies': [],
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: row['address'] for name, row in entries.items()},
              'nativeSymbolModules': {name: row['module'] for name, row in entries.items()},
              'matches': matches, 'matchedFunctions': len(matches), 'matchedBytes': sum(row['bytes'] for row in matches),
              'oracle': {'reports': reports, 'cases': sum(row['cases'] for row in reports),
                         'actualReturns': sum(row['actualReturns'] for row in reports),
                         'routineReturns': sum(row['oracle']['routineReturns'] for row in matches),
                         'setupGetterReturns': sum(row['oracle']['setupGetterReturns'] for row in matches)},
              'replayDependencies': dependencies, 'nativeCalleeCodeOrSourceCredit': 0,
              'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': ['Two complete ordinary-C callers are real-MW-linked; module/full-ROM integration remains the coordinator responsibility.',
                              'Writer fixture executes all native callees; reader fixture substitutes one explicitly declared UI-rendering callee.',
                              'The reader proves raw-byte dispatch and its zero/nonzero choice, not physical rendering or gameplay reachability.',
                              'Source include dependencies are empty because both files are standalone; replay tool dependencies are hashed separately.',
                              'Matched native callees are bindings/evidence only and receive no source credit here.',
                              'Marker status/ownership labels, arbitrary side values and network-mode view selection remain unproved.']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-record33.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': len(matches), 'matchedBytes': report['matchedBytes'],
                      'oracleCases': report['oracle']['cases'], 'actualReturns': report['oracle']['actualReturns'],
                      'routineReturns': report['oracle']['routineReturns'],
                      'setupGetterReturns': report['oracle']['setupGetterReturns'],
                      'report': str(output.relative_to(ROOT)), 'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
