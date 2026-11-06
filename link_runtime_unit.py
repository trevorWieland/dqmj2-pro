import argparse
import json
import os
import re
import struct
import subprocess
from pathlib import Path
from project import ROOT, configuration, read_json, sha256, write_json
from elf_units import split_symbol
import match_lowlevel
from elftools.elf.elffile import ELFFile

LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/runtime-unit-links'


def relocation_rows(path, name):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == name)
        payload = elf.get_section(symbol['st_shndx']).data()
        start = symbol['st_value'] & ~1
        rows = []
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                continue
            table = elf.get_section(section['sh_link'])
            for item in section.iter_relocations():
                offset = item['r_offset'] - start
                if not 0 <= offset < symbol['st_size']:
                    continue
                rows.append({'offset': offset, 'type': item['r_info_type'], 'symbol': table.get_symbol(item['r_info_sym']).name,
                             'format': section['sh_type'], 'explicitAddend': item['r_addend'] if section['sh_type'] == 'SHT_RELA' else None,
                             'originalEncodedWord': payload[start + offset:start + offset + 4].hex()})
        return rows


def binding_object(name, mode, flags, output):
    if not re.fullmatch(r'[A-Za-z_]\w*', name) or mode not in ('arm', 'thumb'):
        raise ValueError('Invalid typed function binding')
    strings = b'\0' + (('$t' if mode == 'thumb' else '$a') + '\0' + name + '\0').encode()
    symbol_name = 4
    symbols = bytes(16) + struct.pack('<IIIBBH', 1, 0, 0, 2, 0, 1) + struct.pack('<IIIBBH', symbol_name, 0, 0, 0x12, 0, 1)
    names = b'\0.text\0.symtab\0.strtab\0.shstrtab\0'
    payload = bytearray(52)
    text_at = len(payload)
    symbol_at = len(payload)
    payload.extend(symbols)
    string_at = len(payload)
    payload.extend(strings)
    name_at = len(payload)
    payload.extend(names)
    payload.extend(bytes((-len(payload)) % 4))
    table_at = len(payload)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (1, 8, 6, 0, text_at, 2 if mode == 'thumb' else 4, 0, 0, 2 if mode == 'thumb' else 4, 0),
                (7, 2, 0, 0, symbol_at, len(symbols), 3, 2, 4, 16),
                (15, 3, 0, 0, string_at, len(strings), 0, 0, 1, 0),
                (23, 3, 0, 0, name_at, len(names), 0, 0, 1, 0)]
    for section in sections:
        payload.extend(struct.pack('<IIIIIIIIII', *section))
    ident = b'\x7fELF\x01\x01\x01' + bytes(9)
    payload[:52] = struct.pack('<16sHHIIIIIHHHHHH', ident, 1, 40, 1, 0, 0, table_at, flags, 52, 0, 0, 40, 5, 4)
    output.write_bytes(payload)


def measured_module(name):
    manifest = read_json(ROOT / 'provenance/seed-manifest.json')
    module = next(module for module in manifest['modules'] if module['name'] == name)
    binary = ROOT / module['binary']
    if sha256(binary) != module['sha256']:
        raise ValueError('Runtime reference module changed')
    config = ROOT / ('config/arm9/symbols.txt' if name == 'main' else f'config/arm9/{name}/symbols.txt' if name in ('itcm', 'dtcm') else f'config/arm9/overlays/{name}/symbols.txt')
    return module, binary.read_bytes(), config.read_text()


def verify_binding(name, binding):
    if binding.get('processor') != 'arm9' or binding.get('program'):
        raise ValueError('Host ARM9 binding crosses CPU/program namespace')
    target = int(binding['address'], 0)
    mode = binding['mode']
    if binding.get('kind') != 'function':
        if mode != 'data':
            raise ValueError('Non-function binding must explicitly name data mode')
        return target
    if mode not in ('arm', 'thumb') or target % (4 if mode == 'arm' else 2):
        raise ValueError('Function binding must use its canonical even instruction address')
    if binding.get('alternateEntryEvidence'):
        from native_alternate_entries import verify
        return verify(name, binding)['address']
    module, binary, config = measured_module(binding['module'])
    if not re.search(r'^\S+ kind:function\(' + mode + r',size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + r'$', config, re.M):
        raise ValueError('Function binding mode/address lacks a qualified configured native entry')
    return target


def validate(entry, bindings, directory=None):
    if sha256(LINKER) != LINKER_HASH:
        raise ValueError('Runtime unit linker pin changed')
    if entry.get('processor') != 'arm9' or entry.get('program'):
        raise ValueError('Unit linker currently supports qualified host ARM9 source callers')
    address, size = int(entry['address'], 0), entry.get('bytes', entry.get('size'))
    module, binary, config = measured_module(entry['module'])
    if entry.get('romSha256', configuration()['romSha256']) != configuration()['romSha256']:
        raise ValueError('Caller names a different original ROM')
    mode = entry['mode'].lower()
    boundary = re.search(r'^\S+ kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
    if boundary is None or int(boundary[1], 0) != size:
        raise ValueError('Caller span lacks its complete configured native boundary')
    offset = address - int(module['base'], 0)
    native = binary[offset:offset + size]
    if len(native) != size or match_lowlevel.sha(native) != entry['targetSha256']:
        raise ValueError('Caller native span hash changed')
    source, original = ROOT / entry['source'], ROOT / entry['object']
    if sha256(source) != entry['sourceSha256'] or sha256(original) != entry['objectSha256']:
        raise ValueError('Caller source/immutable compiled object changed')
    directory = Path(directory or WORK / (entry['name'] + '-' + entry['objectSha256'][:12]))
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with original.open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller, section_padding=entry.get('sectionPaddingBytes', 0))
    original_relocations = relocation_rows(original, entry['name'])
    if original_relocations != relocation_rows(caller, entry['name']):
        raise ValueError('Caller split changed a relocation, addend or encoded instruction/H bit')
    required = set()
    with caller.open('rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] in ('SHT_REL', 'SHT_RELA'):
                table = elf.get_section(section['sh_link'])
                for relocation in section.iter_relocations():
                    symbol = table.get_symbol(relocation['r_info_sym'])
                    if symbol['st_shndx'] == 'SHN_UNDEF':
                        required.add(symbol.name)
    if required - set(bindings):
        raise ValueError('Unqualified caller externs: ' + ','.join(sorted(required - set(bindings))))
    memories = [f'CALL: ORIGIN = {address:#x} > caller.bin']
    sections = ['.caller: { caller.o(.text) } > CALL']
    objects, probes, assignments = [caller], [], []
    for index, name in enumerate(sorted(required)):
        binding = bindings[name]
        target = verify_binding(name, binding)
        if binding['kind'] == 'function':
            probe = directory / f'binding{index}.o'
            binding_object(name, binding['mode'], flags, probe)
            objects.append(probe)
            memories.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin')
            sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}')
            probes.append({'name': name, **binding, 'object': probe.relative_to(ROOT).as_posix(), 'objectSha256': sha256(probe),
                           'initializedCodeBytes': 0, 'nativeCalleeBytesUsed': 0, 'calleeSourceCredit': 0, 'elfSectionKind': 'SHT_NOBITS',
                           'allocatedModeAnchorBytes': 2 if binding['mode'] == 'thumb' else 4, 'functionSymbolSize': 0})
        else:
            assignments.append(f'{name} = {target:#x};')
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memories) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked = directory / 'linked.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    attempt = {'command': command, 'cwd': str(directory), 'exitCode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}
    if process.returncode:
        raise ValueError('Isolated real runtime link failed: ' + json.dumps(attempt))
    output = (directory / 'caller.bin').read_bytes()
    if output != native:
        raise ValueError({'caller': entry['name'], 'nativeBytes': size, 'linkedBytes': len(output), 'matchingBytes': sum(a == b for a, b in zip(output, native)), 'directory': str(directory)})
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if symbol['st_value'] != address or symbol['st_size'] != size:
            raise ValueError('Linked caller symbol range changed')
        for probe in probes:
            target = int(probe['address'], 0)
            symbol = next(symbol for symbol in symbols if symbol.name == probe['name'])
            mapping = '$t' if probe['mode'] == 'thumb' else '$a'
            if symbol['st_value'] != target or symbol['st_size'] != 0:
                raise ValueError('Linked mode anchor acquired callee code or a wrong address')
            anchor_output = (ROOT / probe['object']).with_suffix('.bin')
            if anchor_output.exists() and anchor_output.stat().st_size:
                raise ValueError('A binding-only anchor emitted initialized callee bytes')
            probe['linkedInitializedOutputBytes'] = 0
            if not any(symbol.name == mapping and symbol['st_value'] == target for symbol in symbols):
                raise ValueError('Linked binding lacks its declared ARM/Thumb mapping symbol')
    result = {'exactCallerBytes': True, 'name': entry['name'], 'module': entry['module'], 'processor': 'arm9', 'address': entry['address'],
              'bytes': size, 'sourceSha256': entry['sourceSha256'], 'sourceObjectSha256': entry['objectSha256'], 'splitObjectSha256': sha256(caller),
              'linkedCallerSha256': match_lowlevel.sha(output), 'nativeSpanSha256': entry['targetSha256'], 'linkerSha256': LINKER_HASH,
              'linkerAttempt': attempt, 'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': sha256(lcf),
              'linkedElf': linked.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha256(linked), 'bindingOnlyProbes': probes,
              'originalRelocations': original_relocations, 'splitPreservesRelocationTypesAddendsAndEncodedHBits': True,
              'generator': 'link_runtime_unit.py', 'generatorSha256': sha256(Path(__file__)),
              'calleeCodeOrSourceCredit': 0, 'wholeModuleLinked': False,
              'limitations': ['Only the isolated caller span is linked and compared; zero-sized function symbols in uninitialized2/4-byte mode anchors supply no executable callee body or source credit', 'Source relocations and REL/RELA addends remain unchanged; the pinned real MW linker performs interworking encoding', 'Physical/native callee behavior and a full host-module link remain separate checks']}
    write_json(directory / 'validation.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--name')
    args = parser.parse_args()
    report = read_json(args.report)
    bindings = report.get('nativeSymbolEntries', report.get('bindings', {}))
    entries = [entry for entry in report['matches'] if args.name is None or entry['name'] == args.name]
    results = [validate({**report, **entry}, bindings) for entry in entries]
    print({'validatedCallers': len(results), 'bytes': sum(entry['bytes'] for entry in results), 'calleeCredit': 0})


if __name__ == '__main__':
    main()
