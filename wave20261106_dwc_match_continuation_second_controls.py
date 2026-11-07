import match_runtime
import os
import shutil
import subprocess
from project import ROOT,write_json
from wave20261106_dwc_match_continuation_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_continuation_second_compiler import COMPILER
from wave20261106_dwc_match_continuation_second_bindings import negative_controls
from wave20261106_dwc_match_continuation_second_build import build
from wave20261106_dwc_match_continuation_second_fixtures import run,case_count
from wave20261106_gp_profile_operation_first_controls import allocated

CHECKS=['sizeof(void*)==4','sizeof(OSTick)==8','sizeof(DWCMatchOptMinCompleteIn)==32','(u32)&((DWCMatchOptMinCompleteIn*)0)->valid==0','sizeof(((DWCMatchOptMinCompleteIn*)0)->valid)==1','(u32)&((DWCMatchOptMinCompleteIn*)0)->minEntry==1','(u32)&((DWCMatchOptMinCompleteIn*)0)->retry==2','(u32)&((DWCMatchOptMinCompleteIn*)0)->timeout==4','(u32)&((DWCMatchOptMinCompleteIn*)0)->recvBit==8','(u32)&((DWCMatchOptMinCompleteIn*)0)->timeoutBit==12','(u32)&((DWCMatchOptMinCompleteIn*)0)->startTime==16','(u32)&((DWCMatchOptMinCompleteIn*)0)->lastPollTime==24','sizeof(DWCMatchControl)==1156','(u32)&((DWCMatchControl*)0)->state==416','(u32)&((DWCMatchControl*)0)->clLinkProgress==420','(u32)&((DWCMatchControl*)0)->sbUpdateFlag==232','(u32)&((DWCMatchControl*)0)->sbUpdateTick==236','DWC_MATCH_STATE_SV_POLL_TIMEOUT==19','DWC_MATCH_TYPE_SC_SV==2','DWC_MATCH_TYPE_SC_CL==3']


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=1:raise ValueError('Exact option caller differs')
    row=rows[0];source=ROOT/row['source'];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(folder/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if process.returncode or allocated(folder/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual option prototypes failed/changed payload',process.stdout,process.stderr))
    wrong=[]
    for label,left,right in[('completion-count','qr2NumEntry = (u8)DWCi_GetMatchCnt()->gt2NumConnection;','qr2NumEntry = (u8)(DWCi_GetMatchCnt()->gt2NumConnection + 1);'),('reply-reset','stpOptMinComp->recvBit = 0;','stpOptMinComp->recvBit = 1;')]:
        directory=folder/label;directory.mkdir(parents=True,exist_ok=True)
        for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
        target=directory/'wrong.c';before=source.read_text(encoding='utf-8');after=before.replace(left,right,1)
        if before==after:raise ValueError('Meaningful option whole-C mutation absent')
        target.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);returns=0;partial=0;rejected=0
        for seed in range(case_count(int(row['address'],0))):
            v=run(image,row,body,seed,strict=False);returns+=v['actualReturn'];partial+=v['partialProviderStopped'];rejected+=not v['modelPassed']
        if not rejected or returns!=8 or partial!=1:raise ValueError('Wrong linked option C escaped independent full/partial model')
        wrong.append(dict(label=label,genuineLink=bad['realLink'],exactCallerBytes=False,actualWrongCallerReturns=returns,actualWrongPartialStops=partial,independentModelRejections=rejected,sourceCredit=0))
    directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True)
    for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
    path=directory/'layout.c';path.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(CHECKS))+'\n',encoding='utf-8');argv=[str(COMPILER),*row['compilerFlags'],'-c',str(path),'-o',str(directory/'layout.o')];positive=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual option/Match field geometry differs',positive.stdout,positive.stderr))
    header=directory/'types.h';before=header.read_text(encoding='utf-8');after=before.replace('OSTick startTime;','u32 startTime;',1)
    if before==after:raise ValueError('Actual option clock-width negative absent')
    header.write_text(after,encoding='utf-8');negative=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong option clock width admitted')
    from wave20261106_dwc_match_continuation_second_embedded import inspect
    elf=ROOT/row['realLink']['linkedElf'];payload=(elf.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_option_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(elf,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad actual option ELF mapping admitted')
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=sum(r['actualWrongPartialStops']for r in wrong),requiredPrototypeProofs=[dict(address=row['address'],positiveExitCode=0,allocatedPayloadUnchanged=True,primaryFlagsUnchanged=True)],geometry=dict(checks=CHECKS,positiveExitCode=0,wrongClockWidthRejected=True,negativeExitCode=negative.returncode),embeddedCallerStorageNegativeControls=elf_controls,actualStandaloneOriginalEntryExecutions=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True)
    write_json(LANE/'binding-layout-controls.json',result);return result
