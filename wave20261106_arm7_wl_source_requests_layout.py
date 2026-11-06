import os
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json,sha256
from wave20261106_arm7_wl_source_requests_build import SOURCE,WORK,FLAGS,COMPILER

FIELDS={
'027ec938':{'WL_MAN':['Config.Mode','Work.STA','MLME.State','MLME.pReq.Join','MLME.pCfm.Join'],'WlMlmeJoinReq':['timeOut','bssDesc.bssid','bssDesc.ssidLength','bssDesc.ssid','bssDesc.beaconPeriod','bssDesc.dtimPeriod','bssDesc.channel','bssDesc.rateSet.basic','bssDesc.rateSet.support','bssDesc.capaInfo'],'WlCmdCfm':['header.length'],'WlMlmeJoinCfm':[]},
'027ef5f8':{'WL_MAN':['Config.Mode','Config.WepMode','Work.APCamAdrs','Work.IntervalCount','Work.FrameCtrl','Work.BSSID','CamMan.PowerMgtMode','CamMan.NotClass3','HeapMan.RequestCmd','HeapMan.TxPri[0]'],'WlMaDataReq':['frame.length','frame'],'TXFRM':['FirmHeader.CamAdrs','FirmHeader.FrameTime','FirmHeader.Length','MacHeader.Tx.rsv_AppRate','MacHeader.Tx.Service_Rate','MacHeader.Tx.MPDU','Dot11Header.FrameCtrl.Data','Dot11Header.Adrs1','Dot11Header.Adrs2','Dot11Header.Adrs3']}}



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
    result=all_layouts(WORK/'layout-baseline');write_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-next/requests/layout-baseline.json',result)
    for tag,value in result.items():print(tag,value['fields'])
