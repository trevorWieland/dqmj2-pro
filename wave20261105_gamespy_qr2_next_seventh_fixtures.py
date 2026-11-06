import wave20261105_gamespy_qr2_next_first_fixtures as H
import wave20261105_gamespy_qr2_next_seventh_models as F
from project import ROOT


def run(image,row,body,vector,seed):
    previous=H.F
    try:H.F=F;return H.run(image,row,body,vector,seed)
    finally:H.F=previous


def prove(row,native,source):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
    for seed,vector in enumerate(F.cases(int(row['address'],0))):
        original=run(image,row,native,vector,seed);rebuilt=run(image,row,source,vector,seed)
        if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent string/address caller model differs',vector,original,rebuilt))
        records.append(dict(seed=seed,vector=vector,traceSha256=original['traceSha256'],contractCalls=original['contractCalls']))
    return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,
        originalImportEntryModesChecked=True,suppliedCalleeBodiesExecuted=0,suppliedCalleeSourceOrExecutionCredit=0,networkDevicesOrScenesExecuted=0,
        limits=['Resolver results are explicit supplied ABI inputs; neither real address parsing nor DNS/networking code executes.','Host prefixes up to255 bytes and ports with defined int32 decimal conversion are bounded. All256 candidate port-byte values are checked; overflowing atoi and invalid pointers remain unproved.'])
