import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import sys
import time
from cohort176_epoch_v1 import canonical, identity, require, safe, sha


TOKEN = object()


def local(root, name):
    path = root / safe(name)
    require(path.resolve() == path.absolute() and path.resolve().is_relative_to(root), 'Escaping native input')
    return path


def imported_origins(root, pins, modules):
    root_names = {Path(p).stem for p in pins if len(Path(p).parts) == 1 and p.endswith('.py')}
    observed = []
    for name, module in list(modules.items()):
        if name not in root_names and name.split('.')[0] not in ('elftools', 'ndspy', 'capstone'):
            continue
        require(getattr(module, '__file__', None) is not None, 'Missing reader module origin')
        path = Path(module.__file__).resolve()
        require(path.is_relative_to(root), 'Reader fallback outside owned root')
        relative = path.relative_to(root).as_posix()
        require(relative in pins and sha(local(root, relative).read_bytes()) == pins[relative], 'Unpinned reader source or cache origin')
        observed.append(dict(module=name, path=relative, sha256=pins[relative]))
    return observed


def source_graph(root, row):
    require(row['ordinaryCBytes'] == row['bytes'], 'Incomplete ordinary C extent')
    pins = [(row['source'], row['sourceSha256']), *[(h['path'], h['sha256']) for h in row['sourceDependencies']]]
    documents = {}
    for name, digest in pins:
        path = local(root, name)
        require(name.startswith('src/') and path.suffix == ('.c' if name == row['source'] else '.h'), 'Non-C/header compiler input')
        require(name not in documents and sha(path.read_bytes()) == digest, 'Duplicate or changed compiler input')
        text = path.read_text(encoding='utf-8')
        require(not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin|\\\r?\n|\?\?|%:', text), 'Ambiguous or assembly compiler input')
        documents[name] = text
    edges = {}
    for name, text in documents.items():
        edges[name] = []
        for line in text.splitlines():
            if re.match(r'^\s*#\s*(?:include|include_next|import|embed)\b', line):
                match = re.fullmatch(r'\s*#\s*include\s+"([^"<>]+)"\s*', line)
                require(match is not None, 'Unclosed compiler include')
                target = (PurePosixPath(name).parent / match[1]).as_posix()
                require(target in documents, 'Undeclared quoted header')
                edges[name].append(target)
    reached, active = set(), set()
    def visit(name):
        require(name not in active, 'Cyclic header graph')
        if name in reached:
            return
        active.add(name)
        for child in edges[name]:
            visit(child)
        active.remove(name)
        reached.add(name)
    visit(row['source'])
    require(reached == documents.keys(), 'Unreachable declared header')
    flags = row['compilerFlags']
    require(flags.count('-proc') == 1 and flags[flags.index('-proc') + 1] == 'arm946e', 'Wrong processor flags')
    require(flags.count('-thumb') == (row['mode'] == 'thumb'), 'Wrong mode flags')
    require((flags.count('-lang') == 1 and flags[flags.index('-lang') + 1] == 'c99') if row['mode'] == 'arm' else '-lang' not in flags, 'Wrong frozen language profile')
    for flag in flags:
        lower = flag.lower()
        require(not lower.startswith(('@', '-include', '-prefix', '-i', '-d', '-u')) or lower.startswith(('-inline', '-interworking', '-ipa')), 'Hidden compiler input')
        require(flag not in ('-c', '-o') and not any(x in lower for x in ('extract/', 'inputs/', 'asm/', '\\', '.bin', '.nds', '.o', '.inc')), 'File-bearing compiler flag')
    return dict(edges=edges, source=row['source'], sourceSha256=row['sourceSha256'], includes=row['sourceDependencies'], originalCodeCompilerInput=False)


def object_contract(path, row):
    from elftools.elf.elffile import ELFFile
    with Path(path).open('rb') as stream:
        elf = ELFFile(stream)
        require(elf.elfclass == 32 and elf.little_endian and elf['e_machine'] == 'EM_ARM' and elf['e_type'] == 'ET_REL', 'Wrong relocatable ELF')
        allocated = {i: s for i, s in enumerate(elf.iter_sections()) if s['sh_flags'] & 2}
        nonempty = [(i, s) for i, s in allocated.items() if s['sh_size']]
        require(len(nonempty) == 1 and nonempty[0][1].name == '.text' and nonempty[0][1]['sh_size'] == row['bytes'], 'Extra or incomplete allocated source extent')
        table = elf.get_section_by_name('.symtab')
        symbols = list(table.iter_symbols())
        selected = [s for s in symbols if s.name == row['name']]
        require(len(selected) == 1, 'Duplicate or missing source function')
        function = selected[0]
        require(function['st_info']['type'] == 'STT_FUNC' and function['st_shndx'] == nonempty[0][0] and function['st_size'] == row['bytes'] and function['st_value'] & ~1 == 0, 'Wrong function geometry')
        mapping = '$t' if row['mode'] == 'thumb' else '$a'
        require(any(s.name == mapping and s['st_shndx'] == function['st_shndx'] and s['st_value'] == 0 for s in symbols), 'Wrong actual instruction mapping')
        section_contract = [(s.name, s['sh_type'], s['sh_flags'], s['sh_addralign'], s['sh_size'], sha(s.data()) if s['sh_type'] != 'SHT_NOBITS' else None) for s in allocated.values()]
        def symbol_contract(symbol):
            index = symbol['st_shndx']
            return (symbol.name, allocated[index].name if index in allocated else index, symbol['st_value'], symbol['st_size'], symbol['st_info']['type'], symbol['st_info']['bind'], symbol['st_other']['visibility'])
        defined = sorted(symbol_contract(s) for s in symbols if s['st_shndx'] in allocated)
        relocations = []
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] not in allocated:
                continue
            reference = elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                relocations.append((allocated[section['sh_info']].name, section['sh_type'], relocation['r_offset'], relocation['r_info_type'], relocation['r_addend'] if section['sh_type'] == 'SHT_RELA' else None, symbol_contract(reference.get_symbol(relocation['r_info_sym']))))
    return dict(flags=elf['e_flags'], sections=section_contract, symbols=defined, relocations=relocations)


def derive(root, contract):
    from project import configuration
    from qualify_arm9_thumb_reference_inputs_20261105 import derive as derive_main
    from ndspy.codeCompression import decompress
    cfg = configuration()
    rom = cfg['rom'].read_bytes()
    require(sha(rom) == contract['romSha256'], 'Wrong owned ROM')
    values = {'extract/arm9/arm9.bin': derive_main()}
    table, size = struct.unpack_from('<II', rom, 0x50)
    fat, fat_size = struct.unpack_from('<II', rom, 0x48)
    require(size % 32 == 0 and table + size <= len(rom) and fat + fat_size <= len(rom), 'Overlay table bounds')
    records = [struct.unpack_from('<8I', rom, p) for p in range(table, table + size, 32)]
    require(len({r[0] for r in records}) == len(records), 'Duplicate physical overlay')
    for name, module in contract['modules'].items():
        matches = [r for r in records if r[0] == int(name[2:])]
        require(len(matches) == 1, 'Missing physical overlay')
        entry = matches[0]
        require(entry[6] * 8 + 8 <= fat_size, 'FAT ID out of bounds')
        begin, end = struct.unpack_from('<II', rom, fat + 8 * entry[6])
        require(0 <= begin < end <= len(rom), 'FAT extent')
        data = decompress(rom[begin:end]) if entry[7] >> 24 & 1 else rom[begin:end]
        require(entry[1] == int(module['base'], 0) and entry[2] == len(data) == module['bytes'], 'Wrong native module layout')
        require(sha(data) == module['sha256'] and data == local(root, module['binary']).read_bytes(), 'Wrong derived original image')
        values[module['binary']] = data
    return values


class LiveReferences:
    def __init__(self, token, epoch, root, inputs, rows, started, artifacts):
        require(token is TOKEN, 'Live proofs cannot load from receipts')
        self.token, self.root, self.started = token, root, started
        self.epoch_hash = epoch.contract_hash
        self.inputs = dict(inputs)
        self.rows = rows
        self.rows_hash = canonical(rows)
        self.identities = {tuple(r['identity']) for r in rows}
        self.artifacts = artifacts
        self.ensure(epoch)

    def ensure(self, epoch):
        require(self.token is TOKEN and self.epoch_hash == epoch.contract_hash and len(self.rows) == 6, 'Wrong live qualification capability')
        require(canonical(self.rows) == self.rows_hash and self.identities == {tuple(r['identity']) for r in self.rows}, 'Live proof metadata changed')
        epoch.ensure()
        for name, digest in self.inputs.items():
            require(sha(local(self.root, name).read_bytes()) == digest, 'Live proof input or artifact changed')
        for row in self.rows:
            require(row['exitCode'] == 0 and row['startedTimeNs'] >= self.started and local(self.root, row['freshObject']).stat().st_mtime_ns >= self.started, 'Stale or failed compilation')
            require(row['linked']['exactCallerBytes'] is True and row['linked']['linkedCallerSha256'] == row['targetSha256'], 'Missing genuine native placement')


def qualify(epoch, root, directory):
    require(epoch.committed_revision is not None, 'Native qualification requires a committed audit epoch')
    import link_runtime_unit as linker
    import parallel_packet_native_unit_identity_v1 as names
    from parallel_packet_native_unit_identity_v1 import witness_name
    root, directory = Path(root).resolve(), Path(directory).resolve()
    require(Path(linker.__file__).resolve() == root / 'link_runtime_unit.py' and linker.ROOT.resolve() == root, 'Wrong linker backend origin')
    require(Path(names.__file__).resolve() == root / 'parallel_packet_native_unit_identity_v1.py', 'Wrong identity reader origin')
    require(directory.is_relative_to(root / 'work') and directory == directory.absolute() and not directory.exists(), 'Exclusive confined live output required')
    epoch.ensure()
    inputs = {p['path']: p['sha256'] for p in epoch.contract['nativeInputs']}
    inputs.update({p['path']: p['sha256'] for p in epoch.contract['implementationPins']})
    for name, digest in inputs.items():
        require(sha(local(root, name).read_bytes()) == digest, 'Native qualification input changed')
    images = derive(root, epoch.contract)
    imported_origins(root, inputs, sys.modules)
    directory.mkdir(parents=True)
    started, proofs = time.time_ns(), []
    for name, report in epoch.reports.items():
        descriptor = json.loads(epoch.read_current(report['canonicalPacketDescriptor']))
        require(epoch.read_current(report['canonicalPacketDescriptor']) == epoch.read_committed(report['canonicalPacketDescriptor']), 'Uncommitted descriptor')
        for row in report['matches']:
            if row['processor'] != 'arm9':
                continue
            epoch.ensure()
            require((row.get('program') or '') == '' and row['module'] in ('ov001', 'ov006'), 'Wrong new reference namespace')
            graph = source_graph(root, row)
            for path in [row['source'], *[h['path'] for h in row['sourceDependencies']]]:
                require(epoch.read_current(path) == epoch.read_committed(path), 'Uncommitted source or header')
            witnesses = [w for w in descriptor['nativeUnitIdentities'] if identity(w) == identity(row)]
            require(len(witnesses) == 1 and witness_name(root, row, witnesses[0]) == row['dsdSymbol'], 'Wrong native config alias')
            original = object_contract(local(root, row['object']), row)
            unit = directory / str(len(proofs))
            unit.mkdir()
            output = unit / 'source.o'
            command = [str(local(root, row['compiler'])), *row['compilerFlags'], '-c', str(local(root, row['source'])), '-o', str(output)]
            before = time.time_ns()
            run = subprocess.run(command, cwd=root, capture_output=True, timeout=30, env=dict(os.environ, LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat')))
            (unit / 'compile.log').write_bytes(run.stdout + run.stderr)
            require(run.returncode == 0 and output.is_file() and len(run.stdout) + len(run.stderr) <= 1048576, 'Fresh compiler failed or output budget exceeded')
            require(output.stat().st_mtime_ns >= before and object_contract(output, row) == original, 'Complete fresh object contract differs')
            adjusted = dict(row, object=output.relative_to(root).as_posix(), objectSha256=sha(output.read_bytes()))
            linked = linker.validate(adjusted, row['nativeSymbolEntries'], unit / 'link')
            module = epoch.contract['modules'][row['module']]
            offset = int(row['address'], 0) - int(module['base'], 0)
            body = images[module['binary']][offset:offset + row['bytes']]
            require(len(body) == row['bytes'] and sha(body) == row['targetSha256'] == linked['linkedCallerSha256'] and linked['exactCallerBytes'], 'Fresh genuine whole native extent differs')
            require(all(p['initializedCodeBytes'] == p['nativeCalleeBytesUsed'] == p['calleeSourceCredit'] == p['linkedInitializedOutputBytes'] == 0 for p in linked['bindingOnlyProbes']), 'Executable anchor credit')
            imported_origins(root, inputs, sys.modules)
            proofs.append(dict(identity=list(identity(row)), report=name, bytes=row['bytes'], compilerInputs=graph, startedTimeNs=before, exitCode=run.returncode, command=command, freshObject=adjusted['object'], freshObjectSha256=adjusted['objectSha256'], targetSha256=row['targetSha256'], linked=linked))
    require(len(proofs) == 6 and sum(r['bytes'] for r in proofs) == 1184, 'Incomplete six-host live union')
    artifacts = []
    for path in directory.rglob('*'):
        if path.is_file():
            name = path.relative_to(root).as_posix()
            inputs[name] = sha(path.read_bytes())
            artifacts.append(name)
    return LiveReferences(TOKEN, epoch, root, inputs, proofs, started, artifacts)
