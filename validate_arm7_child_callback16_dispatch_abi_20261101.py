import copy
import json
from pathlib import Path
import prove_arm7_child_callback16_dispatch_abi_20261101 as producer
from project import ROOT, write_json

INPUTS = ROOT / 'provenance/arm7-child-callback16-dispatch-abi-inputs-20261101.json'
INPUT_SHA = '7aa4d39546c2bf49e966bff3a65ee139b90954b9d26e11b22875f6d0110b19b0'
CONTROL = ROOT / 'evidence/verification/arm7-child-callback16-dispatch-abi-controls-20261101.json'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
_FRESH = None


def verify_inputs():
    if producer.engine.digest(INPUTS.read_bytes()) != INPUT_SHA:
        raise ValueError('Read-only dispatcher ABI witness closure changed')
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
        raise ValueError('Fresh qualified native dispatcher ABI evidence differs')
    return {'sourceCredit':0,'scope':report['boundary']['range'],'assemblyExceptionJustified':False}


def publish(path, report):
    if path.resolve() != CONTROL.resolve() or path.resolve() == producer.REPORT.resolve():
        raise ValueError('Dispatcher ABI controls escaped own publication namespace')
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
            raise ValueError('Invalid dispatcher ABI evidence accepted: ' + name)
    changes = [('program', ('boundary','program'), ''), ('processor', ('boundary','processor'), 'arm9'),
        ('module', ('boundary','module'), 'arm7-wram'), ('scope-bytes', ('boundary','bytes'), 264),
        ('code-bytes', ('boundary','instructionBytes'), 260), ('pool-code-credit', ('boundary','poolBytes'), 0),
        ('entry-mode', ('boundary','entries',0,'mode'), 'thumb'), ('entry-hash', ('boundary','entries',0,'sha256'), '0'*64),
        ('stub-target', ('boundary','entries',0,'literals',0,'word'), '0x37fbb88'),
        ('vector', ('boundary','originalVectorWords',4), 0x037FD900),
        ('index-mapping', ('boundary','originalIndexTableU16',5), 0),
        ('scope-adopted', ('boundary','scopeAdopted'), True), ('shared-config', ('boundary','sharedInventoryOrConfigurationChanged'), True),
        ('consumed-R0', ('callbackR0ConsumedAfterReturn',), True), ('assembly-exception', ('assemblyExceptionJustified',), True),
        ('original-assembly', ('originalAssemblyAuthorshipProven',), True), ('physical-IRQ', ('physicalIrqExceptionEntryValidated',), True),
        ('source-credit', ('sourceCredit',), 16), ('denominator', ('dataOrDenominatorCredit',), 260),
        ('return-count', ('actualTableSelectedTimerStubReturns',), 55), ('callback-count', ('actualOriginalCallback16ReturnsSeparate',), 28),
        ('native-arg', ('nativeRecords',0,'originalThunk','events',0,'r0'), 1),
        ('synthetic-mislabeled', ('nativeRecords',0,'syntheticOriginalHandlerPointer','syntheticDirectHandlerPointer'), False),
        ('dead-stack-equality', ('nativeRecords',0,'deadStackMemoryComparedAsEqual'), True),
        ('providers', ('providerReplacements',), ['BIOS']), ('patches', ('nativeInstructionPatches',), True),
        ('cap-credit', ('unsupportedReturnCredit',), 1)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    reject('read-only-body-substitution', lambda: producer.engine.setup({0x037FD900:bytes(16)},0))
    def strict_old_scope():
        import arm7_child_alarm_engine_20261031 as old
        machine=old.setup({},0)
        execution=machine['invoke'](0x037FBB24,[],100)
        if not execution['actualReturn'] and 'escaped known original instruction scope' in (execution['error'] or ''):
            raise ValueError('Unchanged original known-code guard refuses the proposed timer stub')
    reject('unchanged-original-code-scope',strict_old_scope)
    reject('prior-host244-destination', lambda: publish(ROOT / 'evidence/verification/arm7-host-irq244-controls-20261101.json', {}))
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': producer.engine.digest(Path(__file__).read_bytes()),
        'report': producer.REPORT.relative_to(ROOT).as_posix(), 'reportSha256': producer.engine.digest(producer.REPORT.read_bytes()),
        'romSha256': ROM, 'sourceCredit': 0, 'dataOrDenominatorCredit': 0, 'actualTableSelectedTimerStubReturns': report['actualTableSelectedTimerStubReturns'],
        'controls': controls, 'allPassed': all(item['rejected'] for item in controls), 'originalUnknownDataGuardPreserved': True,
        'producerBeforeChecks': True, 'handlerSourceInputsRequired': False,'assemblyExceptionJustified':False}
    publish(CONTROL, result)
    print(json.dumps({'report': CONTROL.relative_to(ROOT).as_posix(), 'sha256': producer.engine.digest(CONTROL.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed'], 'sourceCredit': 0}))


if __name__ == '__main__':
    main()
