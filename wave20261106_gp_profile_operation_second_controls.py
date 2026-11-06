import match_runtime
import os
import shutil
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json
from wave20261106_gp_profile_operation_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gp_profile_operation_second_compiler import COMPILER
from wave20261106_gp_profile_operation_second_bindings import negative_controls
from wave20261106_gp_profile_operation_second_build import build
from wave20261106_gp_profile_operation_second_fixtures import run,case_count


def allocated(path):
    with path.open('rb')as stream:return[(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&2]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=4:raise ValueError('Exact four identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);wrong=[];prototypes=[];layouts=[]
    for row in rows:
        source=ROOT/row['source'];name=format(int(row['address'],0),'08x');directory=folder/name;directory.mkdir(parents=True,exist_ok=True)
        for p in source.parent.iterdir():
            if p.suffix=='.h':shutil.copyfile(p,directory/p.name)
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(directory/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(directory/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual prototypes missing or payload changed',process.stdout,process.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,allocatedPayloadUnchanged=True,primaryFlagsUnchanged=True))
        left,right={'020aab70':('&connClosed, GPITrue','&connClosed, GPIFalse'),'020b27a0':('GPI_PROFILE_SEARCH 3','GPI_PROFILE_SEARCH 4'),'020b28c0':('GPI_NOT_ACCEPTING 2','GPI_NOT_ACCEPTING 3'),'020b2a38':('dest[len - 1]','dest[len - 2]')}[name]
        target=directory/'wrong.c';target.write_bytes(source.read_bytes());path=directory/'context.h'if name in['020b27a0','020b28c0']else target;before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
        if before==after:raise ValueError('Meaningful ordinary-C mutation absent')
        path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);rejected=0;returns=0
        for seed in range(case_count(int(row['address'],0))):
            observed=run(image,row,body,seed,strict=False);returns+=observed['actualReturn'];rejected+=not observed['modelPassed']
        if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError('Wrong complete C escaped independent model')
        wrong.append(dict(address=row['address'],exactCallerBytes=False,genuineLink=bad['realLink'],actualWrongCallerReturns=returns,independentModelRejections=rejected,semanticModelRejected=True,sourceCredit=0))
        (directory/'context.h').write_bytes(source.with_name('context.h').read_bytes())
        checks={'020aab70':['sizeof(void*)==4','sizeof(GPIProfileList)==12','(u32)&((GPIConnection*)0)->cmSocket==496','(u32)&((GPIConnection*)0)->socketBuffer==504','(u32)&((GPIConnection*)0)->inputBuffer==520','(u32)&((GPIConnection*)0)->inputBufferSize==524','(u32)&((GPIConnection*)0)->outputBuffer==528','(u32)&((GPIConnection*)0)->loginTicket==1552','sizeof(((GPIConnection*)0)->loginTicket)==25','(u32)&((GPIConnection*)0)->kaTransmit==1584'],'020b27a0':['sizeof(void*)==4','sizeof(GPISearchData)==340','(u32)&((GPISearchData*)0)->processing==320','(u32)&((GPISearchData*)0)->remove==324','sizeof(GPIOperation)==36','(u32)&((GPIOperation*)0)->pnext==32','(u32)&((GPIOperation*)0)->result==28','(u32)&((GPIConnection*)0)->numSearches==568','(u32)&((GPIConnection*)0)->operationList==1476'],'020b28c0':['sizeof(void*)==4','sizeof(GPITransferID)==12','(u32)&((GPITransferID*)0)->profileid==0','(u32)&((GPITransferID*)0)->count==4','(u32)&((GPITransferID*)0)->time==8'],'020b2a38':['sizeof(void*)==4','sizeof(size_t)==4']}[name]
        layout=directory/'layout.c';layout.write_text('#include "context.h"\n'+('#undef sock\n#undef rcvlen\n#undef rcvmax\n#undef rcvbuffer\n'if name=='020b30c8'else'')+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(checks))+'\n',encoding='utf-8');argv=[str(COMPILER),*row['compilerFlags'],'-c',str(layout),'-o',str(directory/'layout.o')];positive=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if positive.returncode:raise ValueError(('Consumed geometry differs',positive.stdout,positive.stderr))
        good=layout.read_text(encoding='utf-8');layout.write_text(good.replace('sizeof(void*)==4','sizeof(void*)==8',1),encoding='utf-8');negative=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if negative.returncode==0:raise ValueError('Wrong width geometry admitted')
        layouts.append(dict(address=row['address'],checks=checks,positiveExitCode=0,wrongWidthRejected=True,negativeExitCode=negative.returncode))
    manager=next(r for r in rows if int(r['address'],0)==0x020aab70);source=ROOT/manager['source'];context_dir=WORK/'standard-header-control';context_dir.mkdir(parents=True,exist_ok=True)
    for h in source.parent.glob('*.h'):shutil.copyfile(h,context_dir/h.name)
    target=context_dir/'wrong.c';target.write_bytes(source.read_bytes());header=context_dir/'context.h';header.write_text(header.read_text(encoding='utf-8')+'\n#define strstr native_fn_0201d984\n#define memcpy native_fn_0201b19c\n#define memmove native_fn_0201b1bc\n#define strncmp native_fn_0201d914\n#define atoi native_fn_0201f274\n',encoding='utf-8');context_row,context_body=build(target,context_dir/'link',negative=True)
    for seed in range(case_count(0x020aab70)):run(image,manager,context_body,seed)
    result['standardHeaderContext']=dict(standardHeaderBytes=668,nativeAliasHeaderBytes=context_row['compiledBytes'],sameImportedMachineABIs=True,boundedSemanticVectors=case_count(0x020aab70),semanticVectorsPassButExactNativeBodyRejected=True,genuineLink=context_row['realLink'],sourceCredit=0,unusedLayoutFieldsDoNotConferTypeTruth=True)
    from wave20261106_gp_profile_operation_second_embedded import inspect
    row=rows[0];embedded=ROOT/row['realLink']['linkedElf'];payload=(embedded.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_operation_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(embedded,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad ELF caller storage admitted')
    result.update(embeddedCallerStorageNegativeControls=elf_controls,wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototypes,geometry=layouts,actualStandaloneOriginalEntryExecutions=0,actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
