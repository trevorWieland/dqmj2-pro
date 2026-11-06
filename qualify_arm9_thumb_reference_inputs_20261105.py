import argparse
import copy
import hashlib
import re
import os
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from closed_c_compiler_inputs_20261105 import compiler_inputs as closed_inputs
import link_runtime_unit as native_linker


LEDGER = 'provenance/arm9-thumb-reference-only-consumers-20261105.json'
IMAGE = 'extract/arm9/arm9.bin'
IMAGE_SHA = 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'


def derive():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    native_dependencies(config)
    import ndspy.rom
    import ndspy.code
    nds = ndspy.rom.NintendoDSRom(config['rom'].read_bytes())
    code = ndspy.code.MainCodeFile(nds.arm9, nds.arm9RamAddress)
    assert nds.arm9RamAddress == 0x02000000 and code.codeSettingsOffs == 0xB68
    assert [(s.ramAddress, len(s.data), s.implicit) for s in code.sections] == [(0x02000000, 930560, True), (0x01FF8000, 30880, False), (0x027E0000, 96, False)]
    data = bytearray(code.sections[0].data)
    assert struct.unpack_from('<I', data, code.codeSettingsOffs + 20)[0] == 0x02094460
    struct.pack_into('<I', data, code.codeSettingsOffs + 20, 0)
    assert hashlib.sha256(data).hexdigest() == IMAGE_SHA == sha256(ROOT / IMAGE)
    assert bytes(data) == (ROOT / IMAGE).read_bytes()
    return bytes(data)


def compiler_inputs(row):
    assert row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'main' and row['mode'] == 'thumb'
    flags = row['compilerFlags']
    assert flags.count('-thumb') == 1 and '-arm' not in flags
    assert flags.count('-proc') == 1 and flags[flags.index('-proc') + 1] == 'arm946e'
    inputs = closed_inputs(row)
    return dict(inputs, actualMode='thumb', sourceClosureCheckOnly=True)


def linked_output(row, directory, native):
    from elftools.elf.elffile import ELFFile
    link = row['realLink']
    lcf = ROOT / link['lcf']
    assert sha256(lcf) == link['lcfSha256']
    linker = Path(link['linkerAttempt']['command'][0])
    assert linker.is_relative_to(ROOT / 'tools') and sha256(linker) == link['linkerSha256']
    directory.mkdir(parents=True, exist_ok=True)
    copied_lcf = directory / 'unit.lcf'
    copied_lcf.write_bytes(lcf.read_bytes())
    objects = []
    for argument in link['linkerAttempt']['command']:
        if not str(argument).endswith('.o'):
            continue
        source = Path(argument)
        assert source.is_relative_to(ROOT / 'work')
        target = directory / source.name
        target.write_bytes(source.read_bytes())
        assert sha256(target) == sha256(source)
        objects.append(target)
    assert objects and sha256(objects[0]) == link['splitObjectSha256']
    elf_path = directory / 'linked.elf'
    command = [str(linker), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', row['name'], str(copied_lcf), *map(str, objects), '-o', str(elf_path)]
    run = subprocess.run(command, cwd=directory, capture_output=True, timeout=60,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert (directory / 'caller.bin').read_bytes() == native
    with elf_path.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = [s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name']]
        assert len(symbols) == 1 and symbols[0]['st_value'] == int(row['address'], 0) and symbols[0]['st_size'] == row['bytes']
    return dict(command=command, exitCode=run.returncode, rawOutputSha256=sha256(directory / 'caller.bin'),
        linkedElfSha256=sha256(elf_path), exactCopiedLcfSha256=sha256(copied_lcf), unchangedSplitObjects=True)


def object_mode(row):
    from elftools.elf.elffile import ELFFile
    path = ROOT / row['object']
    assert sha256(path) == row['objectSha256']
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf.elfclass == 32 and elf.little_endian
        table = elf.get_section_by_name('.symtab')
        symbols = [s for s in table.iter_symbols() if s.name == row['name']]
        assert len(symbols) == 1
        symbol = symbols[0]
        assert symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == row['bytes']
        start = symbol['st_value'] & ~1
        mappings = sorted((s['st_value'] & ~1, s.name[:2]) for s in table.iter_symbols()
            if s['st_shndx'] == symbol['st_shndx'] and s.name.startswith(('$t', '$a', '$d')) and (s['st_value'] & ~1) <= start)
        assert mappings and mappings[-1] == (start, '$t')
    return dict(relocatableFunctionValue=symbol['st_value'], mapping='$t', mappingOffset=start)


def qualify_report(name, expected, directory, data):
    from elftools.elf.elffile import ELFFile
    report = read_json(ROOT / name)
    rows = report['matches']
    assert len(rows) == len(expected) and {r['address']: r['bytes'] for r in rows} == expected
    configured = (ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8')
    extents = {(int(a, 0), int(n, 0)) for n, a in re.findall(r'kind:function\(thumb,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', configured)}
    proofs = []
    for row in rows:
        inputs = compiler_inputs(row)
        address = int(row['address'], 0)
        assert (address, row['bytes']) in extents and address % 2 == 0
        body = data[address - 0x02000000:address - 0x02000000 + row['bytes']]
        assert len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['targetSha256']
        mode = object_mode(row)
        link = row['realLink']
        assert link['exactCallerBytes'] and link['linkedCallerSha256'] == link['nativeSpanSha256'] == row['targetSha256']
        assert link['sourceObjectSha256'] == row['objectSha256']
        elf_path = (ROOT / link['linkedElf']).resolve()
        assert elf_path.is_relative_to(ROOT / 'work') and sha256(elf_path) == link['linkedElfSha256']
        with elf_path.open('rb') as stream:
            elf = ELFFile(stream)
            symbols = [s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name']]
            assert len(symbols) == 1
            symbol = symbols[0]
            assert (symbol['st_value'] & ~1) == address and symbol['st_size'] == row['bytes']
        assert (elf_path.parent / 'caller.bin').read_bytes() == body
        original_relink = linked_output(row, directory / row['address'] / 'original-real-link', body)
        adjusted = copy.deepcopy(row)
        flags = adjusted['compilerFlags']
        if '-lang' in flags:
            index = flags.index('-lang')
            assert flags.count('-lang') == 1 and flags[index + 1] in ['c', 'c99']
            adjusted['compilerFlags'] = flags[:index] + flags[index + 2:]
        fresh = fresh_c99(adjusted, directory / row['address'])
        fresh_row = copy.deepcopy(row)
        fresh_row.update(object=fresh['explicitC99Object'], objectSha256=fresh['explicitC99ObjectSha256'])
        fresh_mode = object_mode(fresh_row)
        assert fresh_mode == mode
        fresh_link = native_linker.validate(fresh_row, row['nativeSymbolEntries'], directory / row['address'] / 'fresh-c99-real-link')
        assert fresh_link['exactCallerBytes'] and fresh_link['linkedCallerSha256'] == row['targetSha256']
        assert all(p['initializedCodeBytes'] == p['nativeCalleeBytesUsed'] == p['calleeSourceCredit'] == 0 for p in fresh_link['bindingOnlyProbes'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], actualMode='thumb', compilerInputs=inputs,
            actualRelocatableMode=mode, freshRelocatableMode=fresh_mode, originalGenuineRelink=original_relink, freshExplicitC99=fresh, freshGenuineLink=fresh_link, genuineLinkedBytesIndependentlyEqual=True))
    return dict(report=name, reportSha256=sha256(ROOT / name), producer=report['generator'],
        producerSha256=report['generatorSha256'], expectedRanges=expected, proofs=proofs, sourceCredit=0)


def qualify_batches(batches):
    ledger_path = ROOT / LEDGER
    if not ledger_path.exists():
        return copy.deepcopy(batches), []
    import subprocess
    assert subprocess.check_output(['git', 'show', 'HEAD:' + LEDGER], cwd=ROOT) == ledger_path.read_bytes()
    ledger = read_json(ledger_path)
    projected, proofs = copy.deepcopy(batches), []
    consumers = {r['report']: r for r in ledger['consumers']}
    data = derive() if consumers else None
    for batch in projected:
        if batch['report'] not in consumers:
            continue
        consumer = consumers[batch['report']]
        assert batch['sourceHashes'][IMAGE] == IMAGE_SHA and consumer['mode'] == 'thumb'
        proof = qualify_report(batch['report'], consumer['expectedRanges'], ROOT / 'work/integration/thumb-source-input' / str(len(proofs)), data)
        assert proof['producerSha256'] == consumer['producerSha256'] == sha256(ROOT / consumer['producer'])
        del batch['sourceHashes'][IMAGE]
        proofs.append(proof)
    assert {p['report'] for p in proofs} == set(consumers)
    return projected, proofs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    options = parser.parse_args()
    spec = read_json(ROOT / options.specification)
    data, proofs = derive(), []
    ledger = read_json(ROOT / LEDGER) if (ROOT / LEDGER).exists() else dict(sourceCredit=0, consumers=[])
    known = {r['report'] for r in ledger['consumers']}
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        pins = {p['path'] for k in ['generatorSources', 'replayDependencies'] for p in report.get(k, [])}
        if IMAGE not in pins or {r['mode'] for r in report['matches']} != {'thumb'}:
            continue
        descriptor = read_json(ROOT / packet['producer'][1])
        expected = {r['address']: r['bytes'] for r in descriptor['identities']}
        proof = qualify_report(packet['report'], expected, ROOT / f'work/integration/cohort{spec["cohort"]}-thumb-reference' / str(len(proofs)), data)
        proofs.append(proof)
        if packet['report'] not in known:
            ledger['consumers'].append(dict(report=packet['report'], producer=proof['producer'], producerSha256=proof['producerSha256'],
                processor='arm9', program='', module='main', mode='thumb', expectedRanges=expected))
    output = f'evidence/verification/cohort{spec["cohort"]}-thumb-reference-inputs-20261105.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, registered=options.register, qualifications=proofs,
        independentlyDerivedMainImageSha256=IMAGE_SHA, originalSourcesObjectsFlagsReportsAndRegistryUnchanged=True))
    if options.register:
        write_json(ROOT / LEDGER, ledger)
    print(dict(passed=True, thumbReports=len(proofs), functions=sum(len(p['proofs']) for p in proofs), registered=options.register))


if __name__ == '__main__':
    main()
