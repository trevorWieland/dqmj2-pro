import os
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime
from elftools.elf.elffile import ELFFile
from wave20261106_arm7_wm_residual_next_third_build import SOURCE,LANE,WORK,COMPILER,FLAGS
FIELDS={
 '027e03d0':{'WMStatus':['MacAddress','enableChannel','rate','mode','wep_flag','wepMode','wepKeyId','wepKey','preamble'],'WlParamSetAllReq':['staMacAdrs','retryLimit','enableChannel','rate','mode','wepMode','wepKeyId','wepKey','authAlgo','beaconType','probeRes','beaconLostTh','activeZoneTime','ssidMask','preambleType'],'WlParamSetCfm':['resultCode']},
 '027e0520':{'WMSPWork':['rssiHistory','rssiIndex'],'OSSystemWork':['wm_rssi_pool']},
 '027e5c5c':{'WMStatus':['v_tsf','v_tsf_bak','v_remain','VSyncFlag','mp_childVCount']},
 '027e5dc0':{'WMStatus':['v_remain','VSyncFlag','mp_childVCount']},
 '027e5e80':{'WMStatus':['mp_flag','mp_childVCount','mp_lifeTimeTick','mp_lastRecvTick'],'WMSPWork':['requestQ'],'WMIndCallback':['apiid','errcode','state','reason']},
 '027e5f98':{'WMStatus':['valarm_counter','mp_parentVCount']}}
CONSTANTS={
 '027e03d0':['WM_APIID_START_SCAN_EX'],
 '027e0520':[],
 '027e5c5c':[],
 '027e5dc0':[],
 '027e5e80':['WM_APIID_AUTO_DISCONNECT','WM_DISCONNECT_REASON_MP_LIFETIME','WM_APIID_INDICATION','WM_ERRCODE_FIFO_ERROR','WM_STATECODE_FIFO_ERROR'],
 '027e5f98':[]}


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
