import os
import shutil
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256, write_json
import link_runtime_unit as L


def link_private(entry, bindings, canonical_directory, private_directory, origin):
    canonical_directory, private_directory = ROOT / canonical_directory, ROOT / private_directory
    if origin & 3 or not 0x02650000 <= origin < 0x02670000:
        raise ValueError('Private hypothesis origin outside owned aligned window')
    if sha256(L.LINKER) != L.LINKER_HASH:
        raise ValueError('Private hypothesis linker pin differs')
    source, compiled = ROOT / entry['source'], ROOT / entry['object']
    if sha256(source) != entry['sourceSha256'] or sha256(compiled) != entry['objectSha256']:
        raise ValueError('Private hypothesis source/object changed')
    row = L.relocation_rows(compiled, entry['name'])
    if row != L.relocation_rows(canonical_directory / 'caller.o', entry['name']):
        raise ValueError('Canonical split object changed relocation/addend/H-bit records')
    old_lcf = canonical_directory / 'unit.lcf'
    token = 'CALL: ORIGIN = ' + hex(int(entry['address'], 0)) + ' > caller.bin'
    text = old_lcf.read_text()
    if text.count(token) != 1:
        raise ValueError('Private hypothesis expected single canonical CALL origin')
    required = set()
    with (canonical_directory / 'caller.o').open('rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] in ('SHT_REL', 'SHT_RELA'):
                table = elf.get_section(section['sh_link'])
                for relocation in section.iter_relocations():
                    symbol = table.get_symbol(relocation['r_info_sym'])
                    if symbol['st_shndx'] == 'SHN_UNDEF':
                        required.add(symbol.name)
    private_directory.mkdir(parents=True, exist_ok=True)
    objects = [canonical_directory / 'caller.o'] + sorted(canonical_directory.glob('binding*.o'))
    copies = []
    for path in objects:
        target = private_directory / path.name
        shutil.copyfile(path, target)
        if sha256(path) != sha256(target):
            raise ValueError('Private hypothesis object copy changed')
        copies.append(dict(name=path.name, sha256=sha256(target)))
    lcf = private_directory / 'unit.lcf'
    lcf.write_text(text.replace(token, 'CALL: ORIGIN = ' + hex(origin) + ' > caller.bin'))
    if lcf.read_text().replace(hex(origin), hex(int(entry['address'], 0)), 1) != text:
        raise ValueError('Private hypothesis changed LCF beyond caller origin')
    linked = private_directory / 'linked.elf'
    command = [str(L.LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', entry['name'], str(lcf), *[str(private_directory / path.name) for path in objects], '-o', str(linked)]
    process = subprocess.run(command, cwd=private_directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    attempt = dict(command=command, cwd=str(private_directory), exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
    if process.returncode:
        raise ValueError(('Private real linker failed', attempt))
    body = (private_directory / 'caller.bin').read_bytes()
    anchors = []
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        if elf['e_machine'] != 'EM_ARM' or elf.elfclass != 32 or not elf.little_endian:
            raise ValueError('Private linked ELF architecture differs')
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        symbol = next(s for s in symbols if s.name == entry['name'])
        if symbol['st_value'] != origin or symbol['st_size'] != len(body) or len(body) != entry['compiledBytes']:
            raise ValueError('Private caller symbol extent differs')
        if not any(s.name == '$a' and s['st_value'] == origin for s in symbols):
            raise ValueError('Private caller ARM mapping differs')
        for name in sorted(required):
            binding = bindings[name]
            address = L.verify_binding(name, binding)
            if origin <= address < origin + len(body):
                raise ValueError('Private caller overlaps qualified binding')
            if binding['kind'] == 'function':
                symbol = next(s for s in symbols if s.name == name)
                mode = '$t' if binding['mode'] == 'thumb' else '$a'
                if symbol['st_value'] != address or symbol['st_size'] != 0 or not any(s.name == mode and s['st_value'] == address for s in symbols):
                    raise ValueError('Private mode anchor changed')
                anchors.append(dict(name=name, address=address, mode=binding['mode'], functionSymbolSize=0, calleeSourceCredit=0))
        for path in private_directory.glob('binding*.bin'):
            if path.stat().st_size:
                raise ValueError('Private anchor emitted callee bytes')
    proof = dict(schemaVersion=1, sourceCredit=0, canonicalIdentity={key: entry[key] for key in ['processor', 'module', 'mode', 'address', 'bytes', 'targetSha256']}, privateAddress=hex(origin), privateBytes=len(body), sourceSha256=entry['sourceSha256'], originalObjectSha256=entry['objectSha256'], copiedObjects=copies, originalRelocations=row, relocationTypesAddendsAndEncodedHBitsUnchanged=True, canonicalLcf=dict(path=old_lcf.relative_to(ROOT).as_posix(), sha256=sha256(old_lcf)), privateLcf=dict(path=lcf.relative_to(ROOT).as_posix(), sha256=sha256(lcf)), callerOriginOnlyLcfChange=True, linkerSha256=L.LINKER_HASH, linkerAttempt=attempt, linkedElf=dict(path=linked.relative_to(ROOT).as_posix(), sha256=sha256(linked)), callerBinarySha256=sha256(private_directory / 'caller.bin'), qualifiedZeroCodeAnchors=anchors, calleeSourceCredit=0, nativeBytesOverwritten=0, limits=['Separate private-origin genuinely linked ordinary C behavior experiment; canonical source-byte comparison stays independent and unaccepted.', 'PC/LR/code-address differences require explicit fixture qualification; private storage and supplied services add no game/source credit.'])
    write_json(private_directory / 'private-link.json', proof)
    return proof, body
