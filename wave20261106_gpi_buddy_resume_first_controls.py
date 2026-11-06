import os
import shutil
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json
from wave20261106_gpi_buddy_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_compiler import COMPILER
from wave20261106_gpi_buddy_resume_first_bindings import negative_controls
from wave20261106_gpi_buddy_resume_first_build import build
from wave20261106_gpi_buddy_resume_first_fixtures import run,case_count


def allocated(path):
    with path.open('rb')as stream:return[(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&2]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=3:raise ValueError('Exact two grid-controller identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);wrong=[];prototype_proofs=[]
    for row in rows:
        source=ROOT/row['source'];text=source.read_text(encoding='utf-8');header=ROOT/row['sourceDependencies'][0]['path'];name=format(int(row['address'],0),'08x')
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(folder/(name+'-required.o'))];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(folder/(name+'-required.o'))!=allocated(ROOT/row['object']):raise ValueError(('Required actual prototypes failed/changed code',process.stdout,process.stderr))
        prototype_proofs.append(dict(address=row['address'],positiveExitCode=0,actualAllocatedPayloadUnchanged=True,primaryFlagsUnchanged=True))
        mutations={'020abf18':[('copy-bound','source','sizeof(buffer));','sizeof(buffer)-1);')],'020abfe4':[('route-threshold','source','type < 100','type < 101'),('buddy-port-layout','header','u16 buddyPort;','u16 beforePort,buddyPort;')],'020ac0d8':[('reply-type','source','GPI_BM_KEYS_REPLY, message','104, message')]}[name]
        for label,kind,left,right in mutations:
            directory=folder/label;directory.mkdir(parents=True,exist_ok=True);target=directory/'wrong.c';target.write_text(text,encoding='utf-8');(directory/'context.h').write_bytes(header.read_bytes());(directory/'string.h').write_bytes(header.with_name('string.h').read_bytes());path=target if kind=='source'else directory/'context.h';before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
            if before==after:raise ValueError('Meaningful whole-C mutation absent')
            path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);rejected=0;returns=0;partial=0
            for seed in range(case_count(int(row['address'],0))):
                observed=run(image,row,body,seed,strict=False);returns+=observed['actualReturn'];partial+=0;rejected+=not observed['modelPassed']
            if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError('Wrong complete C escaped independent caller/prefix model')
            wrong.append(dict(label=label,exactCallerBytes=False,genuineLink=bad['realLink'],actualWrongCallerReturns=returns,actualWrongPartialStops=partial,independentModelRejections=rejected,semanticModelRejected=True,sourceCredit=0))
    row=rows[0];header=ROOT/row['sourceDependencies'][0]['path']
    context_row=next(r for r in rows if int(r['address'],0)==0x020ac0d8);directory=folder/'arbitrary-strcmp-name';directory.mkdir(parents=True,exist_ok=True);source=ROOT/context_row['source'];target=directory/'context.c';target.write_bytes(source.read_bytes());(directory/'context.h').write_text(source.with_name('context.h').read_text(encoding='utf-8')+'\n#define strcmp native_fn_0201d800\n',encoding='utf-8');(directory/'string.h').write_bytes(source.with_name('string.h').read_bytes());context_bad,context_body=build(target,directory/'link',negative=True)
    context_cases=[run(image,context_row,context_body,i)for i in range(case_count(int(context_row['address'],0)))];context_proof=dict(status='passed',actualStandardHeader='string.h',actualPrototype='int strcmp(const char*,const char*)',arbitraryFunctionNameHasSameABI=True,arbitraryNameWholeNativeMatchRejected=True,arbitraryNameCompleteReturningVectors=len(context_cases),sameBoundedCallerSemantics=True,genuineNonmatchingLink=context_bad['realLink'],actualProviderBodyAndSourceCredit=0,meaning='Known standard strcmp context preserves the escaped message pointer across the read-only comparison. Native instruction order and full bytes agree only with the standard header context; names alone do not establish an arbitrary provider ABI.')
    directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True);actual_header=header.read_text(encoding='utf-8');(directory/'context.h').write_text(actual_header,encoding='utf-8');(directory/'string.h').write_bytes(header.with_name('string.h').read_bytes());checks=['sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(void*)==4','sizeof(GPIBuffer)==16','(u32)&((GPIConnection*)0)->sessKey==0x198','(u32)&((GPIConnection*)0)->outputBuffer==0x210','sizeof(((GPIConnection*)0)->sessKey)==4','(u32)&((GPIPeer*)0)->state==0','(u32)&((GPIPeer*)0)->profile==16','(u32)&((GPIProfile*)0)->buddyStatusInfo==12','(u32)&((GPIProfile*)0)->peerSig==28','(u32)&((GPIBuddyStatusInfo*)0)->buddyPort==32','sizeof(((GPIBuddyStatusInfo*)0)->buddyPort)==2'];layout=directory/'layout.c';layout.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+value+')?1:-1];'for i,value in enumerate(checks))+'\n',encoding='utf-8');command=[str(COMPILER),*row['compilerFlags'],'-c',str(layout),'-o',str(directory/'layout.o')];positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual consumed record/page geometry differs',positive.stdout,positive.stderr))
    (directory/'context.h').write_text(actual_header.replace('u16 buddyPort;','u16 beforePort,buddyPort;',1),encoding='utf-8');negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong consumed record geometry admitted')
    from wave20261106_gpi_buddy_resume_first_embedded import inspect
    embedded=ROOT/row['realLink']['linkedElf'];payload=(embedded.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in [('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_grid_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(embedded,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad actual embedded ELF caller mapping admitted')
    result['embeddedCallerStorageNegativeControls']=elf_controls
    result['standardStringHeaderContextProof']=context_proof
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototype_proofs,geometry=dict(checks=checks,positiveExitCode=0,wrongContextRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout),actualStandaloneOriginalEntryExecutions=0,actualWrongCallerReturns=sum(item['actualWrongCallerReturns']for item in wrong),actualWrongPartialStops=sum(item['actualWrongPartialStops']for item in wrong),separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
