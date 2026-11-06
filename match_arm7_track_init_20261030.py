import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_track_init_boundaries_20261030 as boundary
import arm7_track_init_native_20261030 as fixture
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/track-init-final01'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261030/track-init-final01/closure.json'
PROFILE_SHA = '27673dd035883607a50adf366c2a4d97e9362f845ba29b8070c6b36089d02744'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PIN_SHA = '18563f0e695cdfcfbc674974e3ba6b1c61feb96ff47115ed996bf3ee636704f8'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(pin):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen typed ARM7 C/compiler differs')
    text = source.read_text()
    if '#include' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
        raise ValueError('Track unit is not standalone ordinary bounded C')
    directory = WORK / pin['address'][2:]
    directory.mkdir(parents=True, exist_ok=True)
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, compiler, pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, offsets, body = compiled
    if len(body) != pin['bytes']:
        raise ValueError('Fresh complete track C size differs')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section, offset = symbol['st_shndx'], symbol['st_value'] & ~1
    relocs = [dict(row, format='SHT_RELA', explicitAddend=row['addend'], originalEncodedWord=body[row['offset']:row['offset'] + 4].hex()) for row in derived['relocations']]
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section, sectionOffset=offset,
        relocations=relocs, sourceLanguage='C', sourceDependencies=[], ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=224, generatedLiteralBytes=0, wholeModuleLinked=False)
    proof = linker.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw = (ROOT / pin['binary']).read_bytes()
    address = int(pin['address'], 0)
    original = raw[address - pin['base']:address - pin['base'] + pin['bytes']]
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    return dict(entry, exactAfterDeclaredRelocation=proof['exactLinkedBytes'], exactAfterRealMwLink=proof['exactLinkedBytes'],
        realArm7Link=proof, boundaries=boundary.boundaries(entry, layout),
        oracle=fixture.oracle(entry, original, linked), compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)],
        compileCwd=str(ROOT), sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': [], 'originalCodeCompilerInput': False},
        implementationFamily='typed-track-bitfield-initialization', originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


def main():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned ARM7 execution runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Frozen ARM7 track profile or original ROM differs')
    if digest(PIN_FILE.read_bytes()) != PIN_SHA:
        raise ValueError('Frozen track generator/runtime closure differs')
    pins = json.loads(PIN_FILE.read_text())['files']
    for pin in pins:
        if digest((ROOT / pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('Track generator/runtime dependency differs: ' + pin['path'])
    results = [build(pin) for pin in json.loads(PROFILE.read_text())['matches']]
    symbols, entries = {}, []
    for row in results:
        raw = (ROOT / row['binary']).read_bytes()
        first = int(row['address'], 0) - row['base']
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            symbols[rel['symbol']] = binding['address']
            entries.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'], sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'], nativeEncodedWord=hex(int.from_bytes(raw[first + rel['offset']:first + rel['offset'] + 4], 'little')), sourceCredit=0))
    files = [Path(__file__), Path(fixture.__file__), Path(boundary.__file__), Path(linker.__file__), PROFILE, PIN_FILE,
        ROOT / 'arm7_track_init_opcode_roles_20261030.py', ROOT / 'crossreuse_utility_c.py', ROOT / 'elf_units.py', ROOT / 'link_runtime_unit.py', ROOT / 'arm7_runtime.py', ROOT / 'utility_runtime.py',
        ROOT / 'match_runtime.py', ROOT / 'match_lowlevel.py', ROOT / 'project.py']
    reference = ROOT / 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_seq.c'
    reference_header = ROOT / 'deps/references/pokediamond-b623abef/arm7/lib/include/SND_util.h'
    report = {'schemaVersion': 1, 'romSha256': ROM, 'processor': 'arm7', 'program': '', 'module': 'arm7-wram',
        'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())} for path in files],
        'pinnedGeneratorAndRuntimeDependencies': pins,
        'matches': results, 'nativeSymbols': symbols, 'nativeSymbolEntries': entries,
        'matchedInitializedBytes': 224, 'matchedInstructionBytes': 224, 'generatedLiteralBytes': 0,
        'actualNativeAndCompiledReturns': sum(row['oracle']['actualOriginalAndCompiledReturns'] for row in results),
        'actualSeparatelyObservedNestedLfoReturns': sum(row['oracle']['actualSeparatelyObservedNestedLfoReturns'] for row in results),
        'referenceProvenance': {'path': reference.relative_to(ROOT).as_posix(), 'sha256': digest(reference.read_bytes()),
            'upstreamCommit': 'b623abef1b4dfe204ca50aab42447ac00c134290', 'function': 'TrackInit',
            'compilerInput': False, 'sameSdkVersionPresumed': False,
            'tableDeclaration': {'path': reference_header.relative_to(ROOT).as_posix(), 'sha256': digest(reference_header.read_bytes()), 'entries': 128}},
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'calleeSourceCredit': 0,
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    destination = ROOT / 'evidence/matches/arm7-track-init-20261030.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'functions': 1, 'bytes': 224, 'actualNativeAndCompiledReturns': report['actualNativeAndCompiledReturns'],
        'actualSeparateNestedSetterReturns': report['actualSeparatelyObservedNestedLfoReturns']}), flush=True)


if __name__ == '__main__':
    main()
