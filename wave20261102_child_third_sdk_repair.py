import json
import re
from pathlib import Path
import utility_code
from elftools.elf.elffile import ELFFile
from slice_reference_sdk_entities_v3_20261102 import functions
from wave20261102_child_third_prepare import ROOT, WORK, LANE, SOURCE
from wave20261102_child_third_adapt import validate_candidate
from project import sha256, write_json


def recover(unit, attempt, spec):
    name = attempt['referenceFunction']
    if name not in ['FS_FindArchive', 'FS_RegisterArchiveName', 'CARD_Init']:
        raise ValueError('Unreviewed reference closure defect')
    source = ROOT / attempt['source']
    text = source.read_text()
    raw = ROOT / unit['referenceSource']
    if sha256(raw) != unit['referenceSourceSha256']:
        raise ValueError('Comparative SDK source changed')
    if name.startswith('FS_'):
        if not re.search(r'static\s+FSArchive\s*\*arc_list\s*=\s*NULL\s*;', raw.read_text()):
            raise ValueError('Reference global pointer type does not match measured external-storage hypothesis')
        declaration = 'extern FSArchive *arc_list;\n'
    else:
        expanded = (ROOT / unit['object']).parent / 'expanded.i'
        prototype = 'void (*CARDi_GetRomAccessor(void))(CARDRomStat *);'
        if re.sub(r'\s+', '', prototype) not in re.sub(r'\s+', '', expanded.read_text()):
            raise ValueError('Function-pointer-return prototype lacks exact preprocessor evidence')
        declaration = 'extern ' + prototype + '\n'
        text = re.sub(r'(?m)^CARDRomStat rom_stat __attribute__\s*\(\(aligned\(32\)\)\)\s*;\s*$', '', text)
        text = re.sub(r'(?m)^u32 cardi_rom_base;\s*$', '', text)
    at = next(f['start'] for f in functions(text) if f['name'] == name)
    text = text[:at] + declaration + text[at:]
    label = unit.get('profileLabel', unit['profile'].replace('/', '_'))
    directory = SOURCE / 'reference-research-repair' / label / ('%08x' % spec['address'])
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / (name + '.c')
    if destination.exists() and destination.read_text() != text:
        raise ValueError('Refusing reviewed context overwrite')
    destination.write_text(text)
    obj = ROOT / unit['object']
    if sha256(obj) != unit['objectSha256']:
        raise ValueError('Comparative SDK object changed')
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        symbol = next(s for s in table.iter_symbols() if s.name == name)
        start, size, rels = symbol['st_value'] & ~1, symbol['st_size'], []
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                continue
            if section['sh_type'] != 'SHT_RELA':
                raise ValueError('Unexpected reference relocation format')
            symbols = elf.get_section(section['sh_link'])
            for rel in section.iter_relocations():
                offset = rel['r_offset'] - start
                if 0 <= offset < size:
                    rels.append(dict(offset=offset, type=rel['r_info_type'], symbol=symbols.get_symbol(rel['r_info_sym']).name, addend=rel['r_addend']))
    flags = unit['compilerFlags'][:unit['compilerFlags'].index('-lang')]
    origin = dict(name=name, source=destination.relative_to(ROOT).as_posix(), sourceSha256=sha256(destination),
        bytes=size, relocations=rels, compiler=unit['compiler'], compilerSha256=unit['compilerSha256'], compilerFlags=flags)
    native = (ROOT / spec['binary']).read_bytes()[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    tag = 'sdk-repaired-' + name + '-' + label
    row, code = validate_candidate(origin, spec, native, tag)
    row.update(referenceFunction=name, sourceAdaptationMethod='pinned comparative SDK C with measured external storage and original pointer-return declaration restored',
        researchEvidence=[dict(path=raw.relative_to(ROOT).as_posix(), sha256=sha256(raw))],
        recoveredGlobalStorageCredit=0)
    if code is not None:
        write_json(LANE / 'candidates' / ('%08x-%s.json' % (spec['address'], tag)),
            dict(match=row, address=hex(spec['address']), bytes=spec['bytes'], acceptedSourceCredit=0))
    return dict(address=hex(spec['address']), referenceFunction=name, profile=label, exact=code is not None,
        restoredDeclaration=declaration.strip(), compilerResult=row, externalStorageCredit=0)


def main():
    specs = {hex(s['address']): s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'}
    utility_code.WORK = WORK / 'sdk-repaired-compiled'
    results = []
    for path in sorted((WORK / 'sdk-probes').rglob('result.json')):
        unit = json.loads(path.read_text())
        for attempt in unit.get('closedAttempts', []):
            if attempt.get('exact') or attempt['referenceFunction'] not in ['FS_FindArchive', 'FS_RegisterArchiveName', 'CARD_Init']:
                continue
            try:
                result = recover(unit, attempt, specs[attempt['address']])
            except Exception as error:
                result = dict(address=attempt['address'], referenceFunction=attempt['referenceFunction'], exact=False, refusal=repr(error))
            results.append(result)
    exact = {e['address']: e for e in results if e.get('exact')}
    write_json(LANE / 'sdk-context-repair.json', dict(results=results, exactFunctions=len(exact),
        exactBytes=sum(e['compilerResult']['bytes'] for e in exact.values()), sourceCredit=0,
        externalStorageCredit=0, comparativeTypesAndNamesNotIndependentSemantics=True))
    print(dict(attempts=len(results), exactFunctions=len(exact), exactBytes=sum(e['compilerResult']['bytes'] for e in exact.values())))


if __name__ == '__main__':
    main()
