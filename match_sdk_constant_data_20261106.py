import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from sdk_constant_data_codec_20261106 import render, validate_layout
from match_child_message_data_20261106 import inspect_object, COMPILER, COMPILER_HASH, LINKER, LINKER_HASH


LAYOUT = 'src/runtime/parallel_wave20261106/sdk-constant-data/layout.json'
WORK = ROOT / 'work/sdk-constant-data-20261106'
REPORT = 'evidence/data/sdk-constant-data-20261106.json'


def compile_unit(source, target, flags, env):
    target.mkdir(parents=True, exist_ok=True)
    obj = target / 'data.o'
    command = [str(COMPILER), *flags, '-c', str(source), '-o', str(obj)]
    run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
    assert run.returncode == 0, run.stdout + run.stderr
    return obj, command


def link(obj, section, symbol, row, payload, directory, env):
    directory.mkdir(parents=True, exist_ok=True)
    original_hash = sha256(obj)
    local = directory / 'input.o'
    shutil.copyfile(obj, local)
    lcf = directory / 'data.lcf'
    lcf.write_text('MEMORY { DATA: ORIGIN = ' + row['address'] + ' > data.bin }\nSECTIONS {\n' +
                   section + ': { input.o(' + section + ') } > DATA\n}\n', encoding='utf-8')
    elf_path = directory / 'linked.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-proc', row['compilerProcessor'], '-main', symbol,
               str(lcf), str(local), '-o', str(elf_path)]
    run = subprocess.run(command, cwd=directory, env=env, capture_output=True, timeout=60)
    assert run.returncode == 0, run.stdout + run.stderr
    assert (directory / 'data.bin').read_bytes() == payload
    assert sha256(obj) == sha256(local) == original_hash
    from elftools.elf.elffile import ELFFile
    with elf_path.open('rb') as stream:
        entry = next(item for item in ELFFile(stream).get_section_by_name('.symtab').iter_symbols() if item.name == symbol)
        assert entry['st_info']['type'] == 'STT_OBJECT' and entry['st_size'] == len(payload)
        assert entry['st_value'] == int(row['address'], 0)
    return dict(exactDataBytes=True, exactDataAddress=True, objectUnmodified=True,
        actualSymbolType='STT_OBJECT', linkerSha256=sha256(LINKER), linkedElf=elf_path.relative_to(ROOT).as_posix(),
        linkedElfSha256=sha256(elf_path), linkedDataSha256=sha256(directory / 'data.bin'), command=command)


def main():
    config = configuration()
    native_dependencies(config)
    assert sha256(COMPILER) == COMPILER_HASH and sha256(LINKER) == LINKER_HASH
    original_open = Path.open
    rejections = []

    def source_only(path, *args, **kwargs):
        resolved = path.resolve()
        if any(resolved.is_relative_to(ROOT / name) for name in ['inputs', 'extract', 'deps/reference']):
            raise PermissionError('Original/reference input is blocked during semantic generation')
        return original_open(path, *args, **kwargs)

    generated = []
    with patch.object(Path, 'open', source_only):
        layout = read_json(ROOT / LAYOUT)
        validate_layout(layout)
        for row in layout['assets']:
            assert sha256(ROOT / row['semanticSource']) == row['semanticSourceSha256']
            symbol = row['nativeSymbol']
            code, payload = render(read_json(ROOT / row['semanticSource']), symbol)
            assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['targetSha256']
            generated.append((row, symbol, code, payload))
        for path in [config['rom'], ROOT / layout['assets'][0]['binary']]:
            try:
                path.read_bytes()
            except PermissionError:
                rejections.append(str(path))
            else:
                raise AssertionError('Original generation read was not rejected')
    assert len(generated) == 3 and sum(len(item[3]) for item in generated) == 562
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    matches, controls = [], []
    for row, symbol, code, payload in generated:
        assert sha256(ROOT / row['binary']) == row['inputModuleSha256']
        image = (ROOT / row['binary']).read_bytes()
        offset = int(row['address'], 0) - int(row['moduleBase'], 0)
        assert image[offset:offset + len(payload)] == payload
        unit = ROOT / f'generated/sdk-constant-data/{row["module"]}-{int(row["address"], 0):08x}.c'
        unit.parent.mkdir(parents=True, exist_ok=True)
        unit.write_text(code, encoding='utf-8')
        directory = WORK / (row['module'] + '-' + row['address'])
        flags = ['-O2', '-proc', row['compilerProcessor'], '-sym', 'on', '-nolink', '-lang', 'c99']
        obj, command = compile_unit(unit, directory / 'positive', flags, env)
        section, unused_index, unused_offset, debug = inspect_object(obj, symbol, payload)
        actual_link = link(obj, section, symbol, row, payload, directory / 'positive-link', env)
        wrong_document = read_json(ROOT / row['semanticSource'])
        wrong_document['elements'][0] ^= 1
        wrong_code, wrong_payload = render(wrong_document, symbol)
        wrong_source = directory / 'wrong.c'
        wrong_source.write_text(wrong_code, encoding='utf-8')
        wrong_obj, unused = compile_unit(wrong_source, directory / 'wrong', flags, env)
        wrong_section, unused_index, unused_offset, unused_debug = inspect_object(wrong_obj, symbol, wrong_payload)
        wrong_link = link(wrong_obj, wrong_section, symbol, row, wrong_payload, directory / 'wrong-link', env)
        try:
            inspect_object(wrong_obj, symbol, payload)
        except AssertionError:
            controls.append(dict(address=row['address'], genuinelyLinkedSameSizeWrongObjectRejected=True,
                                 wrongObjectSha256=sha256(wrong_obj), wrongLink=wrong_link))
        else:
            raise AssertionError('Wrong actual data object accepted')
        matches.append(dict(row, kind='data', mode='data', name=symbol, size=len(payload), compiledBytes=len(payload),
            initializedBytes=len(payload), source=unit.relative_to(ROOT).as_posix(), sourceSha256=sha256(unit),
            object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj), sourceLanguage='C',
            compiler=COMPILER.relative_to(ROOT).as_posix(), compilerSha256=COMPILER_HASH, compilerFlags=flags,
            compilerCommand=command, sourceDependencies=[dict(path=name, sha256=sha256(ROOT / name)) for name in [LAYOUT, row['semanticSource']]],
            section=section, outputSha256=hashlib.sha256(payload).hexdigest(), realLink=actual_link,
            relocations=[], executableSectionBytes=0, allocatedZeroFillBytes=0, ordinaryFunctionCredit=0,
            encodedAssetBytes=0, measuredZeroAlignmentBytes=0, nonAllocatedDebugRelocations=debug))
    write_json(ROOT / REPORT, dict(schemaVersion=1, romSha256=config['romSha256'], dataMatches=matches,
        dataMatchedBytes=562, functionMatched=0, functionMatches=[], nativeSymbols={}, ordinaryFunctionCredit=0,
        executableSectionBytes=0, controls=controls, generationOriginalInputsBlocked=True,
        originalReadRejectionControls=len(rejections), sourceCreditPendingSharedAcceptance=True,
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in
                          ['match_sdk_constant_data_20261106.py', 'sdk_constant_data_codec_20261106.py']],
        wholeModuleLinked=False, sourceReconstructionComplete=False, sourceOnlyRomProven=False))
    print(dict(dataObjects=3, initializedBytes=562, wrongObjects=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
