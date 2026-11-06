import copy
import os
import shutil
import subprocess
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_large_longlong_compiler import COMPILER
from wave20261105_main_large_longlong_bindings import verify_original
import native_alternate_entries as P
from prove_main_unsigned64_entries_20261030 import execute as native_entry

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/longlong'

def execute(rows):
    row=rows[0];verify_original(row,row['nativeSymbolEntries']);binding=row['nativeSymbolEntries']['native_fn_020260e8'];negative=[]
    for label,key,value in [('address','address','0x20260ec'),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong['native_fn_020260e8'][key]=value
        try:verify_original(row,wrong)
        except (ValueError,KeyError) as e:negative.append(dict(case=label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed qualified alternate native C call admitted')
    for field in ['identitySha256','verifierSha256']:
        wrong=copy.deepcopy(binding);wrong['alternateEntryEvidence'][field]='0'*64
        try:P.verify('native_fn_020260e8',wrong)
        except ValueError as e:negative.append(dict(case=field,rejected=True,reason=str(e)))
        else:raise ValueError('Changed existing alternate-entry certificate accepted')
    try:P.verify('_ull_mod',binding)
    except ValueError as e:negative.append(dict(case='inferred-intrinsic-name-instead-of-explicit-address',rejected=True,reason=str(e)))
    else:raise ValueError('Inferred helper name bypassed explicit native address policy')
    altered=copy.deepcopy(row);altered['relocations'][0]['offset']+=4
    try:verify_original(altered,row['nativeSymbolEntries'])
    except ValueError as e:negative.append(dict(case='changed-original-caller-origin',rejected=True,reason=str(e)))
    else:raise ValueError('Changed unsigned64 caller origin accepted')
    folder=ROOT/'work/w5mg/longlong/controls/geometry';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    checks=['sizeof(unsigned long long)==8','sizeof(void*)==4','sizeof(wchar_t)==2','sizeof(print_format)==16','(unsigned int)&((print_format*)0)->conversion_char==6','(unsigned int)&((print_format*)0)->field_width==8','(unsigned int)&((print_format*)0)->precision==12'];source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual unsigned64/wchar/format geometry failed',positive.stdout,positive.stderr))
    object_hash=sha256(obj);header=next(p for p in folder.glob('context*.h') if 'unsigned short wchar_t' in p.read_text());header.write_text(header.read_text().replace('unsigned short wchar_t','unsigned int wchar_t'));bad=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if bad.returncode==0 or 'illegal constant expression' not in bad.stdout:raise ValueError('Wrong wchar width passed native format geometry')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();pairs=[(0,0),(1,0),(0,1),(1,1),((1<<64)-1,8),((1<<63)+5,10),((1<<32)+7,16),((1<<32)+7,(1<<32)+1)];abi=[]
    for entry in [0x20260dc,0x20260e8]:
        for a,b in pairs:
            result=native_entry(image,entry,a,b,len(abi));abi.append(dict(entry=hex(entry),numerator=hex(a),denominator=hex(b),result=result))
    report=dict(status='passed',negativeBindingCases=negative,actualCompilerGeometry=dict(checks=checks,objectSha256=object_hash,exitCode=0,wrongWidthRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout),freshOriginalEntryReturns=abi,actualOriginalEntryExecutions=len(abi),existingCertificateRevalidated=True,originalTableUnchanged=True,originalCalleeSourceExtentCredit=0,limits=['Existing activated entry proof is reused unchanged;16 additional fresh quotient/remainder ABI calls execute original code only. Zero-divisor numerator passthrough is a measured entry contract, not a C division claim.'])
    write_json(LANE/'binding-layout-controls.json',report);return report
