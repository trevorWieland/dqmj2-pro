import copy
import hashlib
import json
from pathlib import Path
import match_main_predicate_constants_20261030 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
GENERATOR_SHA = 'fa912a9ea4f0a9e6c4057468e16006a21cb1bbd3d70a2961d9e04f24f9da3e3c'
PROFILE_SHA = 'af72f529ac05b3d7cb4b005b01e21401df3eff618c5f478c4595748a6e523651'
REPORT = ROOT / 'evidence/matches/main-predicate-constants-20261030.json'
_FRESH = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path(value):
    result = (ROOT / value).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError('Main constant proof path escapes repository')
    return result


def verify_file(name, sha):
    current = path(name)
    if not current.is_file() or digest(current.read_bytes()) != sha:
        raise ValueError('Current main constant input/product differs: ' + name)
    return current


def validate(report):
    if report.get('generator') != Path(matcher.__file__).name or report.get('generatorSha256') != GENERATOR_SHA:
        raise ValueError('Frozen main constant generator identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), PROFILE_SHA)
    profile = json.loads(matcher.PROFILE.read_text())
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), 'crossreuse_utility_c.py',
        'link_runtime_unit.py', 'elf_units.py', 'match_runtime.py', 'match_lowlevel.py', 'project.py'}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete main constant generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    if digest((ROOT / 'inputs/game.nds').read_bytes()) != matcher.ROM or report.get('romSha256') != matcher.ROM:
        raise ValueError('Original ROM provenance differs')
    if report.get('processor') != 'arm9' or report.get('program') != '' or report.get('module') != 'main':
        raise ValueError('Qualified main constant namespace differs')
    if report.get('matchedInitializedBytes') != 16 or report.get('actualNativeAndCompiledReturns') != 512:
        raise ValueError('Measured main constant totals differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Main constant scope was overstated')
    if report.get('ordinaryAssemblyOrBlobCredit') != 0 or report.get('newImplementationFamilyNovelty') != 0:
        raise ValueError('Main constant novelty/scaffolding claim differs')
    if report.get('nativeSymbols') != {} or report.get('nativeSymbolEntries') != []:
        raise ValueError('Pure main constant source acquired native anchors')
    rows = report.get('matches', [])
    if len(rows) != 2 or [row['address'] for row in rows] != [pin['address'] for pin in profile['matches']]:
        raise ValueError('Qualified main constant units differ')
    for pin, row in zip(profile['matches'], rows):
        for key, value in pin.items():
            if row.get(key) != value:
                raise ValueError('Frozen main constant source/profile differs: ' + key)
        verify_file(pin['source'], pin['sourceSha256'])
        verify_file(pin['compiler'], pin['compilerSha256'])
        verify_file(row['object'], row['objectSha256'])
        proof = row['realMainLink']
        verify_file(proof['linkedElf'], proof['linkedElfSha256'])
        verify_file(proof['lcf'], proof['lcfSha256'])
        verify_file(proof['linkerAttempt']['command'][0], proof['linkerSha256'])
        binary = path(str(Path(proof['linkerAttempt']['cwd']) / 'caller.bin'))
        if not binary.is_file() or digest(binary.read_bytes()) != pin['targetSha256']:
            raise ValueError('Current freshly linked constant body is absent/different')
    key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if key not in _FRESH:
        _FRESH[key] = [matcher.build(pin) for pin in profile['matches']]
    if rows != _FRESH[key]:
        raise ValueError('Published main constants differ from full source-only link/native replay')
    return {('arm9', '', 'main', row['address'], row['mode']): row for row in rows}


def main():
    report = json.loads(REPORT.read_text())
    accepted = validate(report)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid constant proof accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-namespace', ('processor',), 'arm7'),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('new-family-overclaim', ('newImplementationFamilyNovelty',), 2),
        ('source-closure-missing', ('generatorSources',), []),
        ('wrong-total', ('matchedInitializedBytes',), 20),
        ('wrong-constant', ('matches', 0, 'constant'), 13),
        ('wrong-mode', ('matches', 0, 'mode'), 'thumb'),
        ('wrong-source-hash', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-boundaries', ('matches', 0, 'boundaries', 'configuredWholeBodyBytes'), 4),
        ('no-actual-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('exhaustion-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('changed-native-state', ('matches', 0, 'oracle', 'records', 0, 'stateSha256'), '0' * 64),
        ('wrong-linker-hash', ('matches', 0, 'realMainLink', 'linkerSha256'), '0' * 64),
    )
    for name, keys, value in changes:
        changed, current = copy.deepcopy(report), None
        current = changed
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    first = report['matches'][0]
    artifact = path(str(Path(first['realMainLink']['linkerAttempt']['cwd']) / 'caller.bin'))
    saved = artifact.read_bytes()
    try:
        artifact.unlink()
        reject('missing-current-linked-product-after-positive-cache', lambda: validate(report))
        artifact.write_bytes(bytes([saved[0] ^ 1]) + saved[1:])
        reject('changed-current-linked-product-after-positive-cache', lambda: validate(report))
    finally:
        artifact.write_bytes(saved)
    modified = bytearray(saved)
    modified[0] ^= 1
    reject('native-model-rejects-wrong-constant', lambda: matcher.native(first, bytes(modified), 0, 15))
    modified = bytearray(saved)
    modified[2] ^= 0x10
    reject('native-model-rejects-uncontracted-flag-write', lambda: matcher.native(first, bytes(modified), 0, 15))
    metadata, raw, config = matcher.link_runtime_unit.measured_module('main')
    pc, target = 0x02001000, int(first['address'], 0) + 4
    modified = bytearray(raw)
    modified[pc - 0x02000000:pc - 0x02000000 + 4] = (0xEA000000 | ((target - pc - 8) >> 2 & 0xFFFFFF)).to_bytes(4, 'little')
    reject('boundary-audit-rejects-outside-interior-branch', lambda: matcher.main_references(first, bytes(modified),
        'probe kind:function(arm,size=0x4) addr:0x02001000'))
    modified = bytearray(raw)
    modified[0:4] = target.to_bytes(4, 'little')
    reject('boundary-audit-rejects-interior-pointer', lambda: matcher.main_references(first, bytes(modified), ''))
    pin = copy.deepcopy(json.loads(matcher.PROFILE.read_text())['matches'][0])
    source = matcher.WORK / 'controls/wrong-constant.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('unsigned int ' + pin['name'] + '(void) { return 13; }\n')
    pin.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
    reject('real-mw-link-rejects-compiled-wrong-c', lambda: matcher.build(pin))
    matcher.build(json.loads(matcher.PROFILE.read_text())['matches'][0])
    if len(validate(report)) != 2:
        raise ValueError('Positive proof unavailable after controls')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'positiveMatchedBytes': 16, 'actualNativeAndCompiledReturns': 512,
        'controls': controls, 'allPassed': all(row['rejected'] for row in controls), 'wholeModuleClaim': False}
    destination = ROOT / 'evidence/verification/main-predicate-constants-controls-20261030.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
