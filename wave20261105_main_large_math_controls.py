import copy
import os
import shutil
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256
from wave20261105_main_large_math_compiler import COMPILER
from wave20261105_main_large_math_bindings import verify_original,negative_controls,helper,frozen_inputs,validate

def geometry(row):
    folder=ROOT/'work/w5mg/math/controls/geometry';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    checks=['sizeof(double)==8','sizeof(float)==4','sizeof(int)==4','sizeof(native_data_020d9014)==16','sizeof(native_data_020d9024)==16','sizeof(native_data_020d9034)==16','sizeof(native_data_020dcebc)==4','sizeof(native_data_020ec9b0)==4','(unsigned int)&((DoubleAlignment*)0)->word==4'];source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\ntypedef struct DoubleAlignment {char byte;double word;} DoubleAlignment;\nconst double NativeEndianProbe=1.0;\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if process.returncode:raise ValueError(('Actual float/double native geometry failed',process.stdout,process.stderr))
    with obj.open('rb') as stream:
        elf=ELFFile(stream);symbol=elf.get_section_by_name('.symtab').get_symbol_by_name('NativeEndianProbe')[0];raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+8]
    if raw.hex()!='000000000000f03f':raise ValueError('Actual compiler double word order differs from native little endian')
    positive=dict(checks=checks,objectSha256=sha256(obj),sourceSha256=sha256(source),compilerSha256=sha256(COMPILER),oneDoubleBytesHex=raw.hex(),exitCode=0);header=next(p for p in folder.glob('context*.h') if 'extern const double native_data_020d9014' in p.read_text());text=header.read_text();header.write_text(text.replace('extern const double native_data_020d9014','extern const float native_data_020d9014'));negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or 'illegal constant expression' not in negative.stdout:raise ValueError('Wrong float width double-array view passed actual compiler')
    return dict(status='passed',positive=positive,wrongWidth=dict(exitCode=negative.returncode,stdout=negative.stdout,stderr=negative.stderr))

def execute(rows):
    row=rows[0];pointers,imports=frozen_inputs();inventory=(ROOT/pointers['inventory']['path']).read_text();image=(ROOT/pointers['image']['path']).read_bytes();loads=(ROOT/pointers['relocations']['path']).read_text();negative=[]
    for name in imports['mapping']:
        rel=next(r for r in row['relocations'] if r['symbol']==name);binding=row['nativeSymbolEntries'][name]
        for label,key,value in [('address','address',hex(int(binding['address'],0)+4)),('mode','mode','thumb'),('CPU','processor','arm7'),('program','program','dwc/utility.bin/move/child.srl'),('module','module','ov000'),('kind','kind','data')]:
            wrong=copy.deepcopy(binding);wrong[key]=value
            try:helper(row,rel,wrong,imports,inventory)
            except ValueError as e:negative.append(dict(symbol=name,case=label,rejected=True,reason=str(e)))
            else:raise ValueError('Changed exact software-double helper admitted')
        wrong=copy.deepcopy(rel);wrong['symbol']=name+'_wrong'
        try:helper(row,wrong,binding,imports,inventory)
        except ValueError as e:negative.append(dict(symbol=name,case='unknown-helper',rejected=True,reason=str(e)))
        else:raise ValueError('Unknown software-double helper admitted')
    name='native_fn_02022664'
    for label,key,value in [('mode','mode','thumb'),('module','module','ov000'),('kind','kind','data')]:
        wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[name][key]=value
        try:verify_original(row,wrong)
        except ValueError as e:negative.append(dict(case='source-call-'+label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed original floating absolute-value entry admitted')
    array_cases=[]
    for case in pointers['cases']:
        if case['symbolAddress']=='0x20ec9b0':continue
        rel=next(r for r in row['relocations'] if r['offset']==case['offset']);changed=bytearray(image);changed[int(case['symbolAddress'],0)-0x2000000]^=1
        try:validate(case,row,rel,row['nativeSymbolEntries'][rel['symbol']],bytes(changed),inventory,loads,pointers['adpcmTables'])
        except ValueError as e:array_cases.append(dict(address=case['symbolAddress'],case='changed-original-array-or-NaN-byte',rejected=True,reason=str(e)))
        else:raise ValueError('Changed original constant table/NaN admitted')
    verify_original(row,row['nativeSymbolEntries']);return dict(status='passed',negativeBranchHelperCases=negative,pointerCases=negative_controls(rows),changedArrayCases=array_cases,actualCompilerGeometry=geometry(row),ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
