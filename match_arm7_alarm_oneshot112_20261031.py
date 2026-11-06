import hashlib
import json
import re
import sys
from pathlib import Path
import match_runtime
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import match_arm7_alarm_family572_20261031 as dependency
import arm7_alarm_oneshot112_native_20261031 as fixture
import arm7_alarm_oneshot112_boundaries_20261031 as boundary
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-oneshot112-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-host-oneshot112-final/closure.json'
PROFILE_SHA = '5230938965072cde6519b044302520548e7d23fb083379ed15ec29d70c7f9b19'
PINS = PROFILE.with_name('generator-pins.json')
PIN_SHA = '2d29fee7dfa1d99be7d018cf979cf6079bfedbdd64e06ce8a6af1b75598bc8f6'
REPORT = ROOT / 'evidence/matches/arm7-oneshot112-20261031.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    dependency.verify_inputs()
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest(PINS.read_bytes()) != PIN_SHA:
        raise ValueError('Pinned one-shot source/header/current native dependency differs')
    pins = json.loads(PINS.read_text())['files']
    for row in pins:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Frozen one-shot compiler/runtime/input differs: ' + row['path'])
    profile = json.loads(PROFILE.read_text())
    if digest(Path(dependency.__file__).read_bytes()) != profile['sourceLinkedDependency']['matcherSha256']:
        raise ValueError('Frozen source-linked insertion builder differs')
    header = ROOT / profile['matches'][0]['sourceDependencies'][0]['path']
    if header.read_bytes() != (ROOT / 'src/arm7/lane_20261031_alarm_family572/native_alarm_registration_types.h').read_bytes():
        raise ValueError('One-shot and source-linked insertion use incompatible declarations')
    return pins


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
    seen = set()
    pending = [source]
    while pending:
        current = pending.pop()
        for name in re.findall(r'^#include "([^"<>]+)"$', current.read_text(), re.M):
            included = (current.parent/name).resolve()
            if not included.is_relative_to(source.parent.resolve()):
                raise ValueError('Source-only quoted include escaped promoted closure')
            if included not in seen:
                seen.add(included)
                pending.append(included)
    if {path.relative_to(ROOT).as_posix() for path in seen} != {item['path'] for item in pin['sourceDependencies']}:
        raise ValueError('Actual recursive compiler include closure differs')
    directory = WORK / pin['address'][2:]
    directory.mkdir(parents=True, exist_ok=True)
    match_runtime.WORK = directory / 'isolated-runtime'
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
        compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)],
        compileCwd=str(ROOT), sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': pin['sourceDependencies'], 'originalCodeCompilerInput': False},
        sourceAbiContract={'physicalArgumentWords': 5, 'return': 'void', 'alarmViewBytes': 44},
        implementationFamily='unsigned64-one-shot-delay-and-native-queue-registration', originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)
def publication(rows):
    symbols, bindings = {}, []
    for row in rows:
        raw = (ROOT / row['binary']).read_bytes()
        first = int(row['address'], 0) - row['base']
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            if rel['symbol'] in symbols and symbols[rel['symbol']] != binding['address']:
                raise ValueError('One shared-alarm symbol acquired conflicting measured identities')
            symbols[rel['symbol']] = binding['address']
            bindings.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'], sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'], nativeEncodedWord=hex(int.from_bytes(raw[first + rel['offset']:first + rel['offset'] + 4], 'little')),
                sourceCredit=0, callerIdentity={key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode')}))
    return symbols, bindings


def proof():
    profile = json.loads(PROFILE.read_text())
    row = build(profile['matches'][0])
    dep_pin = next(pin for pin in json.loads(dependency.PROFILE.read_text())['matches'] if int(pin['address'], 0) == 0x037FD3B0)
    dep_row = dependency.build(dep_pin)
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    callee = (Path(dep_row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    row['oracle'] = fixture.oracle(body, callee)
    dep_row.update(dependencyOnly=True, newInitializedCoverageBytes=0, ordinaryFunctionCredit=0)
    symbols, bindings = publication([row])
    return {'matches': [row], 'sourceLinkedDependencies': [dep_row], 'nativeSymbols': symbols, 'nativeSymbolEntries': bindings,
        'matchedInitializedBytes': row['bytes'], 'matchedInstructionBytes': row['codeBytes'], 'generatedLiteralBytes': row['generatedLiteralBytes'],
        'newOrdinaryFunctionCount': 1, 'newInitializedCoverageBytes': row['bytes'], 'sourceLinkedDependencyAdditionalCredit': 0,
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}


def main():
    pins = verify_inputs()
    report = proof()
    names = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report.update(schemaVersion=1, generator=Path(__file__).name, generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        pinnedGeneratorAndRuntimeDependencies=pins, romSha256=ROM, processor='arm7', program='', module='arm7-wram')
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'newSourceBytes': report['newInitializedCoverageBytes'], 'actualOwnReturns': report['matches'][0]['oracle']['actualOriginalAndCompiledReturns']}), flush=True)


if __name__ == '__main__':
    main()
