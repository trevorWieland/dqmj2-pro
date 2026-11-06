import hashlib
import json
import re
import sys
from pathlib import Path
import match_runtime
import utility_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import link_arm7_child_irq_dispatch260_scope_20261101 as qualified
import arm7_child_irq_dispatch_platform_abi_20261101 as platform_abi
import arm7_child_irq_dispatch260_native_20261101 as fixture
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-irq-dispatch260-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261101/lane-child-irq-dispatch260-final/closure.json'
PROFILE_SHA = '7266b7b480939ac7f11ee8243eaa861943edac0652d6c05e7b96f5c96009671c'
PINS = PROFILE.with_name('generator-pins.json')
PIN_SHA = '6457199a5decb7d174a068ce0d10daa6a0a2401926c0afb6a6c6a4ba1b87f7de'
REPORT = ROOT / 'evidence/matches/arm7-child-irq-dispatch260-20261101.json'
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
    profile = json.loads(PROFILE.read_text())
    accepted = json.loads((ROOT / profile['acceptedSnapshot']).read_text())['functions']
    for pin in profile['matches']:
        address = int(pin['address'], 0)
        for old in accepted:
            if all(old.get(key) == pin[key] for key in ('processor', 'program', 'module', 'mode')):
                begin = int(old['address'], 0) if isinstance(old['address'], str) else old['address']
                end = begin + (old.get('bytes') or 1)
                if address < end and begin < address + pin['bytes']:
                    raise ValueError('Proposed host body overlaps a measured accepted identity')
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
            raise ValueError('Host IRQ source/include closure changed')
        code = current.read_text()
        if len(code.splitlines()) > 500 or '/*' in code or '//' in code or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', code):
            raise ValueError('Host IRQ source is not bounded comment-free ordinary C')
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
        raise ValueError('Fresh complete host IRQ C size differs')
    obj = ROOT / derived['probeObject']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section, offset = symbol['st_shndx'], symbol['st_value'] & ~1
    relocs = [dict(row, format='SHT_RELA', explicitAddend=row['addend'], originalEncodedWord=body[row['offset']:row['offset'] + 4].hex()) for row in derived['relocations']]
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section, sectionOffset=offset,
        relocations=relocs, sourceLanguage='C99', ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=pin['bytes'] - pin['codeBytes'], wholeModuleLinked=False)
    entry['qualifiedCanonicalScope']=dict(qualified.REFERENCE)
    try:
        linker.validate(entry,directory/'refused-original-link')
    except ValueError as error:
        refusal=str(error)
        if refusal!='Complete candidate span or canonical ARM7 entry differs':
            raise
    else:
        raise ValueError('Original missing-entry guard was bypassed')
    platform=platform_abi.guard(entry,json.loads(PROFILE.read_text())['fixedPlatformWord']) if int(entry['address'],0)==0x037FBB84 else None
    proof=qualified.validate(entry,directory/'real-link')
    bounds=next(item for item in qualified.inventory()['entries'] if item['address']==entry['address'])
    return dict(entry,exactAfterDeclaredRelocation=proof['exactLinkedBytes'],exactAfterRealMwLink=proof['exactLinkedBytes'],
        realArm7Link=proof,boundaries=bounds,originalDefaultLinkerRefusal=refusal,fixedPlatformAbi=platform,
        compileCommand=[str(compiler),*pin['compilerFlags'],'-c',str(source),'-o',str(obj)],compileCwd=str(ROOT),
        sourceOnlyCompilerInput={'source':pin['source'],'sha256':pin['sourceSha256'],'includes':pin['sourceDependencies'],'originalCodeCompilerInput':False},
        sourceAbiContract={'physicalArgumentWords':1 if int(entry['address'],0)==0x037FBB84 else 0,'return':'void',
            'callbackRecordBytes':12,'definedDispatcherIndexDomain':[0,8],'originalCallbackArrayExtentClaimed':False},
        originalDataSourceCredit=0,nativeCalleeCodeOrSourceCredit=0)


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
    qualified.prepare()
    rows = [build(pin) for pin in json.loads(PROFILE.read_text())['matches']]
    bodies = {int(row['address'], 0): (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes() for row in rows}
    per_unit = fixture.oracle(bodies)
    for row in rows:
        row['oracle'] = per_unit[int(row['address'], 0)]
    oracle = {'trace': next(iter(per_unit.values()))['trace'],
        'actualReturnCountsByEntry': {hex(address): value['actualOriginalAndCompiledReturns'] for address, value in per_unit.items()},
        'sourceLinkedDispatcherTailEntriesSeparate':sum(value['sourceLinkedDispatcherTailEntriesSeparate']for value in per_unit.values()),
        'ownInstructionCoverage': {hex(address): value['instructionCoverage'] for address, value in per_unit.items()},
        'vectors': sum(value['vectors'] for value in per_unit.values()), 'unsupportedReturnCredit': 0,
        'providerReplacements': [], 'originalCallbackCodeOrDataCredit':0, 'allOwnedInstructionBytesVisited':all(not value['instructionCoverage']['unvisited']for value in per_unit.values())}
    symbols, bindings = publication(rows)
    return {'matches': rows, 'nativeSymbols': symbols, 'nativeSymbolEntries': bindings, 'sharedSourceLinkedNativeEvidence': oracle,
        'matchedInitializedBytes': sum(row['bytes'] for row in rows), 'matchedInstructionBytes': sum(row['codeBytes'] for row in rows), 'generatedLiteralBytes': sum(row['generatedLiteralBytes'] for row in rows),
        'newOrdinaryFunctionCount': 8, 'newInitializedCoverageBytes': 260, 'declarationMigrationCount': 0, 'declarationMigrationBytes': 0,
        'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
        'qualifiedCanonicalScope':dict(qualified.REFERENCE),
        'fixedPlatformWord':json.loads(PROFILE.read_text())['fixedPlatformWord'],
        'ordinaryDataAbsoluteAddressGeneralizationAllowed': False,
        'referenceGuidance':json.loads(PROFILE.read_text())['referenceGuidance']}



def main():
    pins = verify_inputs()
    report = proof()
    names = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report.update(schemaVersion=1, generator=Path(__file__).name, generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        pinnedGeneratorAndRuntimeDependencies=pins, romSha256=ROM, processor='arm7', program='dwc/utility.bin/move/child.srl', module='utility-child-arm7-wram')
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'newSourceBytes': 260, 'priorCallerBytesMigrated': 0, 'returns': report['sharedSourceLinkedNativeEvidence']['actualReturnCountsByEntry']}), flush=True)


if __name__ == '__main__':
    main()
