import match_runtime
import os
import shutil
import subprocess
from project import ROOT,write_json
from wave20261106_dwc_match_control_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_control_first_compiler import COMPILER
from wave20261106_dwc_match_control_first_bindings import negative_controls
from wave20261106_dwc_match_control_first_build import build
from wave20261106_dwc_match_control_first_fixtures import run,case_count
from wave20261106_gp_profile_operation_first_controls import allocated

MUTATIONS={'0209dfd8': ('match.c', '->profileID = profileID;', '->profileID = profileID + 1;'), '0209e0fc': ('match.c', '->evalParam = evalParam;', '->evalParam = NULL;'), '0209e258': ('match.c', '(u8)(distantFriend ? 1 : 0)', '(u8)0'), '0209e408': ('match.c', 'qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);', 'qr2_send_statechanged(NULL);'), '0209ed44': ('match.c', 'native_data_020e01bc, -1', 'native_data_020e01bc, -2'), '0209ef04': ('match.c', '->gt2ConnectCount = 0;', '->gt2ConnectCount = 1;')}
CHECKS=['sizeof(void*)==4', 'sizeof(DWCMatchControl)==1156', 'sizeof(struct qr2_implementation_s)==184', '(u32)&((struct qr2_implementation_s*)0)->userstatechangerequested==180', 'sizeof(((struct qr2_implementation_s*)0)->userstatechangerequested)==4', 'sizeof(MatchGlobalsView)==12', '(u32)&((MatchGlobalsView*)0)->option==0', '(u32)&((MatchGlobalsView*)0)->addFilter==8', 'sizeof(DWCConnectionInfo)==8', '(u32)&((DWCConnectionInfo*)0)->index==0', '(u32)&((DWCConnectionInfo*)0)->aid==1', '(u32)&((DWCConnectionInfo*)0)->reserve==2', '(u32)&((DWCConnectionInfo*)0)->param==4', 'sizeof(((DWCConnectionInfo*)0)->reserve)==2', 'DWC_MAX_CONNECTIONS==32', 'DWC_DNS_ERROR_RETRY_MAX==5', 'GT2DuplicateAddress==5', 'GT2TimedOut==6', 'QVERSION_QR2==1', 'DWC_ALLOCTYPE_BASE==4', '(u32)&((DWCMatchControl*)0)->pGt2Socket==4', '(u32)&((DWCMatchControl*)0)->gt2Callbacks==8', '(u32)&((DWCMatchControl*)0)->gt2ConnectCount==12', '(u32)&((DWCMatchControl*)0)->gt2NumConnection==13', '(u32)&((DWCMatchControl*)0)->qr2Obj==16', '(u32)&((DWCMatchControl*)0)->qr2MatchType==21', '(u32)&((DWCMatchControl*)0)->qr2Port==26', '(u32)&((DWCMatchControl*)0)->qr2IP==28', '(u32)&((DWCMatchControl*)0)->sbObj==228', '(u32)&((DWCMatchControl*)0)->sbPidList==244', '(u32)&((DWCMatchControl*)0)->nnFinishTime==396', '(u32)&((DWCMatchControl*)0)->state==416', '(u32)&((DWCMatchControl*)0)->distantFriend==422', '(u32)&((DWCMatchControl*)0)->cancelState==425', '(u32)&((DWCMatchControl*)0)->baseLatency==432', '(u32)&((DWCMatchControl*)0)->profileID==512', '(u32)&((DWCMatchControl*)0)->ipList==528', '(u32)&((DWCMatchControl*)0)->portList==656', '(u32)&((DWCMatchControl*)0)->aidList==720', '(u32)&((DWCMatchControl*)0)->gameName==756', '(u32)&((DWCMatchControl*)0)->secretKey==760', '(u32)&((DWCMatchControl*)0)->friendIdxList==772', '(u32)&((DWCMatchControl*)0)->friendIdxListLen==836', '(u32)&((DWCMatchControl*)0)->evalCallback==1140', '(u32)&((DWCMatchControl*)0)->evalParam==1144']


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=6:raise ValueError('Exact six Match-control identities differ')
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
    header=directory/'types.h';before=header.read_text(encoding='utf-8');after=before.replace('opaquePrefix[0xb4]','opaquePrefix[0xb0]',1)
    if before==after:raise ValueError('Actual transport width negative absent')
    header.write_text(after,encoding='utf-8');negative=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong transport word/stride admitted')
    from wave20261106_dwc_match_control_first_embedded import inspect
    elf=ROOT/row['realLink']['linkedElf'];payload=(elf.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_transport_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(elf,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad actual transport ELF storage admitted')
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=0,requiredPrototypeProofs=prototypes,geometry=dict(checks=CHECKS,positiveExitCode=0,wrongQR2FieldOffsetAndViewExtentRejected=True,negativeExitCode=negative.returncode),embeddedCallerStorageNegativeControls=elf_controls,actualStandaloneOriginalEntryExecutions=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
