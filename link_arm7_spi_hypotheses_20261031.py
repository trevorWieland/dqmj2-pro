import json
import os
from pathlib import Path
import re
import subprocess
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as base
from elf_units import split_symbol
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from project import ROOT, sha256, write_json

PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-spi-functional1204-v1/profile.json'
WORK = ROOT / 'work/arm7-bulk-20261030/lane-spi-functional1204-41'
VIRTUAL = 0x026A0000


def build(row, source_override=None, label=None):
    if (row['program'], row['processor'], row['module'], row['mode']) != ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main', 'arm'):
        raise ValueError('Only qualified child ARM SPI source hypotheses are supported')
    if int(row['address'], 0) not in (0x027F6428, 0x027F6554, 0x027F6680, 0x027F67BC):
        raise ValueError('Unknown SPI entry remains refused')
    source = ROOT / row['source']
    if sha256(source) != row['sourceSha256'] or sha256(base.LINKER) != base.LINKER_HASH:
        raise ValueError('Source hypothesis or original linker changed')
    if source_override is not None:
        source = Path(source_override).resolve()
        source.relative_to((ROOT / 'nonmatching/arm7-bulk/20261031').resolve())
    compiler = ROOT / 'tools/mwccarm/mwccarm/1.2/sp2p3/mwccarm.exe'
    flags = match_runtime.FLAGS[:]
    flags[flags.index('-proc') + 1] = 'arm7tdmi'
    flags[flags.index('-inline') + 1] = 'all'
    flags += ['-lang', 'c99', '-opt', 'space']
    directory = WORK / (label or row['address'][2:])
    directory.mkdir(parents=True, exist_ok=True)
    match_runtime.WORK = directory / 'isolated-runtime'
    origin = {'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source), 'name': row['name']}
    attempt, compiled = crossreuse_utility_c.compile_origin(origin, compiler, flags, directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, masks, body = compiled
    original = ROOT / derived['probeObject']
    caller = directory / 'caller.o'
    with original.open('rb') as stream:
        split_symbol(ELFFile(stream), row['name'], caller)
    if relocation_rows(original, row['name']) != relocation_rows(caller, row['name']):
        raise ValueError('Split object changed relocations/addends')
    modules, unused = base.namespace(row['program'])
    bindings = {}
    with caller.open('rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA'):
                continue
            symbols = elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                symbol = symbols.get_symbol(relocation['r_info_sym'])
                if symbol['st_shndx'] != 'SHN_UNDEF':
                    continue
                match = re.fullmatch(r'native_utility_child_arm7_data_([0-9a-f]{8})', symbol.name)
                if not match or int(match[1], 16) not in (0x040001C0, 0x040001C2):
                    raise ValueError('Unmeasured external symbol remains refused')
                bindings[symbol.name] = base.data_binding(row, int(match[1], 16), modules)
    lcf = directory / 'unit.lcf'
    assignments = '\n'.join(name + ' = ' + binding['address'] + ';' for name, binding in sorted(bindings.items()))
    lcf.write_text('MEMORY {\nCALL: ORIGIN = ' + hex(VIRTUAL) + ' > caller.bin\n}\nSECTIONS {\n.caller: { caller.o(.text) } > CALL\n' + assignments + '\n}\n')
    linked = directory / 'linked.elf'
    argv = [str(base.LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', row['name'], str(lcf), str(caller), '-o', str(linked)]
    result = subprocess.run(argv, cwd=directory, capture_output=True, text=True, timeout=30,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    emitted = (directory / 'caller.bin').read_bytes()
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        own = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
        if own['st_value'] != VIRTUAL or own['st_size'] != len(emitted):
            raise ValueError('Virtual C symbol extent differs')
    proof = dict(origin, processor='arm7', program=row['program'], module=row['module'], mode='arm', nativeAddress=row['address'],
        linkedAddress=hex(VIRTUAL), nativeBytes=row['bytes'], linkedBytes=len(emitted),
        compiler=compiler.relative_to(ROOT).as_posix(), compilerSha256=sha256(compiler), compilerFlags=flags,
        object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], splitObjectSha256=sha256(caller),
        unchangedRelocations=relocation_rows(caller, row['name']), linkerSha256=base.LINKER_HASH,
        linkCommand=argv, cwd=str(directory), lcf=lcf.relative_to(ROOT).as_posix(), lcfSha256=sha256(lcf),
        linkedElfSha256=sha256(linked), emitted=(directory / 'caller.bin').relative_to(ROOT).as_posix(),
        emittedSha256=sha256(directory / 'caller.bin'), bindings=bindings, sourceCredit=0, exactNativeByteCredit=0,
        moduleAdoption=False, originalInstructionsOrAddendsPatched=False)
    write_json(directory / 'link-proof.json', proof)
    return proof, emitted


def main():
    results = []
    for row in json.loads(PROFILE.read_text())['results']:
        proof, body = build(row)
        results.append(proof)
        print(json.dumps({'native': row['address'], 'nativeBytes': row['bytes'], 'compiledBytes': len(body), 'sourceCredit': 0}), flush=True)
    write_json(WORK / 'links.json', {'results': results, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
