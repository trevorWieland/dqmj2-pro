import copy
import os
import re
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_later_more_compiler import COMPILER
from wave20261105_main_later_more_bindings import verify_original,negative_controls,helper,frozen_inputs

def layout_checks(rows):
    row=next(r for r in rows if r['address']=='0x203b870');folder=ROOT/'work/w5ml/more/controls/layout';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    checks=['sizeof(BOOL)==4','sizeof(NNSSndStrm)==0x5c','sizeof(NNSSndStrmChannel)==8','(u32)&((NNSSndStrmChannel*)0)->buffer==0','(u32)&((NNSSndStrmChannel*)0)->volume==4','sizeof(((NNSSndStrmChannel*)0)->volume)==4','(u32)&((NNSSndStrm*)0)->chBufLen==0x28','(u32)&((NNSSndStrm*)0)->interval==0x2c','(u32)&((NNSSndStrm*)0)->callback==0x30','(u32)&((NNSSndStrm*)0)->callbackArg==0x34','(u32)&((NNSSndStrm*)0)->curBuffer==0x38','(u32)&((NNSSndStrm*)0)->volume==0x3c','(u32)&((NNSSndStrm*)0)->format==0x20','(u32)&((NNSSndStrm*)0)->chBitMask==0x44','(u32)&((NNSSndStrm*)0)->numChannels==0x48','(u32)&((NNSSndStrm*)0)->channelNo==0x4c','sizeof(((NNSSndStrm*)0)->channelNo[0])==1','(u32)&((NNSSndStrm*)0)->preSleepInfo==8','(u32)&((NNSSndStrm*)0)->postSleepInfo==0x14']
    path=folder/'layout.c';path.write_text('\n'.join('#include "'+(ROOT/pin['path']).name+'"' for pin in row['sourceDependencies'])+'\n'+'\n'.join('typedef char StreamLayout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(path),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if process.returncode:raise ValueError(('Actual stream geometry failed',process.stdout,process.stderr))
    positive=dict(checks=checks,sourceSha256=sha256(path),objectSha256=sha256(obj),compilerSha256=sha256(COMPILER),exitCode=0)
    header=next(p for p in folder.glob('context*.h') if 'typedef struct NNSSndStrmChannel' in p.read_text());text=header.read_text();wrong=re.sub(r'(typedef struct NNSSndStrmChannel\s*\{[\s\S]*?)\bint\s+volume;',r'\1short volume;',text,count=1)
    if wrong==text:raise ValueError('Wrong channel-width control did not change source')
    header.write_text(wrong);negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or 'illegal constant expression' not in negative.stdout:raise ValueError('Wrong channel volume width passed geometry')
    return dict(status='passed',positive=positive,wrongWidth=dict(exitCode=negative.returncode,stdout=negative.stdout,stderr=negative.stderr,headerSha256=sha256(header)))

def execute(rows):
    pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();row=next(r for r in rows if r['address']=='0x203b9c0');rel=next(r for r in row['relocations'] if r['symbol']=='_u32_div_f');binding=row['nativeSymbolEntries'][rel['symbol']];results=[]
    for label,key,value in [('address','address','0x2026354'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
        changed=copy.deepcopy(binding);changed[key]=value
        try:helper(row,rel,changed,imports,inventory)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong native division helper admitted')
    wrong=copy.deepcopy(rel);wrong['symbol']='_u32_div_f_typo'
    try:helper(row,wrong,binding,imports,inventory)
    except ValueError as error:results.append(dict(case='unknown-helper-name',rejected=True,reason=str(error)))
    else:raise ValueError('Unknown division helper name admitted')
    row=next(r for r in rows if r['address']=='0x203b870');name='native_fn_02009e60'
    for label,key,value in [('mode','mode','thumb'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
        try:verify_original(row,wrong)
        except ValueError as error:results.append(dict(case='branch-'+label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong native volume branch binding admitted')
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    return dict(status='passed',negativeBranchHelperCases=results,pointerCases=negative_controls(rows),actualCompilerGeometry=layout_checks(rows),ordinaryBranchVerifierUnchanged=True,sourceAndStorageExtentCredit=0)
