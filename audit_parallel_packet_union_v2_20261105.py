import argparse
import hashlib
import re
from pathlib import Path
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from parallel_status import interval, collisions, number
from prepare_parallel_packet_wave import mandatory_inputs, reserved_storage
from audit_original_assembly_ranges_20261105 import qualify as qualify_whole_original_assembly


def local(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError('Audit input is absent or outside the workspace')
    return path


def linked_body(path, name, size, address, lcf):
    from elftools.elf.elffile import ELFFile
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = [symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols()
                   if symbol.name == name and isinstance(symbol['st_shndx'], int)]
        if len(symbols) != 1:
            raise ValueError('Linked caller symbol is not unique')
        symbol = symbols[0]
        section = elf.get_section(symbol['st_shndx'])
        if symbol['st_info']['type'] != 'STT_FUNC' or symbol['st_size'] != size or symbol['st_value'] & ~1 != address:
            raise ValueError('Linked caller complete function extent differs')
        offset = (symbol['st_value'] & ~1) - section['sh_addr']
        body = section.data()[offset:offset + size]
        if len(body) == size:
            return body
        exported = re.search(r'CALL\s*:\s*ORIGIN\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*>\s*([A-Za-z0-9_.-]+)', lcf.read_text())
        segments = [segment for segment in elf.iter_segments() if segment['p_type'] == 'PT_LOAD'
                    and segment['p_vaddr'] == address and segment['p_memsz'] == size and segment['p_filesz'] == 0]
        if len(body) or not exported or number(exported[1]) != address or len(segments) != 1:
            raise ValueError('Linked ELF does not identify one complete exported caller binary')
        return local(path.parent / exported[2]).read_bytes()


def audit(specification):
    config = configuration()
    native_dependencies(config)
    rom = config['romSha256']
    spec = read_json(local(specification))
    reserved = reserved_storage(ROOT, rom)
    for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines():
        row = __import__('json').loads(line)
        if row['states']['functionMatched']:
            reserved.append(('selected', interval(row)))
    modules = {}
    for row in read_json(ROOT / 'ledger/modules.json')['modules']:
        key = (row.get('program') or '', row['processor'], row['name'])
        path = local(row['binary'])
        if sha256(path) != row['sha256']:
            raise ValueError('Original module identity changed')
        modules[key] = (number(row['base']), path.read_bytes())
    expected = [interval(row) for row in spec['expectedAdditions']]
    owned, inputs, results, mixed, whole_assembly = [], {}, [], [], []
    for pin in spec['readyPacketInputs']:
        if sha256(local(pin['path'])) != pin['sha256']:
            raise ValueError('Intake READY metadata changed')
    for packet in spec['packets']:
        descriptor = read_json(local(packet['producer'][1]))
        if descriptor['romSha256'] != rom:
            raise ValueError('Replay descriptor ROM differs')
        for pin in mandatory_inputs(descriptor['frozenInputs']):
            if pin['path'] in inputs and inputs[pin['path']] != pin['sha256']:
                raise ValueError('Conflicting mandatory runtime input')
            inputs[pin['path']] = pin['sha256']
        report = read_json(local(packet['report']))
        contracts = {interval(row): row for row in descriptor['identities']}
        actual = [interval(row) for row in report['matches']]
        if len(actual) != len(contracts) or len(set(actual)) != len(actual) or set(actual) != set(contracts):
            raise ValueError('Canonical report membership differs from frozen descriptor')
        for row in report['matches']:
            span = interval(row)
            contract = contracts[span]
            for field in ['source', 'sourceSha256', 'targetSha256']:
                if row[field] != contract[field]:
                    raise ValueError('Canonical source/native contract changed')
            owned.append((packet['report'], span))
            for field, digest in [('source', 'sourceSha256'), ('object', 'objectSha256')]:
                if sha256(local(row[field])) != row[digest]:
                    raise ValueError('Source or current compiler object changed')
            for pin in row.get('sourceDependencies', []):
                if sha256(local(pin['path'])) != pin['sha256']:
                    raise ValueError('Compiler context changed')
            base, image = modules[span[0]]
            offset, size = span[1] - base, span[2] - span[1]
            if offset < 0 or offset + size > len(image):
                raise ValueError('Caller crosses original initialized module')
            native = image[offset:offset + size]
            if hashlib.sha256(native).hexdigest() != row['targetSha256']:
                raise ValueError('Complete original native span differs')
            link = row['realLink']
            for field, digest in [('linkedElf', 'linkedElfSha256'), ('lcf', 'lcfSha256')]:
                if sha256(local(link[field])) != link[digest]:
                    raise ValueError('Current genuine linker artifact changed')
            body = linked_body(local(link['linkedElf']), link['name'], size, span[1], local(link['lcf']))
            if body != native or hashlib.sha256(body).hexdigest() != link['linkedCallerSha256'] or not link['exactCallerBytes'] or not row['exactAfterDeclaredRelocation']:
                raise ValueError('Actual linked ELF caller differs: ' + str(dict(module=row['module'],
                    address=row['address'], bytes=size, linkedBytes=len(body),
                    linkedSha256=hashlib.sha256(body).hexdigest(), nativeSha256=row['targetSha256'],
                    differingBytes=sum(a != b for a, b in zip(body, native)),
                    firstDifference=next((i for i, (a, b) in enumerate(zip(body, native)) if a != b), None))))
            ranges = row.get('justifiedAssemblyRanges', [])
            if row.get('sourceLanguage') == 'c-with-original-inline-assembly':
                assembly = 0
                seen = set()
                for region in ranges:
                    address, length = number(region.get('address', region.get('start'))), number(region.get('bytes', region.get('size')))
                    if length != 4 or address % 4 or not span[1] <= address < span[2] or address in seen:
                        raise ValueError('Original inline primitive range is not an isolated in-span ARM word')
                    seen.add(address)
                    word = int.from_bytes(native[address - span[1]:address - span[1] + 4], 'little')
                    if word & 0x0FFF0FF0 != 0x016F0F10:
                        raise ValueError('Declared original CLZ range is another instruction')
                    assembly += length
                if not row.get('assemblyJustification') or assembly != row['justifiedAssemblyBytes'] or assembly + row['ordinaryCBytes'] != size:
                    raise ValueError('Mixed C/original primitive accounting differs')
                mixed.append(dict(address=row['address'], ordinaryCBytes=row['ordinaryCBytes'], justifiedAssemblyBytes=assembly))
            elif row.get('sourceLanguage') == 'assembly':
                whole_assembly.append(qualify_whole_original_assembly(row, span))
            elif ranges:
                raise ValueError('Assembly ranges lack an explicit mixed-source classification')
            results.append(dict(program=span[0][0], processor=span[0][1], module=span[0][2],
                mode=span[3], address=row['address'], bytes=size, source=row['source'],
                nativeSha256=row['targetSha256'], actualLinkedElfVerified=True))
    if sorted(value for owner, value in owned) != sorted(expected) or collisions(owned, reserved):
        raise ValueError('Prepared union overlaps existing physical bytes or expected membership differs')
    return dict(passed=True, sourceCredit=0, cohort=spec['cohort'], functions=len(results),
        bytes=sum(row['bytes'] for row in results), mandatoryInputs=len(inputs),
        physicalOverlaps=[], mixedSource=mixed, wholeOriginalAssembly=whole_assembly, matches=results,
        actualNativeSpansLinkedSymbolsAndBinaryBytesCompared=True,
        specSha256=sha256(local(specification)),
        limitations=['Read-only packet admission audit; shared module/ROM/regression gates and committed closure remain required'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    result = audit(options.specification)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(__file__))
    write_json(ROOT / options.output, result)
    print({key: result[key] for key in ['passed', 'cohort', 'functions', 'bytes', 'mandatoryInputs']})
