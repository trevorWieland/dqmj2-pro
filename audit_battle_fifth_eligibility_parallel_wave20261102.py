import gzip
import copy
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
from link_runtime_unit import relocation_rows, measured_module
from recover_linked_runtime import qualified_bindings
from host_bindings import apply_typed_bindings
from seal_recovery_evidence_20261031 import code_closure
from audit_next_wave_eligibility_parallel_wave20261102 import identity, ROM


def main():
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/battle-fifth'
    ready = read_json(lane / 'ready.json')
    inputs = read_json(lane / 'all-inputs.json')
    report = read_json(lane / 'all-match.json')
    descriptor = read_json(lane / 'canonical-packet.json')
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in descriptor['frozenInputs'] + ready['mandatoryFrozenInputs'])
    assert report['inputs']['sha256'] == sha256(ROOT / report['inputs']['path']) == sha256(lane / 'all-inputs.json')
    watched = {name: sha256(lane / name) for name in ['ready.json', 'all-inputs.json']}
    produced = {descriptor['workerReport'], descriptor['canonicalReport'],
        *((lane / name).relative_to(ROOT).as_posix() for name in ['packet01-match.json', 'packet02-match.json'])}
    pin_map = {pin['path']: pin['sha256'] for pin in ready['files']}
    refreshed = []
    for name, digest in pin_map.items():
        actual = sha256(ROOT / name)
        if actual != digest:
            assert name in produced
            refreshed.append(dict(artifact=name, historicalSha256=digest, currentSha256=actual))
    assert ready['status'] == 'ready-frozen' and ready['functions'] == len(report['matches']) == 3
    assert ready['bytes'] == sum(row['bytes'] for row in report['matches']) == 1216
    assert report['romSha256'] == descriptor['romSha256'] == ROM and report['allPassed']
    assert report['program'] == '' and report['processor'] == 'arm9' and report['module'] == 'ov001'
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in inputs['files'])
    assert set(code_closure(descriptor['producer'][:1])) <= set(pin_map)
    assert {identity(row, report) for row in report['matches']} == {identity(row) for row in ready['identities']} == {identity(row) for row in descriptor['identities']}
    native_module, native, unused = measured_module('ov001')
    units, relocations, anchors, maximum_lines = [], 0, 0, 0
    for row in report['matches']:
        assert row['module'] == 'ov001' and row['processor'] == 'arm9' and row['mode'] == 'arm'
        address = int(row['address'], 0)
        offset = address - int(native_module['base'], 0)
        original = native[offset:offset + row['bytes']]
        assert hashlib.sha256(original).hexdigest() == row['targetSha256'] and row['bytes'] == row['compiledBytes']
        assert sha256(ROOT / row['object']) == row['objectSha256'] and sha256(Path(row['compilerPath'])) == row['compilerSha256']
        paths = [dict(path=row['source'], sha256=row['sourceSha256']), *row['sourceDependencies']]
        for pin in paths:
            text = (ROOT / pin['path']).read_text()
            assert sha256(ROOT / pin['path']) == pin['sha256'] == pin_map[pin['path']]
            assert len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text and not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text)
            maximum_lines = max(maximum_lines, len(text.splitlines()))
        proof = row['realLink']
        directory = (ROOT / proof['lcf']).parent
        raw = relocation_rows(ROOT / row['object'], row['name'])
        assert raw == proof['originalRelocations'] == relocation_rows(directory / 'caller.o', row['name'])
        relocations += len(raw)
        assert (directory / 'caller.bin').read_bytes() == original and proof['exactCallerBytes']
        assert proof['linkedCallerSha256'] == proof['nativeSpanSha256'] == row['targetSha256']
        assert proof['sourceObjectSha256'] == row['objectSha256'] and proof['sourceSha256'] == row['sourceSha256']
        assert sha256(ROOT / proof['linkedElf']) == proof['linkedElfSha256'] and sha256(ROOT / proof['lcf']) == proof['lcfSha256']
        assert proof['linkerAttempt']['exitCode'] == 0 and sha256(Path(proof['linkerAttempt']['command'][0])) == proof['linkerSha256']
        assert row['nativeSymbolEntries'] == qualified_bindings(row)
        units.append(dict(module='ov001', typedNativeBindings=row['nativeSymbolEntries'], typedBindingRelocations=row['relocations']))
        for probe in proof['bindingOnlyProbes']:
            anchors += 1
            binding = row['nativeSymbolEntries'][probe['name']]
            assert binding['processor'] == 'arm9' and not binding.get('program') and binding['mode'] == 'arm' and binding['kind'] == 'function'
            assert probe['initializedCodeBytes'] == probe['nativeCalleeBytesUsed'] == probe['calleeSourceCredit'] == 0
            assert sha256(ROOT / probe['object']) == probe['objectSha256']
            with (ROOT / probe['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == probe['name'])
                assert symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == symbol['st_value'] == 0
                assert elf.get_section(symbol['st_shndx'])['sh_type'] == 'SHT_NOBITS'
                assert any(s.name == '$a' for s in elf.get_section_by_name('.symtab').iter_symbols())
    qualification = read_json(lane / 'host-typed-export-qualification.json')
    snapshot = qualification['globalSourceUnitsSnapshot']
    assert sha256(ROOT / snapshot['path']) == snapshot['sha256']
    global_units = read_json(ROOT / snapshot['path'])['units']
    normalized = apply_typed_bindings(copy.deepcopy(global_units) + units)[-3:]
    assert sum(len(unit['typedFunctionBindings']) for unit in normalized) == anchors == 29
    for row, unit in zip(report['matches'], normalized):
        expected = next(item for item in qualification['functions'] if item['address'] == row['address'])
        assert unit['typedFunctionBindings'] == expected['typedFunctionBindings'] and unit['relocationAliases'] == expected['relocationAliases']
    cases, positive_returns, all_returns, controls = 0, 0, 0, []
    phases = {}
    for name in ['packet01-match.json', 'packet02-match.json']:
        component = read_json(lane / name)
        trace = component['generatedTrace']
        assert sha256(ROOT / trace['path']) == trace['sha256']
        raw = gzip.decompress((ROOT / trace['path']).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == trace['uncompressedSha256']
        records = json.loads(raw)
        assert len(records) == component['cases'] and component['allPassed']
        families = component.get('negativeEvidence', []) + [c for function in component.get('functions', []) for c in function['negativeEvidence']]
        assert all(control['rejected'] > 0 and control['actualTopReturns'] > 0 for control in families)
        controls.extend(families)
        for record in records:
            first, second = record['results'][:2]
            assert first['kind'] == 'native' and second['kind'] == 'source'
            assert {key: value for key, value in first.items() if key != 'kind'} == {key: value for key, value in second.items() if key != 'kind'}
            assert first['topReturn'] and second['topReturn']
            key = record['profile'].get('target', int(report['matches'][0]['address'], 0))
            phases.setdefault(key, set()).add(record['profile']['rawPhase'])
            all_returns += len(record['results'])
        cases += len(records)
        positive_returns += component['actualNativeAndSourceCallerReturns']
    assert len(phases) == 3 and all(values == set(range(256)) for values in phases.values())
    assert cases == report['cases'] == 1163 and positive_returns == report['actualNativeAndSourceCallerReturns'] == 2326
    assert all_returns == report['actualTopReturnsIncludingControls'] == 4285 and len(controls) == 9 and report['actualNativeHelperReturns'] == 0
    copied = read_json(lane / 'copied-root-proof.json')
    clone = ROOT / copied['clone']
    assert copied['exitCode'] == 0 and copied['startedWithoutWorkOrCanonicalOutputs'] and copied['canonicalObjectsRefreshed']
    assert sha256(clone / descriptor['canonicalReport']) == copied['canonicalReportSha256']
    for row in read_json(clone / descriptor['canonicalReport'])['matches']:
        assert sha256(clone / row['object']) == row['objectSha256']
        proof = row['realLink']
        assert sha256(clone / proof['linkedElf']) == proof['linkedElfSha256'] and sha256(clone / proof['lcf']) == proof['lcfSha256']
        assert sha256((clone / proof['lcf']).parent / 'caller.bin') == row['targetSha256']
    debt = read_json(lane / 'callee-0205d790-abi-debt.json')
    assert debt['sourceCredit'] == debt['calleeExecutionCredit'] == 0
    accepted = debt['acceptedSource']
    assert sha256(ROOT / accepted['path']) == accepted['sha256']
    source_map = json.loads(subprocess.check_output(['git', 'show', '7ee8e5e94f82ffee6ebd91fc3ec63339fb0204c1:source-map.json'], cwd=ROOT))
    reserved = source_map['matchedFunctions'] + read_json(ROOT / 'cohort149-parallel-wave20261102-next-specification.json')['expectedAdditions']
    owned = {identity(row, report): row['bytes'] for row in report['matches']}
    overlaps = [(key, identity(other)) for key, size in owned.items() for other in reserved if key[:4] == identity(other)[:4] and key[5] < int(other['address'], 0) + other['bytes'] and int(other['address'], 0) < key[5] + size]
    assert not overlaps and all(sha256(lane / name) == digest for name, digest in watched.items())
    result = dict(passed=True, sourceCredit=0, functions=3, bytes=1216, readySha256=watched['ready.json'],
        inputManifestSha256=watched['all-inputs.json'], actualFrozenInputPinsVerified=len(inputs['files']), readyPins=len(pin_map),
        historicalProducedReportPinsRefreshed=refreshed, actualOriginalAndSplitRelocations=relocations,
        actualZeroCodeTypedArmFunctionAnchors=anchors, maximumSourceOrHeaderLines=maximum_lines,
        currentGlobalHostAliasesIndependentlyQualified=True,
        actualNativeAndSourceCallerReturns=positive_returns, actualTopReturnsIncludingControls=all_returns,
        actualNativeHelperReturns=0, independentModelCases=cases, wholeCNegativeControlFamilies=9,
        all256RawPhaseBytesPerCaller=True, all8MiBPhysicalRamDigestsAndFullRecordedStateEqual=True,
        existingAccepted0205d790SourceUnchanged=True, unresolvedHelperAbiDebtRetained=True,
        copiedRootRealObjectAndLinkHashesVerified=True, accepted148AndPending149Overlaps=overlaps,
        arbitraryAliasAndSceneReachabilityProven=False, wholeModuleOrRomAcceptanceProven=False,
        producerReruns=0, registryMutations=0, generatorSha256=sha256(Path(__file__)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/battle-fifth-eligibility.json'
    write_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
