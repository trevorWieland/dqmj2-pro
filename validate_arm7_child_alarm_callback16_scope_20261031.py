import copy
import json
from pathlib import Path
import prove_arm7_child_alarm_callback16_scope_20261031 as prover
from project import ROOT, write_json

PROVER_SHA = '6815caa9775db5d64202552a45a16232dded40ad50b4bd9aa2c13c50d378c2cc'
_FRESH = None
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261031').replace('_', '-') + '-controls-20261031.json')


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or prover.digest(path.read_bytes()) != expected:
        raise ValueError('Current native-scope input/product changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(prover.__file__).name, PROVER_SHA)
    pins = prover.verify_inputs()
    names = {Path(prover.__file__).name, prover.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if len(report['generatorSources']) != len(names) or {row['path'] for row in report['generatorSources']} != names:
        raise ValueError('Complete frozen scope generator/input closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != PROVER_SHA or report['generator'] != Path(prover.__file__).name or report['pinnedInputs'] != pins or report['romSha256'] != prover.ROM_SHA:
        raise ValueError('Original-build scope generator identity differs')
    native = report['native']['record']
    checked(native['path'], native['sha256'])
    candidate = report['ordinaryCHypothesis']['entry']
    checked(candidate['object'], candidate['objectSha256'])
    checked(candidate['source'], candidate['sourceSha256'])
    checked(candidate['compiler'], candidate['compilerSha256'])
    checked(Path(prover.linker.__file__).name, report['baseLinkerSha256'])
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(prover.proof()))
    if report != _FRESH:
        raise ValueError('Fresh loader/entry/mode/frame/native-return/unknown-guard proof differs')
    return {'qualifiedBoundary': report['boundary'], 'newFunctionOrSourceCredit': 0, 'sharedScopeAdopted': False}


def publish(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == prover.REPORT.resolve():
        raise ValueError('Boundary-control publication escaped this validator namespace')
    write_json(path, report)


def main():
    prover.main()
    report = json.loads(prover.REPORT.read_text())
    validate(report)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except Exception as failure:
            controls.append({'name': name, 'rejected': True, 'exception': type(failure).__name__, 'reason': str(failure)})
        else:
            raise ValueError('Invalid callback scope/credit/guard evidence accepted: ' + name)

    mutations = [('rom', ('romSha256',), '0' * 64), ('generator', ('generatorSha256',), '0' * 64),
        ('closure', ('generatorSources',), []), ('inputs', ('pinnedInputs',), []),
        ('wrong-processor', ('boundary', 'identity', 'processor'), 'arm9'),
        ('wrong-program', ('boundary', 'identity', 'program'), ''), ('wrong-module', ('boundary', 'identity', 'module'), 'arm7-wram'),
        ('wrong-mode', ('boundary', 'identity', 'mode'), 'thumb'), ('interior-entry', ('boundary', 'identity', 'address'), '0x37fd904'),
        ('wrong-extent', ('boundary', 'bytes'), 20), ('wrong-code', ('boundary', 'codeSha256'), '0' * 64),
        ('code-as-pool', ('boundary', 'literalBytes'), 16), ('padding-credit', ('boundary', 'alignmentBytes'), 16),
        ('frame-width', ('boundary', 'frameBytes'), 4), ('wrong-preserved-register', ('boundary', 'measuredExtraPreservedWord'), 'R1'),
        ('unproved-original-assembly', ('boundary', 'originalAssemblyProvenanceVerified'), True),
        ('source-credit', ('boundary', 'ordinarySourceCredit'), 16), ('adoption-claim', ('scopeAdopted',), True),
        ('denominator-double-add', ('initializedDenominatorDelta',), 16), ('source-count', ('newAcceptedFunctionOrByteCredit',), 1),
        ('producer-return-inflation', ('native', 'actualOriginalProgrammerReturnsSeparate'), 32),
        ('callback-return-inflation', ('native', 'actualOriginalCallbackReturns'), 32),
        ('legacy-guard-bypass', ('native', 'originalScopeRefusal', 'actualReturn'), True),
        ('thumb-guard-bypass', ('native', 'wrongModeRefusal', 'actualReturn'), True),
        ('cap-credit', ('native', 'oneInstructionCap', 'actualReturn'), True),
        ('nonmatching-C-as-linked', ('ordinaryCHypothesis', 'actualGenuineMwldMatch'), True),
        ('unlinked-C-credit', ('ordinaryCHypothesis', 'sourceOrByteCredit'), 156)]
    for name, keys, value in mutations:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    for name, path in [('missing-native-records', ROOT / report['native']['record']['path']),
        ('missing-current-candidate-object', ROOT / report['ordinaryCHypothesis']['entry']['object'])]:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    reject('measurement-engine-cannot-install-code', lambda: prover.proposed_engine.setup({0x037FD900: bytes(16)}, 1))
    reject('prior324-publication', lambda: publish(ROOT / 'evidence/verification/arm7-child-tick324-controls-20261031.json', {}))
    validate(report)
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': prover.digest(Path(__file__).read_bytes()),
        'report': prover.REPORT.relative_to(ROOT).as_posix(), 'reportSha256': prover.digest(prover.REPORT.read_bytes()),
        'controls': controls, 'allPassed': all(row['rejected'] for row in controls), 'sourceOrByteCredit': 0,
        'initializedDenominatorDelta': 0, 'sharedConfigOrLinkerChanged': False, 'producerBeforeProductChecks': True}
    publish(CONTROL_REPORT, result)
    print(json.dumps({'report': CONTROL_REPORT.relative_to(ROOT).as_posix(), 'sha256': prover.digest(CONTROL_REPORT.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
