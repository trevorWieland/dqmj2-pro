import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_lane_driver_leaves_boundaries_20261030 as boundary
import arm7_lane_driver_leaves_oracle_20261030 as fixture
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-driver-leaves-final68'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261030/lane-driver-leaves-final68/closure.json'
PROFILE_SHA = 'da82cdc6ed8fbff02c7bd68a91a89fd9be43198c88dc3e677de5ed0dc2ed1152'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PIN_SHA = '41d2bb1e52fa98573d88aeed3866701937ec3dfcf956a63ceb0b6509ae643841'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(pin):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen typed ARM7 C/compiler differs')
    text = source.read_text()
    inputs = [dict(path=pin['source'], sha256=pin['sourceSha256']), *pin['sourceDependencies']]
    for item in inputs:
        current = (ROOT/item['path']).resolve()
        if not current.is_relative_to(ROOT) or digest(current.read_bytes()) != item['sha256']:
            raise ValueError('Channel-flush source/include closure changed')
        code = current.read_text()
        if len(code.splitlines()) > 500 or '/*' in code or '//' in code or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', code):
            raise ValueError('Channel-flush source is not bounded comment-free ordinary C')
    includes = re.findall(r'^#include "([^"<>]+)"$', text, re.M)
    include_paths = {(source.parent/name).resolve().relative_to(ROOT).as_posix() for name in includes}
    if include_paths != {item['path'] for item in pin['sourceDependencies']}:
        raise ValueError('Actual compiler include paths differ from declared closure')
    if sorted(includes) != ['native_sound_register_types.h'] or any('#include' in (ROOT/item['path']).read_text() for item in pin['sourceDependencies']):
        raise ValueError('Channel-flush declared include closure differs')
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
        relocations=relocs, sourceLanguage='C99', ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=pin['bytes'] - pin['codeBytes'], wholeModuleLinked=False)
    proof = linker.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw = (ROOT / pin['binary']).read_bytes()
    address = int(pin['address'], 0)
    original = raw[address - pin['base']:address - pin['base'] + pin['bytes']]
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    return dict(entry, exactAfterDeclaredRelocation=proof['exactLinkedBytes'], exactAfterRealMwLink=proof['exactLinkedBytes'],
        realArm7Link=proof, boundaries=boundary.boundaries(entry, layout),
        oracle=fixture.oracle(original, linked, address), compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)],
        compileCwd=str(ROOT), sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': pin['sourceDependencies'], 'originalCodeCompilerInput': False},
        implementationFamily='typed-mmio-stop-and-halfword-timer', originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


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
            if rel['symbol'] in symbols and symbols[rel['symbol']] != binding['address']:
                raise ValueError('Conflicting same-program SDK native symbol publication')
            symbols[rel['symbol']] = binding['address']
            entries.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'], sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'], nativeEncodedWord=hex(int.from_bytes(raw[first + rel['offset']:first + rel['offset'] + 4], 'little')), sourceCredit=0,
                callerIdentity={key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode')}))
    files = sorted(set([Path(__file__), PROFILE, PIN_FILE]+[ROOT/item['path'] for item in pins]))
    reference = ROOT / 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_exChannel.c'
    reference_header = ROOT / 'deps/references/pokediamond-b623abef/arm7/lib/include/SND_util.h'
    report = {'schemaVersion': 1, 'romSha256': ROM, 'processor': 'arm7', 'program': '', 'module': 'arm7-wram',
        'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())} for path in files],
        'pinnedGeneratorAndRuntimeDependencies': pins,
        'matches': results, 'nativeSymbols': symbols, 'nativeSymbolEntries': entries,
        'matchedInitializedBytes': sum(row['bytes'] for row in results), 'matchedInstructionBytes': sum(row['codeBytes'] for row in results), 'generatedLiteralBytes': sum(row['generatedLiteralBytes'] for row in results),
        'actualNativeAndCompiledReturns': sum(row['oracle']['actualOriginalAndCompiledReturns'] for row in results),
        'actualSeparatelyObservedNestedReturns': sum(sum(row['oracle']['actualSeparatelyObservedNestedReturns'].values()) for row in results),
        'providerFreeOriginalAndCompiledReturns': sum(row['oracle']['providerFreeOriginalAndCompiledReturns'] for row in results),
        'syntheticBiosContractOriginalAndCompiledReturns': 0,
        'independentlyCheckedSigned64Returns': 0,
        'originalBiosExecutionCredit': 0,
        'referenceProvenance': {'kind': 'measured-native-driver-cpu-behavior', 'compilerInput': False},
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'calleeSourceCredit': 0,
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    destination = ROOT / 'evidence/matches/arm7-lane-driver-leaves-20261030.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'functions': len(results), 'bytes': sum(row['bytes'] for row in results), 'actualNativeAndCompiledReturns': report['actualNativeAndCompiledReturns'],
        'actualSeparateNestedReturns': report['actualSeparatelyObservedNestedReturns']}), flush=True)


if __name__ == '__main__':
    main()
