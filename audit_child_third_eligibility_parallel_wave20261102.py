import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from project import read_json, sha256, write_json
from link_runtime_unit import relocation_rows
from seal_recovery_evidence_20261031 import code_closure
from audit_next_wave_eligibility_parallel_wave20261102 import identity, ROM
import utility_runtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', default='initial')
    args = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', args.phase):
        raise ValueError('Unsafe audit phase')
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-third'
    ready = read_json(lane / 'ready.json')
    report = read_json(lane / 'packet-ready.json')
    inputs = read_json(lane / 'packet-ready-inputs.json')
    watched = {p.relative_to(ROOT).as_posix(): sha256(p) for p in [lane / 'ready.json', lane / 'packet-ready.json', lane / 'packet-ready-inputs.json']}
    checks, failures = [], []

    def check(condition, label):
        (checks if condition else failures).append(label)

    pins = {row['path']: row['sha256'] for row in ready['files']}
    for name, digest in pins.items():
        check((ROOT / name).is_file() and sha256(ROOT / name) == digest, 'Frozen READY source/evidence: ' + name)
    check(ready['functions'] == report['exactFunctions'] == len(report['matches']) == 36 and ready['bytes'] == report['exactInitializedBytes'] == sum(row['bytes'] for row in report['matches']) == 4458, 'Complete sealed36/4458 subset')
    check(ready['romSha256'] == report['romSha256'] == inputs['romSha256'] == ROM and not report['failed'], 'Original ROM and clean report')
    check(report['inputManifestSha256'] == sha256(lane / 'packet-ready-inputs.json'), 'Original immutable input manifest')
    for row in inputs['generatorSources']:
        check(sha256(ROOT / row['path']) == row['sha256'], 'Immutable helper: ' + row['path'])
    closure = code_closure(ready['packets'][0]['producer'][:1])
    check(set(closure) <= set(pins), 'Full imported authored producer closure')
    owned = [(identity(row, report), row['bytes']) for row in report['matches']]
    check({identity(row) for row in inputs['entries']} == {key for key, size in owned} == {identity(row) for row in ready['identities']}, 'Input/report/READY complete namespaces')
    layout, derived = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules']}
    relocations, anchors, extra_callees = 0, 0, 0
    for row in report['matches']:
        module = modules[row['module']]
        data = bytes(derived[ROOT / module['binary']])
        at = int(row['address'], 0) - int(module['base'], 0)
        native = data[at:at + row['bytes']]
        check(row['program'] == utility_runtime.PROGRAM and row['processor'] == module['processor'] == 'arm9' and row['inputModuleSha256'] == module['sha256'], row['address'] + ' independent embedded namespace')
        check(utility_runtime.sha(native) == row['targetSha256'] and row['bytes'] == row['compiledBytes'], row['address'] + ' complete measured original source extent')
        item = next(item for item in inputs['entries'] if item['address'] == row['address'])
        check(all(row.get(k) == item.get(k) for k in ['source', 'sourceSha256', 'sourceDependencies', 'compiler', 'compilerSha256', 'compilerFlags', 'module', 'processor', 'program', 'mode', 'bytes']), row['address'] + ' immutable source/compiler/native contract')
        check(sha256(ROOT / row['compiler']) == row['compilerSha256'] and sha256(ROOT / row['object']) == row['objectSha256'], row['address'] + ' original compiler and original object')
        for pin in [dict(path=row['source'], sha256=row['sourceSha256']), *row['sourceDependencies']]:
            text = (ROOT / pin['path']).read_text()
            check(sha256(ROOT / pin['path']) == pin['sha256'] == pins.get(pin['path']), 'Immutable complete C/header: ' + pin['path'])
            check(len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text and not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text), 'Readable ordinary source policy: ' + pin['path'])
        proof = row['realLink']
        directory = (ROOT / proof['lcf']).parent
        actual_relocations = relocation_rows(ROOT / row['object'], row['name'])
        check(actual_relocations == proof['originalRelocations'] == relocation_rows(directory / 'caller.o', row['name']), row['address'] + ' unchanged original/split relocation fields')
        relocations += len(actual_relocations)
        check((directory / 'caller.bin').read_bytes() == native and proof['exactCallerBytes'] and proof['linkedCallerSha256'] == row['targetSha256'], row['address'] + ' complete genuine MW linked caller')
        check(sha256(ROOT / proof['lcf']) == proof['lcfSha256'] and sha256(ROOT / proof['linkedElf']) == proof['linkedElfSha256'], row['address'] + ' real control and linked ELF hashes')
        check(proof['linkerAttempt']['exitCode'] == 0 and sha256(Path(proof['linkerAttempt']['command'][0])) == proof['linkerSha256'], row['address'] + ' genuine pinned MW invocation')
        with (ROOT / proof['linkedElf']).open('rb') as stream:
            symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
            symbol = next(symbol for symbol in symbols if symbol.name == row['name'])
            check(symbol['st_value'] & ~1 == int(row['address'], 0) and symbol['st_size'] == row['bytes'], row['address'] + ' full linked caller symbol')
        for binding in proof['bindings']:
            check(binding['program'] == row['program'] and binding['processor'] == row['processor'], row['address'] + ' full callee/data namespace')
            if binding['kind'] == 'function':
                anchors += 1
                path = ROOT / binding['anchorObject']
                check(sha256(path) == binding['anchorObjectSha256'] and binding['initializedCodeBytes'] == binding['nativeCalleeBytesUsed'] == binding['calleeSourceCredit'] == 0, row['address'] + ' zero-code callee anchor')
                with path.open('rb') as stream:
                    check(ELFFile(stream).get_section_by_name('.text')['sh_type'] == 'SHT_NOBITS', row['address'] + ' actual uninitialized anchor ELF')
        for qualification in proof['qualifiedAdditionalCalleeBindings']:
            extra_callees += 1
            check(sha256(ROOT / qualification['inventory']) == qualification['inventorySha256'] and qualification['calleeFunctionCredit'] == qualification['calleeSourceBytes'] == 0 and not qualification['fullCalleeBoundaryProved'], row['address'] + ' additional measured entry evidence carries zero callee credit')
        check(not row['oracle']['supported'] and row['oracle']['nativeAndRecompiledCalls'] == row['oracle']['executionCredit'] == 0 and not row['originalObjectScaffolding'], row['address'] + ' zero behavior execution/scaffolding source credit')
    copied = read_json(lane / 'copied-root-canonical-bridge-proof.json')
    check(copied['exitCode'] == 0 and copied['canonicalReportFresh'] and copied['allFreshObjectHashesValid'] and copied['allFreshLinkMetadataValid'] and copied['sourceAndNativeContractsIdentical'] and copied['staleWorkerAndCanonicalReportsReplaced'], 'Copied-root real replay replaces stale canonical/worker reports')
    controls = read_json(lane / 'native-callee-binding-controls.json')
    check(len(controls['negativeControls']) == 5 and all(row['rejected'] for row in controls['negativeControls']), 'Five entry-qualification namespace/mode/span controls')
    reserved_map = subprocess.run(['git', 'show', '2325bb90:source-map.json'], cwd=ROOT, capture_output=True, check=True).stdout
    reserved = [(identity(row), row['bytes']) for row in json.loads(reserved_map)['matchedFunctions']]
    reserved.extend((identity(row), row['bytes']) for row in read_json(ROOT / 'cohort148-parallel-wave20261102-specification.json')['expectedAdditions'])
    for other in ['ov006', 'main-sdk-next', 'main-sdk-second']:
        document = read_json(ROOT / 'evidence/lanes/parallel-wave20261102' / other / 'ready.json')
        reserved.extend((identity(row), row['bytes']) for row in document['identities'])
    overlaps = [(hex(key[5]), hex(other[5])) for key, size in owned for other, other_size in reserved if key[:4] == other[:4] and key[5] < other[5] + other_size and other[5] < key[5] + size]
    check(not overlaps, 'Disjoint from committed147/reserved148/all46 next-wave regions')
    root_descriptor = ROOT / 'provenance/cohort149-parallel-wave20261102-next-utility-child-third-0-replay.json'
    descriptor = read_json(root_descriptor if root_descriptor.exists() else lane / 'canonical-packet.json')
    frozen = {row['path']: row['sha256'] for row in descriptor['frozenInputs']}
    inventory_inputs = ['evidence/utility/ghidra-arm9.json', 'evidence/utility/ghidra-arm7.json']
    missing_inputs = [name for name in inventory_inputs if frozen.get(name) != sha256(ROOT / name)]
    check(not missing_inputs, 'Root descriptor freezes both non-code runtime inventories')
    check(all(sha256(ROOT / name) == digest for name, digest in watched.items()), 'Original sealed worker evidence unchanged during read-only audit')
    output = ROOT / ('evidence/verification/parallel-wave20261102/child-third-eligibility-' + args.phase + '.json')
    if output.exists():
        raise ValueError('Refusing to overwrite previous audit phase')
    result = dict(passed=not failures, sourceCredit=0, eligibilityScope='Read-only complete original object/relocation/link/source and immutable input audit',
        functions=36, bytes=4458, passedChecks=len(checks), failedChecks=failures, watchedHandoffHashes=watched,
        helperPins=len(inputs['generatorSources']), readyFilePins=len(pins), actualRelocationsCompared=relocations,
        zeroCodeAnchors=anchors, additionalCalleeEntryQualifications=extra_callees,
        originalCalleeSourceCredit=0, actualNativeAndSourceExecutionCredit=0, wholeCWrongBodyControls=0,
        entryQualificationNegativeControls=5, noWholeCOrBehaviorControlClaim=True, overlaps=overlaps,
        missingMandatoryInventoryPins=missing_inputs, producedReportDependency='evidence/matches/utility-arm9-startup01.json',
        producedReportHashMustRemainRefreshable=True, producerReruns=0, registryMutations=0,
        fullFreshReplayProven=False, generatorSha256=sha256(Path(__file__)))
    write_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
