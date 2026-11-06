import hashlib
import json
import re
import sys
from pathlib import Path
import match_runtime
import utility_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_child_alarm_handler256_native_20261101 as fixture
import arm7_child_alarm_handler256_boundaries_20261101 as boundary
import arm7_child_irq_check_platform_abi_20261101 as platform_abi
from elftools.elf.elffile import ELFFile
from project import ROOT, write_json

WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-handler256-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261101/lane-child-alarm-handler256-final/closure.json'
PROFILE_SHA = '614264ae6440adca522564190bed69bcd6be58f6bd619c21d3e889453e201238'
PINS = PROFILE.with_name('generator-pins.json')
PIN_SHA = 'b73be38b0efa06364d31b90f950aeb304c4e2d311d5e4b46bfc50d71a0b3b3b2'
REPORT = ROOT / 'evidence/matches/arm7-child-alarm-handler256-20261101.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned alarm handler runtime differs')
    if digest(PROFILE.read_bytes()) != PROFILE_SHA or digest(PINS.read_bytes()) != PIN_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Alarm handler source profile/runtime/build differs')
    pins = json.loads(PINS.read_text())['files']
    for pin in pins:
        path = (ROOT / pin['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != pin['sha256']:
            raise ValueError('Changed alarm handler source/input: ' + pin['path'])
    profile = json.loads(PROFILE.read_text())
    accepted = json.loads((ROOT / profile['acceptedSnapshot']).read_text())['functions']
    for pin in profile['matches']:
        start = int(pin['address'], 0)
        for old in accepted:
            if all(old.get(key) == pin[key] for key in ('processor', 'program', 'module', 'mode')):
                address = int(old['address'], 0) if isinstance(old['address'], str) else old['address']
                if start < address + (old.get('bytes') or 1) and address < start + pin['bytes']:
                    raise ValueError('Proposed alarm handler overlaps accepted source')
    return pins


def source_closure(pin):
    source = ROOT / pin['source']
    declared = [{'path': pin['source'], 'sha256': pin['sourceSha256']}, *pin['sourceDependencies']]
    for item in declared:
        path = (ROOT / item['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != item['sha256']:
            raise ValueError('Declared alarm handler source/header changed')
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


def compile_unit(pin, directory):
    source_closure(pin)
    compiler = ROOT / pin['compiler']
    if digest(compiler.read_bytes()) != pin['compilerSha256']:
        raise ValueError('Pinned alarm handler compiler differs')
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
        sourceLanguage='C99', ordinaryFunctionCredit=1, originalObjectScaffolding=False,
        executableInstructionBytes=pin['codeBytes'], generatedLiteralBytes=pin['bytes'] - pin['codeBytes'], wholeModuleLinked=False)
    return entry, directory


def build(pin):
    entry, directory = compile_unit(pin, WORK / 'handler')
    platform = platform_abi.guard(entry, json.loads(PROFILE.read_text())['fixedPlatformWord'])
    proof = linker.validate(entry, directory / 'real-link')
    layout, unused = utility_runtime.derive()
    return dict(entry, realArm7Link=proof, exactAfterDeclaredRelocation=proof['exactLinkedBytes'],
        exactAfterRealMwLink=proof['exactLinkedBytes'], boundaries=boundary.boundaries(entry, layout),
        fixedPlatformAbi=platform, compileCwd=str(ROOT),
        sourceOnlyCompilerInput={'source': pin['source'], 'sha256': pin['sourceSha256'],
            'includes': pin['sourceDependencies'], 'originalCodeCompilerInput': False},
        sourceAbiContract={'physicalArgumentWords': 0, 'return': 'void', 'alarmViewBytes': 44,
            'queueViewBytes': 8, 'reservedRuntimeWordBytes': 4, 'asynchronousIrqQualification': False},
        originalDataSourceCredit=0, nativeCalleeCodeOrSourceCredit=0)


def named_refusal(pin):
    entry, directory = compile_unit(pin, WORK / 'named-view-refusal')
    try:
        linker.validate(entry, directory / 'real-link')
    except ValueError as error:
        message = str(error)
        if message != 'Unqualified external ARM7 data target: 0x380fff8':
            raise
    else:
        raise ValueError('Unchanged strict base linker no longer refuses the named reserved word')
    return {'source': pin['source'], 'sourceSha256': pin['sourceSha256'], 'object': entry['object'],
        'objectSha256': entry['objectSha256'], 'sourceDependencies': pin['sourceDependencies'],
        'refusal': message, 'sourceCredit': 0, 'ordinaryScalarViewMatchesAllCode': False}


def publication(rows):
    symbols, bindings = {}, []
    for row in rows:
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            if rel['symbol'] in symbols and symbols[rel['symbol']] != binding['address']:
                raise ValueError('Alarm handler symbol acquired conflicting addresses')
            symbols[rel['symbol']] = binding['address']
            bindings.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'],
                sourceRelocationType=rel['type'], unchangedExplicitAddend=rel['explicitAddend'], sourceCredit=0,
                callerIdentity={key: row[key] for key in ('processor', 'program', 'module', 'address', 'mode')}))
    return symbols, bindings


def proof():
    pins = verify_inputs()
    profile = json.loads(PROFILE.read_text())
    row = build(profile['matches'][0])
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    row['oracle'] = fixture.oracle(body)
    symbols, bindings = publication([row])
    return {'matches': [row], 'nativeSymbols': symbols, 'nativeSymbolEntries': bindings,
        'namedViewOriginalStrictRefusal': named_refusal(profile['namedView']),
        'matchedInitializedBytes': 256, 'matchedInstructionBytes': 244, 'generatedLiteralBytes': 12,
        'newOrdinaryFunctionCount': 1, 'newInitializedCoverageBytes': 256,
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'wholeModuleLinked': False,
        'sourceReconstructionComplete': False, 'originalTickCallbackAndCallback16SourceCredit': 0,
        'fixedPlatformWord': profile['fixedPlatformWord'], 'originalDataOrBssExtentCredit': 0,
        'sourceLinkedDependencyAdditionalCredit': 0}


def main():
    pins = verify_inputs()
    report = proof()
    names = sorted({Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    report.update(schemaVersion=1, generator=Path(__file__).name, generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        pinnedGeneratorAndRuntimeDependencies=pins, romSha256=ROM, processor='arm7', program='dwc/utility.bin/move/child.srl', module='utility-child-arm7-wram')
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'newSourceBytes': 256, 'ownReturns': report['matches'][0]['oracle']['actualOriginalAndCompiledReturns'],
        'callbackBodyCredit': 0, 'fixedWordDataCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
