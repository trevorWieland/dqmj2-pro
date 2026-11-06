import subprocess
import sys
from project import ROOT,read_json,sha256
import stage_declared_source_package_v5_20261101 as staging


if __name__=='__main__':
    sys.argv=[sys.argv[0],'cohort132-joint-scale-element-package-v3-20261102.json']
    staging.main()
    registry={p for batch in read_json(ROOT/'recovery.json')['batches']for p in batch['sourceHashes']}
    closure=read_json(ROOT/'evidence/verification/cohort132-captured-oracle-closure-20261031.json')['sourceAndEvidenceHashes']
    deferred=read_json(ROOT/'evidence/verification/cohort132-unregistered-research-script-deferral-20261102.json')['files']
    assert len(deferred)==2
    for row in deferred:
        assert row['path']not in registry and row['path']not in closure
        assert sha256(ROOT/row['path'])==row['sha256']
    subprocess.run(['git','restore','--staged','--',*[r['path']for r in deferred]],cwd=ROOT,check=True)
