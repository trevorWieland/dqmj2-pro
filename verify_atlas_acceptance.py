from export_reconstruction_atlas import accepted_manifest
from project import ROOT, write_json


def main():
    receipt = dict(linksPending=False, acceptedBuildCreatedUtc='2026-11-02', sourceMatchedFunctions=2,
        expectedSourceMatchedFunctions=2, sourceLinkedBytes=16, expectedSourceLinkedBytes=16, moduleComparisonsExact=20)
    closure = dict(passed=True)
    manifest = dict(functionMatched=2, sourceLinkedBytes=16)
    controls = []

    def check(name, current, sealed, mapped, reject=False):
        values = {'README.md': 'Latest accepted source cohort 147: fixture',
            'evidence/verification/cohort-2026-10-29-147.json': current,
            'evidence/verification/cohort147-expanded-source-closure-20261101.json': sealed,
            'manifest.json': mapped}
        try:
            result = accepted_manifest(lambda path, **options: values[path])
        except ValueError:
            if not reject:
                raise
            controls.append(dict(name=name, rejected=True))
            return
        if reject:
            raise AssertionError('Unaccepted source entered atlas: ' + name)
        assert result == (147, manifest)
        controls.append(dict(name=name, passed=True))

    check('finalized-cohort-and-closure', receipt, closure, manifest)
    value = dict(receipt, linksPending=True)
    check('prepared-transaction', value, closure, manifest, True)
    check('failed-committed-closure', receipt, dict(passed=False), manifest, True)
    check('missing-accepted-build', dict(receipt, acceptedBuildCreatedUtc=None), closure, manifest, True)
    check('missing-module-comparison', dict(receipt, moduleComparisonsExact=19), closure, manifest, True)
    check('count-mismatched-manifest', receipt, closure, dict(manifest, functionMatched=3), True)
    check('byte-mismatched-manifest', receipt, closure, dict(manifest, sourceLinkedBytes=20), True)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/atlas-acceptance-controls.json',
        dict(passed=True, sourceCredit=0, controls=controls, liveSourcesAndLedgersChanged=False))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
