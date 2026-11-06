import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_large_compiler import COMPILER
from wave20261105_main_large_bindings import verify_original,negative_controls,helper,frozen_inputs

def geometry(rows):
    groups=[('0x201f114',['sizeof(int)==4','sizeof(long)==4','sizeof(void*)==4','sizeof(__InStrCtrl)==8','(unsigned int)&((__InStrCtrl*)0)->NextChar==0','(unsigned int)&((__InStrCtrl*)0)->NullCharDetected==4']),('0x201ed2c',['sizeof(native_data_020d8e04)==256','sizeof(native_data_020d8e04[0])==2','sizeof(native_data_020d8d84)==128','sizeof(native_data_020d8d84[0])==1']),('0x201f838',['sizeof(wchar_t)==2','sizeof(print_format)==16','(unsigned int)&((print_format*)0)->conversion_char==6','(unsigned int)&((print_format*)0)->field_width==8','(unsigned int)&((print_format*)0)->precision==12']),('0x2020120',['sizeof(decimal)==38','(unsigned int)&((decimal*)0)->exp==2','(unsigned int)&((decimal*)0)->sig.length==4','(unsigned int)&((decimal*)0)->sig.text==5','sizeof(((decimal*)0)->sig.text)==32'])];records=[];negative=None
    for address,checks in groups:
        row=next(r for r in rows if r['address']==address);folder=ROOT/'work/w5mg/controls/geometry'/format(int(address,0),'08x');folder.mkdir(parents=True,exist_ok=True)
        for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
        source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode:raise ValueError(('Native type geometry mismatch',address,process.stdout,process.stderr))
        records.append(dict(address=address,checks=checks,sourceSha256=sha256(source),objectSha256=sha256(obj),exitCode=0))
        if address=='0x2020120':
            header=next(p for p in folder.glob('context*.h') if 'text[32]' in p.read_text());text=header.read_text();header.write_text(text.replace('text[32]','text[36]'));bad=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
            if bad.returncode==0 or 'illegal constant expression' not in bad.stdout:raise ValueError('Wrong comparative36digit decimal layout passed compiler assertions')
            negative=dict(case='wrong36digit-record',exitCode=bad.returncode,stdout=bad.stdout,stderr=bad.stderr,changedHeaderSha256=sha256(header))
    return dict(status='passed',records=records,wrongRecord=negative,actualCompilerSha256=sha256(COMPILER))

def execute(rows):
    pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();row=next(r for r in rows if r['address']=='0x201ed2c');rel=next(r for r in row['relocations'] if r['symbol']=='_u32_div_f');binding=row['nativeSymbolEntries'][rel['symbol']];results=[]
    for label,key,value in [('address','address','0x2026354'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(binding);wrong[key]=value
        try:helper(row,rel,wrong,imports,inventory)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong exact native compiler helper admitted')
    changed=copy.deepcopy(rel);changed['symbol']='_u32_div_f_wrong'
    try:helper(row,changed,binding,imports,inventory)
    except ValueError as error:results.append(dict(case='unknown-helper',rejected=True,reason=str(error)))
    else:raise ValueError('Unknown compiler helper admitted')
    row=next(r for r in rows if r['address']=='0x201f114');name='native_main_0201ed2c'
    for label,key,value in [('mode','mode','thumb'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
        try:verify_original(row,wrong)
        except ValueError as error:results.append(dict(case='branch-'+label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original parser call binding admitted')
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    return dict(status='passed',negativeBranchHelperCases=results,pointerCases=negative_controls(rows),actualCompilerGeometry=geometry(rows),ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
