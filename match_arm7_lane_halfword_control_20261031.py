import argparse
import json
import re
import sys
from pathlib import Path
import arm7_lane_halfword_control_oracle_20261031 as fixture
import arm7_lane_halfword_control_boundaries_20261031 as boundary
import prove_arm7_lane_halfword_pointer_20261031 as producer
import link_arm7_halfword_control80_20261031 as linker
import crossreuse_utility_c
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256, write_json

SOURCE = ROOT / 'src/arm7/lane_20261031_halfword_control80'
WORK = ROOT / 'work/arm7-bulk-20261030/lane-halfword-control80-final'
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-halfword-control80-final/closure.json'
PROFILE_SHA = '9ca4a444676c8965eaea0abcf5aa6c259b1047754a4497ac4e01b0d2f14cb9f3'
PINS = PROFILE.with_name('generator-pins.json')
PINS_SHA = '478d0082a9409d39f0e74d8691ac3588b768719442d6ce582a3a7407da5b45b4'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def build(pin):
    inputs = [dict(path=pin['source'], sha256=pin['sourceSha256']), *pin['sourceDependencies'],
        dict(path=pin['compiler'], sha256=pin['compilerSha256'])]
    for item in inputs:
        path = (ROOT / item['path']).resolve()
        if not path.is_relative_to(ROOT) or sha256(path) != item['sha256']:
            raise ValueError('Frozen halfword source/include/compiler changed')
    for name in [pin['source'], *[p['path'] for p in pin['sourceDependencies']]]:
        text = (ROOT / name).read_text()
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
            raise ValueError('Halfword source is not bounded comment-free ordinary C')
    pending, seen = [ROOT / pin['source']], set()
    while pending:
        path = pending.pop()
        for name in re.findall(r'^#include "([^"<>]+)"$', path.read_text(), re.M):
            include = (path.parent / name).resolve()
            if not include.is_relative_to(SOURCE):
                raise ValueError('Compiler include escaped promoted halfword closure')
            if include not in seen:
                seen.add(include)
                pending.append(include)
    if {p.relative_to(ROOT).as_posix() for p in seen} != {p['path'] for p in pin['sourceDependencies']}:
        raise ValueError('Actual halfword include closure differs')
    directory = WORK / pin['module'] / f"{int(pin['address'], 0):08x}"
    directory.mkdir(parents=True, exist_ok=True)
    import match_runtime
    match_runtime.WORK = directory / 'isolated-runtime'
    attempt, compiled = crossreuse_utility_c.compile_origin(pin, ROOT / pin['compiler'], pin['compilerFlags'], directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, masks, body = compiled
    if len(body) != pin['bytes']:
        raise ValueError('Complete freshly compiled halfword C size differs')
    with (ROOT / derived['probeObject']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == pin['name'])
        section, offset = symbol['st_shndx'], symbol['st_value']
    relocs = [dict(r, format='SHT_RELA', explicitAddend=r['addend'],
        originalEncodedWord=body[r['offset']:r['offset'] + 4].hex()) for r in derived['relocations']]
    entry = dict(pin, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'],
        sectionIndex=section, sectionOffset=offset, relocations=relocs, sourceLanguage='C99', ordinaryFunctionCredit=1,
        originalObjectScaffolding=False, wholeModuleLinked=False, executableInstructionBytes=pin['codeBytes'],
        generatedLiteralBytes=pin['bytes'] - pin['codeBytes'])
    proof = linker.validate(entry, directory / 'real-link')
    linked = (directory / 'real-link/caller.bin').read_bytes()
    raw, address = (ROOT / pin['binary']).read_bytes(), int(pin['address'], 0)
    original = raw[address - pin['base']:address - pin['base'] + pin['bytes']]
    return dict(entry, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, realArm7Link=proof,
        boundaries=boundary.boundaries(entry), oracle=fixture.oracle(original, linked, address),
        compileCommand=[str(ROOT / pin['compiler']), *pin['compilerFlags'], '-c', str(ROOT / pin['source']), '-o', str(ROOT / derived['probeObject'])],
        compileCwd=str(ROOT), sourceOnlyCompilerInput=dict(source=pin['source'], sha256=pin['sourceSha256'],
            includes=pin['sourceDependencies'], originalCodeCompilerInput=False),
        sourceAbiContract=dict(argumentWords=1, argumentWidth=32,
            returnWidth=32, halfwordWidth=16, nativeAddressWordBytes=4,
            copyHalfwordCount=0, definedUnsignedRecurrence=False),
        nativeCalleeCodeOrSourceCredit=0, originalDataSourceCredit=0)


def symbol_map(rows):
    symbols, records = {}, []
    for row in rows:
        native, first = (ROOT / row['binary']).read_bytes(), int(row['address'], 0) - row['base']
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            if rel['symbol'] in symbols and symbols[rel['symbol']] != binding['address']:
                raise ValueError('Conflicting program-qualified halfword binding')
            symbols[rel['symbol']] = binding['address']
            records.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'],
                sourceRelocationType=rel['type'], unchangedExplicitAddend=rel['explicitAddend'],
                nativeEncodedWord=hex(int.from_bytes(native[first + rel['offset']:first + rel['offset'] + 4], 'little')),
                sourceCredit=0, callerIdentity={k: row[k] for k in ('program', 'processor', 'module', 'mode', 'address')}))
    return symbols, records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--program', choices=('host', 'all'), default='host')
    args = parser.parse_args()
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned halfword runtime differs')
    if sha256(PROFILE) != PROFILE_SHA or sha256(PINS) != PINS_SHA or sha256(ROOT / 'inputs/game.nds') != ROM:
        raise ValueError('Frozen halfword profile/runtime/ROM differs')
    pins = json.loads(PINS.read_text())['files']
    for pin in pins:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Halfword generator dependency changed: ' + pin['path'])
    producer.main()
    if sha256(ROOT / linker.RUNTIME_WORD_REPORT) != linker.RUNTIME_WORD_SHA:
        raise ValueError('Fresh absolute runtime-word producer qualification differs')
    profiles = json.loads(PROFILE.read_text())['matches']
    for name in ('host',):
        selected = [p for p in profiles if bool(p['program']) == (name == 'child')]
        rows = [build(p) for p in selected]
        symbols, records = symbol_map(rows)
        files = {Path(__file__).name, PROFILE.relative_to(ROOT).as_posix(), PINS.relative_to(ROOT).as_posix()} | {r['path'] for r in pins}
        report = dict(schemaVersion=1, romSha256=ROM, processor='arm7', program=selected[0]['program'],
            module=selected[0]['module'], generator=Path(__file__).name, generatorSha256=sha256(__file__),
            generatorSources=[dict(path=p, sha256=sha256(ROOT / p)) for p in sorted(files)],
            pinnedGeneratorAndRuntimeDependencies=pins, matches=rows, nativeSymbols=symbols, nativeSymbolEntries=records,
            sharedInterface=json.loads(PROFILE.read_text())['interfaceContract'],
            matchedInitializedBytes=sum(r['bytes'] for r in rows), matchedInstructionBytes=sum(r['codeBytes'] for r in rows),
            generatedLiteralBytes=sum(r['generatedLiteralBytes'] for r in rows),
            actualNativeAndCompiledReturns=sum(r['oracle']['actualOriginalAndCompiledReturns'] for r in rows),
            actualSeparateOriginalInitializerFillReturns=sum(r['oracle']['actualSeparateOriginalInitializerFillReturns'] for r in rows),
            actualOriginalConstructorReturns=0, constructorReturnCredit=0, sourceOnlyRebuild=True, wholeModuleLinked=False,
            sourceReconstructionComplete=False, ordinaryAssemblyOrBlobCredit=0, originalDataSourceCredit=0,
            nativeCalleeSourceCredit=0, zeroCoverageMigrationBytes=0)
        output = ROOT / 'evidence/matches/arm7-lane-halfword-control80-20261031.json'
        write_json(output, report)
        print(dict(report=output.relative_to(ROOT).as_posix(), sha256=sha256(output), functions=len(rows),
            bytes=report['matchedInitializedBytes'], actualOwnedReturns=report['actualNativeAndCompiledReturns'],
            actualSeparateFillReturns=report['actualSeparateOriginalInitializerFillReturns']), flush=True)


if __name__ == '__main__':
    main()
