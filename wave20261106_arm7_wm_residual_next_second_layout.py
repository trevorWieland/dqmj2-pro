import os
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime
from elftools.elf.elffile import ELFFile
from wave20261106_arm7_wm_residual_next_second_build import SOURCE,LANE,WORK,COMPILER,FLAGS
FIELDS={
 '027e386c':{'WMStatus':['state','pInfoBuf','scan_channel','enableChannel','miscFlags','mode','preamble','pwrMgtMode'],'WMStartScanExReq':['scanBuf','scanBufSize','channelList','bssid','maxChannelTime','scanType','ssidLength','ssid','ssidMatchLength'],'WMStartScanExCallback':['apiid','errcode','state','bssDescCount','channelList','bssDesc','linkLevel'],'WlDevGetStationStateCfm':['resultCode','state'],'WlMlmeScanCfm':['resultCode','bssDescCount','bssDescList'],'WMBssDesc':['length','rssi','ssidLength','ssid'],'WlBssDesc':[],'WlMlmeScanReq':[],'WlCmdHeader':[]},
 '027e3ed0':{'WMStatus':['state','miscFlags','enableChannel','rate','preamble','mode','pwrMgtMode'],'WMArm7Buf':['connectPInfo'],'WMBssDesc':['channel','rateSet','capaInfo','gameInfoLength','beaconPeriod','gameInfo'],'WMGameInfo':['attribute'],'WMStartConnectReq':['pInfo','powerSave','authMode','ssid'],'WMStartConnectCallback':['apiid','errcode','state']},
 '027e4be0':{'WMStatus':['state','mp_ignoreSizePrecheckMode','mp_maxSendSize','mp_maxRecvSize','aid','pparam','mode','allowedChannel','mp_flag','mp_waitAckFlag','mp_vsyncOrderedFlag','mp_vsyncFlag','mp_newFrameFlag','mp_pingFlag','mp_pingCounter','sendQueueInUse','mp_setDataFlag','mp_sentDataFlag','mp_bufferEmptyFlag','mp_isPolledFlag','mp_resumeFlag','mp_recvBuf','mp_recvBufSize','mp_recvBufSel','mp_sendBuf','mp_sendBufSize','mp_count','mp_limitCount','mp_prevPollBitmap','mp_prevWmHeader','minRssi','rssiCounter','mp_lastRecvTick','valarm_queuedFlag','mp_maxFreq','mp_minFreq','mp_freq','mp_current_maxFreq','mp_current_minFreq','mp_current_freq','mp_current_defaultRetryCount','mp_current_minPollBmpMode','mp_current_singlePacketMode','mp_current_ignoreFatalErrorMode','mp_defaultRetryCount','mp_minPollBmpMode','mp_singlePacketMode','mp_ignoreFatalErrorMode'],'WMParentParam':['maxEntry'],'WMStartMPReq':['recvBuf','recvBufSize','sendBuf','sendBufSize','param','tmpParam'],'WMStartMPCallback':['apiid','errcode','state'],'WMMPTmpParam':['mask','maxFrequency','minFrequency','frequency','defaultRetryCount','minPollBmpMode','singlePacketMode','ignoreFatalErrorMode']}}
CONSTANTS={
 '027e386c':['WM_APIID_START_SCAN_EX','WM_STATE_IDLE','WM_STATE_CLASS1','WM_STATE_SCAN','WM_STATECODE_PARENT_NOT_FOUND','WM_STATECODE_PARENT_FOUND','WM_ERRCODE_ILLEGAL_STATE','WM_ERRCODE_INVALID_PARAM'],
 '027e3ed0':['WM_APIID_START_CONNECT','WM_STATECODE_CONNECT_START','WM_ERRCODE_NO_ENTRY'],
 '027e4be0':['WM_APIID_START_MP','WM_STATECODE_MP_START','WM_STATE_CHILD','WM_STATE_PARENT','WM_STATE_MP_CHILD','WM_STATE_MP_PARENT']}


def compile_unit(source,obj):
    p=subprocess.run([str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(('Actual closed WM request ABI/layout compile failed',p.stdout,p.stderr))


def evaluate(entry,directory,headers=None):
    directory.mkdir(parents=True,exist_ok=True);sourceDir=SOURCE/entry
    for p in sourceDir.glob('*.h'):(directory/p.name).write_text(p.read_text() if headers is None else headers[p.name])
    expressions=[];keys=[]
    for typ,fields in FIELDS[entry].items():
        expressions.append('sizeof('+typ+')');keys.append((typ,'sizeof'))
        for name in fields:expressions += ['(u32)&(('+typ+'*)0)->'+name,'sizeof((('+typ+'*)0)->'+name+')'];keys += [(typ,name),(typ,name+'.width')]
    expressions+=CONSTANTS[entry];keys += [('constants',n) for n in CONSTANTS[entry]];text='\n'.join('#include "'+p.name+'"' for p in sorted(sourceDir.glob('*.h')))+'\nconst u32 geometry[]={'+','.join(expressions)+'};\n';source=directory/'layout.c';obj=directory/'layout.o';source.write_text(text);compile_unit(source,obj)
    with obj.open('rb') as stream:
        elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name=='geometry');raw=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
    values=[int.from_bytes(raw[i:i+4],'little') for i in range(0,len(raw),4)];fields={}
    if len(values)!=len(keys):raise ValueError('ABI/layout vector size differs')
    for (typ,name),value in zip(keys,values):fields.setdefault(typ,{})[name]=value
    return dict(fields=fields,sourceSha256=sha256(source),objectSha256=sha256(obj),sourceCredit=0)


def all_layouts(directory):return {entry:evaluate(entry,directory/entry) for entry in sorted(FIELDS)}


if __name__=='__main__':
    result=all_layouts(WORK/'layout');write_json(LANE/'layout-baseline.json',result);print({k:v['fields'] for k,v in result.items()},flush=True)
