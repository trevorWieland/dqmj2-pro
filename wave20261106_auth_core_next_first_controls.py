import os
import shutil
import subprocess
from project import ROOT,write_json
from wave20261106_auth_core_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_auth_core_next_first_build import build
from wave20261106_auth_core_next_first_bindings import negative_controls
from wave20261106_auth_core_next_first_compiler import COMPILER
from wave20261106_auth_core_next_first_fixtures import run,helper_specs
from elftools.elf.elffile import ELFFile


def allocated(path):
    with path.open('rb')as stream:return [(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&2]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);result=negative_controls(rows);env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));prototypes=[];wrong=[];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text())
    changes={34166648: ('header', 'WCM_PHASE_IDLE 3', 'WCM_PHASE_IDLE 4'), 34166808: ('source', 'i < 13', 'i < 12'), 34166884: ('header', 'AC_PHASE_SEARCH_AROUND 3', 'AC_PHASE_SEARCH_AROUND 7'), 34167056: ('header', 'DWC_AC_SEARCH_START_CHANNEL1 0', 'DWC_AC_SEARCH_START_CHANNEL1 1'), 34167124: ('header', 'SEARCH_AROUND_TIME_OUT 300', 'SEARCH_AROUND_TIME_OUT 304'), 34167248: ('source', 'wk->count = 0', 'wk->count = 1')}
    seeds={34166808: 14, 34166884: 3, 34167248: 0}
    for row in rows:
        address=int(row['address'],0);folder=WORK/'controls'/format(address,'08x');folder.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];target=folder/'wrong.c'
        for item in row['sourceDependencies']:shutil.copyfile(ROOT/item['path'],folder/(ROOT/item['path']).name)
        command=[str(COMPILER),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(folder/'required.o')];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
        if process.returncode or allocated(folder/'required.o')!=allocated(ROOT/row['object']):raise ValueError(('Actual required prototypes failed or changed caller',process.stdout,process.stderr))
        prototypes.append(dict(address=row['address'],positiveExitCode=0,actualAllocatedPayloadUnchanged=True,primaryFlagsUnchanged=True))
        target.write_bytes(source.read_bytes());kind,left,right=changes[address];path=folder/'context.h'if kind=='header'else target;text=path.read_text();changed=text.replace(left,right,1)
        if changed==text:raise ValueError(('Meaningful whole-C mutation absent',row['address']))
        path.write_text(changed,encoding='utf-8');bad,body=build(target,folder/'link',negative=True);semantic=False;reason='Opaque provider remains unexecuted; complete genuinely linked changed C body rejects.'
        if address in seeds:
            try:run(image,row,body,seeds[address],specs)
            except ValueError as error:semantic=True;reason=str(error)
            if not semantic:raise ValueError('Wrong complete C escaped independent semantic model')
        wrong.append(dict(address=row['address'],exactCallerBytes=False,genuineLink=bad['realLink'],semanticModelRejected=semantic,reason=reason))
    folder=WORK/'geometry';folder.mkdir(parents=True,exist_ok=True);header=ROOT/rows[0]['sourceDependencies'][0]['path'];text=header.read_text();(folder/'context.h').write_text(text,encoding='utf-8')
    checks=['sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(u64)==8','sizeof(void*)==4','sizeof(DWCBmApInfo)==240','sizeof(DWCMemPage)==256','sizeof(tagACWORK)==3352','sizeof(tagACHOLD)==36','sizeof(SOCInAddr)==4','sizeof(IWConfig)==16','(u32)&((IWConfig*)0)->pbdbuffer==4','(u32)&((IWConfig*)0)->nbdbuffer==8','(u32)&((IWConfig*)0)->nbdmode==12','(u32)&((tagACHOLD*)0)->endType==21','(u32)&((tagACHOLD*)0)->errorTest==16','(u32)&((tagACWORK*)0)->timeOut==3248','(u32)&((tagACWORK*)0)->searchList==768','(u32)&((tagACWORK*)0)->findList==1092','(u32)&((tagACWORK*)0)->connectApType==3341','(u32)&((tagACWORK*)0)->searchListNo==3343','(u32)&((tagACWORK*)0)->searchListNum==3344','(u32)&((tagACWORK*)0)->searchChannel==3345','(u32)&((tagACWORK*)0)->findListNum==3346','(u32)&((tagACWORK*)0)->connectNo==3347','(u32)&((tagACWORK*)0)->count==3349','(u32)&((tagACWORK*)0)->stealthChannel==3350','(u32)&((DWCBmApInfo*)0)->ip==192','(u32)&((DWCBmApInfo*)0)->dns==200','sizeof(WMBssDesc)==192','(u32)&((WMBssDesc*)0)->bssid==4','(u32)&((WMBssDesc*)0)->ssid==12','(u32)&((WMBssDesc*)0)->channel==54']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char L'+str(i)+'[('+value+')?1:-1];'for i,value in enumerate(checks))+'\ntagACWORK bitfieldGeometry={.powerMode=3,.authMode=2,.aroundCount=9,.connectType=5,.skipNetCheck=2,.duplicateFlag=1};\n',encoding='utf-8');command=[str(COMPILER),*rows[0]['compilerFlags'],'-c',str(source),'-o',str(folder/'layout.o')];positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode:raise ValueError(('Actual consumed AC geometry failed',positive.stdout,positive.stderr))
    with(folder/'layout.o').open('rb')as stream:
        elf=ELFFile(stream);symbol=next(v for v in elf.get_section_by_name('.symtab').iter_symbols()if v.name=='bitfieldGeometry');payload=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if len(payload)!=3352 or payload[3339:3341]!=bytes([0x9b,0x65]):raise ValueError('Actual consumed AC bitfield bytes differ')
    wrong_header=text.replace('tagACFL findList[11]','tagACFL findList[12]',1)
    if wrong_header==text:raise ValueError('Meaningful actual field layout mutation absent')
    (folder/'context.h').write_text(wrong_header,encoding='utf-8');negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0:raise ValueError('Wrong actual AC field geometry admitted')
    result.update(wholeCNegativeControls=wrong,wholeCNegativeControlsRejected=len(wrong),requiredPrototypeProofs=prototypes,geometry=dict(checks=checks,positiveExitCode=0,bitfieldBytes='9b65',wrongContextRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout),actualStandaloneOriginalEntryExecutions=0,oldCompilerAndNormalizerUnchanged=True);write_json(LANE/'binding-layout-controls.json',result);return result
