import os
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json,sha256
from wave20261106_arm7_wl_source_coherent_build import SOURCE,WORK,FLAGS,COMPILER

FIELDS={
'027f4b88':{'WL_MAN':['ApList'],'AP_LIST':['rssi','channel','capaInfo','bssid','ssidLength','ssid','beaconInterval','lifeTime'],'BEACON_FRAME':['MacHeader.Rx.rsv_RSSI','Dot11Header.BSSID','Body.BeaconInterval','Body.CapaInfo.Data'],'SSID_ELEMENT':['ID','Length','SSID']},
'027f1888':{'WL_MAN':['HeapMan.TmpBuf','Work.CapaInfo'],'WlMaDataReq':['header.code','frame'],'ASSRES_FRAME':['FirmHeader.Length','MacHeader.Tx.MPDU','Dot11Header.FrameCtrl.Data','Dot11Header.DA','Body.CapaInfo.Data','Body.StatusCode','Body.AID','Body.Buf'],'SSID_ELEMENT':['ID','Length','SSID']},
'027f1be8':{'WL_MAN':['HeapMan.TmpBuf','Work.BeaconPeriod','Work.CapaInfo','Work.CurrChannel','Work.GameInfoLength','Work.GameInfoAdrs','Work.GameInfoAlign','Config.ActiveZone'],'WlMaDataReq':['header.code','frame'],'PRBRES_FRAME':['FirmHeader.Length','MacHeader.Tx.MPDU','Dot11Header.FrameCtrl.Data','Body.BeaconInterval','Body.CapaInfo.Data','Body.Buf']},
'027f0484':{'WL_MAN':['Work.Mode','Work.STA','MLME.State','Counter.tx.success','Counter.tx.failed','Counter.tx.retry','Counter.tx.unicast','Counter.tx.multicast','Counter.tx.wep','HeapMan.TxPri[1]','HeapMan.TxPri[1].Count','TxCtrl.Txq[1].Busy','Config.MaxStaNum','CamMan.NotSetTIM','MLME.Work.DisAss.pTxFrm','MLME.pCfm.DisAss','MLME.Work.DeAuth.pTxFrm','MLME.pCfm.DeAuth'],'TXFRM':['FirmHeader.CamAdrs','FirmHeader.FrameId','MacHeader.Tx.Status','MacHeader.Tx.rsv_RetryCount','MacHeader.Tx.MPDU','Dot11Header.FrameCtrl.Data','Dot11Header.Adrs1'],'AUTH_FRAME':['Body.AlgoType','Body.SeqNum','Body.StatusCode'],'ASSRES_FRAME':['Body.StatusCode','Body.AID','Dot11Header.DA']}}


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
    result=all_layouts(WORK/'layout-baseline');write_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-next/coherent/layout-baseline.json',result)
    for tag,value in result.items():print(tag,value['fields'])
