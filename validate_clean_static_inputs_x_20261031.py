import os
import subprocess
import sys
from project import ROOT,read_json,write_json,sha256,now
from validate_clean_checkout import materialize,archive_previous_checks,current_checks


def main():
    target=ROOT.parent/'j2p-clean-20261031-x';path=ROOT/'evidence/verification/clean-batch-static-input-repair-x-20261031.json'
    result=dict(sourceCredit=0,createdUtc=now(),pid=os.getpid(),target=str(target),state='materializing-immutable-source',freshFullReplayProven=False,steps=[],generatorSha256=sha256(__file__))
    write_json(path,result)
    def run(arguments,label,timeout):
        log=target/f'logs/clean-static-input/{label}.txt';log.parent.mkdir(parents=True,exist_ok=True)
        with log.open('w',encoding='utf-8') as stream:process=subprocess.run([sys.executable,*[str(argument) for argument in arguments]],cwd=target.parent,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout)
        result['steps'].append(dict(command=[str(argument) for argument in arguments],exitCode=process.returncode,log=str(log),logSha256=sha256(log)));write_json(path,result)
        return process.returncode
    try:
        result['snapshot']=materialize(target);write_json(path,result)
        assert run([target/'configure.py'],'configure',900)==0
        assert run([target/'verify_oracle_static_inputs_20261031.py'],'static-input-preflight',900)==0
        assert run([target/'verify_batch_static_inputs_20261031.py'],'batch-input-preflight',900)==0
        expected='830288c663af1edf3a81c357df69da0e2f40668c377b39848611a182a95fd181'
        assert sha256(target/'nonmatching/arm7-bulk/20261030/seq-main-final01/native_arm7_wram_037fff54.c')==expected
        assert (target/'evidence/verification/ov000-buffer178-inputs-20261031.json').is_file()
        result['staticInputPreflightPassed']=True;result['batchInputPreflightPassed']=True;result['state']='running-full-immutable-suite'
        result['historicalChecks']=archive_previous_checks(target,target/'logs/clean-static-input');write_json(path,result)
        print(dict(state=result['state'],sourceRevision=result['snapshot']['sourceRevision'],staticInputPreflightPassed=True),flush=True)
        exit_code=run([target/'run_checks.py','--clean','--tools'],'checks',43200);checks=current_checks(target,exit_code)
        result['checksSummary']={key:checks.get(key) for key in ['allChecksPassed','buildAndOracleChecksPassed','sourceHashesCurrent','sourcePreferencesUnchanged']}
        result['freshFullReplayProven']=bool(checks['buildAndOracleChecksPassed']);assert result['freshFullReplayProven']
        result['state']='full-immutable-build-and-oracles-passed'
    except Exception as error:
        result['state']='failed';result['failure']=f'{type(error).__name__}: {error}';raise
    finally:write_json(path,result)


if __name__=='__main__':main()
