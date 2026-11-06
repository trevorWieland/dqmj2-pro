from wave20261106_dwc_auth_next_sixth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
import copy
import hashlib
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_auth_next_sixth_compiler import COMPILER,compare
from wave20261106_dwc_auth_next_sixth_bindings import verify_original,negative_controls
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile


def geometry(row):
    assert_owned(LANE,SOURCE,WORK);folder=WORK/'geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(WMBssDesc)==192','(u32)&((WMBssDesc*)0)->rssi==2','(u32)&((WMBssDesc*)0)->ssidLength==10','(u32)&((WMBssDesc*)0)->ssid==12','(u32)&((WMBssDesc*)0)->capaInfo==44','(u32)&((WMBssDesc*)0)->channel==54','sizeof(tagACFL)==4','sizeof(tagACWORK)==3352','(u32)&((tagACWORK*)0)->findList==1092','(u32)&((tagACWORK*)0)->bssDesc==1136','(u32)&((tagACWORK*)0)->findListNum==3346'];wrong=text.replace('u16 beaconPeriod,dtimPeriod,channel;','u16 beaconPeriod,dtimPeriod,padding,channel;',1)
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef wcmBuffer\n#undef socConfig\n#undef netCheck\n#undef acHold\n#undef acWork\n'+'\n'.join('typedef char Layout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(checks))+'\ntagACWORK bitfieldGeometry={.powerMode=3,.authMode=2,.aroundCount=9,.connectType=5,.skipNetCheck=2,.duplicateFlag=1};\n');obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Actual consumed Auth/CAL layout failed',positive.stdout,positive.stderr))
    with obj.open('rb') as stream:
        elf=ELFFile(stream);symbol=next(x for x in elf.get_section_by_name('.symtab').iter_symbols() if x.name=='bitfieldGeometry');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if len(raw)!=3352 or raw[3339:3341]!=bytes([0x9b,0x65]):raise ValueError('Actual compiler bitfield byte layout differs')
    if wrong==text:raise ValueError('Meaningful wrong layout did not mutate')
    (folder/'context.h').write_text(wrong);negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if negative.returncode==0:raise ValueError('Wrong actual Auth/CAL layout admitted')
    return dict(address=row['address'],checks=checks,positiveExitCode=0,actualWorkBitfieldBytes='9b65',bitfieldOffsets=[3339,3340],wrongLayoutRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout)


def prototype_presence(row):
    folder=WORK/'required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def allocated(path):
        with path.open('rb') as stream:return [(s.name,s['sh_flags'],s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&2]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or allocated(obj)!=allocated(ROOT/row['object']):raise ValueError(('Required actual prototypes failed or changed allocated caller/context',positive.stdout,positive.stderr))
    if row['address']=='0x2095630':return dict(address=row['address'],positiveExitCode=0,actualExecutableAndInitializedContextSectionsUnchanged=True,diagnosticFlags=flags,externalProviderNegativeApplicable=False,reason='Pure complete source body has no imported calls; exact typed field layout and wrong complete C behavior controls apply.',primaryFlagsUnchanged=True,sourceCredit=0)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name={'0x2094ab0':'native_fn_020949e4','0x209545c':'native_fn_020946ec'}[row['address']];changed=text.replace(name+'(','missing_callable_declaration(',1)
    if changed==text:raise ValueError('Actual provider declaration did not mutate')
    header.write_text(changed);negative_obj=folder/'missing.o'
    if negative_obj.exists():negative_obj.unlink()
    negative=subprocess.run([str(COMPILER),*flags,'-c',str(wrong),'-o',str(negative_obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or negative_obj.exists() or 'no prototype' not in negative.stdout:raise ValueError(('Actual missing provider declaration admitted',negative.stdout,negative.stderr))
    return dict(address=row['address'],positiveExitCode=0,actualExecutableAndInitializedContextSectionsUnchanged=True,diagnosticFlags=flags,missingActualProvider=name,negativeExitCode=negative.returncode,negativeStdout=negative.stdout,primaryFlagsUnchanged=True,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],requiredPrototypeDiagnostics=[prototype_presence(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
