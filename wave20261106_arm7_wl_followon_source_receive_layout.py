import os
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json,sha256
from wave20261106_arm7_wl_followon_source_receive_build import SOURCE,WORK,FLAGS,COMPILER

FIELDS={
'027ec7f8':{'WL_MAN':['Config.Mode','Work.STA','MLME.Work.Scan.MaxConfirmLength','MLME.State','MLME.pReq.Scan','MLME.pCfm.Scan'],'WlMlmeScanReq':['ssidLength','scanType','channelList','maxChannelTime','bssidMaskCount','bssid','ssid'],'WlCmdCfm':['header.length'],'WlMlmeScanCfm':[],'WlBssDesc':[]},
'027ed634':{'WL_MAN':['MLME.pCfm.Auth','MLME.State'],'WlMlmeAuthCfm':['resultCode','statusCode']},
'027edfa0':{'WL_MAN':['HeapMan.TmpBuf','Work.GameInfoLength','Work.GameInfoAdrs','Work.GameInfoAlign'],'WlMlmeBeaconRecvInd':['header.code','header.length','rssi','rate','srcMacAdrs','gameInfoLength','gameInfo'],'RXFRM':['MacHeader.Rx.rsv_RSSI','MacHeader.Rx.Service_Rate','Dot11Header.Adrs2']},
'027f2778':{'WL_MAN':['Work.STA','Work.BSSID','Work.LinkAdrs','HeapMan.TmpBuf','RxCtrl.TxKeyReg'],'RXFRM':['FirmHeader.Length','MacHeader.Rx.MPDU','Dot11Header.Adrs2','Dot11Header.Adrs3'],'WlMaMpAckInd':['header.code','header.length','ack.txKeySts'],'WlRxMpAckFrame':[]},
'027f3148':{'WL_MAN':['Config.MaxStaNum'],'PRBREQ_FRAME':['Dot11Header.SA','Dot11Header.BSSID','MacHeader.Rx.Status','Body.Buf','FirmHeader.Length'],'ELEMENT_CHECKER':['pElement','bodyLength','foundFlag','matchFlag']},
'027f35cc':{'WL_MAN':['Work.Mode','Work.STA','MLME.pReq.Auth','MLME.pCfm.Auth','MLME.State','Config.AuthAlgo','TxCtrl.Txq[0].Busy','TxCtrl.Txq[1].Busy','TxCtrl.Txq[2].Busy','RxCtrl.IcvOkCntFlag','WlOperation'],'AUTH_FRAME':['FirmHeader.Length','FirmHeader.CamAdrs','MacHeader.Rx.Status','Dot11Header.SA','Dot11Header.FrameCtrl.Data','Body','Body.AlgoType','Body.SeqNum','Body.StatusCode','Body.ChallengeText.ID','Body.ChallengeText.Length','Body.ChallengeText.Text'],'WlMlmeAuthReq':['algorithm','peerMacAdrs'],'WlMlmeAuthCfm':['resultCode','statusCode']}}



def evaluate(tag,directory,headers=None):
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.suffix in ['.c','.h']:(directory/path.name).write_text((headers or {}).get(path.name,path.read_text()))
    expressions=[];labels=[]
    for typ,fields in FIELDS[tag].items():
        labels.append((typ,'sizeof'));expressions.append('sizeof('+typ+')')
        for field in fields:
            labels.extend([(typ+'.'+field,'offset'),(typ+'.'+field,'width')]);expressions.extend(['(u32)&(('+typ+'*)0)->'+field,'sizeof((('+typ+'*)0)->'+field+')'])
    source=directory/'geometry.c';obj=directory/'geometry.o';source.write_text('#include "main.c"\nu32 geometry[]={'+','.join(expressions)+'};\n'+('u32 bitfield_abi(WL_MAN *p,u32 value){p->Config.BcSsidResponse=value;return p->Config.BcSsidResponse;}\n'if tag=='027f3148'else''));argv=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(('Fresh closed WL C geometry rejected',p.stdout,p.stderr))
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='geometry');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']];values=struct.unpack('<'+'I'*len(labels),raw)
    fields={name+'.'+kind:value for(name,kind),value in zip(labels,values)}
    if tag=='027f3148':fields.update(bitfield(obj))
    return dict(fields=fields,sourceSha256=sha256(source),objectSha256=sha256(obj),sourceCredit=0)


def bitfield(obj):
    import unicorn
    from unicorn import arm_const as R
    with obj.open('rb')as stream:
        elf=ELFFile(stream);sym=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='bitfield_abi');code=elf.get_section(sym['st_shndx']).data()[sym['st_value']:sym['st_value']+sym['st_size']]
    def execute(value,fill):
        vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,code);initial=bytes([fill])*1684;vm.mem_write(0x02001000,initial);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,0x02001000);vm.reg_write(R.UC_ARM_REG_R1,value);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02004000);stores=[];vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda v,a,at,width,data,user:stores.append((at-0x02001000,width)));vm.emu_start(0x02000000,0x02004000,count=128)
        if vm.reg_read(R.UC_ARM_REG_PC)!=0x02004000:raise ValueError('Actual bitfield ABI did not return')
        return bytes(vm.mem_read(0x02001000,1684)),vm.reg_read(R.UC_ARM_REG_R0),stores
    raw,value,stores=execute(1,0)
    if len(stores)!=1 or stores[0][1]!=2:raise ValueError('Actual unsigned16 bitfield store width differs')
    offset=stores[0][0];mask=int.from_bytes(raw[offset:offset+2],'little')
    if value!=1 or mask==0 or mask&(mask-1)or any(raw[:offset]+raw[offset+2:]):raise ValueError('Actual BeaconType is not exactly one bit in its16-bit container')
    for fill in [0,0x5a,255]:
        for value in [0,1,2,3,65535]:
            actual,returned,observed=execute(value,fill);expected=bytearray([fill])*1684;word=int.from_bytes(expected[offset:offset+2],'little');expected[offset:offset+2]=((word&~mask)|mask*(value&1)).to_bytes(2,'little')
            if actual!=expected or returned!=value&1 or observed!=stores:raise ValueError('Actual closed BeaconType bitfield ABI differs')
    return {'WL_MAN.Config.BcSsidResponse.containerOffset':offset,'WL_MAN.Config.BcSsidResponse.containerBytes':2,'WL_MAN.Config.BcSsidResponse.bitMask':mask,'WL_MAN.Config.BcSsidResponse.actualFreshReturns':15}


def all_layouts(directory):return {tag:evaluate(tag,directory/tag)for tag in FIELDS}


if __name__=='__main__':
    result=all_layouts(WORK/'layout-baseline');write_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-followon-next/receive/layout-baseline.json',result)
    for tag,value in result.items():print(tag,len(value['fields']))
