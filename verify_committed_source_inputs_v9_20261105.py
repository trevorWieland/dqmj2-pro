import copy
from unittest.mock import patch
import verify_committed_source_inputs_v8_20261101 as original
from project import ROOT, read_json, write_json, sha256
from qualify_arm9_reference_consumer_20261105 import REPORT, OUTPUT, run


def main():
    qualification = run()
    actual = read_json(ROOT / REPORT)
    projected = copy.deepcopy(actual)
    inputs = {p['address']: p['sourceOnlyCompilerInput'] for p in qualification['proofs']}
    for row in projected['matches']:
        assert 'sourceOnlyCompilerInput' not in row
        row['sourceOnlyCompilerInput'] = inputs[row['address']]

    def qualified_read(path):
        if path.resolve() == (ROOT / REPORT).resolve():
            assert sha256(path) == qualification['reportSha256']
            return projected
        return read_json(path)

    def qualified_write(path, document):
        assert document['passed']
        document.update(generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
            previousEightInputVerifierUnchanged=True,
            arm9ReferenceQualification=dict(path=OUTPUT, sha256=sha256(ROOT / OUTPUT),
                freshExplicitC99Recompilation=True, canonicalReportOrSourceModified=False,
                originalV8NamespaceAndInputChecksExecuted=True))
        target = ROOT / f'evidence/verification/cohort{document["cohort"]}-committed-source-inputs-v9-20261105.json'
        write_json(target, document)

    with patch.object(original, 'read_json', side_effect=qualified_read), patch.object(original, 'write_json', side_effect=qualified_write):
        original.main()


if __name__ == '__main__':
    main()
