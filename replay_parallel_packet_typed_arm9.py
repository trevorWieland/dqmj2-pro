import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from project import ROOT
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from host_bindings import apply_typed_bindings
from project import read_json, write_json, sha256
from recover_linked_runtime import qualified_bindings
from replay_parallel_packet import local
from seal_recovery_evidence_20261031 import code_closure


def address(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def binding_identity(binding):
    return (binding.get('processor'), binding.get('program') or '', binding.get('module'), binding.get('mode'), binding.get('kind'), address(binding['address']))


def verified_bindings(row):
    if row.get('processor') != 'arm9' or row.get('program') or row.get('module') not in {'main', 'itcm', 'dtcm', *('ov' + str(i).zfill(3) for i in range(8))}:
        raise ValueError('Typed packet adapter requires a host ARM9 function namespace')
    proof = row.get('realLink', {})
    if not row.get('exactAfterDeclaredRelocation') or not proof.get('exactCallerBytes'):
        raise ValueError('Typed packet adapter requires a complete genuine caller match')
    if proof.get('sourceObjectSha256') != row['objectSha256'] or proof.get('sourceSha256') != row['sourceSha256'] or proof.get('nativeSpanSha256') != row['targetSha256']:
        raise ValueError('Genuine caller proof differs from fresh source/object/native contracts')
    if not proof.get('splitPreservesRelocationTypesAddendsAndEncodedHBits'):
        raise ValueError('Genuine caller proof lacks unchanged relocation payloads')
    bindings = qualified_bindings(row)
    for field in ['nativeSymbolEntries', 'qualifiedDependencies']:
        if row.get(field) and row[field] != bindings:
            raise ValueError('Existing typed native metadata conflicts with measured bindings')
    functions = {name: binding for name, binding in bindings.items() if binding['kind'] == 'function'}
    probes = proof.get('bindingOnlyProbes', [])
    if len({probe['name'] for probe in probes}) != len(probes) or {probe['name'] for probe in probes} != set(functions):
        raise ValueError('Genuine function mode probe set differs from qualified bindings')
    for probe in probes:
        name = probe['name']
        if binding_identity(probe) != binding_identity(functions[name]):
            raise ValueError('Genuine mode probe disagrees with complete CPU/program/module/mode/address identity: ' + name)
        if probe.get('initializedCodeBytes') != 0 or probe.get('nativeCalleeBytesUsed') != 0 or probe.get('calleeSourceCredit') != 0 or probe.get('linkedInitializedOutputBytes') != 0:
            raise ValueError('Genuine mode anchor unexpectedly contributes initialized callee code')
        path = local(probe['object'])
        if sha256(path) != probe['objectSha256']:
            raise ValueError('Fresh genuine mode anchor object changed')
        with path.open('rb') as stream:
            elf = ELFFile(stream)
            symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
            symbol = next((value for value in symbols if value.name == name), None)
            marker = '$a' if probe['mode'] == 'arm' else '$t'
            if symbol is None or symbol['st_info']['type'] != 'STT_FUNC' or symbol['st_value'] != 0 or symbol['st_size'] != 0:
                raise ValueError('Genuine mode anchor has no zero-sized typed function')
            section = elf.get_section(symbol['st_shndx'])
            if section['sh_type'] != 'SHT_NOBITS' or not any(value.name == marker and value['st_value'] == 0 and value['st_shndx'] == symbol['st_shndx'] for value in symbols):
                raise ValueError('Genuine mode anchor lacks matching uninitialized ARM/Thumb mapping')
    return bindings


def row_contract(row):
    return hashlib.sha256(json.dumps({key: value for key, value in row.items() if key != 'nativeSymbolEntries'}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def adapt(report, descriptor):
    if report.get('processor') != 'arm9' or report.get('program') or not report.get('canonicalReportRefreshedFromFreshWorkerObjects') or not report.get('allPassed', True):
        raise ValueError('Typed adapter requires a fresh successful host ARM9 canonical packet')
    result = copy.deepcopy(report)
    verified = []
    units = []
    for row in result['matches']:
        contract = row_contract(row)
        bindings = verified_bindings(row)
        row['nativeSymbolEntries'] = bindings
        if row_contract(row) != contract:
            raise ValueError('Typed metadata adapter changed a source/object/relocation contract')
        verified.append(dict(name=row['name'], functionBindings=sum(value['kind'] == 'function' for value in bindings.values()), sourceObjectAndRelocationContractSha256=contract))
        units.append(dict(module=row['module'], symbols={row['nativeAlias']: row['name']}, typedNativeBindings=bindings, typedBindingRelocations=row.get('relocations', [])))
    normalized = apply_typed_bindings(units)
    for row, unit in zip(result['matches'], normalized):
        functions = {name: binding for name, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
        resolved = unit.get('typedFunctionBindings', {})
        if set(functions) != set(resolved) or any(binding_identity(functions[name]) != binding_identity(resolved[name]) for name in functions):
            raise ValueError('Existing host binding path changed a qualified function identity')
        for relocation in row.get('relocations', []):
            name = relocation['symbol']
            if name in functions and not functions[name].get('alternateEntryEvidence') and unit['relocationAliases'].get(str(relocation['offset'])) != resolved[name]['linkedNativeSymbol']:
                raise ValueError('Existing host binding path did not resolve a genuine function relocation')
    pins = {pin['path']: pin['sha256'] for pin in result.get('generatorSources', [])}
    for name in code_closure([Path(__file__).name, 'replay_parallel_packet.py']):
        digest = sha256(local(name))
        if name in pins and pins[name] != digest:
            raise ValueError('Frozen canonical producer code changed')
        pins[name] = digest
    result['generatorSources'] = [dict(path=name, sha256=digest) for name, digest in sorted(pins.items())]
    result['typedArm9MetadataAdapter'] = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), reproductionCommand=[Path(__file__).name, descriptor], verifiedRows=verified, existingHostBindingPathQualified=True, sourceObjectRelocationsAndExistingRowContractsUnchanged=True, workerEvidenceUnchanged=True, initializedCalleeCodeAndSourceCredit=0)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('descriptor')
    options = parser.parse_args()
    descriptor_path = local(options.descriptor)
    descriptor = read_json(descriptor_path)
    target = local(descriptor['canonicalReport'])
    if not target.is_relative_to(ROOT / 'evidence/matches') or target.suffix != '.json':
        raise ValueError('Typed canonical report is outside evidence/matches')
    subprocess.run([sys.executable, str(ROOT / 'replay_parallel_packet.py'), options.descriptor], cwd=ROOT, check=True)
    before = read_json(target)
    result = adapt(before, options.descriptor)
    write_json(target, result)
    print(dict(report=descriptor['canonicalReport'], functions=len(result['matches']), bytes=sum(row['bytes'] for row in result['matches']), typedFunctionBindings=sum(row['functionBindings'] for row in result['typedArm9MetadataAdapter']['verifiedRows']), sourceObjectRelocationContractsPreserved=True))


if __name__ == '__main__':
    main()
