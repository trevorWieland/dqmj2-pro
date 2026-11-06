import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_auth_resume_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_auth_resume_next_first_build import build
from wave20261106_auth_resume_next_first_bindings import negative_controls
from wave20261106_auth_resume_next_first_compiler import COMPILER
from wave20261106_auth_resume_next_first_fixtures import run,helper_specs
from elftools.elf.elffile import ELFFile


def allocated(path):
    with path.open('rb')as stream:return [(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&2]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));prototypes=[];wrong=[];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text())
    for row in rows:
        address=int(row['address'],0);folder=WORK/'controls'/format(address,'08x');folder.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];target=folder/'wrong.c'
        for item in row['sourceDependencies']:shutil.copyfile(ROOT/item['path'],folder/(ROOT/item['path']).name)
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(folder/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(folder/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual required prototypes failed or changed caller',process.stdout,process.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,explicitImportedPrototypesRequired=True,actualAllocatedPayloadUnchanged=True,primaryCompilerFlagsUnchanged=True))
        text=source.read_text();replacements={0x02096174:('pos, 10','pos, 9'),0x02096258:('&(temp[3])','&(temp[4])'),0x02096288:('i < 3','i < 2'),0x0209636c:('(long)63','(long)62'),0x020963b4:('destsize >=','destsize >')};left,right=replacements[address];changed=text.replace(left,right,1)
        if changed==text:raise ValueError(('Meaningful wrong complete C mutation absent',row['address'],left))
        target.write_text(changed,encoding='utf-8');bad,body=build(target,folder/'link',negative=True);semantic=False;reason='MD5 provider remains unexecuted; complete genuine linked body rejects changed digest-copy offset.'
        if address!=0x02096258:
            seeds=[47]if address==0x0209636c else [1]if address==0x02096174 else [0]
            for seed in seeds:
                try:run(image,row,body,seed,specs)
                except ValueError as error:semantic=True;reason=str(error);break
            if not semantic:raise ValueError('Wrong complete C escaped independent algorithm model')
        wrong.append(dict(address=row['address'],source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=bad['object'],objectSha256=bad['objectSha256'],exactCallerBytes=False,genuineLink=bad['realLink'],semanticModelRejected=semantic,reason=reason))
    folder=WORK/'geometry';folder.mkdir(parents=True,exist_ok=True);header=ROOT/rows[0]['sourceDependencies'][0]['path'];text=header.read_text();(folder/'context.h').write_text(text,encoding='utf-8');checks=['sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(void*)==4','sizeof(U4B)==4','sizeof(MATHMD5Context)==88','(u32)&((MATHMD5Context*)0)->length==16','(u32)&((MATHMD5Context*)0)->buffer8==24','sizeof(ShopKeys)==16','(u32)&((ShopKeys*)0)->shmask0==0','(u32)&((ShopKeys*)0)->mask0==4','(u32)&((ShopKeys*)0)->shmask1==8','(u32)&((ShopKeys*)0)->mask1==12'];path=folder/'layout.c';path.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(checks))+'\n',encoding='utf-8');command=[str(COMPILER),*rows[0]['compilerFlags'],'-c',str(path),'-o',str(folder/'layout.o')];positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual source type geometry failed',positive.stdout,positive.stderr))
    changed=text.replace('u32 state[4]','u32 state[5]',1)
    if changed==text:raise ValueError('Wrong actual context did not mutate')
    (folder/'context.h').write_text(changed,encoding='utf-8');negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong actual MD5 context geometry admitted')
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),actualStandaloneOriginalEntryExecutions=0,requiredPrototypeProofs=prototypes,geometry=dict(checks=checks,positiveExitCode=0,wrongContextRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout),sharedCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
