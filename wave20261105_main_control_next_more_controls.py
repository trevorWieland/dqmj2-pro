import copy
import hashlib
import os
import shutil
import struct
import subprocess
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_more_compiler import COMPILER
from wave20261105_main_control_next_more_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/more'
HELPERS=LANE/'native-helper-inputs.json'
HELPERS_SHA='f1848672f693f8dc2b714f5891fc27bb7b6ae3c4e2ae583b125d2dd59d1cd6e0'
EXPECTED={0x206ea80:('main',12,[],0x21c4f80),0x2215698:('ov000',12,[],0x22459b4),0x204b53c:('main',116,['r0','r1'],None)}


def helper_proof(item,image,inventory):
    address=int(item['address'],0)
    if address not in EXPECTED:raise ValueError('Unknown original helper address')
    module,size,arguments,pointer=EXPECTED[address]
    if (item.get('program') or '',item['processor'],item['module'],item['mode'],item['bytes'],item['incomingArgumentRegisters'])!=('','arm9',module,'arm',size,arguments):raise ValueError('Original helper CPU/program/module/mode/extent/register interface differs')
    prefix='func_' if module=='main' else 'func_ov000_';record=prefix+format(address,'08x')+' kind:function(arm,size='+hex(size)+') addr:0x'+format(address,'08x')
    if item['canonicalInventoryRecord']!=record or record not in inventory.splitlines():raise ValueError('Original canonical helper entry absent')
    offset=address-int(item['base'],0);body=image[offset:offset+size]
    if hashlib.sha256(body).hexdigest()!=item['nativeSha256']:raise ValueError('Complete original helper body changed')
    if pointer is not None:
        if item['constantReturnPointer']!=hex(pointer) or body[:8].hex()!='00009fe51eff2fe1' or struct.unpack_from('<I',body,8)[0]!=pointer:raise ValueError('Exact no-argument getter/literal pointer changed')
    elif item['constantReturnPointer'] is not None:raise ValueError('Point helper cannot inherit a getter pointer')
    return dict(address=hex(address),module=module,mode='arm',bytes=size,incomingArgumentRegisters=arguments,constantReturnPointer=hex(pointer) if pointer is not None else None,nativeSha256=item['nativeSha256'],calleeSourceCredit=0)


def original_helpers():
    if sha256(HELPERS)!=HELPERS_SHA:raise ValueError('Immutable original helper contracts changed')
    result=[]
    for item in read_json(HELPERS)['helpers']:
        for key in ['image','inventory']:
            pin=item[key]
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original module image/inventory changed')
        result.append(helper_proof(item,(ROOT/item['image']['path']).read_bytes(),(ROOT/item['inventory']['path']).read_text()))
    return result


def geometry(row):
    address=int(row['address'],0);folder=ROOT/'work/w5cn/more/controls'/format(address,'08x');folder.mkdir(parents=True,exist_ok=True)
    for item in row['sourceDependencies']:shutil.copyfile(ROOT/item['path'],folder/(ROOT/item['path']).name)
    checks=['sizeof(int)==4','sizeof(short)==2','sizeof(void*)==4']
    if address==0x207a168:checks+=['sizeof(Input)==8','(unsigned int)&((Input*)0)->b==4','sizeof(Point)==4','(unsigned int)&((Point*)0)->x==0','(unsigned int)&((Point*)0)->y==2'];old,new='short x,y','int x,y'
    else:checks+=['sizeof(Selection)==4','(unsigned int)&((Selection*)0)->slot==2','(unsigned int)&((Selection*)0)->pad==3','sizeof(Context)==13','(unsigned int)&((Context*)0)->dirty==12'];old,new='short id','int id'
    source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+x+')?1:-1];' for i,x in enumerate(checks)));obj=folder/'layout.o';cmd=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Actual minimum context/point layout failed',positive.stdout,positive.stderr))
    positive_hash=sha256(obj);header=next(p for p in folder.glob('context*.h') if old in p.read_text());header.write_text(header.read_text().replace(old,new));wrong=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if wrong.returncode==0 or 'illegal constant expression' not in wrong.stdout:raise ValueError('Wrong measured point/selection layout accepted')
    return dict(address=row['address'],checks=checks,objectSha256=positive_hash,wrongLayoutRejected=True,negativeExitCode=wrong.returncode,negativeStdout=wrong.stdout)


def execute(rows):
    proofs=original_helpers();negative=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for name,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('CPU','processor','arm7'),('program','program','child'),('module','module','main' if binding['module']=='ov000' else 'ov000'),('mode','mode','thumb'),('interior','address',hex(int(binding['address'],0)+4)),('kind','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
                try:verify_original(row,wrong)
                except (ValueError,KeyError) as error:negative.append(dict(caller=row['address'],symbol=name,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original selection/overlay interface accepted')
    helper_negative=[]
    for item in read_json(HELPERS)['helpers']:
        image=(ROOT/item['image']['path']).read_bytes();inventory=(ROOT/item['inventory']['path']).read_text()
        for label,key,value in [('CPU','processor','arm7'),('program','program','child'),('module','module','main' if item['module']=='ov000' else 'ov000'),('mode','mode','thumb'),('extent','bytes',item['bytes']-4),('argument-registers','incomingArgumentRegisters',item['incomingArgumentRegisters']+['r2']),('body','nativeSha256','0'*64)]:
            wrong=copy.deepcopy(item);wrong[key]=value
            try:helper_proof(wrong,image,inventory)
            except ValueError as error:helper_negative.append(dict(address=item['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original getter/point helper evidence accepted')
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],negativeBranchCases=negative,pointerCases=negative_controls(rows),nativeHelperProofs=proofs,negativeHelperCases=helper_negative,originalStorageExtentAuthorshipCredit=0,nativeCalleeSourceCredit=0);write_json(LANE/'binding-layout-controls.json',result);return result
