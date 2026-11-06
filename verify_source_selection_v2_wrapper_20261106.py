import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,now
import verify_source_selection_v2_20261106 as wrapper
import verify_source_selection as original
import source_selection as selection
import ledger_state
import source_dependencies
from probe_source_selection_snapshot_20261106 import WORK,LANE,EpochChanged
from guard_source_selection_snapshot_20261106 import GuardedSnapshot
from verify_source_selection_snapshot_guards_20261106 import FixtureTracker,make


class OutputRoot:
    def __init__(self,private):self.private=private;self.redirected=[]
    def __fspath__(self):return str(ROOT)
    def __truediv__(self,name):
        if name in ['work/source-selection-negatives','evidence/verification/source-selection-negatives-20261030.json']:
            self.redirected.append(name);return self.private/name
        return ROOT/name


def bindings():return (selection.preferences,original.batches,ledger_state.read_json,ledger_state.sha256,source_dependencies.sha256)


def restoration(base):
    outputs=[]
    path=base/'actual-input-under-prototype-work.txt';path.write_bytes(b'actual input');tracker=wrapper.InputTracker();tracker.hash(path);path.write_bytes(b'changed data')
    try:tracker.verify()
    except EpochChanged as error:outputs.append(dict(case='actual-input-under-prototype-private-root-is-tracked',passed=True,reason=str(error)))
    else:raise ValueError('Production tracker excluded an actual private-root input')
    def fail():raise RuntimeError('Owned injected original-main failure')
    for name,entry,expected in [('success-return',lambda:17,17),('original-main-exception',fail,None)]:
        before=bindings()
        with patch.object(original,'main',entry):
            if expected is not None:
                if wrapper.main()!=expected:raise ValueError('Original return status was not preserved')
            else:
                try:wrapper.main()
                except RuntimeError as error:
                    if str(error)!='Owned injected original-main failure':raise
                else:raise ValueError('Original-main failure was suppressed')
        if bindings()!=before:raise ValueError('Delegated globals were not restored: '+name)
        outputs.append(dict(case=name,passed=True,scope='Wrapper plumbing with explicitly injected entry; full original body is tested separately'))
    before=bindings();bad=dict(wrapper.PINS);bad['verify_source_selection.py']='0'*64
    with patch.object(wrapper,'PINS',bad):
        try:wrapper.main()
        except ValueError as error:
            if 'implementation changed' not in str(error):raise
        else:raise ValueError('Wrong implementation pin accepted')
    if bindings()!=before:raise ValueError('Pin-rejection globals changed')
    outputs.append(dict(case='wrong-code-pin-rejected-before-entry',passed=True))
    fixture=base/'final-guard';namespace,row,audit=make(fixture)
    def factory(rom,tracker):return GuardedSnapshot(rom,FixtureTracker(),fixture/'source-preferences.json',fixture/'recovery.json')
    def mutate():write_json(fixture/'recovery.json',dict(batches=[dict(report='owned-changed-registry')]))
    before=bindings()
    with patch.object(selection,'ROOT',fixture),patch.object(wrapper,'GuardedSnapshot',factory),patch.object(original,'main',mutate):
        try:wrapper.main()
        except EpochChanged as error:outputs.append(dict(case='real-private-registry-final-guard-failure-propagates',passed=True,reason=str(error)))
        else:raise ValueError('Wrapper accepted a changed registry after entry')
    if bindings()!=before:raise ValueError('Final guard failure did not restore globals')
    return outputs


def execute():
    if WORK!=ROOT/'work/w6ps' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next':raise ValueError('Wrapper qualification paths differ')
    base=WORK/('wrapper-'+uuid.uuid4().hex[:12]);base.mkdir(parents=True);started=now();before=bindings();output=OutputRoot(base);wrapperSha=sha256(ROOT/'verify_source_selection_v2_20261106.py');mainIdentity=original.main;registryBefore=sha256(ROOT/'recovery.json');policyBefore=sha256(selection.POLICY)
    begin=time.perf_counter()
    with patch.object(original,'ROOT',output):result=wrapper.main()
    elapsed=time.perf_counter()-begin
    if sha256(ROOT/'recovery.json')!=registryBefore or sha256(selection.POLICY)!=policyBefore:raise EpochChanged('Wrapper qualification outer registry/policy epoch differs')
    if result is not None or original.main is not mainIdentity or bindings()!=before:raise ValueError('Full original entry/status/globals changed')
    path=base/'evidence/verification/source-selection-negatives-20261030.json';report=read_json(path);full=read_json(LANE/'full-real-selection-equivalence.json')
    if not report['passed'] or len(report['controls'])!=269 or sha256(path)!=full['samples'][0]['privateOutputSha256']:raise ValueError('True original-main wrapper report differs from full original comparison')
    if output.redirected!=['work/source-selection-negatives','evidence/verification/source-selection-negatives-20261030.json']:raise ValueError('Private qualification redirected non-output paths')
    controls=restoration(base)
    if sha256(ROOT/'verify_source_selection_v2_20261106.py')!=wrapperSha:raise ValueError('Wrapper changed during qualification')
    receipt=dict(passed=True,sourceCredit=0,startedUtc=started,finishedUtc=now(),wrapperPath='verify_source_selection_v2_20261106.py',wrapperSha256=wrapperSha,generatorSha256=sha256(__file__),privateRoot=base.relative_to(ROOT).as_posix(),registrySha256=registryBefore,policySha256=policyBefore,actualOriginalMainCalledUnmodifiedAtFullScope=True,astProjectionUsed=False,onlyPrivateOutputRootRouting=output.redirected,originalControls=269,fullReportByteIdenticalSha256=sha256(path),elapsedSecondsIncludingConstructionAndFinalGuards=elapsed,allActualInputsTrackedIncludingPrototypePrivateRoots=True,restorationControls=controls,fullInputEpochReceipt=dict(path=(LANE/'full-real-selection-equivalence.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'full-real-selection-equivalence.json')),guardControlReceipt=dict(path=(LANE/'snapshot-guard-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'snapshot-guard-controls.json')),implementationPins=wrapper.PINS,productionAdopted=False,canonicalReportAndSharedJobsAndIndexUntouched=True)
    write_json(LANE/'production-wrapper-qualification.json',receipt);print(dict(passed=True,controls=269,restorationControls=len(controls),elapsedSeconds=elapsed,receiptSha256=sha256(LANE/'production-wrapper-qualification.json')))


if __name__=='__main__':execute()
