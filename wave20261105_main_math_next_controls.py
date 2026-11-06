import copy
import hashlib
import os
import shutil
import subprocess
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_math_next_compiler import COMPILER
from wave20261105_main_math_next_bindings import verify_original,negative_controls,helper,frozen_inputs,validate
import native_alternate_entries as P
from prove_main_unsigned64_entries_20261030 import execute as native_entry

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next'
ARGUMENT=LANE/'argument-input.json'
ARGUMENT_SHA='88751a1cbda86d09c6c544686b9a3d7a4566211c72307f161868f1c823887834'


def argument_proof(value,image,inventory):
    if (value.get('program') or '',value['processor'],value['module'],value['mode'],value['caller'],value['callee'],value['calleeBytes'],value['registerArgument']['register'],value['registerArgument']['value'])!=('','arm9','main','arm','0x2026ac0','0x20b9dd0',64,'r0',1):raise ValueError('Original argument namespace/value differs')
    if value['canonicalInventoryRecord']!='func_020b9dd0 kind:function(arm,size=0x40) addr:0x020b9dd0' or value['canonicalInventoryRecord'] not in inventory.splitlines():raise ValueError('Original complete argument-consuming callee entry absent')
    for address,length,key in [(0x2026ac0,56,'callerSha256'),(0x20b9dd0,64,'calleeSha256')]:
        if hashlib.sha256(image[address-0x2000000:address-0x2000000+length]).hexdigest()!=value[key]:raise ValueError('Original argument caller/callee body changed')
    expected={0x2026ad4:'0100a0e3',0x2026ad8:'140081e5',0x2026adc:'bb4c02eb',0x20b9dd4:'0040a0e1',0x20b9dd8:'040ca0e1',0x20b9ddc:'400ca0e1'}
    supplied={int(x['address'],0):x['wordHex'] for x in value['instructions']}
    if supplied!=expected:raise ValueError('Fixed original R0 definition/store/branch/consume words differ')
    for address,word in expected.items():
        if image[address-0x2000000:address-0x2000000+4].hex()!=word:raise ValueError('Measured argument instruction changed')
    return dict(status='passed',register='r0',value=1,caller='0x2026ac0',callee='0x20b9dd0',nativeCalleeExecutionCredit=0)


def geometry(row):
    address=int(row['address'],0);folder=ROOT/'work/w5mn/controls/geometry'/format(address,'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    if address==0x2026ac0:
        checks=['sizeof(RuntimeState)==24','(unsigned int)&((RuntimeState*)0)->value==4','(unsigned int)&((RuntimeState*)0)->initialized==20','sizeof(((RuntimeState*)0)->value)==4','sizeof(((RuntimeState*)0)->initialized)==4']
        old,new='int pad8[3]','int pad8[4]'
    else:
        checks=['sizeof(decimal)==38','(unsigned int)&((decimal*)0)->exponent==2','(unsigned int)&((decimal*)0)->sig.length==4','(unsigned int)&((decimal*)0)->sig.text==5','sizeof(((decimal*)0)->sig.text)==32','sizeof(unsigned long long)==8','sizeof(void*)==4']
        old,new='text[32]','text[36]'
        if address==0x2023790:checks+=['sizeof(double)==8','sizeof(float)==4','sizeof(native_data_020dd18c)==64','sizeof(native_data_020dd18c[0])==8','sizeof(native_data_020dd2a0)==37','sizeof(native_data_020dceb8)==4']
    source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+v+')?1:-1];' for i,v in enumerate(checks)))
    obj=folder/'layout.o';cmd=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Original native geometry failed',positive.stdout,positive.stderr))
    positive_hash=sha256(obj);header=next(p for p in folder.glob('context*.h') if old in p.read_text());header.write_text(header.read_text().replace(old,new));negative=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if negative.returncode==0 or 'illegal constant expression' not in negative.stdout:raise ValueError('Wrong actual compiler record layout passed')
    return dict(address=row['address'],checks=checks,objectSha256=positive_hash,compilerSha256=sha256(COMPILER),exitCode=0,wrongLayoutRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout)


def execute(rows):
    value,imports=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();negative=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for rel in row['relocations']:
            if rel['symbol'] not in imports['mapping']:continue
            binding=row['nativeSymbolEntries'][rel['symbol']]
            for label,key,wrong_value in [('interior','address',hex(int(binding['address'],0)+4)),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('kind','kind','data')]:
                wrong=copy.deepcopy(binding);wrong[key]=wrong_value
                try:helper(row,rel,wrong,imports,inventory)
                except ValueError as error:negative.append(dict(caller=row['address'],case=rel['symbol']+'-'+label,rejected=True,reason=str(error)))
                else:raise ValueError('Changed compiler helper boundary admitted')
    u64=next(r for r in rows if r['address']=='0x2022a94');binding=u64['nativeSymbolEntries']['native_fn_020260e8']
    for label,key,wrong_value in [('address','address','0x20260ec'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(u64['nativeSymbolEntries']);wrong['native_fn_020260e8'][key]=wrong_value
        try:verify_original(u64,wrong)
        except (ValueError,KeyError) as error:negative.append(dict(caller=u64['address'],case='alternate-'+label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed existing unsigned64 entry admitted')
    for field in ['identitySha256','verifierSha256']:
        wrong=copy.deepcopy(binding);wrong['alternateEntryEvidence'][field]='0'*64
        try:P.verify('native_fn_020260e8',wrong)
        except ValueError as error:negative.append(dict(case='alternate-'+field,rejected=True,reason=str(error)))
        else:raise ValueError('Changed existing alternate-entry certificate admitted')
    try:P.verify('_ull_mod',binding)
    except ValueError as error:negative.append(dict(case='implicit-intrinsic-instead-of-explicit-address',rejected=True,reason=str(error)))
    else:raise ValueError('Inferred helper name bypassed explicit address policy')
    arrays=[]
    for case in value['cases']:
        if case['symbolAddress']=='0x20ec9b8':continue
        row=next(r for r in rows if r['address']==case['caller']);rel=next(r for r in row['relocations'] if r['offset']==case['offset']);changed=bytearray(image);changed[int(case['symbolAddress'],0)-0x2000000]^=1
        try:validate(case,row,rel,row['nativeSymbolEntries'][rel['symbol']],bytes(changed),inventory,loads,value['externalArrays'])
        except ValueError as error:arrays.append(dict(address=case['symbolAddress'],rejected=True,reason=str(error)))
        else:raise ValueError('Changed original constant array accepted')
    if sha256(ARGUMENT)!=ARGUMENT_SHA:raise ValueError('Immutable caller argument proof changed')
    arg=read_json(ARGUMENT);argproof=argument_proof(arg,image,inventory);argnegative=[]
    for label,key,wrong_value in [('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('interior-callee','callee','0x20b9dd4'),('callee-extent','calleeBytes',60),('callee-body','calleeSha256','0'*64)]:
        wrong=copy.deepcopy(arg);wrong[key]=wrong_value
        try:argument_proof(wrong,image,inventory)
        except ValueError as error:argnegative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong argument/interface provenance accepted')
    wrong=copy.deepcopy(arg);wrong['registerArgument']['value']=0
    try:argument_proof(wrong,image,inventory)
    except ValueError as error:argnegative.append(dict(case='argument-zero',rejected=True,reason=str(error)))
    else:raise ValueError('Wrong original constant argument accepted')
    standalone=[]
    for entry in [0x20260dc,0x20260e8]:
        for a,b in [(0,0),(1,0),(0,1),(1,1),((1<<64)-1,8),((1<<63)+5,10),((1<<32)+7,16),((1<<32)+7,(1<<32)+1)]:standalone.append(dict(entry=hex(entry),numerator=hex(a),denominator=hex(b),result=native_entry(image,entry,a,b,len(standalone))))
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],negativeBranchHelperCases=negative,pointerCases=negative_controls(rows),changedArrayCases=arrays,argumentProof=argproof,argumentNegativeCases=argnegative,existingAlternateCertificateRevalidated=True,freshStandaloneOriginalEntryReturns=standalone,actualStandaloneOriginalEntryExecutions=len(standalone),originalStorageExtentAuthorshipCredit=0,nativeSourceCalleeCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
