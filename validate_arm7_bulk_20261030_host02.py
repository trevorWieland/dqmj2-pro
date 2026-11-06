import copy
import hashlib
import json
from pathlib import Path
import match_arm7_bulk_20261030_host02 as backend
from elftools.elf.elffile import ELFFile

ROOT, WORK = backend.ROOT, backend.WORK
REPORT = ROOT / 'evidence/matches/arm7-bulk-20261030-host02.json'
CACHE = {}
BACKEND_SHA = 'b7f9abb9e28bae81b247a6274659854743e9fca95bd476add688635878b33051'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_document(report):
    if digest(Path(backend.__file__).read_bytes()) != BACKEND_SHA or report['generator'] != Path(backend.__file__).name or report['generatorSha256'] != BACKEND_SHA:
        raise ValueError('Frozen source-only host reconstruction backend changed')
    expected_sources = {Path(backend.__file__).name, Path(backend.fixture.__file__).name, Path(backend.linker.__file__).name,
        backend.PROFILE.relative_to(ROOT).as_posix(), backend.PIN_FILE.relative_to(ROOT).as_posix()}
    if {row['path'] for row in report['generatorSources']} != expected_sources:
        raise ValueError('Host producer source closure is incomplete')
    if digest(backend.PROFILE.read_bytes()) != backend.PROFILE_SHA or digest(backend.PIN_FILE.read_bytes()) != backend.PIN_SHA:
        raise ValueError('Frozen host source/compiler/runtime profile changed')
    pins = json.loads(backend.PIN_FILE.read_text())['files']
    if pins != report['pinnedGeneratorAndRuntimeDependencies']:
        raise ValueError('Reported pinned closure changed')
    for pin in pins + report['generatorSources']:
        if digest((ROOT / pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('Host generator or runtime dependency unavailable/changed')
    if report['romSha256'] != backend.ROM or digest((ROOT / 'inputs/game.nds').read_bytes()) != backend.ROM or report['program'] != '' or report['processor'] != 'arm7':
        raise ValueError('Native host program/ROM scope changed')
    profile = {row['address']: row for row in json.loads(backend.PROFILE.read_text())['matches']}
    if len(report['matches']) != 2 or {row['address'] for row in report['matches']} != set(profile):
        raise ValueError('Two complete host units are not independently present')
    layout = backend.arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    for row in report['matches']:
        for key, value in profile[row['address']].items():
            if row[key] != value:
                raise ValueError('Qualified source/input profile changed: ' + key)
        for name, sha in (('source', 'sourceSha256'), ('object', 'objectSha256'), ('compiler', 'compilerSha256')):
            if digest((ROOT / row[name]).read_bytes()) != row[sha]:
                raise ValueError('Current C/object/compiler unavailable/changed')
        directory = Path(row['realArm7Link']['cwd']).resolve()
        directory.relative_to(WORK.resolve())
        for name, sha in (('caller.bin', 'targetSha256'), ('caller.o', 'splitObjectSha256'), ('linked.elf', 'linkedElfSha256')):
            expected = row['targetSha256'] if name == 'caller.bin' else row['realArm7Link'][sha]
            if digest((directory / name).read_bytes()) != expected:
                raise ValueError('Current source-linked product unavailable/changed')
        if digest((ROOT / row['realArm7Link']['lcf']).read_bytes()) != row['realArm7Link']['lcfSha256']:
            raise ValueError('Real linker control file changed')
        if row['boundaries'] != backend.boundaries(row, layout):
            raise ValueError('Root/code/literal ownership changed')
        address = int(row['address'], 0)
        raw = (ROOT / row['binary']).read_bytes()
        native = raw[address - row['base']:address - row['base'] + row['bytes']]
        linked = (directory / 'caller.bin').read_bytes()
        if native != linked:
            raise ValueError('Current whole initialized source unit differs')
        key = row['sourceSha256'], row['targetSha256'], backend.PIN_SHA
        if key not in CACHE:
            CACHE[key] = backend.fixture.verify(row, native, linked, row['codeBytes'])
        if row['oracle'] != CACHE[key]:
            raise ValueError('Full native/source effects or supported/unsupported return evidence differs')
    if report['matchedInitializedBytes'] != 204 or report['matchedInstructionBytes'] != 192 or report['generatedLiteralBytes'] != 12 or report['actualOriginalAndRecompiledReturns'] != 2384:
        raise ValueError('Measured code/data/actual-return aggregate differs')
    if 'producer' not in CACHE:
        CACHE['producer'] = backend.fixture.producer()
    producer = report['originalNativeProducer']
    for key, value in CACHE['producer'].items():
        if producer[key] != value:
            raise ValueError('Actual original high-byte producer evidence changed')
    module = next(row for row in layout['modules'] if row['id'] == 'arm7-wram')
    raw = (ROOT / module['binary']).read_bytes()
    base = int(module['base'], 0)
    if producer['inputModuleSha256'] != module['sha256'] or producer['callerBytes'] != 80 or producer['callerSha256'] != digest(raw[0x037FFE14 - base:0x037FFE64 - base]):
        raise ValueError('Qualified original producer body differs')
    view = report['originalInitializedDataDependencies']
    if len(view) != 1 or view[0]['address'] != '0x3806fa9' or view[0]['bytes'] != 160 or view[0]['logicalCenterAddress'] != '0x3807028' or view[0]['logicalCenterOffset'] != 127 or view[0]['recoveredDataSourceCredit'] != 0:
        raise ValueError('Measured original memory view was changed or given source credit')
    if view[0]['inputModuleSha256'] != module['sha256'] or view[0]['sha256'] != digest(raw[0x03806FA9 - base:0x03806FA9 - base + 160]):
        raise ValueError('Original preserved data dependency differs')
    return {'functions': 2, 'initializedBytes': 204, 'instructionBytes': 192, 'literalBytes': 12, 'actualNativeAndSourceReturns': 2384,
        'nativeProducerBoundaryStops': 256, 'actualEarlyProducerReturns': 6, 'boundaryStopWholeCallerReturnCredit': 0}


def main():
    report = json.loads(REPORT.read_text())
    summary = validate_document(report)
    directory = ROOT / 'work/arm7-bulk-20261030/host02-controls'
    directory.mkdir(parents=True, exist_ok=True)
    results = []
    def reject(name, action):
        try:
            action()
        except Exception as error:
            results.append({'name': name, 'rejected': True, 'failure': type(error).__name__ + ': ' + str(error)})
        else:
            raise ValueError('Host negative control was accepted: ' + name)
    table = next(row for row in report['matches'] if row['address'] == '0x37fee58')
    for index, (key, value) in enumerate((('program', 'dwc/utility.bin/move/child.srl'), ('processor', 'arm9'), ('mode', 'thumb'),
        ('bytes', 104), ('targetSha256', '0' * 64), ('sourceSha256', '0' * 64), ('objectSha256', '0' * 64), ('address', '0x037fee5c'))):
        changed = dict(table, **{key: value})
        reject('qualified-link-' + key, lambda changed=changed, index=index: backend.linker.validate(changed, directory / str(index)))
    changed = copy.deepcopy(table)
    changed['relocations'][0]['explicitAddend'] += 1
    reject('wrong-centered-data-relocation-addend', lambda: backend.linker.validate(changed, directory / 'wrong-addend'))
    for name, old, new in (('unsigned-byte-return', '(s8)', '(u8)'), ('wrong-logical-center', '+ 127)', '+ 128)')):
        source = directory / (name + '.c')
        source.write_text((ROOT / table['source']).read_text().replace(old, new))
        changed = dict(table, source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
        layout = backend.arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
        reject('fresh-source-' + name, lambda changed=changed, name=name: backend.build(changed, directory / name, layout))
    mutations = [('fabricated-native-state', lambda value: value['matches'][0]['oracle']['records'][0].update(stateSha256='0' * 64)),
        ('boundary-stop-counted-return', lambda value: value['originalNativeProducer'].update(boundaryStopOuterReturnCredit=256)),
        ('invented-producer-value', lambda value: value['originalNativeProducer']['capturedArgument0Values'].append(256)),
        ('data-scaffolding-source-credit', lambda value: value['originalInitializedDataDependencies'][0].update(recoveredDataSourceCredit=160)),
        ('missing-current-product', lambda value: value['matches'][0]['realArm7Link'].update(cwd=str(directory / 'missing'))),
        ('inflated-complete-returns', lambda value: value.update(actualOriginalAndRecompiledReturns=2640)),
        ('omitted-matching-generator', lambda value: value['generatorSources'].pop()),
        ('forged-matching-generator-hash', lambda value: value.update(generatorSha256='0' * 64)),
        ('omitted-runtime-pin', lambda value: value['pinnedGeneratorAndRuntimeDependencies'].pop()),
        ('busy-exhaustion-return-credit', lambda value: value['matches'][0]['oracle']['unsupportedControls']['busyNeverCleared'].update(actualReturn=True))]
    for name, mutate in mutations:
        changed = copy.deepcopy(report)
        mutate(changed)
        reject(name, lambda changed=changed: validate_document(changed))
    output = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'reportSha256': digest(REPORT.read_bytes()),
        'positive': summary, 'negativeControls': results, 'allRejected': True, 'newSourceCreditFromControls': 0}
    path = ROOT / 'evidence/verification/arm7-bulk-host02-controls-20261030.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'controls': len(results), 'allRejected': True, 'sha256': digest(path.read_bytes()), **summary}), flush=True)


if __name__ == '__main__':
    main()
