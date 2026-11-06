import copy
import subprocess
from pathlib import Path
from unittest.mock import patch
import verify_committed_source_inputs_v8_20261101 as original
from project import ROOT, read_json, write_json, sha256
from qualify_arm9_reference_packets_v2_20261105 import LEDGER, qualify_report


def main():
    ledger = read_json(ROOT / LEDGER)
    assert subprocess.check_output(['git', 'show', 'HEAD:' + LEDGER], cwd=ROOT) == (ROOT / LEDGER).read_bytes()
    projected, qualifications = {}, []
    for consumer in ledger['consumers']:
        if not consumer.get('sourceOnlyCompilerInputQualification'):
            continue
        proof = qualify_report(consumer['report'], consumer['expectedRanges'],
            ROOT / 'work/integration/source-input-v11' / str(len(qualifications)))
        assert proof['producerSha256'] == consumer['producerSha256'] == sha256(ROOT / consumer['producer'])
        report = copy.deepcopy(read_json(ROOT / consumer['report']))
        inputs = {p['address']: p['sourceOnlyCompilerInput'] for p in proof['proofs']}
        for row in report['matches']:
            assert 'sourceOnlyCompilerInput' not in row
            row['sourceOnlyCompilerInput'] = inputs[row['address']]
        projected[(ROOT / consumer['report']).resolve()] = report
        qualifications.append(proof)

    def qualified_read(path):
        path = Path(path).resolve()
        return projected[path] if path in projected else read_json(path)

    def qualified_write(path, document):
        document.update(generator=Path(__file__).name, generatorSha256=sha256(__file__),
            previousEightInputVerifierUnchanged=True, freshCompilerInputQualifications=qualifications,
            sourceRegistrySourcesObjectsFlagsAndCanonicalReportsUnchanged=True)
        target = ROOT / f'evidence/verification/cohort{document["cohort"]}-committed-source-inputs-v11-20261105.json'
        write_json(target, document)

    with patch.object(original, 'read_json', side_effect=qualified_read), patch.object(original, 'write_json', side_effect=qualified_write):
        original.main()


if __name__ == '__main__':
    main()
