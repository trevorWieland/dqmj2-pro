import argparse
import os
import sys
from pathlib import Path
from project import ROOT,now,write_json,read_json
from validate_clean_checkout import materialize,run,archive_previous_checks,current_checks


def main():
    parser=argparse.ArgumentParser();parser.add_argument('target',type=Path);args=parser.parse_args();target=args.target.resolve()
    path=ROOT/'evidence/verification/clean-oracle-repair-u-20261031.json'
    result={'sourceCredit':0,'createdUtc':now(),'pid':os.getpid(),'target':str(target),'state':'materializing','steps':[],'sourceReconstructionComplete':False,'freshFullReplayProven':False}
    write_json(path,result)
    try:
        result['snapshot']=materialize(target);result['state']='configuring';write_json(path,result)
        logs=target/'logs/clean-oracle-repair';logs.mkdir(parents=True)
        row=run([sys.executable,str(target/'configure.py')],target.parent,logs/'configure.txt',900);result['steps'].append(row);assert row['exitCode']==0
        result['historicalChecks']=archive_previous_checks(target,logs)
        result['state']='replaying-previously-missing-oracle';write_json(path,result);print({'state':result['state']},flush=True)
        row=run([sys.executable,str(target/'prove_ov001_scalar_special_near_20261030.py')],target.parent,logs/'previously-missing-oracle.txt',900);result['steps'].append(row);assert row['exitCode']==0
        result['previouslyMissingOraclePassed']=True;result['state']='running-full-immutable-suite';write_json(path,result);print({'state':result['state'],'previouslyMissingOraclePassed':True},flush=True)
        row=run([sys.executable,str(target/'run_checks.py'),'--clean','--tools'],target.parent,logs/'full-suite.txt',43200);result['steps'].append(row)
        checks=current_checks(target,row['exitCode']);result['checksSummary']={k:checks.get(k) for k in ['allChecksPassed','buildAndOracleChecksPassed','sourceHashesCurrent','sourcePreferencesUnchanged']}
        result['state']='finished';result['freshFullReplayProven']=checks['buildAndOracleChecksPassed'];write_json(path,result)
        assert result['freshFullReplayProven']
    except Exception as error:
        result['state']='failed';result['failure']=f'{type(error).__name__}: {error}';write_json(path,result);raise


if __name__=='__main__':
    main()
