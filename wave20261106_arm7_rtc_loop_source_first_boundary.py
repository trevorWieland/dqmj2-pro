import copy
import hashlib
import match_runtime
from project import ROOT,read_json,write_json,sha256
from qualify_arm7_scoped_control import walk

LANE=ROOT/'evidence/lanes/parallel-wave20261106/arm7-rtc-loop-next/first'


def certificate(row,image,base,target):
    if(row['address'],row['bytes'],row['mode'],row['nativeSpanSha256'])!=('0x27f60b4',1156,'arm',target):raise ValueError('Exact admitted channel native boundary differs')
    if base!=0x27e0000 or hashlib.sha256(image[0x27f60b4-base:0x27f6538-base]).hexdigest()!=target:raise ValueError('Original complete channel native span changed')
    return walk(row,image,base,'rtc')


def prepare():
    claim=read_json(LANE.parent/'claim.json')['claimedFunctions'][0];path=LANE/'boundary-certificate.json'
    if path.exists():raise ValueError('Boundary certificate already frozen')
    row=dict(address=claim['address'],mode=claim['mode'],bytes=claim['bytes'],flow=claim['physicalFlow'],entryReachableInstructionBytes=1140,actualLiteralReadBytes=16,nativeSpanSha256=claim['targetSha256'])
    proof=certificate(row,(ROOT/claim['binary']).read_bytes(),claim['base'],claim['targetSha256'])
    value=dict(program='',processor='arm7',module='arm7-main',mode='arm',address=claim['address'],bytes=claim['bytes'],nativeSpanSha256=claim['targetSha256'],flow=row,proof=proof)
    write_json(path,dict(status='passed',sourceCredit=0,functions=[value],originalReturnValidatorChanged=False,scopedQualifier=dict(path='qualify_arm7_scoped_control.py',sha256=sha256(ROOT/'qualify_arm7_scoped_control.py'))));print(sha256(path))


def controls():
    baseline=read_json(LANE/'boundary-certificate.json')['functions'][0];row=baseline['flow'];image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();proof=certificate(row,image,0x27e0000,baseline['nativeSpanSha256']);negatives=[]
    for key,value in [('mode','thumb'),('bytes',648),('address','0x27e9910'),('nativeSpanSha256','0'*64)]:
        altered=copy.deepcopy(row);altered[key]=value
        try:certificate(altered,image,0x27e0000,baseline['nativeSpanSha256'])
        except(ValueError,AssertionError)as error:negatives.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong scoped channel boundary accepted')
    return dict(status='passed',sourceCredit=0,positive=proof,negativeControls=negatives,originalSharedScopedQualification=read_json(LANE.parent/'coordinator-admission.json')['scopedQualification'])


if __name__=='__main__':prepare()
