import os
import shutil
import subprocess
from project import ROOT,read_json,sha256,write_json
from wave20261105_arm7_wm_port_next_build import SOURCE,LANE,WORK,COMPILER,FLAGS
import match_runtime
from elftools.elf.elffile import ELFFile
FIELDS={'WMmpRecvHeader':[],'WMmpRecvData':[],'WMSPWork':['status'],'WMStatus':['state','aid','sendQueueMutex','sendQueueData','sendQueueFreeList','readyQueue','sendQueue','sendQueueInUse','mp_current_defaultRetryCount','child_bitmap','mp_readyBitmap','mp_sendSize','mp_sendBuf','mp_sendBufSize','mp_recvSize','mp_recvBufSize','mp_count','mp_limitCount','mp_current_minPollBmpMode','mp_current_singlePacketMode','mp_newFrameFlag','mp_pingFlag','mp_parentVCount','mp_prevPollBitmap','mp_prevWmHeader','mp_prevTxop','mp_prevDataLength','mp_setDataFlag','VSyncFlag','portSeqNo','mp_parentSize','mp_childSize'],'WMPortSendQueueData':['next','port','destBitmap','restBitmap','sentBitmap','sendingBitmap','data','size','callback','arg','seqNo','retryCount'],'WMPortSendQueue':['head','tail'],'WMPortRecvCallback':['apiid','errcode','state','port','recvBuf','data','length','aid','myAid','seqNo','maxSendDataSize','maxRecvDataSize'],'WMPortSendCallback':['apiid','errcode','state','port','destBitmap','restBitmap','sentBitmap','size','data','callback','arg','seqNo','maxSendDataSize','maxRecvDataSize'],'WlMaMpCfm':['resultCode'],'WlMaKeyDataCfm':['resultCode']}
CONSTANTS=['WM_STATE_MP_PARENT','WM_STATE_MP_CHILD','WM_ERRCODE_INVALID_PARAM','WM_ERRCODE_SEND_QUEUE_FULL','WM_ERRCODE_OPERATING','WM_ERRCODE_SUCCESS','WM_ERRCODE_FAILED','WM_ERRCODE_SEND_FAILED','WM_APIID_PORT_SEND','WM_APIID_PORT_RECV','WM_STATECODE_PORT_SEND','WM_STATECODE_PORT_RECV']


def compile_unit(source,output):
    p=subprocess.run([str(COMPILER),*FLAGS,'-c',str(source),'-o',str(output)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(('WM port fresh layout/ABI C compile failed',p.stdout,p.stderr))


def evaluate(directory,headers=None):
    directory.mkdir(parents=True,exist_ok=True)
    for p in SOURCE.glob('*.h'):
        if headers is None:shutil.copyfile(p,directory/p.name)
        else:(directory/p.name).write_text(headers[p.name])
    expressions=[];keys=[]
    for typ,fields in FIELDS.items():
        keys.append((typ,'sizeof'));expressions.append('sizeof('+typ+')')
        for name in fields:keys += [(typ,name),(typ,name+'.width')];expressions += ['(u32)&(('+typ+'*)0)->'+name,'sizeof((('+typ+'*)0)->'+name+')']
    keys += [('constants',n) for n in CONSTANTS];expressions+=CONSTANTS;source=directory/'layout.c';source.write_text('\n'.join('#include "'+p.name+'"' for p in sorted(SOURCE.glob('*.h')))+'\nconst u32 port_layout[]={'+','.join(expressions)+'};\n');output=directory/'layout.o';compile_unit(source,output)
    with output.open('rb') as stream:
        elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name=='port_layout');raw=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
    values=[int.from_bytes(raw[i:i+4],'little') for i in range(0,len(raw),4)];data={}
    if len(keys)!=len(values):raise ValueError('Closed WM port layout vector mismatch')
    for (typ,name),value in zip(keys,values):data.setdefault(typ,{})[name]=value
    return dict(status='passed',sourceCredit=0,fields=data,sourceSha256=sha256(source),objectSha256=sha256(output),limits=['Compiler layout witnesses verify closed C types; original allocation/storage sizes are not proved or credited. Exact original caller accesses independently constrain used field widths and offsets.'])


if __name__=='__main__':
    result=evaluate(WORK/'layout');write_json(LANE/'layout-baseline.json',result);print(result['fields'],flush=True)
