import hashlib
import re
from pathlib import Path
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json


SPECIFICATION = ROOT / 'provenance/generated-linker-layout.json'


def recipe_valid(text, prefix, alignment):
    names = [prefix + '_' + name for name in ('RODATA_END', 'CTOR_START', 'CTOR_END', 'DATA_START')]
    pattern = (re.escape(names[0]) + r'\s*=\s*\.;\s*\.\s*=\s*ALIGN\(4\);\s*' +
               re.escape(names[1]) + r'\s*=\s*\.;\s*WRITEW\(0\);\s*\.\s*=\s*ALIGN\(4\);\s*' +
               re.escape(names[2]) + r'\s*=\s*\.;\s*\.\s*=\s*ALIGN\(' + str(alignment) + r'\);\s*' +
               re.escape(names[3]) + r'\s*=\s*\.;')
    return len(re.findall(pattern, text)) == 1


def specifications():
    if not SPECIFICATION.exists():
        return []
    specification = read_json(SPECIFICATION)
    if specification['romSha256'] != configuration()['romSha256']:
        raise ValueError('Linker-layout specification belongs to another build')
    return specification['regions']


def annotate(report, work):
    candidates = {row['module']: row for row in report.get('modules', []) if row.get('exactBytes')}
    selected = [spec for spec in specifications() if spec['module'] in candidates]
    if not selected:
        return
    native_dependencies(configuration())
    from elftools.elf.elffile import ELFFile
    lcf, elf_path = work / 'arm9.lcf', work / 'linked.elf'
    with elf_path.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = {symbol.name: symbol['st_value'] for symbol in elf.get_section_by_name('.symtab').iter_symbols()}
    rows = []
    for spec in selected:
        module = candidates[spec['module']]
        for path, expected in spec['dependencies'].items():
            if sha256(ROOT / path) != expected:
                raise ValueError('Pinned layout evidence dependency changed: ' + path)
        start, end, base = (int(spec[key], 0) for key in ('start', 'end', 'base'))
        prefix = spec['module'].upper()
        expected_labels = {prefix + '_RODATA_END': start, prefix + '_CTOR_START': start,
                           prefix + '_CTOR_END': start + 4, prefix + '_DATA_START': end}
        if any(symbols.get(name) != value for name, value in expected_labels.items()):
            raise ValueError('Generated linker-layout symbol boundaries changed')
        if not recipe_valid(lcf.read_text(), prefix, spec['alignment']):
            raise ValueError('Metadata interval is not the verified input-free linker recipe')
        if module['inputSha256'] != spec['moduleInputSha256'] or sha256(module['target']) != spec['moduleInputSha256']:
            raise ValueError('Metadata native module identity changed')
        if sha256(module['output']) != module['outputSha256']:
            raise ValueError('Current linked module identity changed')
        if any(unit['module'] == spec['module'] and int(unit['start'], 0) < end and start < int(unit['end'], 0)
               for unit in report.get('sourceUnits', [])):
            raise ValueError('Generated metadata overlaps an authored source unit')
        original = Path(module['target']).read_bytes()[start - base:end - base]
        linked = Path(module['output']).read_bytes()[start - base:end - base]
        if original != linked or hashlib.sha256(linked).hexdigest() != spec['rangeSha256']:
            raise ValueError('Production linker metadata differs from the measured interval')
        rows.append({'module': spec['module'], 'address': spec['start'], 'bytes': end - start,
                     'sha256': spec['rangeSha256'], 'kind': 'linker-control-metadata',
                     'moduleInputSha256': spec['moduleInputSha256'], 'symbolValues': expected_labels,
                     'output': module['output'], 'outputSha256': module['outputSha256'],
                     'lcf': str(lcf), 'lcfSha256': sha256(lcf), 'elf': str(elf_path), 'elfSha256': sha256(elf_path),
                     'dependencies': spec['dependencies'], 'linkerRegenerated': True,
                     'inputObjectReferencesInRecipe': 0, 'ordinaryFunctionCredit': 0, 'sourceMatchedByteCredit': 0})
    report['generatedLinkerLayoutRegions'] = rows
    report['linkerLayoutVerifierSha256'] = sha256(Path(__file__))
    report['linkerLayoutSpecificationSha256'] = sha256(SPECIFICATION)


def current(row, report):
    try:
        if report.get('linkerLayoutVerifierSha256') != sha256(Path(__file__)):
            return False
        if report.get('linkerLayoutSpecificationSha256') != sha256(SPECIFICATION):
            return False
        spec = next(item for item in specifications() if item['module'] == row['module'] and item['start'] == row['address'])
        if row['bytes'] != int(spec['end'], 0) - int(spec['start'], 0) or row['sha256'] != spec['rangeSha256']:
            return False
        if row['moduleInputSha256'] != spec['moduleInputSha256'] or row['inputObjectReferencesInRecipe'] != 0:
            return False
        if row.get('ordinaryFunctionCredit') != 0 or row.get('sourceMatchedByteCredit') != 0 or not row.get('linkerRegenerated'):
            return False
        if row['dependencies'] != spec['dependencies']:
            return False
        identities = [(row[key], row[key + 'Sha256']) for key in ('output', 'lcf', 'elf')]
        identities.extend(row['dependencies'].items())
        return all((ROOT / path).is_file() and sha256(ROOT / path) == expected for path, expected in identities)
    except (KeyError, OSError, StopIteration):
        return False


def record(modules, report, linked_modules, linkage, write=True):
    for row in report.get('generatedLinkerLayoutRegions', []):
        if row['module'] not in linked_modules or not current(row, report):
            continue
        module = next(item for item in modules if item['name'] == row['module'])
        if module['unresolvedModuleBytes'] < row['bytes']:
            raise ValueError('Linker metadata would overlap existing coverage')
        module['linkerRegeneratedBytes'] += row['bytes']
        module['linkerLinkedBytes'] += row['bytes']
        module['unresolvedModuleBytes'] -= row['bytes']
        module['sourceReconstructionComplete'] = (module['sourceLinkedBytes'] + module['linkerLinkedBytes'] == module['bytes']
            and module['sourceLinkedBssBytes'] == module['expectedBssBytes']
            and module.get('functionInventoryStatus') != 'pending-qualified-analysis')
        module['originalObjectScaffolding'] = not module['sourceReconstructionComplete']
        linkage['regions'].append({**row, 'fullProgramLinkedWithReplacement': True,
                                   'generatedByCurrentLinkerControl': True, 'sourceFunctionCredit': 0})
        linkage['linkerRegeneratedBytes'] += row['bytes']
        linkage['linkerLinkedBytes'] += row['bytes']
    if write:
        write_json(ROOT / 'ledger/linkage.json', linkage)
