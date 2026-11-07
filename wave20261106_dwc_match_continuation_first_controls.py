import match_runtime
import os
import shutil
import subprocess
from project import ROOT,write_json
from wave20261106_dwc_match_continuation_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_continuation_first_compiler import COMPILER
from wave20261106_dwc_match_continuation_first_bindings import negative_controls,inputs,validate
from wave20261106_dwc_match_continuation_first_build import build
from wave20261106_dwc_match_continuation_first_fixtures import run,case_count
from wave20261106_gp_profile_operation_first_controls import allocated

MUTATIONS={'020a2afc':('match.c','i < DWC_MAX_CONNECTIONS','i < DWC_MAX_CONNECTIONS - 1'),'020a2b44':('match.c','listProfileID == profileID','listProfileID != profileID'),'020a2b98':('match.c','return SBServerGetIntValue(server, native_data_020e01f4, 0);','return 0;'),'020a2c38':('match.c','return 0xff;','return 0xfe;'),'020a2c80':('match.c','validAidBitmap & ~1','validAidBitmap & ~3'),'020a2cc8':('match.c','clWaitTimeoutCount = 0','clWaitTimeoutCount = 1'),'020a2ff8':('errors.h','#define DWC_ECODE_GS_GP (-1000)','#define DWC_ECODE_GS_GP (-1001)'),'020a304c':('errors.h','#define DWC_ECODE_GS_SB (-5000)','#define DWC_ECODE_GS_SB (-5001)'),'020a30b4':('errors.h','#define DWC_ECODE_GS_QR2 (-4000)','#define DWC_ECODE_GS_QR2 (-4001)'),'020a3528':('match.c','eval = 0x007fffff','eval = 0x007ffffe'),'020a3694':('match.c','DWCi_GetMathRand32(100)','DWCi_GetMathRand32(99)'),'020a37ac':('types.h','#define DWC_MATCHING_VERSION    3U','#define DWC_MATCHING_VERSION    4U')}
CHECKS=['sizeof(void*)==4','sizeof(u8)==1','sizeof(u32)==4','sizeof(OSTick)==8','sizeof(DWCMatchControl)==1156','(u32)&((DWCMatchControl*)0)->gt2NumConnection==13','(u32)&((DWCMatchControl*)0)->qr2NNFinishCount==20','(u32)&((DWCMatchControl*)0)->qr2MatchType==21','(u32)&((DWCMatchControl*)0)->qr2NumEntry==22','(u32)&((DWCMatchControl*)0)->qr2Reservation==32','(u32)&((DWCMatchControl*)0)->sbObj==228','(u32)&((DWCMatchControl*)0)->sbPidList==244','(u32)&((DWCMatchControl*)0)->aidList==720','(u32)&((DWCMatchControl*)0)->validAidBitmap==752','(u32)&((DWCMatchControl*)0)->friendList==764','(u32)&((DWCMatchControl*)0)->friendIdxList==772','(u32)&((DWCMatchControl*)0)->friendIdxListLen==836','(u32)&((DWCMatchControl*)0)->evalCallback==1140','(u32)&((DWCMatchControl*)0)->evalParam==1144','(u32)&((DWCMatchControl*)0)->clWaitTimeoutCount==429','sizeof(((DWCMatchControl*)0)->clWaitTimeoutCount)==1','(u32)&((DWCMatchControl*)0)->clWaitTime==504','sizeof(((DWCMatchControl*)0)->clWaitTime)==8','sizeof(DWCGameMatchKeyData)==12','(u32)&((DWCGameMatchKeyData*)0)->keyID==0','(u32)&((DWCGameMatchKeyData*)0)->isStr==1','(u32)&((DWCGameMatchKeyData*)0)->keyStr==4','(u32)&((DWCGameMatchKeyData*)0)->value==8','DWC_QR2_GAME_RESERVED_KEYS==154','sizeof(stGameMatchKeys)==1848']


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=12:raise ValueError('Exact twelve identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));folder=WORK/'controls';folder.mkdir(parents=True,exist_ok=True);wrong=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];name=format(int(row['address'],0),'08x');directory=folder/name;directory.mkdir(parents=True,exist_ok=True)
        for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(directory/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(directory/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual required prototypes failed/changed code',name,process.stdout,process.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,allocatedPayloadUnchanged=True,primaryFlagsUnchanged=True))
        target=directory/'wrong.c';target.write_bytes(source.read_bytes());file,left,right=MUTATIONS[name];path=target if file=='match.c'else directory/file;before=path.read_text(encoding='utf-8');after=before.replace(left,right,1)
        if before==after:raise ValueError('Meaningful whole-C/context mutation absent:'+name)
        path.write_text(after,encoding='utf-8');bad,body=build(target,directory/'link',negative=True);rejected=0;returns=0
        for seed in range(case_count(int(row['address'],0))):
            observed=run(image,row,body,seed,strict=False);returns+=observed['actualReturn'];rejected+=not observed['modelPassed']
        if not rejected or returns!=case_count(int(row['address'],0)):raise ValueError(('Wrong complete C escaped independent model',name,rejected,returns))
        wrong.append(dict(address=row['address'],exactCallerBytes=False,genuineLink=bad['realLink'],actualWrongCallerReturns=returns,independentModelRejections=rejected,semanticModelRejected=True,sourceCredit=0))
    row=rows[0];source=ROOT/row['source'];directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True)
    for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
    layout=directory/'layout.c';layout.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+v+')?1:-1];'for i,v in enumerate(CHECKS))+'\n',encoding='utf-8');command=[str(COMPILER),*row['compilerFlags'],'-c',str(layout),'-o',str(directory/'layout.o')];positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual consumed MatchControl/key-record geometry differs',positive.stdout,positive.stderr))
    header=directory/'types.h';good=header.read_text(encoding='utf-8');bad=good.replace('u8 keyID,isStr;','u16 keyID;u8 isStr;',1)
    if bad==good:raise ValueError('Actual key-field-width negative absent')
    header.write_text(bad,encoding='utf-8');negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong typed key-record width/offset admitted')
    qr=next(r for r in rows if int(r['address'],0)==0x020a37ac);value,image,inventory,records,imports=inputs();inventory_line=next(s for s in inventory.splitlines()if s.endswith('kind:bss addr:0x021d1ba8'));table_controls=[]
    for rel in qr['relocations']:
        if rel['symbol']!='stGameMatchKeys':continue
        binding=qr['nativeSymbolEntries']['stGameMatchKeys']
        try:validate(qr,rel,binding,value,image,inventory.replace(inventory_line,''),records,imports)
        except ValueError as error:table_controls.append(dict(origin=rel['offset'],originalAddend=rel['addend'],case='missing-original-BSS-record',rejected=True,reason=str(error)))
        else:raise ValueError('Original table-field load accepted without canonical BSS base')
    from wave20261106_dwc_match_continuation_first_embedded import inspect
    embedded=ROOT/row['realLink']['linkedElf'];payload=(embedded.parent/'caller.bin').read_bytes();elf_controls=[]
    for label,changes,expected in[('address',{'address':hex(int(row['address'],0)+4)},payload),('extent',{'compiledBytes':row['compiledBytes']+4},payload),('symbol',{'name':'wrong_match_entry'},payload),('payload',{},bytes([payload[0]^1])+payload[1:])]:
        try:inspect(embedded,dict(row,**changes),expected)
        except(ValueError,StopIteration)as error:elf_controls.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Bad ELF actual caller storage admitted')
    result.update(embeddedCallerStorageNegativeControls=elf_controls,wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototypes,geometry=dict(checks=CHECKS,positiveExitCode=0,wrongKeyRecordWidthRejected=True,negativeExitCode=negative.returncode),actualStandaloneOriginalEntryExecutions=0,actualWrongCallerReturns=sum(r['actualWrongCallerReturns']for r in wrong),actualWrongPartialStops=0,separateActualHelperReturnCredit=0,oldCompilerAndNormalizerUnchanged=True,tableFieldMissingInventoryControls=table_controls)
    write_json(LANE/'binding-layout-controls.json',result);return result
