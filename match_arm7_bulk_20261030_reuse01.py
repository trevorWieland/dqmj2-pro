import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_bulk_native_20261030 as fixture
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261030/reuse01/closure.json'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PROFILE_SHA = 'f617074c838757dc5588cca5145e697d8761282f22b8ceaa8763507e435f2a4b'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def boundary(entry, layout, files):
    address, size = int(entry['address'], 0), entry['bytes']
    inventory_path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(inventory_path.read_text())
    rows = [row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == address]
    if len(rows) != 1 or rows[0]['mode'] != entry['mode'] or rows[0]['ranges'] != [[f'0x{address:08x}', f'0x{address + size:08x}']]:
        raise ValueError('Candidate does not preserve its one measured configured root/range')
    modules = {module['id']: module for module in layout['modules']}
    outside, internal = [], []
    for row in inventory['functions']:
        if row.get('mode') not in ('arm', 'thumb'):
            continue
        module = modules[row['module']]
        raw, base = bytes(files[ROOT / module['binary']]), int(module['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in row['ranges']:
            start, end = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(raw[start - base:end - base], start):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if address <= target < address + size:
                    record = {'module': row['module'], 'sourceRoot': row['address'], 'sourceMode': row['mode'], 'pc': hex(instruction.address), 'target': hex(target)}
                    if address <= instruction.address < address + size:
                        internal.append(record)
                    else:
                        outside.append(record)
    if any(int(row['target'], 0) != address for row in outside):
        raise ValueError('Unreconciled configured outside branch enters this C body interior')
    encoded_interiors = []
    for module in layout['modules']:
        raw, base = bytes(files[ROOT / module['binary']]), int(module['base'], 0)
        for offset in range(0, len(raw) - 3, 4):
            target = int.from_bytes(raw[offset:offset + 4], 'little')
            if address < (target & ~1) < address + size:
                encoded_interiors.append({'processor': module['processor'], 'module': module['id'], 'storageAddress': hex(base + offset), 'word': hex(target)})
    if encoded_interiors:
        raise ValueError('Unreconciled initialized word points into source body interior')
    module = modules[entry['module']]
    raw, base = bytes(files[ROOT / module['binary']]), int(module['base'], 0)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if entry['mode'] == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(raw[address - base:address - base + size], address))
    if sum(row.size for row in instructions) != size or any(row.group(CS_GRP_CALL) for row in instructions):
        raise ValueError('Leaf C closure includes undecoded bytes or an unqualified call')
    return {'inventorySha256': digest(inventory_path.read_bytes()), 'configuredRootAndRangePreserved': True,
        'bytesFullyDecodedAsInstructions': size, 'literalPoolBytes': 0, 'paddingCredit': 0, 'outsideDirectEntryReferences': outside,
        'internalBranches': internal, 'outsideInteriorBranches': [], 'initializedInteriorPointerWords': [], 'instructionModes': [entry['mode']],
        'limitations': ['Current configured function-mode/range scan plus aligned initialized-word scan; opaque computed pointer producers are not exhaustively recovered',
            'Entry-domain proof does not establish complete-program control-flow or game reachability']}


def build(entry, directory, layout, files):
    source, compiler = ROOT / entry['source'], ROOT / entry['compiler']
    if digest(source.read_bytes()) != entry['sourceSha256'] or digest(compiler.read_bytes()) != entry['compilerSha256']:
        raise ValueError('Frozen ordinary C or pinned compiler changed')
    text = source.read_text()
    if '#include' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
        raise ValueError('Source closure is not the bounded standalone ordinary C unit')
    directory.mkdir(parents=True, exist_ok=True)
    attempt, compiled = crossreuse_utility_c.compile_origin(entry, compiler, entry['compilerFlags'], directory)
    if compiled is None:
        raise ValueError({'freshCCompile': attempt})
    derived, offsets, body = compiled
    if offsets or derived['bytes'] != entry['bytes']:
        raise ValueError('The frozen leaf source acquired relocations or a different extent')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == entry['name'])
        section_index, section_offset = symbol['st_shndx'], symbol['st_value'] & ~1
    current = dict(entry, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section_index,
        sectionOffset=section_offset, relocations=[], exactBytes=True, exactAfterDeclaredRelocation=True,
        objectCodeSha256=digest(body), wholeModuleLinked=False, originalObjectScaffolding=False, sourceDependencies=[])
    proof = linker.validate(current, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    native_binary = bytes(files[ROOT / entry['binary']])
    start = int(entry['address'], 0) - entry['base']
    native = native_binary[start:start + entry['bytes']]
    qualified = boundary(current, layout, files)
    execution = fixture.verify(int(entry['address'], 0), native, linked, entry['mode'])
    if execution['unvisitedInstructionAddresses']:
        raise ValueError('A frozen bounded leaf has an unexecuted instruction address')
    return dict(current, compileCommand=attempt.get('command', [str(compiler), *entry['compilerFlags'], '-c', str(source), '-o', str(obj)]),
        compileCwd=str(ROOT), realArm7Link=proof, boundaries=qualified, oracle=dict(execution, supported=True, verifiedReturn=True),
        ordinaryFunctionCredit=1, assembly=False, calleeSourceCredit=0,
        sourceOnlyCompilerInput={'source': entry['source'], 'sha256': entry['sourceSha256'], 'includes': [], 'originalCodeCompilerInput': False})


def run(batch):
    if not re.fullmatch('[a-z0-9-]+', batch):
        raise ValueError('An exclusive bounded work batch is required')
    if digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Measured input ROM changed')
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned Python/Unicorn/pyelftools runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA:
        raise ValueError('Frozen source/compiler profile changed')
    generator_pins = json.loads(PIN_FILE.read_text())['files']
    for pin in generator_pins:
        if digest((ROOT / pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('Frozen generator/dependency changed: ' + pin['path'])
    profile = json.loads(PROFILE.read_text())
    layout, files = utility_runtime.derive()
    results = []
    for entry in profile['matches']:
        directory = WORK / batch / entry['module'] / entry['address'][2:]
        current = build(entry, directory, layout, files)
        results.append(current)
        print(json.dumps({'module': current['module'], 'address': current['address'], 'bytes': current['bytes'],
            'exactFreshCAndRealMwldLink': True, 'actualNativeAndSourceReturns': current['oracle']['actualOriginalAndRecompiledReturns']}), flush=True)
    paths = [Path(__file__), Path(fixture.__file__), Path(linker.__file__), PROFILE, PIN_FILE]
    report = {'schemaVersion': 1, 'romSha256': ROM, 'program': utility_runtime.PROGRAM, 'processor': 'arm7',
        'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())} for path in paths],
        'pinnedGeneratorAndRuntimeDependencies': generator_pins,
        'runtime': {'pythonVersion': '3.13.5', 'pythonExecutable': sys.executable, 'pythonExecutableSha256': digest(Path(sys.executable).read_bytes()),
            'unicornVersion': unicorn.__version__, 'pyelftoolsVersion': elftools.__version__},
        'matches': results, 'matchedFunctionInstances': len(results), 'matchedInitializedBytes': sum(row['bytes'] for row in results),
        'actualOriginalAndRecompiledReturns': sum(row['oracle']['actualOriginalAndRecompiledReturns'] for row in results),
        'originalObjectScaffoldingCredit': 0, 'wholeModuleLinked': False, 'completeGameCoverage': False,
        'limitations': ['Seven independently qualified child ARM7 leaf instances; not a whole ARM7 module build',
            'Four instances reuse existing ordinary C implementation families; no new algorithm-family novelty is claimed',
            'Synthetic ABI/alias-domain effects and bounded error controls do not prove scene, hardware, concurrency or ownership semantics']}
    path = WORK / batch / 'report.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'reportSha256': digest(path.read_bytes()),
        'functions': len(results), 'bytes': report['matchedInitializedBytes'], 'actualReturns': report['actualOriginalAndRecompiledReturns']}), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    run(parser.parse_args().batch)
