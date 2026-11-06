import re
import struct
from project import sha256


def apply(report, work):
    required = {}
    for unit in report['sourceUnits']:
        if unit.get('kind') != 'data' or unit.get('section') not in ('.data', '.rodata', '.bss'):
            continue
        boundaries = [int(unit[key], 0) for key in ('start', 'end')]
        alignment = min(4, *(value & -value for value in boundaries))
        if alignment < 4:
            key = unit['module'], unit['section']
            required[key] = min(required.get(key, 4), alignment)
    if not required:
        return
    from elftools.elf.elffile import ELFFile
    changes = []
    for path in (work / 'delinks').glob('_dsd_gap@*.o'):
        module = path.stem.removeprefix('_dsd_gap@').rsplit('_', 1)[0]
        offsets = []
        with path.open('rb') as stream:
            elf = ELFFile(stream)
            for index, section in enumerate(elf.iter_sections()):
                alignment = required.get((module, section.name))
                if alignment and section['sh_addralign'] > alignment:
                    offsets.append((elf['e_shoff'] + index * elf['e_shentsize'] + 32, alignment, section.name))
        if not offsets:
            continue
        before = sha256(path)
        payload = bytearray(path.read_bytes())
        for offset, alignment, name in offsets:
            struct.pack_into('<I', payload, offset, alignment)
        path.write_bytes(payload)
        changes.append({'path': str(path), 'inputSha256': before, 'outputSha256': sha256(path), 'sections': [{'name': name, 'alignment': alignment} for offset, alignment, name in offsets]})
    path = work / 'arm9.lcf'
    text = path.read_text()
    placements = []
    for (module, section), alignment in sorted(required.items()):
        prefix = 'ARM9' if module == 'main' else module.upper()
        label = prefix + '_' + section[1:].upper()
        pattern = re.compile(r'(' + label + r'_START = \.;)(.*?)(' + label + r'_END = \.;)', re.S)
        matches = list(pattern.finditer(text))
        if len(matches) != 1:
            raise ValueError('Measured data placement lacks one LCF section region: ' + label)
        match = matches[0]
        preceding = re.findall(r'ALIGNALL\((\d+)\)', text[:match.start()])
        if not preceding:
            raise ValueError('Measured data placement lacks its previous LCF alignment')
        original = int(preceding[-1])
        replacement = match[1] + f'\n        ALIGNALL({alignment});' + match[2] + f'ALIGNALL({original});\n        ' + match[3]
        text = text[:match.start()] + replacement + text[match.end():]
        placements.append({'module': module, 'section': section, 'alignment': alignment, 'restoredInputAlignment': original})
    path.write_text(text)
    report['generatedDataGapAlignmentChanges'] = changes
    report['dataGapAlignmentPlacements'] = placements
    report['dataGapAlignmentReason'] = 'Verified source data boundaries require byte or halfword gap placement; native section start/end alignment and source object alignment remain explicit'
