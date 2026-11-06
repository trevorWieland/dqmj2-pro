import json
from pathlib import Path
import utility_code
from elftools.elf.elffile import ELFFile
from wave20261102_child_fifth_prepare import ROOT, WORK, LANE, SOURCE
from wave20261102_child_fifth_index import candidates
from wave20261102_child_fifth_adapt import validate_candidate
from project import read_json, write_json, sha256


def main():
    specs = {hex(r['address']): r for r in candidates() if r['module'] == 'utility-child-arm7-wram'}
    utility_code.WORK = WORK / 'retry-compiled'
    results = []
    for path in sorted((WORK / 'sdk-probes-arm7-v5').rglob('result.json')):
        unit = read_json(path)
        for previous in unit.get('closedAttempts', []):
            if previous.get('exact') or 'Unknown native symbol identity: _s32_div_f' not in previous.get('refusal', ''):
                continue
            result = dict(address=previous['address'], referenceFunction=previous['referenceFunction'], exact=False)
            try:
                spec = specs[previous['address']]
                name, label = previous['referenceFunction'], unit['profileLabel']
                flat = SOURCE / 'reference-research-v5' / (path.parent.parent.name + '-' + label) / name / (name + '.c')
                obj = ROOT / unit['object']
                if sha256(obj) != unit['objectSha256']:
                    raise ValueError('Original comparative SDK object changed')
                rels = []
                with obj.open('rb') as stream:
                    elf = ELFFile(stream)
                    symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == name)
                    start, size = symbol['st_value'] & ~1, symbol['st_size']
                    for section in elf.iter_sections():
                        if section['sh_type'] != 'SHT_RELA' or section['sh_info'] != symbol['st_shndx']:
                            continue
                        symbols = elf.get_section(section['sh_link'])
                        for rel in section.iter_relocations():
                            offset = rel['r_offset'] - start
                            if 0 <= offset < size:
                                rels.append(dict(offset=offset, type=rel['r_info_type'], symbol=symbols.get_symbol(rel['r_info_sym']).name, addend=rel['r_addend']))
                origin = dict(name=name, source=flat.relative_to(ROOT).as_posix(), sourceSha256=sha256(flat),
                    bytes=size, relocations=rels, compiler=unit['compiler'], compilerSha256=unit['compilerSha256'],
                    compilerFlags=unit['compilerFlags'][:unit['compilerFlags'].index('-lang')])
                raw = (ROOT / spec['binary']).read_bytes()
                native = raw[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
                row, code = validate_candidate(origin, spec, native, 'qualified-helper-retry-' + label)
                row.update(referenceFunction=name, sourceAdaptationMethod='Comparative SDK ordinary C with qualified compiler-generated import; no callee behavior or implementation credit')
                if code is not None:
                    write_json(LANE / 'candidates' / ('%08x-compiler-helper-retry-%s.json' % (spec['address'], label)),
                        dict(address=hex(spec['address']), bytes=spec['bytes'], match=row, sourceCredit=0))
                result.update(exact=code is not None, compilerResult=row)
            except Exception as error:
                result['refusal'] = repr(error)
            results.append(result)
    write_json(LANE / 'compiler-import-retries.json', dict(results=results, sourceCredit=0, functionCredit=0))
    print(dict(attempts=len(results), exact=sum(r['exact'] for r in results)))


if __name__ == '__main__':
    main()
