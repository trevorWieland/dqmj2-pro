import copy
import hashlib
import json
from pathlib import Path
import match_arm7_bulk_20261030_reuse01 as matcher
import link_arm7_bulk_20261030 as linker
from elftools.elf.elffile import ELFFile

ROOT, WORK = matcher.ROOT, matcher.WORK
REPORT = ROOT / 'evidence/matches/arm7-bulk-20261030-reuse01.json'
REPORT_SHA = '5390df68d1a03a4818479d7896c496b22beeec4bbb4248458fcaeebb6e4dee1c'
PIN_SHA = '4543fc97d959d5326ddfc00ae267c5b8a6f0339fe490cfa66348bfc13fd3e1e0'
MATCHER_SHA = '55212b4f1e7c4030fa2ed7ccc4ed771fd6162350b8abc4979d22079f4810efbb'
PUBLISHER_SHA = 'fc7644ad43143db28672f8f03d522d67ed878b3bd604db169e07a897717340d6'
NATIVE_CACHE = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_document(report):
    if report.get('romSha256') != matcher.ROM or digest((ROOT / 'inputs/game.nds').read_bytes()) != matcher.ROM:
        raise ValueError('ROM scope changed')
    if digest(matcher.PROFILE.read_bytes()) != matcher.PROFILE_SHA or digest(matcher.PIN_FILE.read_bytes()) != PIN_SHA:
        raise ValueError('Frozen source/tool closure changed')
    if digest(Path(matcher.__file__).read_bytes()) != MATCHER_SHA:
        raise ValueError('Frozen source-only matching backend changed')
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report['pinnedGeneratorAndRuntimeDependencies'] != pins:
        raise ValueError('Reported runtime/generator closure omitted or changed a pin')
    if report.get('processor') != 'arm7' or report.get('program') != matcher.utility_runtime.PROGRAM:
        raise ValueError('Reported processor/program scope changed')
    source_names = {Path(matcher.__file__).name, Path(matcher.fixture.__file__).name, Path(linker.__file__).name,
        matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()}
    if report['generator'] == 'publish_arm7_bulk_20261030_reuse01.py':
        source_names.add(report['generator'])
        if report['generatorSha256'] != PUBLISHER_SHA or digest((ROOT / report['generator']).read_bytes()) != PUBLISHER_SHA:
            raise ValueError('Frozen canonical report producer changed')
        if report.get('oracleGenerator') != Path(matcher.__file__).name or report.get('oracleGeneratorSha256') != MATCHER_SHA or not report.get('canonicalReportRegeneratedFromFreshSource'):
            raise ValueError('Canonical publication lost fresh matching generator provenance')
    elif report['generator'] != Path(matcher.__file__).name:
        raise ValueError('Unknown source-only report producer')
    if {row['path'] for row in report['generatorSources']} != source_names:
        raise ValueError('Producer source closure differs')
    for row in report['generatorSources'] + report['pinnedGeneratorAndRuntimeDependencies']:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Frozen generator/dependency unavailable or changed')
    expected = {row['address']: row for row in json.loads(matcher.PROFILE.read_text())['matches']}
    rows = report['matches']
    if len(rows) != 7 or len({row['address'] for row in rows}) != 7 or sum(row['bytes'] for row in rows) != 252:
        raise ValueError('Qualified function count/extent changed')
    layout, files = matcher.utility_runtime.derive()
    records = []
    for row in rows:
        pin = expected[row['address']]
        for key in ('program', 'processor', 'module', 'address', 'mode', 'bytes', 'name', 'base', 'binary', 'source', 'sourceSha256', 'compiler', 'compilerSha256', 'compilerFlags', 'targetSha256', 'inputModuleSha256'):
            if row[key] != pin[key]:
                raise ValueError('Source instance profile differs: ' + key)
        for path_key, hash_key in (('source', 'sourceSha256'), ('object', 'objectSha256'), ('compiler', 'compilerSha256')):
            if digest((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise ValueError('Current source/object/compiler unavailable or changed')
        directory = Path(row['realArm7Link']['cwd']).resolve()
        directory.relative_to(WORK.resolve())
        linked, lcf = directory / 'caller.bin', ROOT / row['realArm7Link']['lcf']
        if digest(linked.read_bytes()) != row['targetSha256'] or digest(lcf.read_bytes()) != row['realArm7Link']['lcfSha256']:
            raise ValueError('Current genuine linked product unavailable or changed')
        for name, hash_key in (('caller.o', 'splitObjectSha256'), ('linked.elf', 'linkedElfSha256')):
            if digest((directory / name).read_bytes()) != row['realArm7Link'][hash_key]:
                raise ValueError('Current real link/object product unavailable or changed')
        address = int(row['address'], 0)
        native = (ROOT / row['binary']).read_bytes()[address - row['base']:address - row['base'] + row['bytes']]
        if linked.read_bytes() != native:
            raise ValueError('Current native initialized body differs')
        if matcher.boundary(row, layout, files) != row['boundaries']:
            raise ValueError('Current boundary qualification differs')
        oracle = row['oracle']
        profiles = matcher.fixture.profiles(address)
        if oracle['vectors'] != len(profiles) or oracle['actualOriginalAndRecompiledReturns'] != 2 * len(profiles):
            raise ValueError('Actual return count differs from supported profiles')
        if [entry['profile'] for entry in oracle['records']] != profiles or any(entry['actualOriginalAndRecompiledReturns'] != 2 or not entry['modelPassed'] for entry in oracle['records']):
            raise ValueError('Independent complete native profile evidence differs')
        if not oracle['verifiedReturn'] or not oracle['allFullStateAndOrderedWritesEqual'] or not oracle['independentFieldModelPassed'] or oracle['unvisitedInstructionAddresses']:
            raise ValueError('Supported return/model/instruction evidence incomplete')
        if oracle['negativeControls']['countExhausted']['actualReturn'] or oracle['negativeControls']['invalidPointer']['actualReturn'] or oracle['malformedAndExhaustedReturnCredit'] != 0:
            raise ValueError('Unsupported execution received return credit')
        if row['relocations'] or row['realArm7Link']['zeroCodeAnchors'] or not row['realArm7Link']['exactLinkedBytes']:
            raise ValueError('Frozen no-callee source closure changed')
        cache_key = (row['targetSha256'], row['sourceSha256'], row['mode'], address, PIN_SHA)
        if cache_key not in NATIVE_CACHE:
            NATIVE_CACHE[cache_key] = dict(matcher.fixture.verify(address, native, linked.read_bytes(), row['mode']), supported=True, verifiedReturn=True)
        if oracle != NATIVE_CACHE[cache_key]:
            raise ValueError('Current independently rerun native/source model/effect evidence differs')
        records.append({'program': row['program'], 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'], 'address': row['address'],
            'bytes': row['bytes'], 'source': row['source'], 'sourceSha256': row['sourceSha256'], 'actualReturns': oracle['actualOriginalAndRecompiledReturns']})
    if report['matchedInitializedBytes'] != 252 or report['matchedFunctionInstances'] != 7 or report['actualOriginalAndRecompiledReturns'] != 1120:
        raise ValueError('Measured aggregate differs from seven qualified complete units')
    return records


def validate():
    return validate_document(json.loads(REPORT.read_text()))


def controls():
    report = json.loads(REPORT.read_text())
    validate()
    entry = report['matches'][0]
    directory = WORK / 'reuse01-link-controls'
    directory.mkdir(parents=True, exist_ok=True)
    results = []
    def reject(name, action):
        try:
            action()
        except Exception as error:
            results.append({'name': name, 'rejected': True, 'failure': type(error).__name__ + ': ' + str(error)})
        else:
            raise ValueError('Negative control was incorrectly accepted: ' + name)
    changes = [('processor', 'arm9'), ('program', 'wrong-child.srl'), ('module', 'arm7-wram'), ('mode', 'thumb'),
        ('address', hex(int(entry['address'], 0) + 4)), ('bytes', entry['bytes'] - 4), ('targetSha256', '0' * 64),
        ('inputModuleSha256', '0' * 64), ('sourceSha256', '0' * 64), ('objectSha256', '0' * 64), ('object', 'work/arm7-bulk-20261030/missing.o')]
    for index, (key, value) in enumerate(changes):
        changed = dict(entry, **{key: value})
        reject('link-' + key, lambda changed=changed, index=index: linker.validate(changed, directory / str(index)))
    obj = ROOT / entry['object']
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == entry['name'])
        offset = elf.get_section(symbol['st_shndx'])['sh_offset'] + (symbol['st_value'] & ~1)
    corrupted = bytearray(obj.read_bytes())
    corrupted[offset] ^= 4
    mutant = directory / 'negative-only-mutated-object.o'
    mutant.write_bytes(corrupted)
    changed = dict(entry, object=mutant.relative_to(ROOT).as_posix(), objectSha256=digest(corrupted))
    reject('correctly-rehashed-object-code-change', lambda: linker.validate(changed, directory / 'actual-byte-gate'))
    source = directory / 'negative-only-mutated-source.c'
    source.write_text((ROOT / entry['source']).read_text().replace('return (u32) temp_r2;', 'return 0;'))
    changed = dict(entry, source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
    layout, files = matcher.utility_runtime.derive()
    reject('fresh-compiled-source-return-change', lambda: matcher.build(changed, directory / 'source-byte-gate', layout, files))
    for name, mutate in [('claimed-return-count', lambda row: row['oracle'].update(actualOriginalAndRecompiledReturns=999)),
        ('exhaustion-return-credit', lambda row: row['oracle']['negativeControls']['countExhausted'].update(actualReturn=True)),
        ('missing-linked-product', lambda row: row['realArm7Link'].update(cwd=str(directory / 'empty-products'))),
        ('linked-product-path-escape', lambda row: row['realArm7Link'].update(cwd=str(ROOT.parent))),
        ('native-profile-omission', lambda row: row['oracle']['records'].pop()),
        ('fabricated-native-state-hash', lambda row: row['oracle']['records'][0].update(stateSha256='0' * 64)),
        ('invented-source-unit', lambda row: row.update(address='0x037fc998'))]:
        changed_report = copy.deepcopy(report)
        mutate(changed_report['matches'][0])
        reject(name, lambda changed_report=changed_report: validate_document(changed_report))
    for name, mutate in [('omitted-generator-pin', lambda value: value['pinnedGeneratorAndRuntimeDependencies'].pop()),
        ('false-canonical-generation', lambda value: value.update(canonicalReportRegeneratedFromFreshSource=False))]:
        changed_report = copy.deepcopy(report)
        mutate(changed_report)
        reject(name, lambda changed_report=changed_report: validate_document(changed_report))
    output = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'reportSha256': digest(REPORT.read_bytes()),
        'prePublicationReportSha256': REPORT_SHA,
        'positiveQualifiedUnits': 7, 'positiveInitializedBytes': 252, 'negativeControls': results, 'allRejected': True,
        'linkerScope': 'ARM7 no-extern leaf source units; external-call interworking is not established by this batch', 'sourceCreditAddedByControls': 0}
    path = ROOT / 'evidence/verification/arm7-bulk-reuse01-controls-20261030.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'controls': len(results), 'allRejected': True, 'output': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())}), flush=True)


if __name__ == '__main__':
    controls()
