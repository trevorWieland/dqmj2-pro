import gzip
import hashlib
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


ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def identity(row, parent=None):
    row = {**(parent or {}), **row}
    return ROM, row.get('processor', 'arm9'), row.get('program') or '', row['module'], row['mode'], int(row['address'], 0)


def main():
    baseline = subprocess.run(['git', 'show', '2325bb90:source-map.json'], cwd=ROOT,
        check=True, capture_output=True).stdout
    reserved = [(identity(row), row['bytes']) for row in json.loads(baseline)['matchedFunctions']]
    specification = ROOT / 'cohort148-parallel-wave20261102-specification.json'
    reserved.extend((identity(row), row['bytes']) for row in read_json(specification)['expectedAdditions'])
    seed = read_json(ROOT / 'provenance/seed-manifest.json')
    modules = {row['name']: row for row in seed['modules']}
    packets, all_owned = [], []
    for lane in ['ov006', 'main-sdk-next', 'main-sdk-second']:
        folder = ROOT / 'evidence/lanes/parallel-wave20261102' / lane
        ready_path, input_path, match_path = [folder / name for name in ['ready.json', 'inputs.json', 'match.json']]
        ready, inputs, report = [read_json(path) for path in [ready_path, input_path, match_path]]
        watched = {str(path.relative_to(ROOT)): sha256(path) for path in [ready_path, input_path, match_path]}
        failures, checks = [], []

        def check(condition, label):
            (checks if condition else failures).append(label)

        pin_map = {row['path']: row['sha256'] for row in ready['files']}
        for name, digest in pin_map.items():
            check((ROOT / name).is_file() and sha256(ROOT / name) == digest, 'READY pin: ' + name)
        check(ready['romSha256'] == report['romSha256'] == inputs['romSha256'] == ROM, 'Complete original ROM namespace')
        check(report['allPassed'] and len(report['matches']) == ready['functions'], 'Report cardinality and passed state')
        check(sum(row['bytes'] for row in report['matches']) == ready['bytes'], 'Complete configured byte total')
        owned = [(identity(row, report), row['bytes']) for row in report['matches']]
        check(len({key for key, size in owned}) == len(owned), 'No duplicate native identities')
        check({identity(row, ready) for row in ready['identities']} == {key for key, size in owned}, 'READY/full report namespaces agree')
        check({identity(row) for row in inputs['entries']} == {key for key, size in owned}, 'Immutable input/full report namespaces agree')
        closure = code_closure(ready['packets'][0]['producer'][:1])
        check(set(closure) <= set(pin_map), 'Complete locally imported authored code closure is pinned')
        for row in report.get('generatorSources', []):
            check(sha256(ROOT / row['path']) == row['sha256'], 'Report generator: ' + row['path'])
        for row in inputs.get('immutableNativeConfiguration', []):
            check(sha256(ROOT / row['path']) == row['sha256'], 'Original configuration pin: ' + row['path'])
        metadata = modules[report['module']]
        binary = ROOT / metadata['binary']
        check(sha256(binary) == metadata['sha256'] == report['moduleSha256'], 'Original measured module hash')
        data = binary.read_bytes()
        config_path = ROOT / ('config/arm9/symbols.txt' if report['module'] == 'main' else 'config/arm9/overlays/ov006/symbols.txt')
        config = config_path.read_text()
        layout_count, relocations, anchors = 0, 0, 0
        for row in report['matches']:
            address, size = int(row['address'], 0), row['bytes']
            item = next(item for item in inputs['entries'] if int(item['address'], 0) == address)
            native = data[address - int(metadata['base'], 0):address - int(metadata['base'], 0) + size]
            check(hashlib.sha256(native).hexdigest() == row['targetSha256'] == item['targetSha256'], row['address'] + ' original full native extent')
            boundary = re.search(r'^\S+ kind:function\(' + row['mode'] + r',size=(0x[0-9a-f]+)\) addr:0x' + format(address, '08x') + '$', config, re.M)
            check(boundary is not None and int(boundary[1], 0) == size, row['address'] + ' complete configured boundary')
            source_pins = [dict(path=row['source'], sha256=row['sourceSha256']), *row['sourceDependencies']]
            for pin in source_pins:
                source = ROOT / pin['path']
                text = source.read_text()
                check(sha256(source) == pin['sha256'] and pin_map.get(pin['path']) == pin['sha256'], 'Frozen compiler source/header: ' + pin['path'])
                check(len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text and not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text), 'Readable ordinary C/header policy: ' + pin['path'])
            check(sha256(ROOT / row['compilerPath']) == row['compilerSha256'] == item['compilerSha256'], row['address'] + ' original compiler pin')
            obj = ROOT / row['object']
            proof = row['realLink']
            check(sha256(obj) == row['objectSha256'] == proof['sourceObjectSha256'], row['address'] + ' untouched source compiler object')
            directory = (ROOT / proof['lcf']).parent
            split = directory / 'caller.o'
            original_relocations = relocation_rows(obj, row['name'])
            check(original_relocations == proof['originalRelocations'] == relocation_rows(split, row['name']), row['address'] + ' original relocation types/addends/encoded words retained')
            relocations += len(original_relocations)
            check(sha256(split) == proof['splitObjectSha256'], row['address'] + ' immutable split object')
            check((directory / 'caller.bin').read_bytes() == native and proof['exactCallerBytes'] and proof['linkedCallerSha256'] == row['targetSha256'], row['address'] + ' complete genuine linked caller bytes')
            check(proof['linkerAttempt']['exitCode'] == 0 and sha256(Path(proof['linkerAttempt']['command'][0])) == proof['linkerSha256'], row['address'] + ' genuine pinned MW linker')
            check(sha256(ROOT / proof['lcf']) == proof['lcfSha256'] and sha256(ROOT / proof['linkedElf']) == proof['linkedElfSha256'], row['address'] + ' original link control/ELF pins')
            with (ROOT / proof['linkedElf']).open('rb') as stream:
                elf = ELFFile(stream)
                symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
                symbol = next(symbol for symbol in symbols if symbol.name == row['name'])
                check(symbol['st_value'] == address and symbol['st_size'] == size, row['address'] + ' genuine linked entry/size')
            for anchor in proof['bindingOnlyProbes']:
                anchors += 1
                path = ROOT / anchor['object']
                check(sha256(path) == anchor['objectSha256'] and anchor['initializedCodeBytes'] == anchor['nativeCalleeBytesUsed'] == anchor['calleeSourceCredit'] == anchor['linkedInitializedOutputBytes'] == 0, row['address'] + ' zero-code callee anchor')
                with path.open('rb') as stream:
                    elf = ELFFile(stream)
                    check(elf.get_section_by_name('.text')['sh_type'] == 'SHT_NOBITS', row['address'] + ' actual uninitialized anchor section')
            if lane != 'ov006':
                check(row['compiledBytes'] == size and row['relocations'] == item['priorRelocations'] and row['qualifiedDependencies'] == item['qualifiedDependencies'], row['address'] + ' full source extent and declared bindings')
                check(row['actualNativeFunctionReturns'] == row['calleeCodeOrSourceCredit'] == row['originalStorageSourceCredit'] == 0 and not row['originalObjectScaffolding'], row['address'] + ' zero execution/storage/callee credit')
        for negative in report['negativeEvidence']:
            if lane == 'ov006':
                check(negative['rejected'] > 0 and negative['rejected'] + negative['positive'] == 8, negative['address'] + ' bounded wrong-C control rejected')
                check(negative['proof']['privateLink']['originalRelocationTypesAddendsAndHBitsUnchanged'], negative['address'] + ' wrong-C original relocation provenance')
            else:
                directory = Path(negative['comparison']['directory'])
                row = next(row for row in report['matches'] if row['address'] == negative['address'])
                original = ROOT / row['source']
                wrong = directory.parent / original.name
                check(sha256(wrong) == negative['wrongSourceSha256'] and sha256(original) == row['sourceSha256'], negative['address'] + ' distinct complete wrong-C/source preservation')
                check(negative['rejectedByFullGenuineLinkComparison'] and (directory / 'caller.bin').read_bytes() != data[int(row['address'], 0)-int(metadata['base'],0):int(row['address'],0)-int(metadata['base'],0)+row['bytes']], negative['address'] + ' physical full wrong-C MW mismatch')
        if lane == 'ov006':
            artifact = ROOT / report['generatedTrace']['path']
            raw = gzip.decompress(artifact.read_bytes())
            traces = json.loads(raw)
            check(sha256(artifact) == report['generatedTrace']['sha256'] and hashlib.sha256(raw).hexdigest() == report['generatedTrace']['uncompressedSha256'], 'Bounded trace compressed/raw hashes')
            check(len(traces) == report['cases'] == 128 and report['actualNativeAndSourceCallerReturns'] == 256 and all(row['result']['actualTopReturn'] and not row['result']['modelFailures'] for row in traces), '128 bounded fixtures and256 actual caller returns')
        else:
            layout_count = sum(row['compilerChecks'] for row in report['typedLayoutChecks'])
            check(layout_count == ready['typedNativeCompilerLayoutChecks'] and report['actualNativeFunctionReturns'] == 0, 'Native compiler layouts and zero actual native execution')
            copied = read_json(folder / 'copied-root-replay.json')
            check(copied['allPassed'] and copied['startedWithNoWorkProductsOrWorkerOrCanonicalReport'] and copied['canonicalReportFreshObjectsVerified'] and copied['everyLinkerWorkingDirectoryInsideCopiedRoot'], 'Cold copied-root replay evidence')
        descriptor = ROOT / ('provenance/cohort149-parallel-wave20261102-next-' + lane + '-0-replay.json')
        desc = read_json(descriptor)
        check({identity(row) for row in desc['identities']} == {key for key, size in owned} and desc['producer'] == ready['packets'][0]['producer'], 'Root replay descriptor complete namespace/producer')
        check(bool(desc['frozenInputs']) and all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in desc['frozenInputs']), 'Mandatory immutable descriptor inputs')
        check(all(sha256(ROOT / path) == digest for path, digest in watched.items()), 'No worker handoff changed during audit')
        packets.append(dict(lane=lane, functions=ready['functions'], bytes=ready['bytes'], eligibleForFreshCoordinatorReplay=not failures,
            failedChecks=failures, passedChecks=len(checks), readySha256=sha256(ready_path), readyFilePins=len(pin_map),
            importedAuthoredClosure=len(closure), actualRelocationsCompared=relocations, zeroCodeAnchors=anchors,
            compilerLayoutChecks=layout_count, actualNativeFunctionReturns=0 if lane != 'ov006' else 128,
            actualSourceCallerReturns=128 if lane == 'ov006' else 0,
            privateDerivedInputsNotForSourceStaging=[name for name in pin_map if name.startswith('extract/')], sourceCredit=0))
        all_owned.extend((lane, key, size) for key, size in owned)
    overlaps = []
    for index, (lane, key, size) in enumerate(all_owned):
        for other_key, other_size in reserved:
            if key[:4] == other_key[:4] and key[5] < other_key[5] + other_size and other_key[5] < key[5] + size:
                overlaps.append(dict(lane=lane, address=hex(key[5]), other=hex(other_key[5])))
        for other_lane, other_key, other_size in all_owned[:index]:
            if key[:4] == other_key[:4] and key[5] < other_key[5] + other_size and other_key[5] < key[5] + size:
                overlaps.append(dict(lane=lane, otherLane=other_lane, address=hex(key[5])))
    upstream = (ROOT / 'match_runtime.py').read_text().split('\ndef execute(', 1)[0]
    old = 'r"_(?:[us](?:32|64)|f|d)_\\w+"'
    new = 'r"(?:_(?:[us](?:32|64)|f|d)_\\w+|_ll_(?:sdiv|udiv|mod|umod))"'
    adapter_ok = upstream.count(old) == 1 and (ROOT / 'wave20261102_main_sdk_second_compiler.py').read_text() == upstream.replace(old, new)
    result = dict(passed=not overlaps and adapter_ok and all(packet['eligibleForFreshCoordinatorReplay'] for packet in packets),
        scope='Read-only eligibility audit; no producer, compiler, linker, registry mutation or evidence regeneration',
        sourceCredit=0, baseline='Committed2325bb90 cohort147 plus reserved immutable298-function cohort148 proposal',
        reservedCohort148SpecificationSha256=sha256(specification), packets=packets, overlaps=overlaps,
        compilerAdapterExactlyHelperRecognitionOnly=adapter_ok,
        allOriginalObjectAndRelocationReadsOnly=True, producerReruns=0, fullFreshReplayProven=False,
        completeOriginalFourteenCaseValidatorRun=False,
        childThirdReady=(ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-third/ready.json').exists())
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/next-wave-eligibility.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
