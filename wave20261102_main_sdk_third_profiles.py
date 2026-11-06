import argparse
import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path

import match_runtime as C
from elftools.elf.elffile import ELFFile
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/main-sdk-third'
WORK = ROOT / 'work/parallel-wave20261102/main-sdk-third'
REF = ROOT / 'deps/reference/NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85'
SDK = ROOT / 'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840'
PROFILES = [
    ('base', 'base4p', ['-O4,p', '-ipa', 'file', '-inline', 'on,noauto']),
    ('base', 'base2space', ['-O2', '-inline', 'off']),
    ('base', 'base3space', ['-O3', '-inline', 'off']),
    ('base', 'base3speed', ['-O3', '-opt', 'speed', '-inline', 'off']),
    ('base', 'base4space', ['-O4', '-inline', 'off']),
    ('base', 'base4speed', ['-O4', '-opt', 'speed', '-inline', 'off']),
    ('base', 'base3file', ['-O3', '-ipa', 'file', '-inline', 'on,noauto']),
    ('sp1p5', 'sp4p', ['-O4,p', '-ipa', 'file', '-inline', 'on,noauto']),
]


def private_headers(variant):
    directory = WORK / 'profile-headers' / variant
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'string.h').write_text('\n')
    (directory / 'stdlib.h').write_text('int abs(int value);\n')
    (directory / 'wchar_t.h').write_text('typedef unsigned short wchar_t;\n')
    if variant == 'no-direction':
        source = REF / 'include/nnsys/g2d/g2d_config.h'
        text = source.read_text().replace('#define NNS_G2D_FONT_ENABLE_DIRECTION_SUPPORT', '')
        path = directory / 'nnsys/g2d/g2d_config.h'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return directory


def build(source, version, label, extra, variant):
    profile = label + '-' + variant
    directory = WORK / 'profile-objects' / source.stem / profile
    directory.mkdir(parents=True, exist_ok=True)
    compiler = ROOT / f'tools/mwccarm/mwccarm/2.0/{version}/mwccarm.exe'
    header = private_headers(variant)
    flags = [*C.FLAGS, *extra, '-lang', 'c99', '-DSDK_CW_FORCE_EXPORT_SUPPORT', '-DSDK_TS', '-DSDK_4M', '-DSDK_ARM9', '-DSDK_CW', '-DSDK_FINALROM', '-DSDK_CODE_ARM', '-DNNS_FINALROM']
    includes = [header, REF / 'include', SDK / 'include', ROOT / 'generated/sdk-reference/20261101/parse-only-headers', ROOT / 'generated/sdk-reference/20261101/include']
    includes.extend(folder for folder in (REF / 'libraries').glob('*/include') if folder.is_dir())
    includes.extend(folder for folder in (SDK / 'libraries').glob('*/include') if folder.is_dir())
    for folder in includes:
        flags.extend(['-i', folder.as_posix()])
    output = directory / 'compiled.o'
    command = [str(compiler), *flags, '-c', str(source), '-o', str(output)]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    row = dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), compiler=compiler.relative_to(ROOT).as_posix(), compilerSha256=sha256(compiler), compilerFlags=flags, profile=profile, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr, configurationVariant=variant, privateExplorationHeaderPins=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in sorted(header.rglob('*.h'))], sourceCredit=0)
    if not process.returncode:
        row.update(object=output.relative_to(ROOT).as_posix(), objectSha256=sha256(output))
    write_json(directory / 'result.json', row)
    return row


def masked(unit, image, sizes, module):
    if unit['exitCode']:
        return []
    output = []
    with (ROOT / unit['object']).open('rb') as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name('.symtab').iter_symbols():
            size = symbol['st_size']
            if symbol['st_info']['type'] != 'STT_FUNC' or not isinstance(symbol['st_shndx'], int) or size not in sizes or symbol['st_value'] & 1:
                continue
            start = symbol['st_value']
            body = elf.get_section(symbol['st_shndx']).data()[start:start + size]
            if len(body) != size:
                raise ValueError('Reference function extent escaped its section')
            mask = bytearray([255] * size)
            relocations = []
            supported = True
            for section in elf.iter_sections():
                if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                    continue
                table = elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    offset = rel['r_offset'] - start
                    if not 0 <= offset < size:
                        continue
                    kind = rel['r_info_type']
                    if kind == 2:
                        mask[offset:offset + 4] = bytes(4)
                    elif kind in (1, 28, 29):
                        mask[offset:offset + 3] = bytes(3)
                    else:
                        supported = False
                    target = table.get_symbol(rel['r_info_sym'])
                    relocations.append(dict(offset=offset, type=kind, symbol=target.name, sourceSymbolType=target['st_info']['type'], sourceSymbolBinding=target['st_info']['bind'], sourceSymbolSection=target['st_shndx'], format=section['sh_type'], explicitAddend=rel['r_addend'] if section['sh_type'] == 'SHT_RELA' else None, originalEncodedWord=body[offset:offset + 4].hex()))
            if not supported or sum(value.bit_count() for value in mask) < size * 4:
                continue
            for native in sizes[size]:
                address = int(native['address'], 0)
                original = image[address - 0x02000000:address - 0x02000000 + size]
                if len(original) == size and not any((a ^ b) & m for a, b, m in zip(body, original, mask)):
                    output.append(dict(referenceFunction=symbol.name, referenceSource=unit['source'], sourceSha256=unit['sourceSha256'], object=unit['object'], objectSha256=unit['objectSha256'], compiler=unit['compiler'], compilerSha256=unit['compilerSha256'], compilerFlags=unit['compilerFlags'], profile=unit['profile'], identity=dict(processor='arm9', program='', module='main', mode='arm', address=hex(address), bytes=size, inputModuleSha256=module['sha256']), originalBoundaryConfidence='configured complete native function extent', sourceOwner='root', originalOpcodeBitsAndNonRelocatedBytesExact=True, relocations=relocations, configurationVariant=unit['configurationVariant'], privateExplorationHeaderPins=unit['privateExplorationHeaderPins'], sourceCredit=0))
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--g3d', action='store_true')
    options = parser.parse_args()
    claims = read_json(LANE / 'claim.json')['claimedFunctions']
    allowed = {(r['address'], r['bytes']) for r in claims}
    sizes = defaultdict(list)
    for row in claims:
        sizes[row['bytes']].append(row)
    metadata, image, unused = measured_module('main')
    old = read_json(ROOT / 'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json')['candidates']
    candidates = [row for row in old if (row['identity']['address'], row['identity']['bytes']) in allowed]
    if options.g3d:
        candidates += read_json(LANE / 'masked-candidates.json')['candidates']
    units = []
    sources = sorted((REF / 'libraries/g2d').rglob('*.c'))
    queue = [(source, *profile, 'reference') for source in sources for profile in PROFILES]
    queue += [(REF / 'libraries/g2d/src/g2d_TextCanvas.c', *profile, 'no-direction') for profile in PROFILES]
    if options.g3d:
        queue = [(source, *PROFILES[-1], 'reference') for source in sorted((REF / 'libraries/g3d').rglob('*.c'))]
    for index, item in enumerate(queue):
        unit = build(*item)
        units.append(unit)
        candidates.extend(masked(unit, image, sizes, metadata))
        write_json(LANE / 'masked-candidates.json', dict(schemaVersion=1, candidates=candidates, sourceCredit=0, fullClosedSourceAndGenuineLinksStillRequired=True))
        if (index + 1) % 16 == 0 or index == len(queue) - 1:
            unique = {r['identity']['address']:r['identity']['bytes'] for r in candidates}
            print(dict(completed=index + 1, total=len(queue), compiling=sum(not r['exitCode'] for r in units), candidateFunctions=len(unique), candidateBytes=sum(unique.values())), flush=True)
    write_json(LANE / ('profile-campaign-g3d.json' if options.g3d else 'profile-campaign.json'), dict(schemaVersion=1, units=units, candidateRows=len(candidates), originalReferenceFilesUnchanged=True, privateHeaderExplorationOnly=True, nativeSourceCredit=0))
    selected = {}
    for row in candidates:
        selected.setdefault(row['identity']['address'], row)
    write_json(LANE / 'reference-selection.json', dict(schemaVersion=1, input=(LANE / 'masked-candidates.json').relative_to(ROOT).as_posix(), inputSha256=sha256(LANE / 'masked-candidates.json'), rows=list(selected.values()), sourceCredit=0))


if __name__ == '__main__':
    main()
