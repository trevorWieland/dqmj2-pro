import copy
import json
import subprocess
import sys
from project import ROOT, read_json, sha256, write_json
import reproduce_arm7_host_irq_gap208_witness_20261101 as frozen


def main():
    wrapper = ROOT / 'reproduce_arm7_host_irq_gap208_witness_20261101.py'
    manifest_path = ROOT / 'provenance/arm7-host-irq-gap208-witness-handoff-20261101.json'
    manifest = read_json(manifest_path)
    assert sha256(manifest_path) == '21e60aa84eb697700bea2461035a92e6b89f4272ba3189627a094b718451b1f3'
    assert sha256(wrapper) == '2927f63a88e55431f9923807d27d2bd135fac34c09ca526e9283e1f1cfa961ad'
    for path, expected in frozen.PINS.items():
        assert sha256(ROOT / path) == expected, path
    for row in manifest['requiredExistingFiles']:
        assert sha256(ROOT / row['path']) == row['sha256'], row['path']
    logs = ROOT / 'logs/integration/irq-witness-path-transport-20261101'
    logs.mkdir(parents=True, exist_ok=True)
    for script in frozen.SCRIPTS:
        run = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT.parent,
                             capture_output=True, text=True, timeout=300)
        (logs / (script + '.stdout.txt')).write_text(run.stdout, encoding='utf-8')
        (logs / (script + '.stderr.txt')).write_text(run.stderr, encoding='utf-8')
        assert run.returncode == 0, (script, run.stderr[-1200:])
    products = []
    for path, original_hash in frozen.PRODUCTS.items():
        archive = ROOT / 'provenance/handoffs/arm7-host-irq-gap208-witness-20261101' / path.replace('/', '__')
        assert sha256(archive) == original_hash
        original, current = read_json(archive), read_json(ROOT / path)
        restored = copy.deepcopy(current)
        differences = []
        if path == 'evidence/verification/arm7-host-irq-gap208-scope-controls-20261101.json':
            before = original['negativeControls'][40]['error']
            after = current['negativeControls'][40]['error']
            lane = ROOT.parent / 'j2p-recovery-lanes/arm7'
            assert before.endswith("absent-native-records.json.gz'")
            assert after == before.replace(str(lane).replace('\\', '\\\\'), str(ROOT).replace('\\', '\\\\'))
            restored['negativeControls'][40]['error'] = before
            differences = ['negativeControls[40].error: checkout-specific missing-record path only']
        assert restored == original, path
        products.append(dict(path=path, currentSha256=sha256(ROOT / path),
                             archivedOriginalSha256=original_hash, allowedDiagnosticDifferences=differences))
    report = dict(generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
                  frozenWrapperSha256=sha256(wrapper), manifestSha256=sha256(manifest_path),
                  products=products, negativeControls=71, frozenValidatorsUnchanged=True,
                  sourceAdmissionAdapterGranted=False, sourceCredit=0, dataCredit=0,
                  initializedDenominatorDelta=0, passed=True)
    write_json(ROOT / 'evidence/verification/irq-witness-path-transport-20261101.json', report)
    print(json.dumps(dict(passed=True, negativeControls=71, products=len(products), sourceCredit=0)))


if __name__ == '__main__':
    main()
