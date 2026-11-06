import wave20261105_gamespy_qr2_next_first_fixtures as H
import wave20261105_gamespy_qr2_next_fourth_models as F
from project import ROOT


def run(image,row,body,vector,seed):
    previous=H.F
    try:
        H.F=F
        return H.run(image,row,body,vector,seed)
    finally:H.F=previous


def prove(row,native,source):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
    for seed,vector in enumerate(F.cases(int(row['address'],0))):
        original=run(image,row,native,vector,seed);rebuilt=run(image,row,source,vector,seed)
        if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent bounded QR2 dispatcher model differs',row['address'],vector,original,rebuilt))
        records.append(dict(seed=seed,vector=vector,traceSha256=original['traceSha256'],contractCalls=original['contractCalls']))
    return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,
        allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,originalImportEntryModesChecked=True,suppliedCalleeBodiesExecuted=0,
        suppliedCalleeSourceOrExecutionCredit=0,networkDevicesOrScenesExecuted=0,temporaryHarnessAdapterRestoresFrozenModule=True,
        limits=['Reply builders supply opaque bounded buffer bytes and progress transitions. Sendto is a captured six-word ABI contract with an8-byte sender; no original networking or reply-builder implementation executes.'])
