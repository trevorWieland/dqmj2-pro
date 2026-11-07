import shutil
import sys
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256, now
import build_modules as builder
from link_runtime_unit import relocation_rows

HANDOFF = 'evidence/lanes/parallel-wave20261106/mb-local-context-next/register-consumer-handoff-v1.json'
HANDOFF_SHA = '75c582a0581bee5612aea8bbc9550bf6c8e3c044918d78499abdb4aa87ab6167'


def main():
    assert sha256(ROOT / HANDOFF) == HANDOFF_SHA
    handoff = read_json(ROOT / HANDOFF)
    for pin in [handoff['sourceObject'], *handoff['sourcePins']]:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    source = next(p for p in handoff['sourcePins'] if p['path'].endswith('.c'))
    dependencies = [p for p in handoff['sourcePins'] if p['path'].endswith('.h')]
    work = ROOT / 'work/root-mb-register-module' / uuid.uuid4().hex[:12]
    work.mkdir(parents=True)
    common = dict(module='main', processor='arm9', unit='root_mb_register.c',
        object=handoff['sourceObject']['path'], sha256=handoff['sourceObject']['sha256'],
        source=source['path'], sourceSha256=source['sha256'], sourceDependencies=dependencies,
        interiorSymbols={}, sectionPaddingBytes=0, assemblyJustification=None)
    text = dict(common, kind='function', mode='arm', function='MB_RegisterFile',
        section='.text', sourceSection='.text', start='0x2015c70', end='0x2015f00',
        symbols={'func_02015c70': 'MB_RegisterFile'})
    bss = dict(common, kind='data', mode=None, section='.bss', sourceSection='.bss',
        start='0x20e68a4', end='0x20e68a5', symbols={'data_020e68a4': 'update$40'})
    bindings = handoff['realLink']['bindingOnlyProbes'] + handoff['realLink']['dataBindings']
    native_symbols = {r['name']: hex(int(r['address'], 0) | (r['mode'] == 'thumb')) for r in bindings}
    specification = work / 'source-units-input.json'
    write_json(specification, dict(schemaVersion=1, units=[text, bss], nativeSymbols=native_symbols))
    original_split, original_prepare = builder.split_symbol, builder.prepare_units
    observations = []

    def split(elf, name, output, *extra, **options):
        if name != 'MB_RegisterFile':
            return original_split(elf, name, output, *extra, **options)
        path = Path(elf.stream.name)
        assert sha256(path) == handoff['sourceObject']['sha256']
        assert extra == ({}, None, 0) and options == {'target_section': None}
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        defined = [s for s in symbols if s['st_info']['type'] == 'STT_FUNC' and s['st_shndx'] != 'SHN_UNDEF']
        assert all(s['st_size'] or s.name in ('$a', '$d') for s in defined)
        functions = [s for s in defined if s['st_size']]
        assert any(s.name == '$a' and s['st_value'] == 0 for s in defined)
        assert len(functions) == 1
        function = functions[0]
        assert function.name == name and function['st_info']['bind'] == 'STB_GLOBAL'
        assert function['st_size'] == 656 and function['st_value'] == 0
        section = elf.get_section(function['st_shndx'])
        assert section.name == '.text' and section['sh_type'] == 'SHT_PROGBITS' and section['sh_size'] == 656
        locals_ = [s for s in symbols if s.name == 'update$40']
        assert len(locals_) == 1
        local = locals_[0]
        assert local['st_info']['bind'] == 'STB_LOCAL' and local['st_info']['type'] == 'STT_OBJECT'
        assert local['st_value'] == 0 and local['st_size'] == 1
        storage = elf.get_section(local['st_shndx'])
        assert storage.name == '.bss' and storage['sh_type'] == 'SHT_NOBITS'
        assert storage['sh_size'] == storage['sh_addralign'] == 1
        relocations = relocation_rows(path, name)
        assert relocations == handoff['realLink']['sourceRelocations']
        shutil.copyfile(path, output)
        assert sha256(output) == handoff['sourceObject']['sha256']
        observations.append(dict(unchangedWholeCompilerObject=True, localObjectBindingPreserved=True,
            functionBytes=656, uninitializedStorageBytes=1, initializedStorageCredit=0))
        return section.data(), [r['offset'] for r in relocations]

    def prepare(path, report):
        result = original_prepare(path, report)
        target = builder.WORK / 'config-arm9/delinks.txt'
        content = target.read_text()
        first = '\nroot_mb_register.c:\n    complete\n    .text start:0x02015c70 end:0x02015f00\n'
        second = '\nroot_mb_register.c:\n    complete\n    .bss start:0x020e68a4 end:0x020e68a5\n'
        assert content.count(first) == content.count(second) == 1
        target.write_text(content.replace(first, first.rstrip('\n') + '\n    .bss start:0x020e68a4 end:0x020e68a5\n').replace(second, ''))
        target = builder.WORK / 'config-arm9/symbols.txt'
        content = target.read_text()
        line = 'update$40 kind:bss(size=0x1) addr:0x020e68a4'
        assert content.count(line) == 1
        target.write_text(content.replace(line, line + ' local'))
        return result

    before = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json', 'build_modules.py', 'elf_units.py']}
    write_json(work / 'state.json', dict(state='running', sourceCredit=0, createdUtc=now(), inputPins=before))
    print(dict(started=True, output=work.relative_to(ROOT).as_posix()), flush=True)
    with patch.object(builder, 'WORK', work / 'link-work'), patch.object(builder, 'EVIDENCE', work / 'evidence'), \
            patch.object(builder, 'split_symbol', split), patch.object(builder, 'prepare_units', prepare), \
            patch.object(sys, 'argv', [__file__, '--source-units', str(specification)]):
        code = builder.main()
    assert before == {n: sha256(ROOT / n) for n in before}
    report = read_json(work / 'evidence/latest.json')
    write_json(work / 'state.json', dict(state='passed' if code == 0 else 'failed', sourceCredit=0,
        exitCode=code, finishedUtc=now(), observations=observations, failure=report.get('failure'),
        allModuleBytesExact=report.get('allModuleBytesExact'), symbolCheckPassed=report.get('symbolCheckPassed'),
        productionOrSelectionsChanged=False, allAcceptedSourceCorpusPlacementProven=False))
    print(dict(exitCode=code, output=work.relative_to(ROOT).as_posix(), failure=report.get('failure')), flush=True)
    raise SystemExit(code)


if __name__ == '__main__':
    main()
