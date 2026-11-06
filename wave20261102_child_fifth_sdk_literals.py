import ast
import json
import re
from pathlib import Path
import utility_code
from wave20261102_child_fifth_index import candidates
from elftools.elf.elffile import ELFFile
from wave20261102_child_fifth_prepare import ROOT, WORK, LANE, SOURCE
from wave20261102_child_fifth_adapt import validate_candidate
from project import sha256, write_json


def recover(unit, attempt, spec):
    obj = ROOT / unit['object']
    if sha256(obj) != unit['objectSha256']:
        raise ValueError('SDK research object changed')
    name = attempt['referenceFunction']
    unit_name = Path(unit['referenceSource']).relative_to('deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840').as_posix().removesuffix('.c').replace('/', '-')
    profile_label = unit.get('profileLabel', unit['profile'].replace('/', '_'))
    original_source = ROOT / attempt['source'] if attempt.get('source') else SOURCE / 'reference-research' / (unit_name + '-' + profile_label) / (name + '.c')
    text = original_source.read_text()
    raw = (ROOT / spec['binary']).read_bytes()
    native = raw[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    rels, constants = [], []
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        function = next(s for s in table.iter_symbols() if s.name == name)
        start, size = function['st_value'] & ~1, function['st_size']
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != function['st_shndx']:
                continue
            if section['sh_type'] != 'SHT_RELA':
                raise ValueError('Unsupported SDK relocation form')
            symbols = elf.get_section(section['sh_link'])
            for rel in section.iter_relocations():
                offset = rel['r_offset'] - start
                if not 0 <= offset < size:
                    continue
                symbol = symbols.get_symbol(rel['r_info_sym'])
                label = symbol.name
                if label.startswith('@'):
                    if rel['r_info_type'] != 2 or rel['r_addend'] != 0 or not isinstance(symbol['st_shndx'], int):
                        raise ValueError('Anonymous target is not one complete zero-addend original constant')
                    contents = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
                    if not contents or contents[-1:] != b'\0' or b'\0' in contents[:-1]:
                        raise ValueError('Anonymous target is not a bounded original string')
                    matching = [m[0] for m in re.finditer(r'"(?:\\.|[^"\\])*"', text)
                        if ast.literal_eval(m[0]).encode('ascii') + b'\0' == contents]
                    if len(set(matching)) != 1:
                        raise ValueError('String literal source identity is ambiguous')
                    address = int.from_bytes(native[offset:offset + 4], 'little')
                    relative = address - spec['base']
                    if relative < 0 or relative + len(contents) > len(raw) or raw[relative:relative + len(contents)] != contents:
                        raise ValueError('Original caller pointer does not resolve the exact SDK constant within the same measured module')
                    label = 'child_reference_string_%08x' % address
                    text = text.replace(matching[0], label)
                    declaration = 'extern const char %s[%d];\n' % (label, len(contents))
                    if declaration not in text:
                        text = declaration + text
                    constants.append(dict(referenceObjectSymbol=symbol.name, referenceObjectSha256=sha256(obj),
                        originalPointerOffset=offset, originalPointerWord=hex(address), address=hex(address),
                        processor=spec['processor'], program=spec['program'], module=spec['module'],
                        inputModuleSha256=spec['inputModuleSha256'], bytes=len(contents), measuredHex=contents.hex(),
                        originalCSpelling=matching[0], dataStorageCredit=0, sourceFunctionCredit=0))
                rels.append(dict(offset=offset, type=rel['r_info_type'], symbol=label, addend=rel['r_addend']))
    label = unit.get('profileLabel', unit['profile'].replace('/', '_'))
    destination = SOURCE / 'reference-literal-research' / label / ('%08x.c' % spec['address'])
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_text() != text:
        raise ValueError('Refusing constant qualification source overwrite')
    destination.write_text(text)
    flags = unit['compilerFlags'][:unit['compilerFlags'].index('-lang')]
    origin = dict(name=name, source=destination.relative_to(ROOT).as_posix(), sourceSha256=sha256(destination),
        bytes=size, relocations=rels, compiler=unit['compiler'], compilerSha256=unit['compilerSha256'], compilerFlags=flags)
    entry, code = validate_candidate(origin, spec, native, 'sdk-literals-' + name + '-' + label)
    entry.update(referenceFunction=name, qualifiedOriginalConstants=constants,
        sourceAdaptationMethod='pinned comparative SDK ordinary C with qualified original external string storage; zero data-storage credit')
    if code is not None:
        write_json(LANE / 'candidates' / ('%08x-sdk-literals-%s-%s.json' % (spec['address'], name, label)),
            dict(match=entry, address=hex(spec['address']), bytes=spec['bytes'], acceptedSourceCredit=0))
    return dict(address=hex(spec['address']), referenceFunction=name, exact=code is not None,
        qualifiedOriginalConstants=constants, compilerResult=entry)


def main():
    specs = {hex(s['address']): s for s in candidates() if s['module'] == 'utility-child-arm7-wram'}
    utility_code.WORK = WORK / 'sdk-literal-compiled'
    results = []
    for path in sorted((WORK / 'sdk-probes-arm7-v2').rglob('result.json')):
        unit = json.loads(path.read_text())
        for attempt in unit.get('closedAttempts', []):
            if attempt.get('exact') or 'Unknown native symbol identity: @' not in attempt.get('refusal', ''):
                continue
            try:
                result = recover(unit, attempt, specs[attempt['address']])
            except Exception as error:
                result = dict(address=attempt['address'], referenceFunction=attempt['referenceFunction'], exact=False, refusal=repr(error))
            results.append(result)
    exact = {r['address']: r for r in results if r.get('exact')}
    write_json(LANE / 'sdk-qualified-constants.json', dict(results=results, exactFunctions=len(exact),
        exactBytes=sum(r['compilerResult']['bytes'] for r in exact.values()),
        stringStorageCredit=0, sourceCredit=0, sdkNamesAndVersionRemainComparative=True))
    print(dict(attempts=len(results), exactFunctions=len(exact), exactBytes=sum(r['compilerResult']['bytes'] for r in exact.values())))


if __name__ == '__main__':
    main()
