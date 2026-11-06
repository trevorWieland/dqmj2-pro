import os
import subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256

WORK=ROOT/'work/arm7-bulk-20261030/lane-channel-lock-callback'
SOURCE=ROOT/'nonmatching/arm7-bulk/20261031/lane-channel-lock-callback/native_channel_lock_probe_callback.c'
ADDRESS,LOG=0x023C7000,0x023C7800
TEXT='''typedef unsigned int u32;
extern volatile u32 fixture_records[49];
void native_channel_lock_probe_callback(void *channel,int reason,void *argument)
{
    u32 index=fixture_records[0];
    fixture_records[1+index*3]=(u32)channel;
    fixture_records[2+index*3]=(u32)reason;
    fixture_records[3+index*3]=(u32)argument;
    fixture_records[0]=index+1;
}
'''



def build(variant=None):
    import crossreuse_utility_c
    directory=WORK if variant is None else WORK/'controls'/variant
    source=SOURCE if variant is None else directory/'native_channel_lock_probe_callback.c'
    text=TEXT
    if variant=='swapped-pointers':
        text=text.replace('(u32)channel;','(u32)temporary;').replace('(u32)argument;','(u32)channel;').replace('(u32)temporary;','(u32)argument;')
    elif variant is not None:
        raise ValueError('Unqualified destructor callback negative variant')
    source.parent.mkdir(parents=True,exist_ok=True)
    if source.exists() and source.read_text()!=text:
        raise ValueError('Synthetic callback probe source changed')
    source.write_text(text)
    directory.mkdir(parents=True,exist_ok=True)
    compiler=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
    linker=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
    if sha256(linker)!='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise ValueError('Synthetic probe linker pin differs')
    flags=match_runtime.FLAGS[:]
    flags[flags.index('-proc')+1]='arm7tdmi'
    flags+=['-lang','c99']
    origin=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),name='native_channel_lock_probe_callback')
    attempt,compiled=crossreuse_utility_c.compile_origin(origin,compiler,flags,directory)
    if compiled is None:
        raise ValueError(attempt)
    entry,masks,payload=compiled
    if len(entry['relocations'])!=1 or entry['relocations'][0]['symbol']!='fixture_records' or entry['relocations'][0]['type']!=2:
        raise ValueError('Synthetic callback is not one bounded leaf with a log-word relocation')
    original=ROOT/entry['probeObject']
    caller=directory/'probe.o'
    caller.write_bytes(original.read_bytes())
    lcf=directory/'probe.lcf'
    lcf.write_text('MEMORY { CALL: ORIGIN = 0x023c7000 > probe.bin }\nSECTIONS { .probe: { probe.o(.text) } > CALL\nfixture_records = 0x023c7800; }\n')
    elf_path=directory/'probe.elf'
    command=[str(linker),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main',origin['name'],str(lcf),str(caller),'-o',str(elf_path)]
    result=subprocess.run(command,cwd=directory,capture_output=True,text=True,timeout=30,
        env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError('Synthetic callback link failed: '+result.stdout+result.stderr)
    body=(directory/'probe.bin').read_bytes()
    with elf_path.open('rb') as stream:
        elf=ELFFile(stream)
        symbol=next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name==origin['name'])
        if symbol['st_value']!=ADDRESS or symbol['st_size']!=len(body) or len(body)!=len(payload):
            raise ValueError('Synthetic callback compiled/linked extent differs')
    code=len(body)-4
    if entry['relocations'][0]['offset']!=code or int.from_bytes(body[code:],'little')!=LOG:
        raise ValueError('Synthetic callback log pool location differs')
    return body,dict(source=origin['source'],sourceSha256=origin['sourceSha256'],compiler=entry['compiler'],compilerSha256=entry['compilerSha256'],
        compilerFlags=flags,object=entry['probeObject'],objectSha256=entry['probeObjectSha256'],linkerSha256=sha256(linker),linkCommand=command,
        lcfSha256=sha256(lcf),linkedElfSha256=sha256(elf_path),linkedBodySha256=sha256(directory/'probe.bin'),address=hex(ADDRESS),codeBytes=code,
        bytes=len(body),logAddress=hex(LOG),sourceCredit=0,originalCalleeCredit=0,syntheticCallbackContract=True,physicalArgumentWords=3,
        limitation='Compiled test callback is an explicit synthetic boundary, never original ROM source or an original-native callee')


if __name__=='__main__':
    body,proof=build()
    print(proof)
