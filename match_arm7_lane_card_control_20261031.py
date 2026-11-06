import hashlib
import json
import re
import sys
from pathlib import Path
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import qualified_arm7_card_scope_20261031 as qualified
import arm7_lane_card_abi16_boundaries_20261031 as boundary
import arm7_lane_card_control_oracle_20261031 as fixture
from elftools.elf.elffile import ELFFile
from project import write_json

ROOT = Path(__file__).resolve().parent
ABI_ROOT=ROOT/'src/arm7/lane_20261031_card_control452'
WORK = ROOT / 'work/arm7-bulk-20261030/lane-card-control452-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-card-control452-final/closure.json'
PROFILE_SHA = '664be46d2202ff7d50082f573a759387dfe8143687bf270e5ba3f0bf9e957d28'
PIN_FILE = PROFILE.with_name('generator-pins.json')
PIN_SHA = '75de7163c4890840ccbd5cc6daac0bcd6c76455d3ee90df3d7d8d464d1866d7e'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(pin):
    source, compiler = ROOT / pin['source'], ROOT / pin['compiler']
    if digest(source.read_bytes()) != pin['sourceSha256'] or digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Frozen typed ARM7 C/compiler differs')
    text = source.read_text()
    address=int(pin['address'],0)
    signatures={0x03802824:r'\(void\)',0x03803094:r'\(void\)',0x03803114:r'\(CardCommonStorage \*state,void \(\*callback\)\(void \*\),void \*argument\)',0x038031d4:r'\(u32 tag,u32 data,s32 enabled\)'}
    kinds={0x03802824:'s32',0x03803094:'u32',0x03803114:'void',0x038031d4:'void'}
    if not re.search(r'^'+kinds[address]+r'\s+'+re.escape(pin['name'])+signatures[address],text,re.M):
        raise ValueError('Measured full-word or void control ABI differs')
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
            if not included.is_relative_to(ABI_ROOT.resolve()):
                raise ValueError('Source-only quoted include escaped promoted closure')
            if included not in seen:
                seen.add(included)
                pending.append(included)
    if {path.relative_to(ROOT).as_posix() for path in seen} != {item['path'] for item in pin['sourceDependencies']}:
        raise ValueError('Actual recursive compiler include closure differs')
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
    proof = qualified.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw = (ROOT / pin['binary']).read_bytes()
    address = int(pin['address'], 0)
    original = raw[address - pin['base']:address - pin['base'] + pin['bytes']]
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    return dict(entry, exactAfterDeclaredRelocation=proof['exactLinkedBytes'], exactAfterRealMwLink=proof['exactLinkedBytes'],
        realArm7Link=proof, boundaries=boundary.boundaries(entry, layout),
        oracle=fixture.oracle(original, linked, address), compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(source), '-o', str(obj)],
        compileCwd=str(ROOT), sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'], 'includes': pin['sourceDependencies'], 'originalCodeCompilerInput': False},
        sourceAbiContract={'physicalArgumentWords':{0x03802824:0,0x03803094:0,0x03803114:3,0x038031d4:3}[address],
            'return':{0x03802824:'s32 boolean0/1',0x03803094:'u32 full-word',0x03803114:'void',0x038031d4:'void'}[address],
            'argumentWidths':32,'sharedCardTransferBytes':16},
        implementationFamily='shared-compatible-card-storage-views-and-ordinary-source', originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


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
    import prove_arm7_lane_card_callbacks_scope_20261031 as scope
    scope.main()
    if digest((ROOT/'evidence/arm7/lane-card-callback-scope-20261031.json').read_bytes())!='762a389d613559fa4216031db86a72fda3fad9a327d443e33347efe6131f2258':
        raise ValueError('Fresh callback-role dependency differs')
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
        'sharedInterface': json.loads(PROFILE.read_text())['interfaceContract'],
        'unchangedCBodyHistory': json.loads(PROFILE.read_text())['sourceBodyHistory'],
        'matches': results, 'nativeSymbols': symbols, 'nativeSymbolEntries': entries,
        'matchedInitializedBytes': sum(row['bytes'] for row in results), 'matchedInstructionBytes': sum(row['codeBytes'] for row in results), 'generatedLiteralBytes': sum(row['generatedLiteralBytes'] for row in results),
        'actualNativeAndCompiledReturns': sum(row['oracle']['actualOriginalAndCompiledReturns'] for row in results),
        'newCandidateBytes': sum(row['bytes'] for row in results if not row['migrationOnly']),
        'zeroCoverageMigrationBytes': sum(row['bytes'] for row in results if row['migrationOnly']),
        'actualResumedOuterSleepReturns': sum(row['oracle'].get('actualResumedOuterSleepReturns',0) for row in results),
        'actualNonlocalContextTransfers': sum(row['oracle'].get('actualNonlocalContextTransfers',0) for row in results),
        'actualSeparatelyObservedNestedReturns': sum(sum(row['oracle']['actualSeparatelyObservedNestedReturns'].values()) for row in results),
        'providerFreeOriginalAndCompiledReturns': sum(row['oracle']['providerFreeOriginalAndCompiledReturns'] for row in results),
        'syntheticBiosContractOriginalAndCompiledReturns': sum(row['oracle']['syntheticBiosContractOriginalAndCompiledReturns'] for row in results),
        'independentlyCheckedSigned64Returns': 0,
        'originalBiosExecutionCredit': 0,
        'referenceProvenance': {'kind': 'native-qualified-card-protocol-controls-and-word-interfaces', 'compilerInput': False},
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'calleeSourceCredit': 0,
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    destination = ROOT / 'evidence/matches/arm7-lane-card-control452-20261031.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'functions': len(results), 'bytes': sum(row['bytes'] for row in results), 'actualNativeAndCompiledReturns': report['actualNativeAndCompiledReturns'],
        'actualSeparateNestedReturns': report['actualSeparatelyObservedNestedReturns']}), flush=True)


if __name__ == '__main__':
    main()
