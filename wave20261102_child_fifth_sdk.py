import argparse
import concurrent.futures
import json
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path
import utility_code
import match_lowlevel
import reuse_utility_c as reuse
import crossreuse_utility_c as cross
from elftools.elf.elffile import ELFFile
from wave20261102_child_fifth_slice import functions, slice_closed
from wave20261102_child_fifth_prepare import ROOT, LANE, WORK, SOURCE
from wave20261102_child_fifth_adapt import validate_candidate
from wave20261102_child_fifth_index import candidates
from wave20261102_child_fifth_types import write_closed
from project import sha256, write_json

REF = ROOT / 'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840'
SPECS = []


def build(item):
    source, profile, optimization, inline, label, speed = item
    unit = source.relative_to(REF).as_posix().removesuffix('.c').replace('/', '-')
    directory = WORK / 'sdk-probes-arm7-v5' / unit / label
    directory.mkdir(parents=True, exist_ok=True)
    result_path = directory / 'result.json'
    if result_path.exists():
        return json.loads(result_path.read_text())
    compiler = ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')
    if sha256(compiler) != utility_code.compiler_pins()[compiler.relative_to(ROOT).as_posix()]:
        raise ValueError('SDK compiler pin differs')
    flags = match_lowlevel.FLAGS[:]
    flags[0] = '-O' + str(optimization)
    flags[flags.index('-inline') + 1] = inline
    flags[flags.index('-proc') + 1] = 'arm7tdmi'
    if speed:
        flags.extend(['-opt', 'speed'])
    expanded_flags = [*flags, '-lang', 'c99', '-DSDK_CW_FORCE_EXPORT_SUPPORT', '-DSDK_TS', '-DSDK_4M',
        '-DSDK_ARM7', '-DSDK_CW', '-DSDK_FINALROM', '-DSDK_CODE_ARM', '-DNNS_FINALROM', '-DSDK_WIRELESS_IN_VRAM', '-DSDK_NOINIT']
    for include in [REF / 'include', REF / 'include/nitro_wl/ARM7', ROOT / 'generated/sdk-reference/20261101/parse-only-headers',
        ROOT / 'generated/sdk-reference/20261101/include', *sorted((REF / 'libraries').glob('*/include')),
        *sorted((REF / 'libraries').glob('*/include/ARM7'))]:
        expanded_flags.extend(['-i', include.as_posix()])
    obj = directory / 'compiled.o'
    command = [str(compiler), *expanded_flags, '-c', str(source), '-o', str(obj)]
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60, env=env)
    row = dict(referenceSource=source.relative_to(ROOT).as_posix(), referenceSourceSha256=sha256(source),
        profile=profile, profileLabel=label, command=command, compilerFlags=expanded_flags, compiler=compiler.relative_to(ROOT).as_posix(),
        compilerSha256=sha256(compiler), exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr,
        sourceCredit=0, provisionalHeadersNotAdopted=True, matches=[], maskedMatches=[])
    if process.returncode:
        write_json(result_path, row)
        return row
    row.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj))
    candidates = []
    by_size = defaultdict(list)
    for spec in SPECS:
        by_size[spec['bytes']].append(spec)
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        for symbol in table.iter_symbols():
            if symbol['st_info']['type'] != 'STT_FUNC' or not isinstance(symbol['st_shndx'], int):
                continue
            start, size = symbol['st_value'] & ~1, symbol['st_size']
            if size not in by_size or size < 32:
                continue
            payload = elf.get_section(symbol['st_shndx']).data()[start:start + size]
            rels, valid = [], True
            for section in elf.iter_sections():
                if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                    continue
                symbols = elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    at, kind = rel['r_offset'] - start, rel['r_info_type']
                    if not 0 <= at < size:
                        continue
                    if kind not in cross.MASKS or at + 4 > size or section['sh_type'] != 'SHT_RELA':
                        valid = False
                        continue
                    target = symbols.get_symbol(rel['r_info_sym'])
                    rels.append(dict(offset=at, type=kind, symbol=target.name, addend=rel['r_addend']))
            if not valid:
                continue
            offsets = tuple(sorted((r['offset'], cross.MASKS[r['type']]) for r in rels))
            fingerprint = reuse.normalized(payload, offsets)
            for spec in by_size[size]:
                native = (ROOT / spec['binary']).read_bytes()[spec['address'] - spec['base']:spec['address'] - spec['base'] + size]
                if reuse.normalized(native, offsets) == fingerprint:
                    candidates.append((symbol.name, spec, native, rels, fingerprint))
                    row['maskedMatches'].append(dict(referenceFunction=symbol.name, address=hex(spec['address']), bytes=size))
    if candidates:
        expanded = directory / 'expanded.i'
        command = [str(compiler), *expanded_flags, '-E', str(source), '-o', str(expanded)]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60, env=env)
        if process.returncode:
            row['preprocessorFailure'] = process.stdout + process.stderr
        else:
            original_text = expanded.read_text()
            for name, spec, native, rels, fingerprint in candidates:
                result = dict(referenceFunction=name, address=hex(spec['address']), bytes=spec['bytes'])
                try:
                    text = original_text
                    for function in sorted(functions(text), key=lambda f: f['start'], reverse=True):
                        header = text[function['start']:function['opening']]
                        if function['name'] == name or re.search(r'\binline\b', header):
                            continue
                        text = text[:function['start']] + re.sub(r'\bstatic\s+', '', header).rstrip() + ';\n' + text[function['end']:]
                    text, selected = slice_closed(text, [name])
                    if re.search(r'\b(?:asm|__asm|__asm__|va_list|size_t|J2pUnknownVaList)\b', text):
                        raise ValueError('Closed ordinary source contains provisional tokens or exceeds500lines')
                    flat = SOURCE / 'reference-research-v5' / (unit + '-' + label) / name / (name + '.c')
                    flat.parent.mkdir(parents=True, exist_ok=True)
                    write_closed(text, name, flat)
                    origin = dict(name=name, source=flat.relative_to(ROOT).as_posix(), sourceSha256=sha256(flat),
                        compiler=compiler.relative_to(ROOT).as_posix(), compilerSha256=sha256(compiler),
                        compilerFlags=flags, bytes=spec['bytes'], relocations=rels)
                    tag = 'sdk-v5-' + unit + '-' + label
                    entry, code = validate_candidate(origin, spec, native, tag)
                    entry.update(referenceFunction=name, normalizedFingerprint=fingerprint,
                        researchEvidence=[dict(path=source.relative_to(ROOT).as_posix(), sha256=sha256(source))],
                        sourceAdaptationMethod='pinned comparative SDK ordinary C; macros expanded and closed types selected; measured relocation adaptation')
                    result.update(source=flat.relative_to(ROOT).as_posix(), selection=selected, exact=code is not None)
                    if code is not None:
                        row['matches'].append(entry)
                        write_json(LANE / 'candidates' / ('%08x-%s.json' % (spec['address'], tag)),
                            dict(match=entry, address=hex(spec['address']), bytes=spec['bytes'], acceptedSourceCredit=0))
                    else:
                        result['compileResult'] = entry
                except Exception as error:
                    result.update(exact=False, refusal=repr(error))
                row.setdefault('closedAttempts', []).append(result)
    write_json(result_path, row)
    return row


def main():
    global SPECS
    parser = argparse.ArgumentParser()
    parser.add_argument('--extra-profiles', action='store_true')
    args = parser.parse_args()
    wanted = {int(e['address'], 0) for e in json.loads((LANE / 'claim.json').read_text())['functions']}
    SPECS = [s for s in candidates() if s['module'] == 'utility-child-arm7-wram' and s['mode'] == 'arm' and s['address'] in wanted]
    utility_code.WORK = WORK / 'sdk-flat-compiled'
    sources = [s for s in sorted((REF / 'libraries/wl_arm7/src').rglob('*.c'))]
    profiles = [('1.2/base', 2, 'off', '1.2_base', False), ('1.2/sp4', '4,p', 'on,noauto', '1.2_sp4', False)]
    if args.extra_profiles:
        profiles = [('1.2/base', 2, 'on,noauto', '1.2_base_o2_inline', False),
            ('1.2/base', 2, 'on,noauto', '1.2_base_o2_speed_inline', True),
            ('1.2/sp4', 2, 'on,noauto', '1.2_sp4_o2_inline', False),
            ('1.2/base', '4,p', 'on,noauto', '1.2_base_o4_inline', False),
            ('1.2/base', '4,s', 'on,noauto', '1.2_base_o4s_inline', False),
            ('2.0/base', '4,s', 'on,noauto', '2.0_base_o4s_inline', False)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(build, [(s, *p) for s in sources for p in profiles]))
    exact = {e['address']: e for row in rows for e in row['matches']}
    suffix = '-extra' if args.extra_profiles else ''
    write_json(LANE / ('sdk-reference-summary' + suffix + '.json'), dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        attempts=len(rows), compiledUnits=sum(r['exitCode'] == 0 for r in rows), maskedRows=sum(len(r['maskedMatches']) for r in rows),
        exactFunctions=len(exact), exactBytes=sum(e['bytes'] for e in exact.values()), results=rows,
        sourceCredit=0, sdkVersionAndNamesRemainComparative=True, provisionalHeadersAbsentFromSelectedSources=True))
    print(dict(attempts=len(rows), compiledUnits=sum(r['exitCode'] == 0 for r in rows),
        maskedRows=sum(len(r['maskedMatches']) for r in rows), exactFunctions=len(exact), exactBytes=sum(e['bytes'] for e in exact.values())), flush=True)


if __name__ == '__main__':
    main()
