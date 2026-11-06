import argparse
from project import ROOT,read_json,write_json,sha256,now
from freeze_source_selection_snapshot_20261106 import validate,OUTPUT as PROTOTYPE


LANE=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next'
OUTPUT=LANE/'production-wrapper-handoff.json'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();validate();proof=read_json(LANE/'production-wrapper-qualification.json')
    if not proof['passed'] or proof['sourceCredit'] or not proof['actualOriginalMainCalledUnmodifiedAtFullScope'] or proof['astProjectionUsed'] or not proof['allActualInputsTrackedIncludingPrototypePrivateRoots']:raise ValueError('Production wrapper qualification differs')
    if proof['originalControls']!=269 or len(proof['restorationControls'])!=5 or not all(c['passed'] for c in proof['restorationControls']):raise ValueError('Production wrapper control scope differs')
    if sha256(ROOT/proof['wrapperPath'])!=proof['wrapperSha256'] or sha256(ROOT/'verify_source_selection_v2_wrapper_20261106.py')!=proof['generatorSha256']:raise ValueError('Qualified wrapper or controls changed')
    if args.verify:
        result=read_json(OUTPUT)
        for row in result['files']:
            if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen wrapper handoff input changed: '+row['path'])
    else:
        if OUTPUT.exists():raise ValueError('Wrapper handoff already frozen; use --verify')
        names=['verify_source_selection_v2_20261106.py','verify_source_selection_v2_wrapper_20261106.py','freeze_source_selection_wrapper_20261106.py',PROTOTYPE.relative_to(ROOT).as_posix(),(LANE/'production-wrapper-qualification.json').relative_to(ROOT).as_posix(),(LANE/'wrapper-first-live-epoch-rejection.json').relative_to(ROOT).as_posix()]
        names+=list(proof['implementationPins'])+['verify_source_selection_snapshot_guards_20261106.py']
        write_json(OUTPUT,dict(passed=True,sourceCredit=0,frozenUtc=now(),files=[dict(path=n,sha256=sha256(ROOT/n)) for n in dict.fromkeys(names)],originalEntry='verify_source_selection.main',productionCli=['python','verify_source_selection_v2_20261106.py'],privateRequalificationCli=['python','verify_source_selection_v2_wrapper_20261106.py'],allOriginal269ControlsPassed=True,additionalEpochControls=10,additionalWrapperControls=5,fullReportSha256=proof['fullReportByteIdenticalSha256'],wrapperFullCurrent164EpochSeconds=proof['elapsedSecondsIncludingConstructionAndFinalGuards'],productionAdopted=False,coordinatorSteps=['Review and stage frozen runtime helpers plus qualification receipts.','Select the new CLI only for a future validation stage; leave current jobs and original scripts unchanged.','Run through the usual shared pipeline and require successful process status plus its original canonical report.'],limits=['The35.2572percent paired prototype gain was measured on a prior immutable input epoch. The163.3908second new-wrapper run includes full guards but has no paired baseline on its newer164epoch; no new speed ratio is claimed.','The archived rejected attempt is diagnostic provenance only; it contains historical source/log text, not current runtime dependencies.','The new CLI executes the original full main body with original canonical output paths. Private qualification redirects only its two output roots.']))
    print(dict(passed=True,path=OUTPUT.relative_to(ROOT).as_posix(),sha256=sha256(OUTPUT)))


if __name__=='__main__':main()
