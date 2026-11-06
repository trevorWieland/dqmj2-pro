import hashlib
import json
from pathlib import Path
import sys
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_lane_mmio_poll44_native_20261031 as fixture
import arm7_lane_mmio_poll44_boundaries_20261031 as boundary
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-mmio-poll44-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-mmio-poll44-final/closure.json'
PROFILE_SHA = '2350deb275a1b576c4a59abc0df327ac02bec84a2107a863af080a39ce71e4d5'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PIN_SHA = 'e0ae1c06fb4b6089f47340d70dde0b3dcf332f521a5393627950a7bb3e39aecf'
REPORT = ROOT / 'evidence/matches/arm7-lane-mmio-poll44-20261031.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned poll compiler/execution runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest(PIN_FILE.read_bytes()) != PIN_SHA:
        raise ValueError('Frozen poll source/runtime profiles differ')
    if digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Original ROM differs')
    pins = json.loads(PIN_FILE.read_text())['files']
    for row in pins:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Frozen poll dependency differs: ' + row['path'])
    return pins


def build(pin):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen poll C/compiler differs')
    if pin.get('sourceDependencies') != []:
        raise ValueError('Poll has an undeclared include closure')
    text = source.read_text()
    if len(text.splitlines()) > 500 or any(value in text for value in ('#include', '__asm', 'asm(', 'INCBIN', '/*', '//')):
        raise ValueError('Poll source is not standalone comment-free ordinary C')
    directory = WORK / pin['address'][2:]
    directory.mkdir(parents=True, exist_ok=True)
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, compiler, pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, offsets, body = compiled
    if len(body) != pin['bytes']:
        raise ValueError('Complete newly compiled poll size differs')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section, offset = symbol['st_shndx'], symbol['st_value'] & ~1
    relocations = [dict(row, format='SHT_RELA', explicitAddend=row['addend'], originalEncodedWord=body[row['offset']:row['offset'] + 4].hex()) for row in derived['relocations']]
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section,
        sectionOffset=offset, relocations=relocations, sourceLanguage='C', ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=4, wholeModuleLinked=False)
    proof = linker.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw = (ROOT / pin['binary']).read_bytes()
    original = raw[int(pin['address'], 0) - pin['base']:int(pin['address'], 0) - pin['base'] + pin['bytes']]
    return dict(entry, realArm7Link=proof, exactAfterDeclaredRelocation=proof['exactLinkedBytes'],
        exactAfterRealMwLink=proof['exactLinkedBytes'], boundaries=boundary.boundaries(entry), oracle=fixture.oracle(original, linked),
        compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)], compileCwd=str(ROOT),
        sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': [], 'originalCodeCompilerInput': False},
        implementationFamily='bounded-volatile-halfword-poll-with-raw-word-result', originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


def publication(rows):
    symbols, bindings = {}, []
    for row in rows:
        raw = (ROOT / row['binary']).read_bytes()
        first = int(row['address'], 0) - row['base']
        for relocation in row['relocations']:
            binding = row['realArm7Link']['bindings'][relocation['symbol']]
            symbols[relocation['symbol']] = binding['address']
            bindings.append(dict(binding, symbol=relocation['symbol'], sourceRelocationOffset=relocation['offset'],
                sourceRelocationType=relocation['type'], unchangedExplicitAddend=relocation['explicitAddend'],
                nativeEncodedWord=hex(int.from_bytes(raw[first + relocation['offset']:first + relocation['offset'] + 4], 'little')),
                sourceCredit=0, callerIdentity={key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode')}))
    return symbols, bindings


def main():
    pins = verify_inputs()
    rows = [build(row) for row in json.loads(PROFILE.read_text())['matches']]
    symbols, bindings = publication(rows)
    files = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PIN_FILE.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in files],
        'pinnedGeneratorAndRuntimeDependencies': pins, 'romSha256': ROM, 'processor': 'arm7', 'program': '', 'module': 'arm7-wram',
        'matches': rows, 'nativeSymbols': symbols, 'nativeSymbolEntries': bindings, 'matchedInitializedBytes': 44,
        'matchedInstructionBytes': 40, 'generatedLiteralBytes': 4, 'actualNativeAndCompiledReturns': sum(row['oracle']['actualOriginalAndCompiledReturns'] for row in rows),
        'actualSeparatelyObservedNestedReturns': sum(row['oracle']['actualSeparatelyObservedNestedPollReturns'] for row in rows),
        'actualSeparatelyObservedNativeCallerSuffixReturns': sum(row['oracle']['actualSeparatelyObservedNativeCallerSuffixReturns'] for row in rows),
        'providerFreeReturnCredit': 0, 'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'bytes': 44, 'ownReturns': report['actualNativeAndCompiledReturns'], 'callerSuffixReturns': report['actualSeparatelyObservedNativeCallerSuffixReturns']}), flush=True)


if __name__ == '__main__':
    main()
