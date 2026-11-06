import hashlib
import json
import re
import main_group_grid292_fixture_v2_20261102 as original
from project import ROOT,write_json
from wave20261106_main_grid_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK


LIMITS='192 synthetic packed-record/group/page cases run actual complete original and C292 callers to384 returns; original seven ARM helper bodies execute and entries are observed,with0separate physical helper return or source-code credit. Only ARM main02065818 service is supplied,100%of its body bypassed. Whole-RAM/callee-save/stack and ordered service-word model checked. No supplied-service meaning,real save/game scene,malformed/gapped records,concurrency,hardware,Windows/Android execution or imported storage authorship.'


def helper_specs(image,inventory):
    specs=[]
    for address,size in original.HELPERS.items():
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(size,address),line)),None)
        if canonical is None:raise ValueError('Actual original helper full boundary/mode differs')
        specs.append(dict(address=hex(address),bytes=size,mode='arm',canonicalInventoryRecord=canonical,nativeSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),sourceCredit=0,separatePhysicalReturnCredit=0))
    return specs


def run(image,row,body,seed,specs=None):
    if(row.get('program')or'',row['processor'],row['module'],row['mode'],row['address'])!=('','arm9','main','arm','0x20d0ad8'):raise ValueError('Actual model caller namespace differs')
    value=original.execute(image,body,seed)
    if not value['actualReturn']or not value['modelPassed']:raise ValueError('Actual complete caller differs from independent ordered group/grid model')
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=1:raise ValueError('Exact singleton grid packet differs')
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text());native=image[0xd0ad8:0xd0bfc];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();records=[];own=set();observed_helpers={}
    for index in range(192):
        left=run(image,row,native,index,specs);right=run(image,row,body,index,specs)
        if left!=right:raise ValueError('Actual original/C group-grid traces differ')
        own.update(left['observedInstructionAddresses']);entries=sum(left['logicalNativeHelperEntries'].values())
        for address,count in left['logicalNativeHelperEntries'].items():observed_helpers[address]=observed_helpers.get(address,0)+2*count
        records.append(dict(address=row['address'],case=index,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=entries,actualOriginalHelperReturns=0,suppliedServiceCalls=len(left['suppliedCalls']),original=left,candidate=right))
    if own!=set(range(original.ENTRY,original.ENTRY+288,4)):raise ValueError('Actual complete caller instruction coverage differs')
    try:original.execute(image,native,0,bound=1)
    except AssertionError:pass
    else:raise ValueError('Incomplete caller prefix counted as return')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=384,nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=sum(observed_helpers.values()),actualNativeHelperEntryObservations=observed_helpers,separateActualNativeHelperReturnCredit=0,helperSourceCodeCredit=0,suppliedServiceCalls=sum(r['suppliedServiceCalls']for r in records)*2,suppliedServiceBodyInstructionsExecuted=0,observedCallerInstructionBytes=288,generatedLiteralBytes=4,boundedPrefixRejected=True,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
