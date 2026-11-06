import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_large_format_compiler import COMPILER
from wave20261105_main_large_format_bindings import verify_original,negative_controls,frozen_inputs,validate

def execute(rows):
    row=rows[0];negative=[];name='native_fn_0201f2c0'
    for label,key,value in [('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('kind','kind','data'),('interior','address','0x201f2c4')]:
        changed=copy.deepcopy(row['nativeSymbolEntries']);changed[name][key]=value
        try:verify_original(row,changed)
        except ValueError as e:negative.append(dict(case=label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed measured format-parser native call admitted')
    wrong=copy.deepcopy(row);wrong['relocations'][0]['offset']+=4
    try:verify_original(wrong,row['nativeSymbolEntries'])
    except ValueError as e:negative.append(dict(case='changed-original-call-origin',rejected=True,reason=str(e)))
    else:raise ValueError('Changed formatter original call origin accepted')
    pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();loads=(ROOT/pointers['relocations']['path']).read_text();image=(ROOT/pointers['image']['path']).read_bytes();array_cases=[]
    for case in pointers['cases']:
        rel=next(r for r in row['relocations'] if r['offset']==case['offset']);changed=bytearray(image);changed[int(case['symbolAddress'],0)-0x2000000]^=1
        try:validate(case,row,rel,row['nativeSymbolEntries'][rel['symbol']],bytes(changed),inventory,loads,pointers['externalArrays'])
        except ValueError as e:array_cases.append(dict(address=case['symbolAddress'],rejected=True,reason=str(e)))
        else:raise ValueError('Changed original narrow/wide empty array admitted')
    folder=ROOT/'work/w5mg/format/controls/geometry';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    checks=['sizeof(ptrdiff_t)==4','sizeof(va_list)==4','sizeof(size_t)==4','sizeof(wchar_t)==2','sizeof(long long)==8','sizeof(long double)==8','sizeof(print_format)==16','(unsigned int)&((print_format*)0)->argument_options==4','(unsigned int)&((print_format*)0)->conversion_char==6','(unsigned int)&((print_format*)0)->field_width==8','(unsigned int)&((print_format*)0)->precision==12','sizeof(native_data_020dd184)==2','sizeof(native_data_020dd188)==1','ptrdiff_argument==8','intmax_argument==6','size_t_argument==7','zero_fill==2'];source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\nvoid RequirePtrdiffLong(ptrdiff_t *);\nvoid RequirePtrdiffLong(long *);\nvoid RequireVaPointer(va_list *);\nvoid RequireVaPointer(char **);\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));good=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if good.returncode:raise ValueError(('Actual ARM MSL type/format geometry failed',good.stdout,good.stderr))
    original_hash=sha256(obj);header=next(p for p in folder.glob('context*.h') if 'typedef long ptrdiff_t' in p.read_text());header.write_text(header.read_text().replace('typedef long ptrdiff_t','typedef int ptrdiff_t'));bad=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if bad.returncode==0:raise ValueError('Same-width wrong ptrdiff_t=int passed actual type-identity assertion')
    verify_original(row,row['nativeSymbolEntries']);return dict(status='passed',negativeBranchCases=negative,pointerCases=negative_controls(rows),changedArrayCases=array_cases,actualCompilerGeometry=dict(checks=checks,typeIdentityChecks=['ptrdiff_t is long','va_list is char*'],objectSha256=original_hash,exitCode=0,wrongSameWidthPtrdiffRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout),ordinaryBranchVerifierUnchanged=True,originalStorageSourceExtentCredit=0)
