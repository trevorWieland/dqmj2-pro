import copy
import json
from pathlib import Path
import prove_arm7_tick_callback104_scope_20261031 as producer
from project import write_json

ROOT = Path(__file__).resolve().parent
PRODUCER_SHA = '84ce7c62e4a0cae8a59ba759a4a1e2def64744209209730a78f6b66026f3d99c'
REPORT = ROOT / 'evidence/arm7/tick-callback104-boundary-20261031.json'
_FRESH = None


def validate(report):
    global _FRESH
    producer.verify_inputs()
    if producer.digest(Path(producer.__file__).read_bytes()) != PRODUCER_SHA or producer.digest(producer.MODULE.read_bytes()) != producer.MODULE_SHA:
        raise ValueError('Frozen callback characterization/module changed')
    if producer.digest((ROOT / producer.SOURCE).read_bytes()) != producer.SOURCE_SHA:
        raise ValueError('Frozen unaccepted hypothesis changed')
    row = report['unacceptedC']
    path = ROOT / row['object']
    if not path.is_file() or producer.digest(path.read_bytes()) != row['objectSha256']:
        raise ValueError('Current unaccepted compiled object is missing or changed')
    if _FRESH is None:
        _FRESH = producer.build_report()
    if json.loads(json.dumps(_FRESH)) != report:
        raise ValueError('Fresh boundary/launcher/tail/real-return/strict-refusal evidence differs')
    return report['scope']


def main():
    producer.main()
    report = json.loads(REPORT.read_text())
    validate(report)
    controls = []
    changes = [('processor', ('scope', 'processor'), 'arm9'), ('program', ('scope', 'program'), 'utility'),
        ('module', ('scope', 'module'), 'arm7-main'), ('mode', ('scope', 'mode'), 'thumb'),
        ('entry', ('scope', 'address'), '0x37fd1b8'), ('extent', ('scope', 'bytes'), 88),
        ('pool-as-code', ('scope', 'codeRange'), ['0x37fd1b4', '0x37fd21c']),
        ('tail-target', ('scope', 'tailDestination'), '0x37fb8a4'),
        ('interior-hidden', ('scope', 'outsideInteriorReferences'), [{'target': '0x37fd1b8'}]),
        ('canonical-claim', ('scope', 'canonicalEntryCurrentlyPresent'), True),
        ('denominator-added', ('denominatorIncrease',), 104), ('source-added', ('sourceCredit',), 104),
        ('assembly-provenance', ('originalAssemblyProvenanceCredit',), 104),
        ('callback-returns-inflated', ('actualCallbackReturns',), 108),
        ('initializer-as-callback', ('separateActualInitializerReturns',), 0),
        ('provider-added', ('providersReplaced',), ['timer']),
        ('linker-guard-relaxed', ('linkerUnknownEntryGuardsChanged',), True),
        ('genuine-link-invented', ('unacceptedC', 'genuineLinkSucceeded'), True),
        ('source-credit-from-prefix', ('unacceptedC', 'sourceCredit'), 32),
        ('budget-as-return', ('boundedExhaustionControl', 'actualReturn'), True)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        try:
            validate(changed)
        except ValueError as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Invalid callback scope/return evidence accepted: ' + name)
    path = ROOT / report['unacceptedC']['object']
    saved = path.read_bytes()
    try:
        path.unlink()
        try:
            validate(report)
        except ValueError as error:
            controls.append({'name': 'missing-current-object-after-cache', 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Missing current hypothesis object accepted')
    finally:
        path.write_bytes(saved)
    validate(report)
    output = ROOT / 'evidence/verification/tick-callback104-boundary-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': producer.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': producer.digest(REPORT.read_bytes()),
        'controls': controls, 'allPassed': all(row['rejected'] for row in controls), 'sourceCredit': 0,
        'sharedInventoryOrLinkerChanged': False, 'producerBeforeValidator': True}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': producer.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
