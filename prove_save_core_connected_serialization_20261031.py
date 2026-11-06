import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import verify_inputs,sha,file_identity
CASE_DIGEST='d3059a46a2c68b8c8389d3141b4539c74622891eb0bb3c10760363c6ea5fe2d1'
REPORT='evidence/functional/save-core-connected-serialization-20261031.json'
CONTROL='evidence/functional/save-core-connected-serialization-controls-20261031.json'
SCRIPTS=['evidence/application/save_core_persistence_fixtures_20261031.py','evidence/application/save_core_persistence_controls_20261031.py']


def main():
    verify_inputs()
    for script in SCRIPTS:
        process=subprocess.run([sys.executable,str(ROOT/script)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    evidence=json.loads((ROOT/REPORT).read_text());controls=json.loads((ROOT/CONTROL).read_text())
    assert evidence['nativeCaseDigest']==CASE_DIGEST
    assert evidence['counts']['actualHostReturns']==164 and evidence['counts']['sourceCreditAdded']==0
    assert evidence['counts']['contexts']==63 and evidence['counts']['nativeDeserializeContexts']==4 and evidence['counts']['nativeBankValidationContexts']==15
    assert controls['counts']['independentRejections']==2 and controls['counts']['positiveControls']==2
    assert controls['counts']['nativeWriterReturns']==4 and controls['counts']['wrongSummaryWriterReturns']==4
    for row in evidence['sourceReuse']:
        assert row['exactByteEqual'] and row['reusedAcceptedSource'] and row['newCoverageBytes']==0
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        proof=row['realLinkSnapshot']
        assert sha((ROOT/proof['isolatedCallerBinary']).read_bytes())==row['targetSha256']
        validation=json.loads((ROOT/proof['isolatedCallerLinkValidation']).read_text())
        assert validation['exactCallerBytes'] is True and validation['linkerAttempt']['exitCode']==0
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==row['sourceSha256']
    dependencies=[entry['path'] for entry in evidence['runtimeDependencies']]+[REPORT,CONTROL,*SCRIPTS,
        'evidence/application/save_core_persistence_units_20261031.py','evidence/application/save_core_persistence_machine_20261031.py',
        'evidence/application/save_core_persistence_model_20261031.py','prove_save_core_connected_serialization_20261031.py',
        evidence['primaryIdentitySnapshot']['path'],*[row['source'] for row in controls['wholeSourceRealLinks']]]
    assert sha((ROOT/evidence['primaryIdentitySnapshot']['path']).read_bytes())==evidence['primaryIdentitySnapshot']['sha256']
    verify_inputs()
    receipt=dict(schemaVersion=1,sourceCreditAdded=0,matchedFunctionCreditAdded=0,independentContextPairs=82,
        actualHostReturns=164,negativeControlReturns=8,nativeCaseDigest=CASE_DIGEST,
        reports=[file_identity(REPORT),file_identity(CONTROL)],
        replayDependencies=[file_identity(path) for path in sorted(set(dependencies))],replayRequires=[],
        sourceReuseUnits=len(evidence['sourceReuse']),inputIntegrityVerified=True,
        limitations=evidence['limitations'])
    target=ROOT/'evidence/functional/save-core-connected-serialization-replay-20261031.json'
    target.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(dict(sourceCreditAdded=0,contextPairs=82,actualReturns=164,negativeControlReturns=8,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
