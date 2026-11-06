import match_runtime
import os
import shutil
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json
from wave20261106_gp_profile_operation_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gp_profile_operation_first_compiler import COMPILER
from wave20261106_gp_profile_operation_first_bindings import negative_controls
from wave20261106_gp_profile_operation_first_build import build
from wave20261106_gp_profile_operation_first_fixtures import run,case_count


def allocated(path):
    with path.open('rb')as stream:return[(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&2]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=5:raise ValueError('Exact five identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);wrong=[];prototypes=[];layouts=[]
    for row in rows:
        source=ROOT/row['source'];name=format(int(row['address'],0),'08x');directory=folder/name;directory.mkdir(parents=True,exist_ok=True)
        for p in source.parent.iterdir():
            if p.suffix=='.h':shutil.copyfile(p,directory/p.name)
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(directory/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(directory/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual prototypes missing or payload changed',process.stdout,process.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,allocatedPayloadUnchanged=True,primaryFlagsUnchanged=True))
        left,right={'020b0cd4':('29901','29902'),'020b0e04':('data->type = type;','data->type = type + 1;'),'020b2908':('arg->result = GP_NO_ERROR;','arg->result = GP_SERVER_ERROR;'),'020b29a0':('arg->result = GP_NO_ERROR;','arg->result = GP_SERVER_ERROR;'),'020b30c8':('rcvlen -= processed;','rcvlen = processed;')}[name]
        target=directory/'wrong.c';target.write_bytes(source.read_bytes());path=directory/'context.h'if name=='020b0cd4'else target;before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
        if before==after:raise ValueError('Meaningful ordinary-C mutation absent')
        path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);rejected=0;returns=0
        for seed in range(case_count(int(row['address'],0))):
            observed=run(image,row,body,seed,strict=False);returns+=observed['actualReturn'];rejected+=not observed['modelPassed']
        if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError('Wrong complete C escaped independent model')
        wrong.append(dict(address=row['address'],exactCallerBytes=False,genuineLink=bad['realLink'],actualWrongCallerReturns=returns,independentModelRejections=rejected,semanticModelRejected=True,sourceCredit=0))
        (directory/'context.h').write_bytes(source.with_name('context.h').read_bytes())
        checks=['sizeof(void*)==4','sizeof(u32)==4']if name!='020b30c8'else['sizeof(void*)==4','sizeof(u32)==4','sizeof(StatsReceiveView)==48','(u32)&((StatsReceiveView*)0)->rcvlen==8','(u32)&((StatsReceiveView*)0)->rcvmax==24','(u32)&((StatsReceiveView*)0)->rcvbuffer==40','(u32)&((StatsReceiveView*)0)->state==44','sizeof(StatsInitializedView)==8','(u32)&((StatsInitializedView*)0)->sock==4']
        if name in['020b0cd4','020b0e04']:checks+=['sizeof(GPISearchData)==340','(u32)&((GPISearchData*)0)->inputBuffer==8','(u32)&((GPISearchData*)0)->outputBuffer==24','(u32)&((GPISearchData*)0)->processing==320','(u32)&((GPISearchData*)0)->remove==324','(u32)&((GPISearchData*)0)->searchStartTime==328','sizeof(GPIOperation)==36','(u32)&((GPIOperation*)0)->data==4','(u32)&((GPIOperation*)0)->state==20']
        if name=='020b0cd4':checks+=['sizeof(struct sockaddr_in)==8','(u32)&((struct sockaddr_in*)0)->sin_family==1','(u32)&((struct sockaddr_in*)0)->sin_port==2','(u32)&((struct sockaddr_in*)0)->sin_addr.s_addr==4','(u32)&((struct hostent*)0)->h_addr_list==12']
        if name in['020b2908','020b29a0']:checks+=['sizeof(GPICallback)==8','sizeof(GPIOperation)==36','(u32)&((GPIOperation*)0)->callback==12','sizeof(GPRegisterUniqueNickResponseArg)==4','sizeof(GPRegisterCdKeyResponseArg)==4']
        layout=directory/'layout.c';layout.write_text('#include "context.h"\n'+('#undef sock\n#undef rcvlen\n#undef rcvmax\n#undef rcvbuffer\n'if name=='020b30c8'else'')+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(checks))+'\n',encoding='utf-8');argv=[str(COMPILER),*row['compilerFlags'],'-c',str(layout),'-o',str(directory/'layout.o')];positive=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if positive.returncode:raise ValueError(('Consumed geometry differs',positive.stdout,positive.stderr))
        good=layout.read_text(encoding='utf-8');layout.write_text(good.replace('sizeof(void*)==4','sizeof(void*)==8',1),encoding='utf-8');negative=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if negative.returncode==0:raise ValueError('Wrong width geometry admitted')
        layouts.append(dict(address=row['address'],checks=checks,positiveExitCode=0,wrongWidthRejected=True,negativeExitCode=negative.returncode))
    from wave20261106_gp_profile_operation_first_embedded import inspect
    row=rows[0];embedded=ROOT/row['realLink']['linkedElf'];payload=(embedded.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_operation_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(embedded,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad ELF caller storage admitted')
    result.update(embeddedCallerStorageNegativeControls=elf_controls,wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototypes,geometry=layouts,actualStandaloneOriginalEntryExecutions=0,actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
