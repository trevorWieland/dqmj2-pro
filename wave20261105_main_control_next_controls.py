import copy
import hashlib
import os
import shutil
import subprocess
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_compiler import COMPILER
from wave20261105_main_control_next_bindings import frozen_inputs,verify_original,negative_controls,validate

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next'
HELPERS=LANE/'native-helper-inputs.json'
HELPERS_SHA='39c3efa0dbf109dfca6d0b741784add1aa0b144b4a7e99d4934a239fe3f175e0'
SIGNATURES={0x207b94c:(40,['r0','r1'],'int32'),0x201b248:(64,['r0','r1','r2'],'int32'),0x203d294:(72,['r0'],'int32'),0x207afec:(24,['r0'],'pointer32'),0x207b058:(40,['r0','r1'],'bool32'),0x207d2c8:(84,['r0'],'pointer32'),0x207f1ec:(104,['r0'],'ignored'),0x2026144:(524,['r0','r1'],'quotient-r0-remainder-r1')}


def helper_proof(value,image,inventory):
    address=int(value['address'],0)
    if address not in SIGNATURES or (value.get('program') or '',value['processor'],value['module'],value['mode'])!=('','arm9','main','arm'):raise ValueError('Original helper namespace differs')
    size,args,returns=SIGNATURES[address]
    if (value['bytes'],value['incomingArgumentRegisters'],value['returnView'])!=(size,args,returns):raise ValueError('Original measured helper boundary/register interface differs')
    record='func_'+format(address,'08x')+' kind:function(arm,size='+hex(size)+') addr:0x'+format(address,'08x')
    if value['canonicalInventoryRecord']!=record or record not in inventory.splitlines():raise ValueError('Canonical original helper entry absent')
    if hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest()!=value['nativeSha256']:raise ValueError('Complete original helper body changed')
    return dict(address=hex(address),bytes=size,mode='arm',nativeSha256=value['nativeSha256'],argumentRegisters=args,returnView=returns,calleeSourceCredit=0)


def original_helpers():
    if sha256(HELPERS)!=HELPERS_SHA:raise ValueError('Immutable original helper inputs changed')
    value=read_json(HELPERS)
    for key in ['image','inventory']:
        item=value[key]
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Original helper image/inventory changed')
    image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text()
    return [helper_proof(h,image,inventory) for h in value['helpers']]


def geometry(row):
    address=int(row['address'],0);folder=ROOT/'work/w5cn/controls/geometry'/format(address,'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(short)==2','sizeof(char)==1'];old=new=None
    if address==0x207b02c:checks+=['sizeof(Row40)==40','(unsigned int)&((Row40*)0)->flags==4','sizeof(((Row40*)0)->flags)==2','sizeof(State)==8','(unsigned int)&((State*)0)->rows==4'];old,new='pad0[4]','pad0[6]'
    if address==0x207b974:
        checks+=['sizeof(RangeRow)==40']+['(unsigned int)&((RangeRow*)0)->'+field+'=='+str(offset) for field,offset in [('lower0',16),('upper0',18),('lower1',20),('upper1',22),('threshold0',24),('threshold1',26)]];old,new='unknown0[16]','unknown0[20]'
    if address==0x207d8e4:checks+=['sizeof(Observed)==4','(unsigned int)&((Observed*)0)->code==3','sizeof(((Observed*)0)->code)==1'];old,new='pad[3]','pad[4]'
    if address==0x207f1a4:checks+=['sizeof(State)==12','(unsigned int)&((State*)0)->pending==4','(unsigned int)&((State*)0)->count==8'];old,new='reserved,pending,count','reserved,pad,pending,count'
    if address==0x207ffb4:checks+=['sizeof(Match)==4','(unsigned int)&((Match*)0)->column==2','sizeof(native_data_020db298)==1260','sizeof(native_data_020db298[0])==12','sizeof(native_data_020db298[0][0])==3'];old,new='u16 row,column','unsigned int row,column'
    source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+v+')?1:-1];' for i,v in enumerate(checks)));obj=folder/'layout.o';cmd=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if p.returncode:raise ValueError(('Actual control source layout failed',row['address'],p.stdout,p.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if old:
        header=next(p for p in folder.glob('context*.h') if old in p.read_text());header.write_text(header.read_text().replace(old,new));p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if p.returncode==0 or 'illegal constant expression' not in p.stdout:raise ValueError('Wrong measured record layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=p.returncode,negativeStdout=p.stdout)
    return result


def execute(rows):
    pointers,unused=frozen_inputs();image=(ROOT/pointers['image']['path']).read_bytes();inventory=(ROOT/pointers['inventory']['path']).read_text();loads=(ROOT/pointers['relocations']['path']).read_text();proofs=original_helpers();negative=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for name,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('interior','address',hex(int(binding['address'],0)+4)),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('kind','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
                try:verify_original(row,wrong)
                except (ValueError,KeyError) as error:negative.append(dict(caller=row['address'],symbol=name,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Changed original control branch interface accepted')
    arrays=[]
    for case in pointers['cases']:
        if case['symbolAddress']!='0x20db298':continue
        row=next(r for r in rows if r['address']==case['caller']);rel=next(r for r in row['relocations'] if r['offset']==case['offset']);changed=bytearray(image);changed[0xdb298]^=1
        try:validate(case,row,rel,row['nativeSymbolEntries'][rel['symbol']],bytes(changed),inventory,loads,pointers['externalArrays'])
        except ValueError as error:arrays.append(dict(case='changed-original-triple-table-byte',rejected=True,reason=str(error)))
        else:raise ValueError('Changed original comparison table accepted')
    helper_negative=[]
    for item in read_json(HELPERS)['helpers']:
        for label,key,value in [('CPU','processor','arm7'),('mode','mode','thumb'),('module','module','ov000'),('extent','bytes',item['bytes']-4),('body','nativeSha256','0'*64),('argument-registers','incomingArgumentRegisters',item['incomingArgumentRegisters']+['r3'])]:
            wrong=copy.deepcopy(item);wrong[key]=value
            try:helper_proof(wrong,image,inventory)
            except ValueError as error:helper_negative.append(dict(address=item['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original helper body/interface evidence accepted')
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],negativeBranchCases=negative,pointerCases=negative_controls(rows),changedArrayCases=arrays,nativeHelperProofs=proofs,negativeOriginalHelperCases=helper_negative,ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0,nativeCalleeSourceCredit=0);write_json(LANE/'binding-layout-controls.json',result);return result
