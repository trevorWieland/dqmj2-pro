import match_runtime
import os
import shutil
import subprocess
from project import ROOT,write_json
from wave20261106_dwc_transport_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_transport_resume_first_compiler import COMPILER
from wave20261106_dwc_transport_resume_first_bindings import negative_controls
from wave20261106_dwc_transport_resume_first_build import build
from wave20261106_dwc_transport_resume_first_fixtures import run,case_count
from wave20261106_gp_profile_operation_first_controls import allocated

MUTATIONS={'020a3f84':('match.c','requestSendSize = size;','requestSendSize = size + 1;'),'020a40a4':('match.c','sendCallback = callback;','sendCallback = NULL;'),'020a40c0':('match.c','recvCallback = callback;','recvCallback = NULL;'),'020a40dc':('match.c','recvTimeoutCallback = callback;','recvTimeoutCallback = NULL;'),'020a4114':('match.c','return header.type;','return header.type + 1;'),'020a4144':('match.c','sizeof(DWCTransportHeader) + DWC_MATCH_SYN_DATA_BODY_SIZE','sizeof(DWCTransportHeader) + DWC_MATCH_SYN_DATA_BODY_SIZE + 1'),'020a4158':('match.c','recvTimeoutTime = time;','recvTimeoutTime = time + 1;'),'020a41dc':('match.c','pingCallback(latency, aid);','pingCallback(latency + 1, aid);'),'020a431c':('match.c','recvBufferSize = 0;','recvBufferSize = 1;'),'020a4404':('errors.h','#define DWC_ECODE_TYPE_TRANS_HEADER (-610)','#define DWC_ECODE_TYPE_TRANS_HEADER (-611)'),'020a449c':('match.c','recvBufferSize >= size','recvBufferSize > size'),'020a44f4':('match.c','requestRecvSize = header.size;','requestRecvSize = header.size + 1;'),'020a456c':('match.c','recvingSize += size;','recvingSize += size + 1;'),'020a45fc':('match.c','recvState = transConnection->lastRecvState;','recvState = 0;')}
CHECKS=['sizeof(void*)==4','sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(OSTick)==8','sizeof(DWCTransportConnection)==48','(u32)&((DWCTransportConnection*)0)->sendBuffer==0','(u32)&((DWCTransportConnection*)0)->recvBuffer==4','(u32)&((DWCTransportConnection*)0)->recvBufferSize==8','(u32)&((DWCTransportConnection*)0)->sendingSize==12','(u32)&((DWCTransportConnection*)0)->recvingSize==16','(u32)&((DWCTransportConnection*)0)->requestSendSize==20','(u32)&((DWCTransportConnection*)0)->requestRecvSize==24','(u32)&((DWCTransportConnection*)0)->sendState==28','(u32)&((DWCTransportConnection*)0)->recvState==29','(u32)&((DWCTransportConnection*)0)->lastRecvState==30','(u32)&((DWCTransportConnection*)0)->lastRecvType==34','sizeof(((DWCTransportConnection*)0)->lastRecvType)==2','(u32)&((DWCTransportConnection*)0)->previousRecvTick==36','(u32)&((DWCTransportConnection*)0)->recvTimeoutTime==44','sizeof(DWCTransportInfo)==1556','sizeof(((DWCTransportInfo*)0)->connections)==1536','(u32)&((DWCTransportInfo*)0)->sendCallback==1536','(u32)&((DWCTransportInfo*)0)->recvCallback==1540','(u32)&((DWCTransportInfo*)0)->recvTimeoutCallback==1544','(u32)&((DWCTransportInfo*)0)->pingCallback==1548','(u32)&((DWCTransportInfo*)0)->sendSplitMax==1552','sizeof(DWCTransportHeader)==8','(u32)&((DWCTransportHeader*)0)->size==0','(u32)&((DWCTransportHeader*)0)->type==4','(u32)&((DWCTransportHeader*)0)->magicStrings==6','sizeof(((DWCTransportHeader*)0)->magicStrings)==2']


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=14:raise ValueError('Exact fourteen transport identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);wrong=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];name=format(int(row['address'],0),'08x');directory=folder/name;directory.mkdir(parents=True,exist_ok=True)
        for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
        argv=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(directory/'required.o')];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if p.returncode or allocated(directory/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual transport prototypes failed/changed payload',name,p.stdout,p.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,allocatedPayloadUnchanged=True,primaryFlagsUnchanged=True));target=directory/'wrong.c';target.write_bytes(source.read_bytes());file,left,right=MUTATIONS[name];path=target if file=='match.c'else directory/file;before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
        if before==after:raise ValueError('Meaningful whole-C transport mutation absent:'+name)
        path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);returns=0;rejected=0
        for seed in range(case_count(int(row['address'],0))):
            v=run(image,row,body,seed,strict=False);returns+=v['actualReturn'];rejected+=not v['modelPassed']
        if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError(('Wrong linked transport C escaped independent model',name,returns,rejected))
        wrong.append(dict(address=row['address'],genuineLink=bad['realLink'],exactCallerBytes=False,actualWrongCallerReturns=returns,independentModelRejections=rejected,sourceCredit=0))
    row=rows[0];source=ROOT/row['source'];directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True)
    for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
    path=directory/'layout.c';path.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(CHECKS))+'\n',encoding='utf-8');argv=[str(COMPILER),*row['compilerFlags'],'-c',str(path),'-o',str(directory/'layout.o')];positive=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual release connection/transport/wire geometry differs',positive.stdout,positive.stderr))
    header=directory/'transport.h';before=header.read_text(encoding='utf-8');after=before.replace('u16 lastRecvType;','u32 lastRecvType;',1)
    if before==after:raise ValueError('Actual transport width negative absent')
    header.write_text(after,encoding='utf-8');negative=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong transport word/stride admitted')
    from wave20261106_dwc_transport_resume_first_embedded import inspect
    elf=ROOT/row['realLink']['linkedElf'];payload=(elf.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_transport_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(elf,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad actual transport ELF storage admitted')
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=0,requiredPrototypeProofs=prototypes,geometry=dict(checks=CHECKS,positiveExitCode=0,wrongTypeWidthAndStrideRejected=True,negativeExitCode=negative.returncode),embeddedCallerStorageNegativeControls=elf_controls,actualStandaloneOriginalEntryExecutions=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
