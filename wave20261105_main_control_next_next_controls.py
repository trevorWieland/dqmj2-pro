import copy
import hashlib
import os
import shutil
import subprocess
import struct
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_next_compiler import COMPILER
from wave20261105_main_control_next_next_bindings import verify_original

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/next'
HELPERS=LANE/'native-helper-inputs.json'
HELPERS_SHA='9a1bba3462bf092129f8b98ed223dff911f616dbf545421ae9fe7416865ffb51'
EXPECTED={0x207d2c8:(84,['r0']),0x203d294:(72,['r0']),0x2026350:(484,['r0','r1'])}


def helper_proof(item,image,inventory):
    a=int(item['address'],0)
    if a not in EXPECTED:raise ValueError('Unknown original helper')
    size,arguments=EXPECTED[a]
    if (item.get('program') or '',item['processor'],item['module'],item['mode'],item['bytes'],item['incomingArgumentRegisters'])!=('','arm9','main','arm',size,arguments):raise ValueError('Exact original helper namespace/boundary/argument registers differ')
    record='func_'+format(a,'08x')+' kind:function(arm,size='+hex(size)+') addr:0x'+format(a,'08x')
    if item['canonicalInventoryRecord']!=record or record not in inventory.splitlines():raise ValueError('Original canonical helper entry absent')
    if hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest()!=item['nativeSha256']:raise ValueError('Complete original helper body changed')
    return dict(address=hex(a),bytes=size,mode='arm',nativeSha256=item['nativeSha256'],incomingArgumentRegisters=arguments,sourceCredit=0)


def original_helpers():
    if sha256(HELPERS)!=HELPERS_SHA:raise ValueError('Immutable helper context changed')
    value=read_json(HELPERS)
    for key in ['image','inventory','relocations']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original helper image/inventory changed')
    image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();relocations=(ROOT/value['relocations']['path']).read_text();model=value['model']
    if [struct.unpack_from('<I',image,p-0x2000000)[0] for p in [0x203d2d4,0x203d2d8,0x207d318]]!=[int(model['randomState'],0),model['multiplier'],int(model['lookupState'],0)] or model['increment']!=12345:raise ValueError('Exact original RNG/lookup literal model changed')
    if model['originalHelperBranch']!='from:0x0203d2c8 kind:arm_call to:0x02026350 module:main' or model['originalHelperBranch'] not in relocations.splitlines() or any(model[k] not in inventory.splitlines() for k in ['randomStateRecord','lookupStateRecord']):raise ValueError('Exact original helper branch/data namespace records absent')
    return [helper_proof(item,image,inventory) for item in value['helpers']]


def geometry(row):
    folder=ROOT/'work/w5cn/next/controls'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    checks=['sizeof(unsigned int)==4','sizeof(int)==4','sizeof(void*)==4','sizeof(u8)==1']
    checks+=['sizeof(Info)==8','(unsigned int)&((Info*)0)->kind==3','(unsigned int)&((Info*)0)->subtype==4']
    source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+x+')?1:-1];' for i,x in enumerate(checks)));obj=folder/'layout.o';cmd=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if p.returncode:raise ValueError(('Actual byte-record/address-width geometry failed',p.stdout,p.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address']=='0x207d74c':
        header=next(p for p in folder.glob('context*.h') if 'unknown[3]' in p.read_text());header.write_text(header.read_text().replace('unknown[3]','unknown[4]'));bad=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
        if bad.returncode==0 or 'illegal constant expression' not in bad.stdout:raise ValueError('Wrong metadata row stride accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    proofs=original_helpers();negative=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for name,binding in row['nativeSymbolEntries'].items():
            for label,key,value in [('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('mode','mode','thumb'),('interior','address',hex(int(binding['address'],0)+4)),('kind','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
                try:verify_original(row,wrong)
                except (ValueError,KeyError) as error:negative.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original byte-control helper binding admitted')
    value=read_json(HELPERS);image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();helper_negative=[]
    for item in value['helpers']:
        for label,key,wrong_value in [('CPU','processor','arm7'),('mode','mode','thumb'),('module','module','ov000'),('extent','bytes',item['bytes']-4),('body','nativeSha256','0'*64),('argument-registers','incomingArgumentRegisters',item['incomingArgumentRegisters']+['r3'])]:
            wrong=copy.deepcopy(item);wrong[key]=wrong_value
            try:helper_proof(wrong,image,inventory)
            except ValueError as error:helper_negative.append(dict(address=item['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original byte-control helper proof admitted')
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],negativeBranchCases=negative,nativeHelperProofs=proofs,negativeHelperCases=helper_negative,originalStorageExtentAuthorshipCredit=0,nativeCalleeSourceCredit=0);write_json(LANE/'binding-layout-controls.json',result);return result
