import os
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json,sha256
from wave20261106_arm7_wl_configuration_source_software_build import SOURCE,WORK,FLAGS,COMPILER

FIELDS={
'027e8da8':{'HEAPBUF_MAN':['Head','Count'],'HEAPBUF_HEADER':['Next']},
'027e8de8':{'WL_MAN':['Config','Work','Config.pCAM','Config.CamMaxStaNum','Config.MaxStaNum','Work.GameInfoAdrs']},
'027e8f3c':{'WL_MAN':['Config.Mode','Work.Mode','Work.PowerMgtMode','Config.ParamFlag']},
'027e95dc':{'WL_MAN':['Work.STA','Config.Mode','Work.SSIDLength','Work.SSID','Work.Ofst.Beacon.SSID','TxCtrl.Beacon.pMacFrm']},
'027e96ec':{'WL_MAN':['Work.BeaconPeriod','Config.FrameLifeTimePerBeacon']},
'027e9f60':{'WL_MAN':['Work.GameInfoAdrs','Work.GameInfoAlign','Work.GameInfoLength','Work.bUpdateGameInfo']},
'027ea048':{'WL_MAN':['Work.AID','Work.APCamAdrs']},
'027ec690':{'WL_MAN':['HeapMan.ToWM','HeapMan.ToWM.Head','HeapMan.ToWM.Count','pSendMsgQueue']},
'027ee438':{'WL_MAN':['Config.pCAM','Config.MaxStaNum'],'WlParamSetLifeTimeReq':['tableNumber','camLifeTime','frameLifeTime'],'WlCmdCfm':['header.length'],'WlStaElement':['maxLifeTime','lifeTime']}}



def evaluate(tag,directory,headers=None):
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.suffix in ['.c','.h']:(directory/path.name).write_text((headers or {}).get(path.name,path.read_text()))
    expressions=[];labels=[]
    for typ,fields in FIELDS[tag].items():
        labels.append((typ,'sizeof'));expressions.append('sizeof('+typ+')')
        for field in fields:
            labels.extend([(typ+'.'+field,'offset'),(typ+'.'+field,'width')]);expressions.extend(['(u32)&(('+typ+'*)0)->'+field,'sizeof((('+typ+'*)0)->'+field+')'])
    source=directory/'geometry.c';obj=directory/'geometry.o';source.write_text('#include "main.c"\nu32 geometry[]={'+','.join(expressions)+'};\n');argv=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(('Fresh closed WL C geometry rejected',p.stdout,p.stderr))
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='geometry');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']];values=struct.unpack('<'+'I'*len(labels),raw)
    fields={name+'.'+kind:value for(name,kind),value in zip(labels,values)}
    return dict(fields=fields,sourceSha256=sha256(source),objectSha256=sha256(obj),sourceCredit=0)


def all_layouts(directory):return {tag:evaluate(tag,directory/tag)for tag in FIELDS}


if __name__=='__main__':
    result=all_layouts(WORK/'layout-baseline');write_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-configuration-next/software/layout-baseline.json',result)
    for tag,value in result.items():print(tag,len(value['fields']))
