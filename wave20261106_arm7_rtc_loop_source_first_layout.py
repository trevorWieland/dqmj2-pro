import os
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json,sha256
from wave20261106_arm7_rtc_loop_source_first_build import SOURCE,WORK,FLAGS,COMPILER

FIELDS={'027f60b4':{'RTCImportedView':['opaquePrefix','work','work.msgQueue','work.busy','work.command'],'RTCWork':['msgQueue','msgArray','thread','stack','busy','command'],'RTCRawData':['t.date','t.time','a.status1','a.status2','a.pulse','a.alarm','a.adjust','a.free'],'OSSystemWork':['real_time_clock']}}



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


def all_layouts(directory):return {tag:evaluate(tag,directory/tag)for tag in FIELDS}


if __name__=='__main__':
    result=all_layouts(WORK/'layout-baseline');write_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-rtc-loop-next/first/layout-baseline.json',result)
    for tag,value in result.items():print(tag,len(value['fields']))
