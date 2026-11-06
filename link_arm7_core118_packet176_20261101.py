import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path
import match_lowlevel
import arm7_runtime
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from link_runtime_unit import binding_object, relocation_rows

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def namespace(program):
    if program:
        if program != utility_runtime.PROGRAM:
            raise ValueError('Unknown ARM7 program namespace')
        layout, unused = utility_runtime.derive()
        inventory = json.loads((ROOT / 'evidence/utility/ghidra-arm7.json').read_text())
    else:
        layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
        inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    functions = {}
    for row in inventory['functions']:
        if row.get('mode') in ('arm', 'thumb') and row['module'] in modules:
            address = int(row['address'], 0)
            binding = {'program': program, 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'],
                'kind': 'function', 'address': hex(address), 'boundarySource': 'measured-runtime-map-Ghidra-entry; caller-boundary-audit-separate'}
            if address in functions and functions[address] != binding:
                raise ValueError('Conflicting same-program ARM7 function modes')
            functions[address] = binding
    return modules, functions


def data_binding(entry, target, modules):
    ranges = []
    for module in modules.values():
        base = int(module.get('base', module['runtimeBase']), 0)
        if base <= target < base + module['bytes']:
            ranges.append((module['id'], 'initialized'))
        if int(module['bssStart'], 0) <= target < int(module['bssEnd'], 0):
            ranges.append((module['id'], 'bss'))
    if len(ranges) > 1:
        raise ValueError('Data target ambiguously overlaps ARM7 modules')
    if ranges:
        module, region = ranges[0]
    elif 0x02000000 <= target < 0x02400000:
        module, region = 'external-shared-main-ram', 'not-owned-by-initialized-ARM7-module'
    elif 0x04000000 <= target < 0x05000000:
        module, region = 'external-mmio', 'address-region-only-no-register-meaning'
    elif target == 0x0380FFF4:
        expected_identities = {('', 'arm7', 'arm7-main', 'arm', '0x27e91bc', 176): 'c8f566b189a9e887cf5377f75030b319eda6c3150541f63b21a925758c590cb2'}
        source_closures = {'0x27e91bc': ('src/arm7/20261101_core118_packet176/native_arm7_main_027e91bc.c', '8f3b5bd14bc05b910a7dcb80bcfb5b0845931530cca1eaf4690065bb92a3a88a')}
        if (entry.get('source'), entry.get('sourceSha256')) != source_closures.get(entry.get('address')):
            raise ValueError('Qualified runtime pointer caller source closure differs')
        actual_identity = tuple(entry.get(key, '') for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes'))
        qualification = {'report': 'evidence/attempts/arm7-lane-setting-producer-20261031.json', 'sha256': 'e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4', 'storageBytes': 4}
        if actual_identity not in expected_identities or entry.get('targetSha256') != expected_identities[actual_identity] or entry.get('romSha256') != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or entry.get('runtimePointerQualification') != qualification:
            raise ValueError('External runtime pointer lacks its exact qualified caller/word contract')
        evidence = ROOT / qualification['report']
        if digest(evidence.read_bytes()) != qualification['sha256'] or digest((ROOT / 'link_arm7_bulk_20261030.py').read_bytes()) != 'f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c':
            raise ValueError('External runtime pointer producer/base policy differs')
        report = json.loads(evidence.read_text())
        if digest((ROOT / report['generator']).read_bytes()) != report['generatorSha256']:
            raise ValueError('External runtime pointer producer generator differs')
        if report['storage'] != '0x0380fff4' or report['storageBytes'] != 4 or report['origin'] != 'incoming descriptor word0' or report['constructorReturnCredit'] != 0 or report['moduleBssOwnership'] is not False:
            raise ValueError('External runtime pointer producer scope differs')
        return {'program': '', 'processor': 'arm7', 'module': 'external-arm7-runtime-pointer-word',
            'kind': 'data', 'mode': 'data', 'address': hex(target), 'region': 'descriptor-produced-absolute-pointer-no-module-ownership',
            'storageBytes': 4, 'producerQualification': qualification, 'sourceCredit': 0}
    else:
        raise ValueError('Unqualified external ARM7 data target: ' + hex(target))
    return {'program': entry.get('program', ''), 'processor': 'arm7', 'module': module,
        'kind': 'data', 'mode': 'data', 'address': hex(target), 'region': region}


def derive_bindings(entry, native, functions, modules):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if entry['mode'] == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    address = int(entry['address'], 0)
    source = (ROOT / entry['source']).read_text()
    bindings = {}
    for rel in entry['relocations']:
        name, offset, kind = rel['symbol'], rel['offset'], rel['type']
        if kind == 2:
            addend = rel['explicitAddend'] if rel['format'] == 'SHT_RELA' else int.from_bytes(bytes.fromhex(rel['originalEncodedWord']), 'little')
            target = (struct.unpack_from('<I', native, offset)[0] - addend) & 0xFFFFFFFF
            function = bool(re.search(r'\b' + re.escape(name) + r'\s*\(', source)) or '_fn_' in name or '_thumb_' in name or '_arm_' in name
        elif kind in (1, 10, 15, 28, 29):
            instruction = next(decoder.disasm(native[offset:offset + 4], address + offset), None)
            if instruction is None or not instruction.operands or instruction.operands[0].type != 2:
                raise ValueError('Original relocated call/jump has no immediate native target')
            target, function = instruction.operands[0].imm & 0xFFFFFFFF, True
        else:
            raise ValueError('Unsupported unmodified ARM7 relocation')
        if function:
            canonical = target & ~1
            if canonical not in functions:
                raise ValueError('Unqualified ARM7 native function/alternate entry: ' + name + ' ' + hex(target))
            binding = functions[canonical]
            if kind == 2 and bool(target & 1) != (binding['mode'] == 'thumb'):
                raise ValueError('Function-pointer native tag/mode disagrees')
        else:
            binding = data_binding(entry, target, modules)
        encoded = re.search(r'_([0-9a-fA-F]{8})$', name)
        if encoded and (int(encoded[1], 16) & (~1 if function else 0xFFFFFFFF)) != (target & (~1 if function else 0xFFFFFFFF)):
            raise ValueError('Address-labelled source symbol conflicts with measured native binding')
        if name in bindings and bindings[name] != binding:
            raise ValueError('One source symbol has conflicting native identities')
        bindings[name] = binding
    return bindings


def validate_caller_contract(entry):
    allowed = {('', 'arm7', 'arm7-main', 'arm', '0x27e91bc', 176): {'source': 'src/arm7/20261101_core118_packet176/native_arm7_main_027e91bc.c', 'sourceSha256': '8f3b5bd14bc05b910a7dcb80bcfb5b0845931530cca1eaf4690065bb92a3a88a', 'targetSha256': 'c8f566b189a9e887cf5377f75030b319eda6c3150541f63b21a925758c590cb2', 'inputModuleSha256': 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'}}
    identity = tuple(entry.get(key, '') for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes'))
    if identity not in allowed or any(entry.get(key) != value for key, value in allowed[identity].items()):
        raise ValueError('New runtime-pointer policy requires its full caller/source/module identity')
    if entry.get('romSha256') != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or entry.get('runtimePointerQualification') != {'report': 'evidence/attempts/arm7-lane-setting-producer-20261031.json', 'sha256': 'e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4', 'storageBytes': 4}:
        raise ValueError('Exact original-ROM/producer-write four-byte qualification absent')


def validate(entry, directory):
    validate_caller_contract(entry)
    if entry.get('processor') != 'arm7' or digest(LINKER.read_bytes()) != LINKER_HASH:
        raise ValueError('Pinned ARM7-only linker contract differs')
    modules, functions = namespace(entry.get('program', ''))
    metadata = modules[entry['module']]
    path = ROOT / metadata['binary']
    binary = path.read_bytes()
    if digest(binary) != metadata['sha256'] or entry['inputModuleSha256'] != metadata['sha256']:
        raise ValueError('ARM7 source module input changed')
    address, size = int(entry['address'], 0), entry['bytes']
    base = int(metadata.get('base', metadata.get('runtimeBase')), 0)
    native = binary[address - base:address - base + size]
    if len(native) != size or digest(native) != entry['targetSha256'] or address not in functions or functions[address]['mode'] != entry['mode']:
        raise ValueError('Complete candidate span or canonical ARM7 entry differs')
    source, original = ROOT / entry['source'], ROOT / entry['object']
    if digest(source.read_bytes()) != entry['sourceSha256'] or digest(original.read_bytes()) != entry['objectSha256']:
        raise ValueError('Candidate source/immutable object changed')
    bindings = derive_bindings(entry, native, functions, modules)
    directory = Path(directory).resolve()
    directory.relative_to(WORK.resolve())
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with original.open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    before, after = relocation_rows(original, entry['name']), relocation_rows(caller, entry['name'])
    if before != after:
        raise ValueError('Function split modified a relocation/addend/encoded instruction')
    required = set()
    with caller.open('rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] in ('SHT_REL', 'SHT_RELA'):
                table = elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    symbol = table.get_symbol(rel['r_info_sym'])
                    if symbol['st_shndx'] == 'SHN_UNDEF':
                        required.add(symbol.name)
    if required - set(bindings):
        raise ValueError('Unbound ARM7 caller externs')
    memories, sections, objects, probes, assignments = [f'CALL: ORIGIN = {address:#x} > caller.bin'], ['.caller: { caller.o(.text) } > CALL'], [caller], [], []
    for index, name in enumerate(sorted(required)):
        binding = bindings[name]
        target = int(binding['address'], 0)
        if binding['kind'] == 'function':
            anchor = directory / ('anchor' + str(index) + '.o')
            binding_object(name, binding['mode'], flags, anchor)
            objects.append(anchor)
            memories.append(f'BIND{index}: ORIGIN = {target:#x} > anchor{index}.bin')
            sections.append(f'.binding{index}: {{ anchor{index}.o(.text) }} > BIND{index}')
            probes.append({'symbol': name, **binding, 'object': anchor.relative_to(ROOT).as_posix(), 'objectSha256': digest(anchor.read_bytes()),
                'initializedCodeBytes': 0, 'calleeSourceCredit': 0})
        else:
            assignments.append(name + ' = ' + hex(target) + ';')
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memories) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked = directory / 'linked.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError('Real ARM7 link failed: ' + result.stdout + result.stderr)
    output = (directory / 'caller.bin').read_bytes()
    if output != native:
        raise ValueError({'nativeBytes': size, 'linkedBytes': len(output), 'matchingBytes': sum(a == b for a, b in zip(output, native))})
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        own = next(row for row in symbols if row.name == entry['name'])
        if own['st_value'] != address or own['st_size'] != size:
            raise ValueError('Linked ARM7 function symbol extent differs')
        for probe in probes:
            target = int(probe['address'], 0)
            symbol = next(row for row in symbols if row.name == probe['symbol'])
            if symbol['st_value'] != target or symbol['st_size'] != 0:
                raise ValueError('ARM7 zero-code callee binding changed extent')
            if not any(row.name == ('$t' if probe['mode'] == 'thumb' else '$a') and row['st_value'] == target for row in symbols):
                raise ValueError('ARM7 binding lost canonical instruction-mode mapping')
            output_path = (ROOT / probe['object']).with_suffix('.bin')
            if output_path.exists() and output_path.stat().st_size:
                raise ValueError('ARM7 binding acquired initialized callee code')
    proof = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'processor': 'arm7',
        'program': entry.get('program', ''), 'module': entry['module'], 'address': entry['address'], 'mode': entry['mode'], 'bytes': size,
        'exactLinkedBytes': True, 'linkedCallerSha256': digest(output), 'targetSha256': entry['targetSha256'], 'sourceSha256': entry['sourceSha256'],
        'sourceObjectSha256': entry['objectSha256'], 'splitObjectSha256': digest(caller.read_bytes()), 'unchangedRelocations': before,
        'bindings': bindings, 'zeroCodeAnchors': probes, 'linkerSha256': LINKER_HASH, 'linkCommand': command, 'cwd': str(directory),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': digest(lcf.read_bytes()), 'linkedElfSha256': digest(linked.read_bytes()),
        'boundaryAndAbiAndNativeExecutionStillRequired': True, 'wholeModuleLinked': False, 'currentSourceCredit': 0, 'calleeSourceCredit': 0}
    (directory / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text())
    results = []
    for index, entry in enumerate(report['relocationOnlyCandidates']):
        try:
            proof = validate(entry, WORK / args.batch / entry['module'] / (entry['address'][2:] + '-' + entry['objectSha256'][:12]))
            results.append({'entry': entry, 'proof': proof})
        except Exception as error:
            results.append({'entry': entry, 'failure': type(error).__name__ + ': ' + str(error)})
        print(json.dumps({'processed': index + 1, 'address': entry['address'], 'module': entry['module'], 'realLinkExact': 'proof' in results[-1]}), flush=True)
    output = WORK / args.batch / 'results.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'results': results, 'currentSourceCredit': 0}, indent=2) + '\n')


if __name__ == '__main__':
    main()
