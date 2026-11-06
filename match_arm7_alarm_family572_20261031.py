import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_runtime
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_alarm_family572_boundaries_20261031 as boundary
import arm7_alarm_family572_connected_20261031 as fixture
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-alarm-family572-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-host-alarm-family572-final/closure.json'
PROFILE_SHA = '076a60f705bf330af761c50f28cbe5793deee1edd8e5c94a748cb86b50bbc845'
PINS = PROFILE.with_name('generator-pins.json')
PIN_SHA = '6d02f6a956047bb12fa45608636c01a979a7476d40c8fd0dd83cd1a59d965936'
REPORT = ROOT / 'evidence/matches/arm7-alarm-family572-20261031.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned shared-alarm source/runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest(PINS.read_bytes()) != PIN_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Shared-alarm source/include profile or original ROM differs')
    pins = json.loads(PINS.read_text())['files']
    for row in pins:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Changed shared-alarm input: ' + row['path'])
    history = json.loads(PROFILE.read_text())['bodyHistory']
    if digest((ROOT / history['oldSource']).read_bytes()) != history['oldSourceSha256'] or digest((ROOT / history['oldHeader']).read_bytes()) != history['oldHeaderSha256']:
        raise ValueError('Historical frozen caller source/header changed')
    if history['oldSourceSha256'] != history['newCallerBodySha256'] or not history['sourceBytesIdentical']:
        raise ValueError('Prior caller body changed during declaration migration')
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
        sourceAbiContract={'physicalArgumentWords': {0x037FD54C: 7, 0x037FD3B0: 3, 0x037FE5C0: 0}[address], 'return': 'BOOL32' if address == 0x037FE5C0 else 'void', 'alarmViewBytes': 44},
        implementationFamily={0x037FD54C: 'typed-periodic-alarm-state-and-IRQ-bracket', 0x037FD3B0: 'modular64-fire-and-intrusive-queue-insertion', 0x037FE5C0: 'availability-gated-periodic-registration-and-reentry'}[address], originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


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
    rows = [build(pin) for pin in json.loads(PROFILE.read_text())['matches']]
    bodies = {int(row['address'], 0): (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes() for row in rows}
    oracle = fixture.oracle(bodies)
    for row in rows:
        row['oracle'] = {'supported': True, 'verifiedReturn': True,
            'actualOriginalAndCompiledReturns': oracle['actualReturnCountsByEntry'][row['address']],
            'sourceLinkedFamilyEvidence': 'sharedSourceLinkedNativeEvidence', 'instructionCoverage': oracle['ownInstructionCoverage'][row['address']],
            'originalDataOrCalleeCredit': 0, 'unsupportedReturnCredit': 0}
    symbols, bindings = publication(rows)
    return {'matches': rows, 'nativeSymbols': symbols, 'nativeSymbolEntries': bindings, 'sharedSourceLinkedNativeEvidence': oracle,
        'matchedInitializedBytes': sum(row['bytes'] for row in rows), 'matchedInstructionBytes': sum(row['codeBytes'] for row in rows), 'generatedLiteralBytes': sum(row['generatedLiteralBytes'] for row in rows),
        'newOrdinaryFunctionCount': sum(not row['declarationMigration'] for row in rows), 'newInitializedCoverageBytes': sum(row['newInitializedCoverageBytes'] for row in rows), 'declarationMigrationCount': sum(row['declarationMigration'] for row in rows), 'declarationMigrationBytes': sum(row['bytes'] for row in rows if row['declarationMigration']),
        'sourceBodyHistory': json.loads(PROFILE.read_text())['bodyHistory'], 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
        'alarmLayout': {'sourceViewBytes': 44, 'handler': 0, 'argument': 4, 'tag': 8, 'fire': 12, 'previous': 20, 'next': 24, 'period': 28, 'start': 36,
            'allThreeUnitsUseOneHeaderAndCompatibleCFunctionDeclarations': True, 'originalTotalObjectExtentClaimed': False}}


def main():
    pins = verify_inputs()
    report = proof()
    names = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report.update(schemaVersion=1, generator=Path(__file__).name, generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        pinnedGeneratorAndRuntimeDependencies=pins, romSha256=ROM, processor='arm7', program='', module='arm7-wram')
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'newSourceBytes': 416, 'priorCallerBytesMigrated': 156, 'returns': report['sharedSourceLinkedNativeEvidence']['actualReturnCountsByEntry']}), flush=True)


if __name__ == '__main__':
    main()
