import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
import match_lowlevel
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
COMPILER_HASH = '89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca'
PROFILES = ((2, 'off', False, True), (2, 'off', True, True), (2, 'on', True, True),
    (2, 'on', True, False), (2, 'noauto', True, True), (3, 'off', True, True))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compile_source(row, origin, source, profile, directory):
    optimization, inline, speed, symbols = profile
    flags = match_lowlevel.FLAGS[:]
    flags[0] = '-O' + str(optimization)
    for key, value in (('-proc', 'arm7tdmi'), ('-inline', inline), ('-sym', 'on' if symbols else 'off')):
        flags[flags.index(key) + 1] = value
    if speed:
        flags += ['-opt', 'speed']
    if row['mode'] == 'thumb':
        flags += ['-thumb']
    key = digest(json.dumps(flags).encode())[:16]
    obj = directory / (key + '.o')
    command = [str(COMPILER), *flags, '-c', str(source), '-o', str(obj)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    record = {'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': digest(source.read_bytes()),
        'originSource': origin['source'], 'originSourceSha256': origin['sourceSha256'], 'module': row['module'], 'program': row.get('program', ''),
        'processor': 'arm7', 'address': row['address'], 'mode': row['mode'], 'name': row['name'], 'bytes': row['bytes'],
        'inputModuleSha256': row['inputModuleSha256'], 'binary': row['binary'], 'base': row['base'],
        'compiler': COMPILER.relative_to(ROOT).as_posix(), 'compilerSha256': COMPILER_HASH, 'compilerFlags': flags,
        'command': command, 'cwd': str(ROOT), 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    if result.returncode:
        return record
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name('.symtab')
        symbol = next((item for item in symbols.iter_symbols() if item.name == row['name']), None)
        if symbol is None or not isinstance(symbol['st_shndx'], int):
            record['missingNamedFunctionSymbol'] = True
            return record
        start, size = symbol['st_value'] & ~1, symbol['st_size']
        body = elf.get_section(symbol['st_shndx']).data()[start:start + size]
        relocations = []
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                continue
            table = elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                offset = relocation['r_offset'] - start
                if 0 <= offset < size:
                    relocations.append({'offset': offset, 'type': relocation['r_info_type'], 'symbol': table.get_symbol(relocation['r_info_sym']).name,
                        'format': section['sh_type'], 'explicitAddend': relocation['r_addend'] if section['sh_type'] == 'SHT_RELA' else None,
                        'originalEncodedWord': body[offset:offset + 4].hex()})
    object_hash = digest(obj.read_bytes())
    stable = directory / (object_hash + '.immutable.o')
    if not stable.exists():
        shutil.copyfile(obj, stable)
    binary = (ROOT / row['binary']).read_bytes()
    if digest(binary) != row['inputModuleSha256']:
        raise ValueError('ARM7 measured module changed')
    offset = int(row['address'], 0) - row['base']
    native = binary[offset:offset + row['bytes']]
    covered = {item['offset'] + index for item in relocations for index in range(4)}
    valid_relocations = all(item['type'] in (1, 2, 10, 15, 28, 29) and 0 <= item['offset'] <= size - 4 for item in relocations)
    exact_outside = len(body) == len(native) and valid_relocations and all(a == b for index, (a, b) in enumerate(zip(body, native)) if index not in covered)
    record.update(compiledBytes=size, matchingBytes=sum(a == b for a, b in zip(body, native)), rawBytesEqual=body == native,
        relocationOnlyCandidate=exact_outside, relocations=relocations, object=stable.relative_to(ROOT).as_posix(), objectSha256=object_hash,
        targetSha256=digest(native), unlinkedFunctionSha256=digest(body), sectionIndex=symbol['st_shndx'], sectionOffset=start,
        requiresActualLinkBeforeCredit=True, currentSourceCredit=0)
    return record


def research(item, batch):
    row, origins = item
    directory = WORK / batch / row['module'] / (row['address'][2:].zfill(8))
    directory.mkdir(parents=True, exist_ok=True)
    records = []
    for origin in origins:
        original = ROOT / origin['source']
        if digest(original.read_bytes()) != origin['sourceSha256']:
            raise ValueError('Historical ordinary-C hypothesis changed')
        text = original.read_text()
        if re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
            continue
        source = directory / (row['name'] + '-' + origin['sourceSha256'][:16] + '.c')
        if source.exists() and source.read_bytes() != original.read_bytes():
            raise ValueError('Refusing to overwrite a different candidate')
        source.write_bytes(original.read_bytes())
        for profile in PROFILES:
            try:
                record = compile_source(row, origin, source, profile, directory)
            except Exception as error:
                record = {'source': source.relative_to(ROOT).as_posix(), 'failure': type(error).__name__ + ': ' + str(error)}
            records.append(record)
            if record.get('relocationOnlyCandidate'):
                break
        if any(record.get('relocationOnlyCandidate') for record in records):
            break
    journal = {'identity': {name: row[name] for name in ('program', 'module', 'address', 'mode', 'name', 'bytes')}, 'attempts': records,
        'sourceCredit': 0, 'actualLinkAndBoundaryAndNativeEvidenceStillRequired': True}
    (directory / 'probe.json').write_text(json.dumps(journal, indent=2) + '\n')
    return journal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--limit', type=int, default=240)
    parser.add_argument('--sources-per-function', type=int, default=2)
    parser.add_argument('--same-size-first', action='store_true')
    options = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', options.batch):
        raise ValueError('Simple exclusive batch name required')
    if digest(COMPILER.read_bytes()) != COMPILER_HASH:
        raise ValueError('Pinned SP1p5 compiler differs')
    inventory = json.loads((WORK / 'inventory.json').read_text())
    rows = [row for row in inventory['remainingHeuristicCandidates'] if row['sourceDrafts']]
    rows.sort(key=lambda row: (row['sourceDrafts'][0]['score'][0] != 0 if options.same_size_first else False,
        row['sourceDrafts'][0]['score'][0], -row['bytes'], row['module'], row['address']))
    selected = [(row, row['sourceDrafts'][:options.sources_per_function]) for row in rows[:options.limit]]
    output = WORK / options.batch
    output.mkdir(parents=True, exist_ok=True)
    if (output / 'results.json').exists():
        raise ValueError('Choose a new bulk compiler batch')
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(lambda item: research(item, options.batch), selected):
            results.append(result)
            if any(row.get('relocationOnlyCandidate') for row in result['attempts']) or len(results) % 25 == 0:
                print(json.dumps({'processed': len(results), 'identity': result['identity'],
                    'relocationOnlyCandidate': any(row.get('relocationOnlyCandidate') for row in result['attempts'])}), flush=True)
    candidates = [row for result in results for row in result['attempts'] if row.get('relocationOnlyCandidate')]
    report = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'inventorySha256': digest((WORK / 'inventory.json').read_bytes()), 'compilerSha256': COMPILER_HASH, 'results': results,
        'relocationOnlyCandidates': candidates, 'actualLinkStillRequired': True, 'sourceCredit': 0, 'registered': False}
    (output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'functionsProbed': len(results), 'relocationOnlyCandidates': len(candidates), 'candidateBytes': sum(row['bytes'] for row in candidates), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
