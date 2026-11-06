import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_large_tail_compiler import COMPILER
from wave20261105_main_large_tail_bindings import verify_original,negative_controls,helper,frozen_inputs

def geometry(rows):
    groups=[('0x201ec3c',['sizeof(Reader)==8','(unsigned int)&((Reader*)0)->next==0','(unsigned int)&((Reader*)0)->null_seen==4','sizeof(double)==8','sizeof(int)==4']),('0x20211e8',['sizeof(Output)==12','(unsigned int)&((Output*)0)->text==0','(unsigned int)&((Output*)0)->capacity==4','(unsigned int)&((Output*)0)->written==8','sizeof(wchar_t)==2','sizeof(size_t)==4','sizeof(va_list)==4'])];results=[];wrong=None
    for address,checks in groups:
        row=next(r for r in rows if r['address']==address);folder=ROOT/'work/w5mg/tail/controls/geometry'/format(int(address,0),'08x');folder.mkdir(parents=True,exist_ok=True)
        for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
        source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode:raise ValueError(('Actual reader/output wrapper layout failed',process.stdout,process.stderr))
        results.append(dict(address=address,checks=checks,objectSha256=sha256(obj),sourceSha256=sha256(source),exitCode=0))
        if address=='0x20211e8':
            header=next(p for p in folder.glob('context*.h') if 'unsigned short wchar_t' in p.read_text());text=header.read_text();header.write_text(text.replace('unsigned short wchar_t','unsigned int wchar_t'));bad=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
            if bad.returncode==0 or 'illegal constant expression' not in bad.stdout:raise ValueError('Wrong32bit wchar_t passed actual ABI geometry')
            wrong=dict(exitCode=bad.returncode,stdout=bad.stdout,stderr=bad.stderr)
    return dict(status='passed',records=results,wrongWcharWidth=wrong)

def execute(rows):
    pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();row=next(r for r in rows if r['address']=='0x201ec3c');negative=[]
    for name in imports['mapping']:
        rel=next(r for r in row['relocations'] if r['symbol']==name);binding=row['nativeSymbolEntries'][name]
        for label,key,value in [('address','address',hex(int(binding['address'],0)+4)),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
            wrong=copy.deepcopy(binding);wrong[key]=value
            try:helper(row,rel,wrong,imports,inventory)
            except ValueError as e:negative.append(dict(symbol=name,case=label,rejected=True,reason=str(e)))
            else:raise ValueError('Wrong native floating-wrapper helper admitted')
        wrong=copy.deepcopy(rel);wrong['symbol']=name+'_wrong'
        try:helper(row,wrong,binding,imports,inventory)
        except ValueError as e:negative.append(dict(symbol=name,case='unknown-helper',rejected=True,reason=str(e)))
        else:raise ValueError('Unknown helper admitted')
    name='native_fn_0201d9f0'
    for label,key,value in [('mode','mode','thumb'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
        try:verify_original(row,wrong)
        except ValueError as e:negative.append(dict(case='source-call-'+label,rejected=True,reason=str(e)))
        else:raise ValueError('Wrong actual floating-reader target admitted')
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    return dict(status='passed',negativeBranchHelperCases=negative,pointerCases=negative_controls(rows),actualCompilerGeometry=geometry(rows),ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
