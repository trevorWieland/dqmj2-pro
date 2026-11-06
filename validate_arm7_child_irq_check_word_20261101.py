import copy
import json
from pathlib import Path
import prove_arm7_child_irq_check_word_20261101 as producer
from project import ROOT, write_json

INPUTS = ROOT / 'provenance/arm7-child-irq-check-word-oracle-inputs-20261101.json'
INPUT_SHA = 'e1a72439d00312b6301622093d4ee5078ad7395940c4b71a443052f207a815ab'
CONTROL = ROOT / 'evidence/verification/arm7-child-irq-check-word-controls-20261101.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
_FRESH = None


def verify_inputs():
    if producer.engine.digest(INPUTS.read_bytes()) != INPUT_SHA:
        raise ValueError('Read-only runtime-word witness closure changed')
    for item in json.loads(INPUTS.read_text())['files']:
        path = (ROOT / item['path']).resolve()
        if not path.is_relative_to(ROOT) or producer.engine.digest(path.read_bytes()) != item['sha256']:
            raise ValueError('Current native/reference/runtime witness input differs: ' + item['path'])
    if producer.engine.digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Measured ROM changed')


def validate(report):
    global _FRESH
    verify_inputs()
    if _FRESH is None:
        _FRESH = {'schemaVersion': 1, 'generator': Path(producer.__file__).name,
            'generatorSha256': producer.engine.digest(Path(producer.__file__).read_bytes()), **producer.proof()}
    if report != _FRESH:
        raise ValueError('Fresh qualified native runtime-word evidence differs')
    return {'program': report['program'], 'processor': report['processor'], 'mode': 'data',
        'address': report['address'], 'width': report['width'], 'sourceCredit': 0}


def publish(path, report):
    if path.resolve() != CONTROL.resolve() or path.resolve() == producer.REPORT.resolve():
        raise ValueError('Runtime-word controls escaped own publication namespace')
    write_json(path, report)


def main():
    verify_inputs()
    producer.main()
    report = json.loads(producer.REPORT.read_text())
    validate(report)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid runtime-word evidence accepted: ' + name)
    changes = [('program', ('program',), ''), ('processor', ('processor',), 'arm9'),
        ('neighbor', ('address',), '0x380fff4'), ('width', ('width',), 8), ('instruction-mode', ('mode',), 'arm'),
        ('classification', ('classification',), 'initialized-data'), ('source', ('sourceCredit',), 4),
        ('extent-credit', ('sourceDataExtentCredit',), 4), ('denominator', ('initializedDenominatorDelta',), 4),
        ('ownership', ('moduleStorageOwnership',), ['utility-child-arm7-wram']), ('module', ('inputModuleSha256',), '0' * 64),
        ('primary-pin', ('primaryReference', 'commit'), '0' * 40), ('current-references', ('originalReferences', 'references'), []),
        ('invented-consumer', ('originalReferences', 'separateOriginalClearOrWaitConsumerProven'), True),
        ('unknown-data-guard-lost', ('unchangedDataGuardRefusal',), 'accepted'),
        ('native-count', ('actualOriginalReturns',), 11), ('native-return', ('originalReturnRecords', 0, 'actualReturn'), False),
        ('native-word-effect', ('originalReturnRecords', 0, 'expectedOrderedWrites', 1, 2), 0),
        ('providers', ('providerReplacements',), ['BIOS']), ('cap-credit', ('unsupportedReturnCredit',), 1)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    reject('prior-callback76-destination', lambda: publish(ROOT / 'evidence/verification/arm7-child-timer-callback76-controls-20261101.json', {}))
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': producer.engine.digest(Path(__file__).read_bytes()),
        'report': producer.REPORT.relative_to(ROOT).as_posix(), 'reportSha256': producer.engine.digest(producer.REPORT.read_bytes()),
        'romSha256': ROM, 'sourceCredit': 0, 'dataOrDenominatorCredit': 0, 'actualOriginalReturns': report['actualOriginalReturns'],
        'controls': controls, 'allPassed': all(item['rejected'] for item in controls), 'originalUnknownDataGuardPreserved': True,
        'producerBeforeChecks': True, 'handlerSourceInputsRequired': False}
    publish(CONTROL, result)
    print(json.dumps({'report': CONTROL.relative_to(ROOT).as_posix(), 'sha256': producer.engine.digest(CONTROL.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed'], 'sourceCredit': 0}))


if __name__ == '__main__':
    main()
