import os
import shutil
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json
from wave20261106_gp_core_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gp_core_resume_first_compiler import COMPILER
from wave20261106_gp_core_resume_first_bindings import negative_controls
from wave20261106_gp_core_resume_first_build import build
from wave20261106_gp_core_resume_first_fixtures import run,case_count


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
        mutations={'020aa9b4':[('next-operation','source','nextOperationID = 2','nextOperationID = 3'),('keepalive-layout','header','unknownBeforeKeepalive[48]','unknownBeforeKeepalive[44]')],'020aced4':[('selector-modulus','header','rand()%62','rand()%61')],'020acf00':[('retry-limit','source','GPI_PEER_PORT + 100','GPI_PEER_PORT + 99'),('socket-layout','header','u8 sin_len,sin_family;','u8 sin_family,sin_len;')]}[name]
        for label,kind,left,right in mutations:
            directory=folder/label;directory.mkdir(parents=True,exist_ok=True);target=directory/'wrong.c';target.write_text(text,encoding='utf-8');(directory/'context.h').write_bytes(header.read_bytes());(directory/'string.h').write_bytes(header.with_name('string.h').read_bytes());path=target if kind=='source'else directory/'context.h';before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
            if before==after:raise ValueError('Meaningful whole-C mutation absent')
            path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);rejected=0;returns=0;partial=0
            for seed in range(case_count(int(row['address'],0))):
                observed=run(image,row,body,seed,strict=False);returns+=observed['actualReturn'];partial+=0;rejected+=not observed['modelPassed']
            if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError('Wrong complete C escaped independent caller/prefix model')
            wrong.append(dict(label=label,exactCallerBytes=False,genuineLink=bad['realLink'],actualWrongCallerReturns=returns,actualWrongPartialStops=partial,independentModelRejections=rejected,semanticModelRejected=True,sourceCredit=0))
    row=rows[0];header=ROOT/row['sourceDependencies'][0]['path']
    directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True);actual_header=header.read_text(encoding='utf-8');(directory/'context.h').write_text(actual_header,encoding='utf-8');(directory/'string.h').write_bytes(header.with_name('string.h').read_bytes());checks=['sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(void*)==4','sizeof(GPIBuffer)==16','(u32)&((GPIConnection*)0)->nick==272','(u32)&((GPIConnection*)0)->uniquenick==303','(u32)&((GPIConnection*)0)->email==324','(u32)&((GPIConnection*)0)->sessKey==408','(u32)&((GPIConnection*)0)->cmSocket==496','(u32)&((GPIConnection*)0)->connectState==500','(u32)&((GPIConnection*)0)->socketBuffer==504','(u32)&((GPIConnection*)0)->inputBuffer==520','(u32)&((GPIConnection*)0)->outputBuffer==528','(u32)&((GPIConnection*)0)->mHeader==544','(u32)&((GPIConnection*)0)->peerPort==560','(u32)&((GPIConnection*)0)->nextOperationID==564','(u32)&((GPIConnection*)0)->lastStatusState==572','(u32)&((GPIConnection*)0)->lastStatusString==952','(u32)&((GPIConnection*)0)->lastLocationString==1208','(u32)&((GPIConnection*)0)->fatalError==1468','(u32)&((GPIConnection*)0)->operationList==1476','(u32)&((GPIConnection*)0)->profileList.numBuddies==1488','(u32)&((GPIConnection*)0)->peerList==1492','(u32)&((GPIConnection*)0)->updateproBuffer==1504','(u32)&((GPIConnection*)0)->updateuiBuffer==1520','(u32)&((GPIConnection*)0)->kaTransmit==1584','sizeof(((GPIConnection*)0)->unknownBeforeKeepalive)==48'];layout=directory/'layout.c';layout.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+value+')?1:-1];'for i,value in enumerate(checks))+'\n',encoding='utf-8');command=[str(COMPILER),*row['compilerFlags'],'-c',str(layout),'-o',str(directory/'layout.o')];positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual consumed record/page geometry differs',positive.stdout,positive.stderr))
    (directory/'context.h').write_text(actual_header.replace('unknownBeforeKeepalive[48]','unknownBeforeKeepalive[44]',1),encoding='utf-8');negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong consumed record geometry admitted')
    startup=next(v for v in rows if int(v['address'],0)==0x020acf00);startup_source=ROOT/startup['source'];extra_dir=WORK/'socket-geometry';extra_dir.mkdir(parents=True,exist_ok=True)
    for name in['context.h','string.h']:(extra_dir/name).write_bytes(startup_source.with_name(name).read_bytes())
    socket_checks=['sizeof(struct sockaddr_in)==8','(u32)&((struct sockaddr_in*)0)->sin_family==1','sizeof(((struct sockaddr_in*)0)->sin_family)==1','(u32)&((struct sockaddr_in*)0)->sin_port==2','sizeof(((struct sockaddr_in*)0)->sin_port)==2','(u32)&((struct sockaddr_in*)0)->sin_addr.s_addr==4','(u32)&((struct hostent*)0)->h_addr_list==12','(u32)&((GPIOperation*)0)->state==20']
    socket_source=extra_dir/'layout.c';socket_source.write_text('#include "context.h"\n'+'\n'.join('typedef char S'+str(i)+'[('+check+')?1:-1];'for i,check in enumerate(socket_checks))+'\n',encoding='utf-8');socket_command=[str(COMPILER),*startup['compilerFlags'],'-c',str(socket_source),'-o',str(extra_dir/'layout.o')];socket_result=subprocess.run(socket_command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if socket_result.returncode:raise ValueError(('Actual consumed DS sockaddr/host/operation geometry differs',socket_result.stdout,socket_result.stderr))
    from wave20261106_gp_core_resume_first_embedded import inspect
    embedded=ROOT/row['realLink']['linkedElf'];payload=(embedded.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in [('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_grid_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(embedded,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad actual embedded ELF caller mapping admitted')
    result['embeddedCallerStorageNegativeControls']=elf_controls
    result['socketGeometry']=dict(checks=socket_checks,positiveExitCode=0,fullNativeStackArgumentBytesChecked=True)
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototype_proofs,geometry=dict(checks=checks,positiveExitCode=0,wrongContextRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout),actualStandaloneOriginalEntryExecutions=0,actualWrongCallerReturns=sum(item['actualWrongCallerReturns']for item in wrong),actualWrongPartialStops=sum(item['actualWrongPartialStops']for item in wrong),separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
