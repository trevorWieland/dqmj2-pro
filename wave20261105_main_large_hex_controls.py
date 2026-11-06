import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_large_hex_compiler import COMPILER
from wave20261105_main_large_hex_bindings import verify_original,negative_controls,helper,frozen_inputs,validate

def geometry(row):
    folder=ROOT/'work/w5mg/hex/controls/geometry';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    checks=['sizeof(long double)==8','sizeof(double)==8','sizeof(wchar_t)==2','sizeof(print_format)==16','(unsigned int)&((print_format*)0)->conversion_char==6','(unsigned int)&((print_format*)0)->precision==12','sizeof(decimal)==38','(unsigned int)&((decimal*)0)->exp==2','(unsigned int)&((decimal*)0)->sig.length==4','(unsigned int)&((decimal*)0)->sig.text==5','sizeof(((decimal*)0)->sig.text)==32','sizeof(decform)==4','(unsigned int)&((decform*)0)->digits==2']
    pointers,imports=frozen_inputs()
    for key,array in pointers['adpcmTables'].items():
        if array['type']=='const-wchar16-array':checks.append('sizeof(native_data_'+format(int(key,0),'08x')+')=='+str(array['bytes']))
    source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if process.returncode:raise ValueError(('Actual float formatting geometry failed',process.stdout,process.stderr))
    positive=dict(checks=checks,sourceSha256=sha256(source),objectSha256=sha256(obj),compilerSha256=sha256(COMPILER),exitCode=0);header=next(p for p in folder.glob('context*.h') if 'text[32]' in p.read_text());text=header.read_text();header.write_text(text.replace('text[32]','text[36]'));negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or 'illegal constant expression' not in negative.stdout:raise ValueError('Comparative36digit record passed native layout')
    return dict(status='passed',positive=positive,wrongRecord=dict(exitCode=negative.returncode,stdout=negative.stdout,stderr=negative.stderr))

def execute(rows):
    row=rows[0];pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();image=(ROOT/pointers['image']['path']).read_bytes();loads=(ROOT/pointers['relocations']['path']).read_text();rel=next(r for r in row['relocations'] if r['symbol']=='_deq');binding=row['nativeSymbolEntries'][rel['symbol']];negative=[]
    for label,key,value in [('address','address','0x202520c'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(binding);wrong[key]=value
        try:helper(row,rel,wrong,imports,inventory)
        except ValueError as e:negative.append(dict(case=label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed float compiler helper binding admitted')
    wrong=copy.deepcopy(rel);wrong['symbol']='_deq_wrong'
    try:helper(row,wrong,binding,imports,inventory)
    except ValueError as e:negative.append(dict(case='unknown-helper',rejected=True,reason=str(e)))
    else:raise ValueError('Unknown float helper admitted')
    name='native_fn_020236e8'
    for label,key,value in [('mode','mode','thumb'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
        try:verify_original(row,wrong)
        except ValueError as e:negative.append(dict(case='branch-'+label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed original decimal conversion entry admitted')
    array_cases=[]
    for case in pointers['cases']:
        rel=next(r for r in row['relocations'] if r['offset']==case['offset']);changed=bytearray(image);changed[int(case['symbolAddress'],0)-0x2000000]^=1
        try:validate(case,row,rel,row['nativeSymbolEntries'][rel['symbol']],bytes(changed),inventory,loads,pointers['adpcmTables'])
        except ValueError as e:array_cases.append(dict(address=case['symbolAddress'],case='changed-original-external-array-byte',rejected=True,reason=str(e)))
        else:raise ValueError('Changed original wide/class array accepted')
    verify_original(row,row['nativeSymbolEntries']);return dict(status='passed',negativeBranchHelperCases=negative,pointerCases=negative_controls(rows),changedArrayCases=array_cases,actualCompilerGeometry=geometry(row),ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
