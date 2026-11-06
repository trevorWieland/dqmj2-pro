import os
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime
from elftools.elf.elffile import ELFFile
from wave20261105_arm7_wm_requests_next_build import SOURCE,LANE,WORK,COMPILER,FLAGS
FIELDS={
 '027e609c':{'WMSPWork':['status','requestQ','wm7buf'],'WMStatus':['valarm_queuedFlag'],'WMIndCallback':['apiid','errcode','state','reason']},
 '027e614c':{'WMStatus':['state','valarm_queuedFlag','mp_newFrameFlag','rssiCounter','minRssi','linkLevel','child_bitmap','mp_count','mp_limitCount','mp_current_freq','mp_current_maxFreq','mp_current_minPollBmpMode','mp_pingCounter','mp_pingFlag','sendQueueInUse','mp_vsyncFlag']},
 '027e7cc8':{'WMStatus':['pparam'],'WMParentParam':['entryFlag','userGameInfoLength'],'WMGameInfo':[],'WMCallback':['apiid','errcode','wlCmdID','wlResult']},
 '027e7d58':{'WMCallback':['apiid','errcode','wlCmdID','wlResult'],'WlCmdCfm':['resultCode']},
 '027e8110':{'WMStatus':['enableChannel','allowedChannel','mp_lifeTimeTick','rate','preamble','wlVersion','macVersion','bbpVersion','rfVersion','MacAddress'],'WlParamGetEnableChannelCfm':['resultCode','enableChannel'],'WlDevGetVerInfoCfm':['resultCode','wlVersion','macVersion','bbpVersion','rfVersion'],'WlParamGetMacAdrsCfm':['resultCode','staMacAdrs']},
 '027e8320':{'WMStatus':['state'],'WMCallback':['apiid','errcode','wlCmdID','wlResult']},
 '027e83cc':{'WMMPParam':['mask'],'WMSetMPParameterReq':['param'],'WMSetMPParameterCallback':['apiid','errcode','mask','oldParam']},
 '027e87d8':{'WMStatus':['state','rate','parentMacAddress','MacAddress','dcf_destAdr','dcf_sendData','dcf_sendSize','dcf_sendFlag'],'WMCallback':['apiid','errcode','wlCmdID','wlResult'],'WlTxFrame':['frameId','length','rate','destAdrs','srcAdrs','datap']}}
CONSTANTS={
 '027e609c':['WM_APIID_VALARM_MP','WM_APIID_INDICATION','WM_ERRCODE_FIFO_ERROR','WM_STATECODE_FIFO_ERROR'],
 '027e614c':['WM_STATE_MP_PARENT','WM_STATE_MP_CHILD'],
 '027e7cc8':['WM_APIID_SET_ENTRY','WM_ERRCODE_SUCCESS','WM_ERRCODE_FAILED'],
 '027e7d58':['WM_APIID_AUTO_DEAUTH','WM_ERRCODE_SUCCESS','WM_ERRCODE_FAILED'],
 '027e8110':[],
 '027e8320':['WM_STATE_IDLE','WM_STATE_STOP','WM_APIID_POWER_OFF','WM_ERRCODE_ILLEGAL_STATE','WM_ERRCODE_FAILED'],
 '027e83cc':['WM_APIID_SET_MP_PARAMETER'],
 '027e87d8':['WM_STATE_DCF_CHILD','WM_APIID_SET_PS_MODE','WM_ERRCODE_ILLEGAL_STATE','WM_ERRCODE_FAILED']}


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
