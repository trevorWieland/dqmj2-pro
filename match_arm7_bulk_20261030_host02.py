import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_bulk_host_native_20261030_v2 as fixture
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
from project import write_json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/host02-proof'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261030/host02/closure.json'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PIN_SHA = 'a99e1dcb8d7c7fd536a947aba77ea73226b188afcbb3d8ef767996bbf349cde9'
PROFILE_SHA = '4ee85cd8605ddc1bed47a65a951751e2feaa4139754908bea6064ed1243342bf'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def boundaries(entry, layout):
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    inventory = json.loads(inventory_path.read_text())
    address, code_size, size = int(entry['address'], 0), entry['codeBytes'], entry['bytes']
    rows = [row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == address]
    if len(rows) != 1 or rows[0]['mode'] != 'arm' or [[int(value, 0) for value in pair] for pair in rows[0]['ranges']] != [[address, address + code_size]]:
        raise ValueError('Host configured root/code range differs')
    if any(address < int(row['address'], 0) < address + size for row in inventory['functions']):
        raise ValueError('Another configured function enters the full source unit')
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    module = modules[entry['module']]
    base = int(module['base'], 0)
    native = binaries[entry['module']][address - base:address - base + size]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native[:code_size], address))
    if sum(row.size for row in instructions) != code_size or any(row.group(CS_GRP_CALL) for row in instructions):
        raise ValueError('Host bounded source body has unknown bytes or callees')
    literal_references = []
    for instruction in instructions:
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                target = instruction.address + 8 + operand.mem.disp
                if not address + code_size <= target <= address + size - 4 or target % 4:
                    raise ValueError('Unreconciled PC-relative source data')
                literal_references.append({'pc': hex(instruction.address), 'storageAddress': hex(target),
                    'word': hex(int.from_bytes(native[target - address:target - address + 4], 'little'))})
    if {int(row['storageAddress'], 0) for row in literal_references} != set(range(address + code_size, address + size, 4)):
        raise ValueError('Compiler pool range includes unattributed bytes/alignment')
    references, interiors = [], []
    for row in inventory['functions']:
        if row.get('mode') not in ('arm', 'thumb'):
            continue
        other = modules[row['module']]
        raw, other_base = binaries[row['module']], int(other['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(raw[first - other_base:last - other_base], first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if address <= target < address + size and not address <= instruction.address < address + code_size:
                    item = {'module': row['module'], 'sourceRoot': row['address'], 'mode': row['mode'], 'pc': hex(instruction.address), 'target': hex(target)}
                    references.append(item)
                    if target != address:
                        interiors.append(item)
    if interiors:
        raise ValueError('Configured outside flow enters a body interior/pool')
    for name, raw in binaries.items():
        for offset in range(0, len(raw) - 3, 4):
            value = int.from_bytes(raw[offset:offset + 4], 'little')
            if address < (value & ~1) < address + size:
                raise ValueError('Unreconciled initialized pointer into source body/pool')
    return {'inventorySha256': digest(inventory_path.read_bytes()), 'configuredRootCodeAndPoolQualified': True, 'instructionBytes': code_size,
        'generatedLiteralBytes': size - code_size, 'literalReferences': literal_references, 'outsideRootReferences': references,
        'outsideInteriorOrPoolReferences': [], 'paddingCredit': 0, 'instructionMode': 'arm',
        'limitations': ['Configured direct-flow and aligned initialized-word scan; opaque computed pointer producers remain outside this entry-domain proof']}


def build(pin, directory, layout):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen host C or pinned compiler changed')
    text = source.read_text()
    if '#include' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
        raise ValueError('Host unit is not standalone bounded ordinary C')
    directory.mkdir(parents=True, exist_ok=True)
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, compiler, pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError({'compileFailure': attempt})
    derived, offsets, body = compiled
    if len(body) != pin['bytes']:
        raise ValueError('Fresh complete host C size differs')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section_index, section_offset = symbol['st_shndx'], symbol['st_value'] & ~1
    relocations = [{'offset': row['offset'], 'type': row['type'], 'symbol': row['symbol'], 'format': 'SHT_RELA', 'explicitAddend': row['addend'],
        'originalEncodedWord': body[row['offset']:row['offset'] + 4].hex()} for row in derived['relocations']]
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section_index,
        sectionOffset=section_offset, relocations=relocations, objectCodeSha256=digest(body), exactAfterDeclaredRelocation=True,
        sourceDependencies=[], sourceLanguage='C', ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=pin['bytes'] - pin['codeBytes'])
    proof = linker.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw = (ROOT / pin['binary']).read_bytes()
    address = int(pin['address'], 0)
    native = raw[address - pin['base']:address - pin['base'] + pin['bytes']]
    qualified = boundaries(entry, layout)
    native_proof = fixture.verify(entry, native, linked, pin['codeBytes'])
    if native_proof['unvisitedInstructionAddresses']:
        raise ValueError('The bounded host source has unvisited instruction addresses')
    return dict(entry, exactAfterRealMwLink=True, realArm7Link=proof, boundaries=qualified, oracle=native_proof,
        compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)], compileCwd=str(ROOT),
        sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': [], 'originalCodeCompilerInput': False},
        nativeCalleeCodeOrSourceCredit=0, wholeModuleLinked=False, state='function-matched')


def main():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Host pinned Python/native runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Frozen host source profile or measured ROM changed')
    if digest(PIN_FILE.read_bytes()) != PIN_SHA:
        raise ValueError('Host generator/runtime pins changed')
    pins = json.loads(PIN_FILE.read_text())['files']
    for pin in pins:
        if digest((ROOT / pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('Pinned generator/runtime dependency changed: ' + pin['path'])
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    results = []
    for pin in json.loads(PROFILE.read_text())['matches']:
        result = build(pin, WORK / pin['address'][2:], layout)
        results.append(result)
        print(json.dumps({'address': pin['address'], 'bytes': pin['bytes'], 'realMwldExact': True,
            'actualNativeAndSourceReturns': result['oracle']['actualOriginalAndRecompiledReturns']}), flush=True)
    sources = [Path(__file__), Path(fixture.__file__), Path(linker.__file__), PROFILE, PIN_FILE]
    producer = fixture.producer()
    wram = next(module for module in layout['modules'] if module['id'] == 'arm7-wram')
    original = (ROOT / wram['binary']).read_bytes()
    wram_base = int(wram['base'], 0)
    producer.update(inputModuleSha256=wram['sha256'], callerBytes=80,
        callerSha256=digest(original[0x037FFE14 - wram_base:0x037FFE64 - wram_base]),
        fieldReads={'gateByte': 2, 'secondMultiplierByte': 3, 'thresholdHalfword': 4, 'positionHalfword': 6, 'phaseHalfword': 8},
        argument0Transformation='zero-extend u16 at state+8, then logical shift right by 8',
        argument1Observation='native R1 retains zero-extended position halfword at state+6; no callee dependency meaning assigned')
    view = original[fixture.TABLE_STORAGE - wram_base:fixture.TABLE_STORAGE - wram_base + fixture.TABLE_STORAGE_BYTES]
    report = {'schemaVersion': 1, 'romSha256': ROM, 'program': '', 'processor': 'arm7', 'generator': Path(__file__).name,
        'generatorSha256': digest(Path(__file__).read_bytes()), 'generatorSources': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())} for path in sources],
        'pinnedGeneratorAndRuntimeDependencies': pins, 'originalNativeProducer': producer,
        'originalInitializedDataDependencies': [{'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'inputModuleSha256': wram['sha256'],
            'address': hex(fixture.TABLE_STORAGE), 'bytes': fixture.TABLE_STORAGE_BYTES, 'sha256': digest(view), 'recoveredDataSourceCredit': 0,
            'qualification': 'minimal byte-addressed view derived from the complete 0..255 producer domain; original object extent/name is not established',
            'logicalCenterAddress': hex(fixture.TABLE), 'logicalCenterOffset': fixture.TABLE - fixture.TABLE_STORAGE}],
        'matches': results, 'matchedInitializedBytes': sum(row['bytes'] for row in results),
        'matchedInstructionBytes': sum(row['codeBytes'] for row in results), 'generatedLiteralBytes': sum(row['generatedLiteralBytes'] for row in results),
        'actualOriginalAndRecompiledReturns': sum(row['oracle']['actualOriginalAndRecompiledReturns'] for row in results),
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False, 'originalObjectScaffoldingCredit': 0,
        'limitations': ['A signed-byte lookup is qualified for phase 0..255 and declared synthetic table bytes; caller/input contract outside that domain remains unresolved',
            'MMIO command source uses explicitly synthetic status-read schedules; physical I/O, ownership, timing and scene reachability are not established',
            'The 160-byte original addressed lookup view dependency is preserved oracle/scaffolding data and receives zero recovered-data source credit']}
    destination = ROOT / 'evidence/matches/arm7-bulk-20261030-host02.json'
    write_json(destination, report)
    print(json.dumps({'canonicalReport': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'functions': len(results), 'bytes': report['matchedInitializedBytes'], 'actualReturns': report['actualOriginalAndRecompiledReturns']}), flush=True)


if __name__ == '__main__':
    main()
