import hashlib
import json
import re
import sys
from pathlib import Path
import crossreuse_utility_c
import link_runtime_unit
import match_runtime
from main_overlap_copy_native_20261030 import oracle
from project import write_json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_CPU_ARM_946
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/main-predicate-scope-20261030/overlap-copy01'
PROFILE = ROOT / 'nonmatching/main-predicate-scope/20261030/overlap-copy01/closure.json'
PROFILE_SHA = 'd9bb77adab2e204611a75651a5bdcf645eb65c1fb1915334ba33f58444213b14'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
STACK, RETURN = 0x023E0000, 0x023FF000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main_references(entry, raw, config):
    address, size = int(entry['address'], 0), entry['bytes']
    references = []
    for mode, length, first in re.findall(r'^\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]{8})$', config, re.M):
        first, length = int(first, 0), int(length, 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for instruction in decoder.disasm(raw[first - 0x02000000:first - 0x02000000 + length], first):
            if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                continue
            target = instruction.operands[0].imm & ~1
            if address <= target < address + size and not address <= instruction.address < address + size:
                if target != address:
                    raise ValueError('Outside main branch enters a overlap copy-body interior')
                references.append({'pc': hex(instruction.address), 'mode': mode, 'target': hex(target)})
    for offset in range(0, len(raw) - 3, 4):
        value = int.from_bytes(raw[offset:offset + 4], 'little')
        if address < (value & ~1) < address + size:
            raise ValueError('Initialized main word points into overlap copy-body interior')
    return {'mainDirectRootReferences': references, 'outsideMainInteriorReferences': [], 'mainInitializedInteriorPointers': [],
        'generatedLiteralOrPaddingBytes': 0, 'configuredWholeBodyBytes': size,
        'limitations': ['Current configured main ARM/Thumb direct flows and aligned main initialized words; opaque/other-module producers remain separately scoped']}


def build(pin):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen overlap copy C/compiler changed')
    directory = WORK / pin['address'][2:]
    directory.mkdir(parents=True, exist_ok=True)
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, compiler, pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, offsets, body = compiled
    if len(body) != pin['bytes'] or offsets:
        raise ValueError('Fresh ordinary overlap copy C changed size or acquired a dependency')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section_index, section_offset = symbol['st_shndx'], symbol['st_value'] & ~1
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section_index,
        sectionOffset=section_offset, relocations=[], exactBytes=True, exactAfterDeclaredRelocation=True, sourceLanguage='C', sourceDependencies=[],
        originalObjectScaffolding=False, ordinaryFunctionCredit=1, wholeModuleLinked=False)
    proof = link_runtime_unit.validate(entry, {}, directory / 'real-main-link')
    rebuilt = (directory / 'real-main-link/caller.bin').read_bytes()
    metadata, raw, config = link_runtime_unit.measured_module('main')
    address = int(entry['address'], 0)
    original = raw[address - 0x02000000:address - 0x02000000 + entry['bytes']]
    return dict(entry, realMainLink=proof, boundaries=main_references(entry, raw, config), oracle=oracle(entry, original, rebuilt),
        compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)], compileCwd=str(ROOT),
        sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': [], 'originalCodeCompilerInput': False},
        implementationFamily='overlap-safe-byte-copy', originalDataSourceCredit=0, newImplementationFamilyNovelty=0)


def main():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned main native runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Measured ROM or frozen source/compiler profile changed')
    profile = json.loads(PROFILE.read_text())
    results = [build(pin) for pin in profile['matches']]
    files = [Path(__file__), PROFILE, ROOT / 'crossreuse_utility_c.py', ROOT / 'link_runtime_unit.py', ROOT / 'elf_units.py', ROOT / 'match_runtime.py', ROOT / 'match_lowlevel.py', ROOT / 'project.py', ROOT / 'main_overlap_copy_native_20261030.py']
    report = {'schemaVersion': 1, 'romSha256': ROM,
        'processor': 'arm9', 'program': '', 'module': 'main', 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())} for path in files],
        'matches': results, 'nativeSymbols': {}, 'nativeSymbolEntries': [], 'matchedInitializedBytes': sum(row['bytes'] for row in results),
        'actualNativeAndCompiledReturns': sum(row['oracle']['actualOriginalAndCompiledReturns'] for row in results),
        'ordinaryAssemblyOrBlobCredit': 0, 'newImplementationFamilyNovelty': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    destination = ROOT / 'evidence/matches/main-overlap-copy-20261030.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()), 'functions': len(results),
        'bytes': report['matchedInitializedBytes'], 'actualNativeAndCompiledReturns': report['actualNativeAndCompiledReturns']}), flush=True)


if __name__ == '__main__':
    main()
