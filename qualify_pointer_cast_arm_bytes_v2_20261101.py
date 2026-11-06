import concurrent.futures
import hashlib
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import ELFFile, validate
from recover_linked_runtime import qualified_bindings
import link_arm7_bulk_20261030 as arm7_linker

WORK = ROOT / 'work/windows-pointer-cast-arm-20261101'


def allocated_fingerprint(path):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        allocated = {}
        sections = []
        for index, section in enumerate(elf.iter_sections()):
            if section['sh_flags'] & 2:
                allocated[index] = section.name
                content = section.data() if section['sh_type'] != 'SHT_NOBITS' else bytes(section['sh_size'])
                sections.append(dict(name=section.name, kind=section['sh_type'], flags=section['sh_flags'],
                    size=section['sh_size'], alignment=section['sh_addralign'], sha256=hashlib.sha256(content).hexdigest()))
        symbols = []
        for symbol in elf.get_section_by_name('.symtab').iter_symbols():
            if symbol['st_shndx'] in allocated and symbol['st_info']['type'] in ['STT_FUNC', 'STT_OBJECT']:
                symbols.append(dict(name=symbol.name, section=allocated[symbol['st_shndx']], value=symbol['st_value'],
                    size=symbol['st_size'], kind=symbol['st_info']['type'], binding=symbol['st_info']['bind']))
        relocations = []
        for section in elf.iter_sections():
            if section['sh_type'] not in ['SHT_REL', 'SHT_RELA'] or section['sh_info'] not in allocated:
                continue
            table = elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                symbol = table.get_symbol(relocation['r_info_sym'])
                relocations.append(dict(section=allocated[section['sh_info']], offset=relocation['r_offset'],
                    type=relocation['r_info_type'], symbol=symbol.name, symbolValue=symbol['st_value'],
                    symbolSection=allocated.get(symbol['st_shndx'], symbol['st_shndx']),
                    format=section['sh_type'], addend=relocation['r_addend'] if section['sh_type'] == 'SHT_RELA' else None))
        return dict(flags=elf['e_flags'], machine=elf['e_machine'], sections=sections,
            symbols=sorted(symbols, key=lambda row: (row['name'], row['value'])), relocations=relocations)


def main():
    draft_path = ROOT / 'evidence/portability/windows-pointer-cast-drafts-20261101.json'
    draft = read_json(draft_path)
    candidates = [row for row in draft['candidates'] if row['state'] == 'windows-compiled-unqualified']
    selection_path = ROOT / 'evidence/verification/cohort112-before-adoption-20261101.json'
    selected = read_json(selection_path)['selected']
    prior_path = ROOT / 'evidence/portability/windows-pointer-cast-arm-proof-20261101.json'
    prior = {row['source']: row for row in read_json(prior_path)['candidates']}
    reports = {row['report']: read_json(ROOT / row['report']) for row in selected
        if any(candidate['source'] == row['source'] for candidate in candidates)}
    compiler_by_hash = {}
    for executable in (ROOT / 'tools/mwccarm/mwccarm').rglob('mwccarm.exe'):
        compiler_by_hash.setdefault(sha256(executable), executable)
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    WORK.mkdir(parents=True, exist_ok=True)

    def process(item):
        number, candidate = item
        source, changed = ROOT / candidate['source'], ROOT / candidate['candidate']
        assert sha256(source) == candidate['originalSourceSha256']
        assert sha256(changed) == candidate['candidateSha256']
        earlier = prior.get(candidate['source'])
        if earlier and earlier['state'] == 'genuine-arm-linked-unadopted':
            for unit in earlier['units']:
                assert sha256(ROOT / unit['seed']['object']) == unit['seed']['objectSha256']
            return dict(earlier, priorGenuineProofReused=True, priorObjectsIndependentlyRehashed=True)
        context = [row for row in selected if row['source'] == candidate['source']
            and row['sourceSha256'] == candidate['originalSourceSha256']]
        seeds = []
        for record in context:
            report = reports[record['report']]
            for row in report.get('matches', []) + report.get('functionMatches', []):
                if row.get('source', report.get('source')) == candidate['source'] and row.get('sourceSha256', report.get('sourceSha256')) == candidate['originalSourceSha256']:
                    signature = (row.get('module'), row.get('mode'), row.get('address'), row.get('name'))
                    if signature not in {entry[0] for entry in seeds}:
                        normalized = dict(row)
                        if 'compilerFlags' not in normalized and 'flags' in normalized:
                            normalized['compilerFlags'] = list(normalized['flags'])
                        seeds.append((signature, normalized, record['report']))
        result = dict(source=candidate['source'], sourceSha256=candidate['originalSourceSha256'],
            candidate=candidate['candidate'], candidateSha256=candidate['candidateSha256'], sourceCredit=0, units=[])
        if not seeds:
            return dict(result, state='missing-original-compiler-seed')
        profiles = {(row.get('compilerSha256'), tuple(row.get('compilerFlags', []))) for signature, row, report in seeds}
        if len(profiles) != 1 or not next(iter(profiles))[1]:
            return dict(result, state='missing-or-ambiguous-original-profile')
        compiler_hash, flags = next(iter(profiles))
        executable = compiler_by_hash.get(compiler_hash)
        if executable is None:
            return dict(result, state='pinned-original-compiler-unavailable')
        directory = WORK / f'{number:03}'
        directory.mkdir(parents=True, exist_ok=True)
        objects = []
        for label, current in [('original', source), ('candidate', changed)]:
            obj = directory / (label + '.o')
            command = [str(executable), *flags, '-c', str(current), '-o', str(obj)]
            run = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
                timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
            if run.returncode:
                return dict(result, state='original-profile-compile-refused', failedVariant=label,
                    command=command, exitCode=run.returncode, diagnostics=run.stderr.decode(errors='replace'))
            objects.append(obj)
        first, second = map(allocated_fingerprint, objects)
        result.update(compilerSha256=compiler_hash, compilerFlags=list(flags),
            originalObjectSha256=sha256(objects[0]), candidateObjectSha256=sha256(objects[1]),
            allocatedSectionsSymbolsAndRelocationsIdentical=first == second,
            originalAllocated=first, candidateAllocated=second)
        if first != second:
            return dict(result, state='allocated-code-data-or-relocations-differ')
        for signature, seed, report_name in seeds:
            with objects[1].open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name == seed['name'])
                seed.update(sectionIndex=symbol['st_shndx'], sectionOffset=symbol['st_value'] & ~1,
                    compiledBytes=symbol['st_size'])
            seed.update(source=changed.relative_to(ROOT).as_posix(), sourceSha256=sha256(changed),
                object=objects[1].relative_to(ROOT).as_posix(), objectSha256=sha256(objects[1]))
            try:
                measured_relocations = {}
                with objects[1].open('rb') as stream:
                    elf = ELFFile(stream)
                    symbol = next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name == seed['name'])
                    start = symbol['st_value'] & ~1
                    body = elf.get_section(symbol['st_shndx']).data()[start:start + symbol['st_size']]
                    for section in elf.iter_sections():
                        if section['sh_type'] not in ['SHT_REL', 'SHT_RELA'] or section['sh_info'] != symbol['st_shndx']:
                            continue
                        table = elf.get_section(section['sh_link'])
                        for relocation in section.iter_relocations():
                            offset = relocation['r_offset'] - start
                            if 0 <= offset < symbol['st_size']:
                                key = offset, relocation['r_info_type'], table.get_symbol(relocation['r_info_sym']).name
                                measured_relocations[key] = dict(format=section['sh_type'],
                                    explicitAddend=relocation['r_addend'] if section['sh_type'] == 'SHT_RELA' else None,
                                    originalEncodedWord=body[offset:offset + 4].hex())
                legacy = []
                for relocation in seed.get('relocations', []):
                    original_metadata = dict(relocation)
                    key = relocation['offset'], relocation['type'], relocation['symbol']
                    measured = measured_relocations[key]
                    if 'format' in relocation:
                        assert relocation['format'] == measured['format']
                    for name, value in measured.items():
                        relocation.setdefault(name, value)
                    if original_metadata != relocation:
                        legacy.append(dict(before=original_metadata, measuredSupplement=measured))
                if legacy:
                    result.setdefault('measuredLegacyRelocationMetadata', []).extend(legacy)
                if seed.get('processor') == 'arm7':
                    target = arm7_linker.WORK / 'native-pointer-casts-20261101' / str(number) / seed['name']
                    proof = arm7_linker.validate(seed, target)
                else:
                    seed.setdefault('processor', 'arm9')
                    proof = validate(seed, qualified_bindings(seed), directory / seed['name'])
                result['units'].append(dict(originalReport=report_name, seed=seed, genuineLink=proof, passed=True))
            except Exception as error:
                result['units'].append(dict(originalReport=report_name, seed=seed,
                    guardRefusal=repr(error), passed=False))
        assert sha256(source) == candidate['originalSourceSha256']
        return dict(result, state='genuine-arm-linked-unadopted' if all(unit['passed'] for unit in result['units']) else 'existing-link-guard-refused-unadopted')

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(process, item): item[1]['source'] for item in enumerate(candidates)}
        for future in concurrent.futures.as_completed(pending):
            try:
                results.append(future.result())
            except Exception as error:
                results.append(dict(source=pending[future], state='qualification-error', error=repr(error), sourceCredit=0))
    results.sort(key=lambda row: row['source'])
    counts = {}
    for row in results:
        counts[row['state']] = counts.get(row['state'], 0) + 1
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        drafts=dict(path=draft_path.relative_to(ROOT).as_posix(), sha256=sha256(draft_path)),
        selection=dict(path=selection_path.relative_to(ROOT).as_posix(), sha256=sha256(selection_path)),
        sourceCredit=0, selectedSourceModified=False, nativeBehaviorProven=False, counts=counts, candidates=results,
        limitations=['No source selection or acceptance claim; genuine ARM links and allocated-object equivalence are reported per source',
            'All existing compiler, processor/program/module and linker guards remain active',
            'Original profile gaps, changed code and guard refusals are not treated as matched or ignored',
            'Windows behavior tests and source-policy review remain required before adopting any candidate'])
    report['priorProof'] = dict(path=prior_path.relative_to(ROOT).as_posix(), sha256=sha256(prior_path))
    write_json(ROOT / 'evidence/portability/windows-pointer-cast-arm-proof-v2-20261101.json', report)
    print(dict(counts=counts, acceptedSourceChanges=0, sourceCredit=0))


if __name__ == '__main__':
    main()
