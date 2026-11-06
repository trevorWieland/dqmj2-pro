import gzip
import hashlib
import subprocess
from project import ROOT, read_json, write_json, sha256, now


def main():
    archive=ROOT/'evidence/attempts/cohort172-unaccepted-transaction-before-repair-20261106/manifest.json'
    frozen=read_json(archive)
    prior=read_json(ROOT/'evidence/verification/cohort-2026-10-29-171.json')
    plan=read_json(ROOT/'evidence/verification/cohort-2026-10-29-172.json')
    failed=read_json(ROOT/'evidence/verification/cohort172-validation-driver.json')
    assert frozen['registryNotChanged'] and frozen['pendingCohort']==172
    assert plan['linksPending'] and not prior['linksPending'] and failed['state']=='failed'
    assert failed['steps'][-1]['command']==['integrate_context_v3_20261106.py','--clean']
    assert failed['steps'][-1]['exitCode']==1
    assert sha256(ROOT/'recovery.json')==plan['sourceRegistrySha256']
    assert sha256(ROOT/'source-preferences.json')==prior['sourcePreferenceSha256']==plan['sourcePreferenceSha256']
    baseline=frozen['baselineRegistry']
    assert sha256(ROOT/baseline['path'])==baseline['archiveSha256']
    data=gzip.decompress((ROOT/baseline['path']).read_bytes())
    assert hashlib.sha256(data).hexdigest()==baseline['uncompressedSha256']==prior['sourceRegistrySha256']
    committed=subprocess.check_output(['git','show','0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb:recovery.json'],cwd=ROOT)
    assert data==committed
    original=(ROOT/'recovery.json').read_bytes()
    protected={p:sha256(ROOT/p)for p in ['source-preferences.json','cohort172-parallel-wave20261105-q-specification.json',
        'evidence/verification/cohort171-expanded-source-closure-20261101.json','ledger/functions.jsonl']}
    try:
        (ROOT/'recovery.json').write_bytes(data)
        from recovery_registry import verify_sources
        from ledger_state import collect_matches
        from project import configuration
        verify_sources()
        matches,rejected=collect_matches(configuration()['romSha256'])
        assert not rejected and len(matches)==prior['sourceMatchedFunctions']==11452
        assert protected=={p:sha256(ROOT/p)for p in protected}
    except BaseException:
        (ROOT/'recovery.json').write_bytes(original)
        raise
    result=dict(passed=True,sourceCredit=0,createdUtc=now(),failedUnacceptedCohort=172,
        acceptedCohort=171,exactCommittedBaselineRegistryRestored=True,
        originalPendingRegistryPreservedInLosslessArchive=True,oldPendingPlanRetainedUntilRepreparation=True,
        acceptedSourceHashesAnd11452IdentitiesVerified=True,sourcePreferencesAndLedgerUnchanged=True,
        noSourceObjectReadyOrGuardModified=True,archive=archive.relative_to(ROOT).as_posix(),
        archiveSha256=sha256(archive),restoredRegistrySha256=sha256(ROOT/'recovery.json'),
        generatorSha256=sha256(__file__))
    write_json(ROOT/'evidence/verification/cohort172-failed-registry-restored-to-closed171-v1-20261106.json',result)
    print(dict(passed=True,acceptedBaseline=171,functions=11452,sourceCredit=0))


if __name__=='__main__':
    main()
