import argparse
import copy
import gzip
import json
import shutil
from pathlib import Path
import match_arm7_lane_node_initialization216_20261031 as matcher
import link_arm7_bulk_20261030 as original_linker
from project import ROOT, sha256, write_json

GENERATOR_SHA = '3a71e31d0389a35f6f4a8d76e0016b190d7cb06afc01aa6d92ad2b524883de5c'
_FRESH = {}


def verify(name, pin):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or sha256(path) != pin:
        raise ValueError('Current halfword source/runtime/product changed: ' + str(name))
    return path


def validate(report):
    verify(Path(matcher.__file__).name, GENERATOR_SHA)
    verify(matcher.PROFILE, matcher.PROFILE_SHA)
    verify(matcher.PINS, matcher.PINS_SHA)
    verify('inputs/game.nds', matcher.ROM)
    program = report.get('program')
    if program not in ('', 'dwc/utility.bin/move/child.srl'):
        raise ValueError('Unqualified halfword program')
    profile = json.loads(matcher.PROFILE.read_text())
    selected = [p for p in profile['matches'] if p['program'] == program]
    pins = json.loads(matcher.PINS.read_text())['files']
    required = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {p['path'] for p in pins}
    if report.get('generator') != Path(matcher.__file__).name or report.get('generatorSha256') != GENERATOR_SHA:
        raise ValueError('Frozen halfword generator differs')
    if len(report.get('generatorSources', [])) != len(required) or {p['path'] for p in report['generatorSources']} != required:
        raise ValueError('Complete halfword runtime/generator closure differs')
    for item in report['generatorSources']:
        verify(item['path'], item['sha256'])
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published halfword runtime pins differ')
    if (report.get('romSha256'), report.get('processor'), report.get('module')) != (matcher.ROM, 'arm7', selected[0]['module']):
        raise ValueError('Qualified original halfword namespace differs')
    if report.get('sharedInterface') != profile['interfaceContract']:
        raise ValueError('Primitive address-word and halfword view contract differs')
    expected = (216, 212, 4, 384, 256)
    actual = tuple(report.get(k) for k in ('matchedInitializedBytes', 'matchedInstructionBytes', 'generatedLiteralBytes', 'actualNativeAndCompiledReturns', 'actualSeparateOriginalInitializerFillReturns'))
    if actual != expected:
        raise ValueError('Complete unit bytes/owned returns/separate prerequisite returns differ')
    if any(report.get(k) != 0 for k in ('actualOriginalConstructorReturns', 'constructorReturnCredit', 'ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'nativeCalleeSourceCredit', 'zeroCoverageMigrationBytes')):
        raise ValueError('Halfword constructor/scaffold/original-data credit overstated')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False or report.get('sourceOnlyRebuild') is not True:
        raise ValueError('Halfword source/module scope overstated')
    rows = report.get('matches', [])
    if len(rows) != len(selected):
        raise ValueError('Halfword namespace unit missing or duplicated')
    for pin, row in zip(selected, rows):
        if any(row.get(k) != v for k, v in pin.items()):
            raise ValueError('Frozen halfword source/profile/qualification differs')
        verify(pin['source'], pin['sourceSha256'])
        for item in pin['sourceDependencies']:
            verify(item['path'], item['sha256'])
        verify(row['object'], row['objectSha256'])
        proof = row['realArm7Link']
        verify(proof['linkCommand'][0], proof['linkerSha256'])
        verify(proof['lcf'], proof['lcfSha256'])
        verify(Path(proof['cwd']) / 'linked.elf', proof['linkedElfSha256'])
        verify(Path(proof['cwd']) / 'caller.bin', pin['targetSha256'])
        for anchor in proof['zeroCodeAnchors']:
            verify(anchor['object'], anchor['objectSha256'])
        trace = row['oracle']['traceProduct']
        packed = verify(trace['path'], trace['compressedSha256']).read_bytes()
        raw = gzip.decompress(packed)
        if len(packed) != trace['compressedBytes'] or len(raw) != trace['rawBytes'] or matcher.fixture.native.digest(raw) != trace['rawSha256'] or packed[4:8] != bytes(4):
            raise ValueError('Current halfword native trace changed')
        records = json.loads(raw)
        address = int(pin['address'], 0)
        count = 128
        if len(records) != count or trace['records'] != count:
            raise ValueError('Current halfword native scenario count differs')
        for record in records:
            state = record['state']
            if not state['actualReturn'] or state['constructorPrefixReturnCredit'] or state['actualOriginalClearPrerequisiteReturns']!=1:
                raise ValueError('Owned node return versus prerequisite prefix scope differs')
            if state['actualOwnedReturns']!=len(state['steps']) or any(not step['execution']['actualReturn'] for step in state['steps']):
                raise ValueError('Every connected node entry must actually return')
            if any(step['actualNativeHelperReturns']['0x27e8c5c']!=11 or step['actualNativeHelperReturns']['0x37f886c']!=1 or len(step['lowerAllocationProviders'])!=1 for step in state['steps']):
                raise ValueError('Actual original native helper/provider contract differs')
    symbols, entries = matcher.symbol_map(rows)
    if report.get('nativeSymbols') != symbols or report.get('nativeSymbolEntries') != entries:
        raise ValueError('Current qualified native address-word publication differs')
    key = (program, matcher.fixture.native.digest(json.dumps(report['generatorSources'], sort_keys=True).encode()))
    if key not in _FRESH:
        _FRESH[key] = [matcher.build(pin) for pin in selected]
    if rows != _FRESH[key]:
        raise ValueError('Published halfword source/link/native/boundary evidence differs from full fresh build')
    return {(r['processor'], r['program'], r['module'], r['address'], r['mode']): r for r in rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--program', choices=('host', 'all'), default='all')
    args = parser.parse_args()
    names = ('host',)
    reports = {name: json.loads((ROOT / 'evidence/matches/arm7-lane-node-initialization216-20261031.json').read_text()) for name in names}
    for report in reports.values():
        validate(report)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid halfword source evidence accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64), ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-program', ('program',), 'other-program'), ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('missing-generator-closure', ('generatorSources',), []), ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('constructor-return-overclaim', ('constructorReturnCredit',), 1), ('original-data-credit', ('originalDataSourceCredit',), 4),
        ('wrong-owned-returns', ('actualNativeAndCompiledReturns',), 1), ('mixed-initializer-returns', ('actualSeparateOriginalInitializerFillReturns',), 0),
        ('missing-native-symbols', ('nativeSymbols',), {}), ('missing-binding-identities', ('nativeSymbolEntries',), []),
        ('wrong-mode', ('matches', 0, 'mode'), 'thumb'), ('missing-include', ('matches', 0, 'sourceDependencies'), []),
        ('wrong-source', ('matches', 0, 'sourceSha256'), '0' * 64), ('absent-real-byte-match', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('wrong-native-address-width', ('matches', 0, 'sourceAbiContract', 'nativeAddressWordBytes'), 8),
        ('false-supported-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('removed-independent-memory-model', ('matches', 0, 'oracle', 'independentCompleteMappedMemoryAndOwnedStoreModel'), False))
    for namespace, report in reports.items():
        for name, keys, value in changes:
            changed = copy.deepcopy(report)
            target = changed
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = value
            reject(namespace + '-' + name, lambda changed=changed: validate(changed))
        first = report['matches'][0]
        product = (ROOT / first['realArm7Link']['cwd']) / 'caller.bin'
        saved = product.read_bytes()
        try:
            product.unlink()
            reject(namespace + '-missing-linked-product-after-cache', lambda report=report: validate(report))
            product.write_bytes(bytes([saved[0] ^ 1]) + saved[1:])
            reject(namespace + '-changed-linked-product-after-cache', lambda report=report: validate(report))
        finally:
            product.write_bytes(saved)
        trace = ROOT / first['oracle']['traceProduct']['path']
        saved = trace.read_bytes()
        try:
            trace.unlink()
            reject(namespace + '-missing-trace-after-cache', lambda report=report: validate(report))
            trace.write_bytes(bytes([saved[0] ^ 1]) + saved[1:])
            reject(namespace + '-changed-trace-after-cache', lambda report=report: validate(report))
        finally:
            trace.write_bytes(saved)
    rows = [row for report in reports.values() for row in report['matches']]
    for row in rows:
        matcher.linker.qualified_runtime_word(row, 0x0380fff4)
        for label, change in [('processor', dict(processor='arm9')), ('mode', dict(mode='thumb')), ('module', dict(module='arm7-wram')),
            ('address', dict(address=hex(int(row['address'], 0) + 4))), ('size', dict(bytes=row['bytes'] - 4)),
            ('qualification', dict(runtimePointerQualification={})), ('input-module', dict(inputModuleSha256='0' * 64))]:
            changed = dict(row, **change)
            reject(row['address'] + '-word-scope-' + label, lambda changed=changed: matcher.linker.qualified_runtime_word(changed, 0x0380fff4))
        reject(row['address'] + '-different-absolute-word', lambda row=row: matcher.linker.qualified_runtime_word(row, 0x0380fff0))
        reject(row['address'] + '-preserved-original-unknown-word-refusal', lambda row=row: original_linker.validate(row, matcher.WORK / 'controls' / row['module'] / row['address'] / 'base-refusal'))
    import crossreuse_utility_c
    from elftools.elf.elffile import ELFFile
    negative = []
    row=rows[0]
    for name,old,new in (
        ('wrong-first-node-id','0x188, 2U','0x188, 3U'),
        ('wrong-payload-advance',') + 0xC);',') + 0x8);'),
        ('wrong-last-halfword',', 0xA4)',', 0xA6)')):
        directory=matcher.WORK/'controls'/name;unit=directory/'src';shutil.copytree(matcher.SOURCE,unit,dirs_exist_ok=True)
        source=unit/Path(row['source']).name;text=source.read_text()
        if text.count(old)!=1:raise ValueError('Required unique node initializer negative token absent')
        source.write_text(text.replace(old,new),encoding='utf-8')
        dependencies=[dict(path=(unit/Path(p['path']).name).relative_to(ROOT).as_posix(),sha256=sha256(unit/Path(p['path']).name)) for p in row['sourceDependencies']]
        changed=dict(row,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=dependencies)
        attempt,compiled=crossreuse_utility_c.compile_origin(changed,ROOT/row['compiler'],row['compilerFlags'],directory)
        if compiled is None:raise ValueError('Wrong node C failed compilation: '+str(attempt))
        derived,masks,body=compiled
        if len(body)!=216:raise ValueError('Wrong node C did not retain216bytes')
        with (ROOT/derived['probeObject']).open('rb') as stream:
            elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==row['name']);section,offset=symbol['st_shndx'],symbol['st_value']
        entry=dict(changed,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
            relocations=[dict(r,format='SHT_RELA',explicitAddend=r['addend'],originalEncodedWord=body[r['offset']:r['offset']+4].hex()) for r in derived['relocations']])
        reject('real-compiler-link-rejects-'+name,lambda entry=entry,directory=directory:matcher.linker.validate(entry,directory/'wrong-real-link'))
        bad=(directory/'wrong-real-link/caller.bin').read_bytes()
        if len(bad)!=216 or matcher.fixture.native.digest(bad)==row['targetSha256']:raise ValueError('Node negative is not actual changed linked C')
        native=matcher.fixture.native;case=dict(offset=0x40,selector=1,allocated=True,context=0xffffffff,passes=1)
        machine=native.setup(bad,case,0)
        try:native.execute(machine)
        except ValueError as error:
            execution=machine.get('lastExecution',{})
            if not execution.get('actualReturn'):raise ValueError('Wrong node C must actually return before model rejection')
            controls.append(dict(name='actually-returning-wrong-C-model-rejects-'+name,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong returning node C passed independent model')
        negative.append(dict(name=name,program='',address=row['address'],executionBeforeModel=execution,sourceSha256=sha256(source),includeClosure=dependencies,
            objectSha256=derived['probeObjectSha256'],linkedSha256=native.digest(bad),sourceCredit=0))
    for report in reports.values():
        validate(report)
    output = ROOT / 'evidence/verification/arm7-lane-node-initialization216-controls-20261031.json'
    write_json(output, dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), programSelection=args.program,
        reports=[dict(path='evidence/matches/arm7-lane-node-initialization216-20261031.json', sha256=sha256(ROOT / 'evidence/matches/arm7-lane-node-initialization216-20261031.json')) for name in reports],
        positiveUnits=len(rows), matchedInitializedBytes=sum(r['bytes'] for r in rows), actualWrongCompiledSourceReturns=len(negative),
        negativeSourceProofs=negative, controls=controls, allPassed=all(r['rejected'] for r in controls)))
    print(dict(report=output.relative_to(ROOT).as_posix(), sha256=sha256(output), controls=len(controls), allPassed=True))


if __name__ == '__main__':
    main()
