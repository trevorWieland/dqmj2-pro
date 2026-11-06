import copy
import os
import re
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_later_sdk_compiler import COMPILER
from wave20261105_main_later_sdk_bindings import verify_original,negative_controls,helper,frozen_inputs


def layout_checks(rows):
    row=next(r for r in rows if r['address']=='0x203ab50');directory=ROOT/'work/w5ml/sdk/controls/layout';directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source']
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    includes='\n'.join('#include "'+(ROOT/pin['path']).name+'"' for pin in row['sourceDependencies'])
    checks=['sizeof(BOOL)==4','sizeof(void*)==4','sizeof(NNSSndStrm)==0x5c','sizeof(FSFile)==0x48','sizeof(NNSSndStrmData)==0x40','sizeof(AdpcmState)==4','sizeof(NNSSndStrmPlayer)==0x174','(u32)&((NNSSndStrmPlayer*)0)->info==0xa8','(u32)&((NNSSndStrmPlayer*)0)->info.format==0xc0','sizeof(((NNSSndStrmPlayer*)0)->info.format)==1','(u32)&((NNSSndStrmPlayer*)0)->info.numChannels==0xc2','sizeof(((NNSSndStrmPlayer*)0)->info.numChannels)==1','(u32)&((NNSSndStrmPlayer*)0)->adpcmState==0xf8','(u32)&((NNSSndStrmPlayer*)0)->finishCounter==0x114','(u32)&((NNSSndStrmPlayer*)0)->prepareFlag==0x118','(u32)&((NNSSndStrmPlayer*)0)->curSample==0x160','(u32)&((NNSSndStrmPlayer*)0)->readStreamFunc==0x16c','(u32)&((NNSSndStrmPlayer*)0)->strmCallback==0x134','sizeof(LoadCommand)==0x30','(u32)&((LoadCommand*)0)->player==8','(u32)&((LoadCommand*)0)->status==0xc','(u32)&((LoadCommand*)0)->numChannels==0x10','(u32)&((LoadCommand*)0)->buffer==0x14','(u32)&((LoadCommand*)0)->bufLen==0x2c','sizeof(J2StreamGlobals)==12','(u32)&((J2StreamGlobals*)0)->prepareThread==4','(u32)&((J2StreamGlobals*)0)->decodeBuffer==8']
    text=includes+'\n'+'\n'.join('typedef char SdkLayout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(checks))+'\n';path=directory/'layout.c';path.write_text(text);obj=directory/'layout.o';flags=row['compilerFlags'];command=[str(COMPILER),*flags,'-c',str(path),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if process.returncode:raise ValueError(('Actual stream SDK type geometry failed',process.stdout,process.stderr))
    positive=dict(checks=checks,compilerSha256=sha256(COMPILER),sourceSha256=sha256(path),objectSha256=sha256(obj),exitCode=process.returncode)
    header=next(p for p in directory.glob('context*.h') if re.search(r'\bu8\s+format\s*;',p.read_text()));old=header.read_text();wrong=re.sub(r'\bu8\s+format\s*;','u16 format;',old,count=1);header.write_text(wrong)
    failure=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if failure.returncode==0 or 'illegal constant expression' not in failure.stdout:raise ValueError('Wrong format/channel width geometry accepted by actual compiler')
    negative=dict(wrongFormatWidthRejected=True,exitCode=failure.returncode,headerSha256=sha256(header),stdout=failure.stdout,stderr=failure.stderr)
    thread=next(r for r in rows if r['address']=='0x203b510');thread_dir=directory/'thread';thread_dir.mkdir(exist_ok=True)
    for pin in thread['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],thread_dir/(ROOT/pin['path']).name)
    thread_checks=['(u32)&((NNSSndStrmThread*)0)->threadQ==0x4c0','(u32)&((NNSSndStrmThread*)0)->mutex==0x4c8','(u32)&((NNSSndStrmThread*)0)->commandList==0x4e0','sizeof(((NNSSndStrmThread*)0)->commandList)==12','sizeof(OSMutex)==24']
    thread_source=thread_dir/'layout.c';thread_source.write_text('\n'.join('#include "'+(ROOT/pin['path']).name+'"' for pin in thread['sourceDependencies'])+'\n'+'\n'.join('typedef char ThreadLayout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(thread_checks)))
    thread_obj=thread_dir/'layout.o';thread_process=subprocess.run([str(COMPILER),*flags,'-c',str(thread_source),'-o',str(thread_obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if thread_process.returncode:raise ValueError(('Actual SDK thread/list offsets failed',thread_process.stdout,thread_process.stderr))
    return dict(status='passed',playerAndCommand=positive,wrongFormatWidth=negative,threadAndMutex=dict(checks=thread_checks,exitCode=thread_process.returncode,objectSha256=sha256(thread_obj)),sourceAndStorageExtentCredit=0)


def execute(rows):
    pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();results=[]
    for name in ('_ll_udiv','_u32_div_f'):
        row=next(r for r in rows if any(rel['symbol']==name for rel in r['relocations']));relocation=next(r for r in row['relocations'] if r['symbol']==name);binding=row['nativeSymbolEntries'][name]
        for label,key,value in [('address','address','0x2025a28'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
            changed=copy.deepcopy(binding);changed[key]=value
            try:helper(row,relocation,changed,imports,inventory)
            except ValueError as error:results.append(dict(symbol=name,case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid exact SDK compiler helper accepted:'+label)
        changed=copy.deepcopy(relocation);changed['symbol']=name+'_typo'
        try:helper(row,changed,binding,imports,inventory)
        except ValueError as error:results.append(dict(symbol=name,case='unknown-name-at-same-address',rejected=True,reason=str(error)))
        else:raise ValueError('Unknown helper name admitted')
    row=next(r for r in rows if r['address']=='0x203b510');name='native_fn_0200708c'
    for label,key,value in [('target-mode','mode','thumb'),('target-module','module','ov000'),('target-kind','kind','data')]:
        changed=copy.deepcopy(row['nativeSymbolEntries']);changed[name][key]=value
        try:verify_original(row,changed)
        except ValueError as error:results.append(dict(symbol=name,case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid regular SDK branch admitted')
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    return dict(status='passed',negativeBindingAndHelperCases=results,pointerCases=negative_controls(rows),actualCompilerGeometry=layout_checks(rows),ordinaryBranchVerifierUnchanged=True,sourceAndStorageExtentCredit=0)
