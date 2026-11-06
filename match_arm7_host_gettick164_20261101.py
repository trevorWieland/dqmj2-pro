import hashlib
import json
import re
import sys
from pathlib import Path
import match_runtime
import arm7_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_host_gettick164_native_20261101 as fixture
import arm7_host_gettick164_boundaries_20261101 as boundary
import match_arm7_host_timer_init124_20261101 as initializer_matcher
from elftools.elf.elffile import ELFFile
from project import ROOT, write_json

WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-gettick164-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261101/lane-host-gettick164-final/closure.json'
PROFILE_SHA = '111c3201f7d60590a61b52ee73fe447ecda341549aae060b2047be6562c65b57'
PINS = PROFILE.with_name('generator-pins.json')
PIN_SHA = 'dfa4a3d95a71b5e89ae43f5203ee88a8ec319150868d49bda258db1354be4c3f'
REPORT = ROOT / 'evidence/matches/arm7-host-gettick164-20261101.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned timer callback writer runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest(PINS.read_bytes()) != PIN_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Timer callback writer source profile/runtime/build differs')
    pins = json.loads(PINS.read_text())['files']
    for pin in pins:
        path = (ROOT / pin['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != pin['sha256']:
            raise ValueError('Changed timer callback writer source/input: ' + pin['path'])
    profile = json.loads(PROFILE.read_text())
    accepted = json.loads((ROOT / profile['acceptedSnapshot']).read_text())['functions']
    for pin in profile['matches']:
        start = int(pin['address'], 0)
        for old in accepted:
            if all(old.get(key) == pin[key] for key in ('processor', 'program', 'module', 'mode')):
                address = int(old['address'], 0) if isinstance(old['address'], str) else old['address']
                if start < address + (old.get('bytes') or 1) and address < start + pin['bytes']:
                    raise ValueError('Proposed programmer overlaps accepted source')
    return pins


def source_closure(pin):
    source = ROOT / pin['source']
    declared = [{'path': pin['source'], 'sha256': pin['sourceSha256']}, *pin['sourceDependencies']]
    for item in declared:
        path = (ROOT / item['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != item['sha256']:
            raise ValueError('Declared programmer source/header changed')
        text = path.read_text()
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
            raise ValueError('Programmer inputs are not bounded comment-free ordinary C')
    pending, seen = [source], set()
    while pending:
        for name in re.findall(r'^#include "([^"<>]+)"$', pending.pop().read_text(), re.M):
            path = (source.parent / name).resolve()
            if not path.is_relative_to(source.parent.resolve()):
                raise ValueError('Quoted source include escaped its own closure')
            if path not in seen:
                seen.add(path)
                pending.append(path)
    if {path.relative_to(ROOT).as_posix() for path in seen} != {row['path'] for row in pin['sourceDependencies']}:
        raise ValueError('Actual compiler header closure differs')


def build(pin, dependency=False):
    source_closure(pin)
    compiler = ROOT / pin['compiler']
    if digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Pinned programmer compiler differs')
    directory = WORK / ('writer-dependency' if dependency else 'tick-callback')
    directory.mkdir(parents=True, exist_ok=True)
    match_runtime.WORK = directory / 'isolated-runtime'
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, compiler, pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, masks, body = compiled
    if len(body) != pin['bytes']:
        raise ValueError('Fresh complete C size differs')
    with (ROOT / derived['probeObject']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        section, offset = symbol['st_shndx'], symbol['st_value'] & ~1
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section,
        sectionOffset=offset, relocations=[dict(row, format='SHT_RELA', explicitAddend=row['addend'],
            originalEncodedWord=body[row['offset']:row['offset'] + 4].hex()) for row in derived['relocations']],
        sourceLanguage='C99', ordinaryFunctionCredit=0 if dependency else 1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=pin['bytes'] - pin['codeBytes'], wholeModuleLinked=False)
    proof = linker.validate(entry, directory / 'real-link')
    layout = arm7_runtime.derive((ROOT/'extract/arm7/arm7.bin').read_bytes())
    bounds = boundary.boundaries(entry, layout)
    return dict(entry, realArm7Link=proof, exactAfterDeclaredRelocation=proof['exactLinkedBytes'],
        exactAfterRealMwLink=proof['exactLinkedBytes'], boundaries=bounds,
        compileCommand=[str(compiler), *pin['compilerFlags'], '-c', str(ROOT / pin['source']), '-o', str(ROOT / derived['probeObject'])],
        compileCwd=str(ROOT), sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'],
            'includes': pin['sourceDependencies'], 'originalCodeCompilerInput': False},
        sourceAbiContract={'physicalArgumentWords':0,'return':'u64-r0-r1','counterBytes':8,'counterMaskBits':48,
            'hardwareSampleBytes':2,'pendingWordBytes':4,'pendingMask':8,'correctionSampleThreshold':0x8000,
            'compatibleTickStateViewBytes':16,'originalObjectExtentClaimed':False,'counterVolatileAccessQualification':True,
            'counterGlobalDeclarationChanged':False,'counterMmioOrHistoricalQualifierClaimed':False},
        originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


def publication(rows):
    symbols, bindings = {}, []
    for row in rows:
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            if rel['symbol'] in symbols and symbols[rel['symbol']] != binding['address']:
                raise ValueError('Timer callback writer symbol acquired conflicting addresses')
            symbols[rel['symbol']] = binding['address']
            bindings.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'],
                sourceRelocationType=rel['type'], unchangedExplicitAddend=rel['explicitAddend'], sourceCredit=0,
                callerIdentity={key: row[key] for key in ('processor', 'program', 'module', 'address', 'mode')}))
    return symbols, bindings


def proof():
    verify_inputs()
    profile=json.loads(PROFILE.read_text())
    initializer_matcher.scoped.prepare()
    row=build(profile['matches'][0])
    initializer_matcher.WORK=WORK/'source-producers/initializer'
    initialized=initializer_matcher.build(profile['sourceLinkedDependencies'][0])
    initialized['ordinaryFunctionCredit']=0
    callbacks=initializer_matcher.callback_matcher
    callbacks.WORK=WORK/'source-producers/callback-and-writer'
    callback=callbacks.build(profile['sourceLinkedDependencies'][1])
    callback['ordinaryFunctionCredit']=0
    writer=callbacks.build(profile['sourceLinkedDependencies'][2],True)
    dependencies=[initialized,callback,writer]
    bodies={int(item['address'],0):(Path(item['realArm7Link']['cwd'])/'caller.bin').read_bytes()for item in [row,*dependencies]}
    row['oracle']=fixture.oracle(bodies)
    symbols,bindings=publication([row])
    return {'matches':[row],'sourceLinkedDependencies':dependencies,'nativeSymbols':symbols,'nativeSymbolEntries':bindings,
        'matchedInitializedBytes':164,'matchedInstructionBytes':152,'generatedLiteralBytes':12,
        'newOrdinaryFunctionCount':1,'newInitializedCoverageBytes':164,'sourceLinkedDependencyAdditionalCredit':0,
        'ordinaryAssemblyOrBlobCredit':0,'originalDataSourceCredit':0,'wholeModuleLinked':False,'sourceReconstructionComplete':False,
        'volatileTimerHardwareViews':{'0x04000100':2,'0x04000214':4},'counterViewBytes':8,'counterMaskBits':48,
        'compatibleTickStateViewBytes':16,'sharedCounterAccessQualificationIsNewHypothesis':True,
        'counterGlobalDeclarationChanged':False,'counterMmioOrHistoricalQualifierClaimed':False,
        'ordinaryDataAbsoluteAddressGeneralizationAllowed':False}


def main():
    pins = verify_inputs()
    report = proof()
    names = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report.update(schemaVersion=1, generator=Path(__file__).name, generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        pinnedGeneratorAndRuntimeDependencies=pins, romSha256=ROM, processor='arm7', program='', module='arm7-wram')
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'newSourceBytes': 164, 'ownReturns': report['matches'][0]['oracle']['actualOriginalAndCompiledReturns'],
        'writerAdditionalCredit':0,'dataCredit':0}), flush=True)


if __name__ == '__main__':
    main()
