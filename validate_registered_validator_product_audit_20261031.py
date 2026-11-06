import contextlib
import io
import json
from pathlib import Path
import uuid
import audit_registered_validator_products_20261031 as scanner

ROOT = Path(__file__).resolve().parent


def main():
    directory = ROOT / 'work/validation-repair-20261031' / ('audit-controls-' + uuid.uuid4().hex)
    directory.mkdir(parents=True)
    fixture = directory / 'repository'
    (fixture / 'evidence').mkdir(parents=True)
    source = fixture / 'validate_fixture.py'
    source.write_text("from pathlib import Path\nROOT = Path(__file__).resolve().parent\nREPORT = ROOT / 'evidence/input.json'\ndef validate(row):\n    verify_file(row['object'], row['objectSha256'])\n")
    (fixture / 'producer.py').write_text('pass\n')
    input_report = fixture / 'evidence/input.json'
    input_report.write_text(json.dumps({'generator': 'producer.py', 'matches': [{'object': 'work/fresh/unit.o'}]}))
    registry = {'batches': [], 'oracles': [{'report': 'evidence/control.json', 'reproduce': ['validate_fixture.py']}]}
    controls = []

    def require(name, condition):
        if not condition:
            raise ValueError('Audit control failed: ' + name)
        controls.append({'name': name, 'passed': True})

    require('relative-work-object-recognized', scanner.work_product('work/fresh/unit.o') == 'work/fresh/unit.o')
    require('absolute-windows-work-object-normalized', scanner.work_product('C:\\checkout\\work\\fresh\\unit.o') == 'work/fresh/unit.o')
    require('native-input-is-not-cache', scanner.work_product('extract/arm7/runtime/arm7-wram.bin') is None)
    require('ordinary-C-is-not-generated-object', scanner.work_product('work/fresh/unit.c') is None)

    def run(name):
        (fixture / 'recovery.json').write_text(json.dumps(registry))
        output = directory / (name + '.json')
        with contextlib.redirect_stdout(io.StringIO()):
            scanner.audit(fixture, fixture, output)
        return json.loads(output.read_text())['oracles'][0]

    row = run('missing-unregistered')
    require('missing-unregistered-producer-flagged', row['status'] == 'requires-producer-order-review'
        and row['missingColdWorkProducts'] == ['work/fresh/unit.o'] and row['producersNotDirectlyRegistered'] == ['producer.py'])
    registry['batches'] = [{'report': 'evidence/input.json', 'reproduce': ['producer.py']}]
    row = run('registered-producer')
    require('registered-producer-does-not-prove-order', row['status'] == 'missing-products-with-registered-producer-or-indirect-regeneration')
    product = fixture / 'work/fresh/unit.o'
    product.parent.mkdir(parents=True)
    product.write_bytes(b'synthetic object-presence marker; never compiled or executed')
    row = run('present-product')
    require('present-current-product-not-missing', row['status'] == 'no-missing-products-found' and row['missingColdWorkProducts'] == [])
    input_report.write_bytes(b' ' * (8 * 1024 * 1024 + 1))
    row = run('oversize-withheld')
    require('oversize-input-explicitly-withheld', row['status'] == 'large-reports-require-targeted-review'
        and row['largeReportsWithheld'] == [{'path': 'evidence/input.json', 'bytes': 8 * 1024 * 1024 + 1}])
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': scanner.digest(Path(__file__)),
        'auditor': Path(scanner.__file__).name, 'auditorSha256': scanner.digest(Path(scanner.__file__)),
        'fixtureDirectory': directory.relative_to(ROOT).as_posix(), 'syntheticOnly': True,
        'coldCheckoutOrRegistryEdits': False, 'sourceAcceptanceCredit': 0, 'controls': controls, 'allPassed': True}
    destination = ROOT / 'evidence/verification/registered-validator-product-audit-controls-20261031.json'
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': scanner.digest(destination), 'controls': len(controls), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
