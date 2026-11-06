import os
import struct
import subprocess
from pathlib import Path
import utility_code
import unicorn as un
from unicorn import arm_const as ar
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wm/final'
WORK = ROOT / 'work/wm1104final/conditions'
BASE, STATUS, REQUEST = 0x027e0000, 0x02400000, 0x02401000


def fragment(image, address, body, kind, values):
    cpu = un.Uc(un.UC_ARCH_ARM, un.UC_MODE_ARM)
    cpu.mem_map(BASE,0x20000)
    cpu.mem_map(STATUS,0x10000)
    cpu.mem_write(BASE,image)
    cpu.mem_write(address,body)
    cpu.reg_write(ar.UC_ARM_REG_CPSR,0xf0000010)
    if kind=='fatal':
        mode,error=values
        cpu.mem_write(STATUS+0x9a,struct.pack('<H',mode))
        cpu.mem_write(STATUS+0x7cc,struct.pack('<H',1-mode if mode in (0,1) else 1))
        cpu.mem_write(REQUEST+0x10,struct.pack('<H',error))
        cpu.reg_write(ar.UC_ARM_REG_R5,STATUS)
        cpu.reg_write(ar.UC_ARM_REG_R0,REQUEST)
        start,yes,no=0x027e0e18,0x027e0e30,0x027e0e8c
        expected=mode==1 and error==32
        expected_reads=[(STATUS+0x9a,2)]+([(REQUEST+0x10,2)] if mode==1 else [])
    elif kind=='channel':
        channels,enabled,misc=values
        cpu.mem_write(STATUS+0x1f4,struct.pack('<H',enabled))
        cpu.mem_write(STATUS+0xc8,struct.pack('<I',misc))
        cpu.reg_write(ar.UC_ARM_REG_R4,STATUS)
        cpu.reg_write(ar.UC_ARM_REG_R10,channels)
        start,yes,no=0x027e3b78,0x027e3bb4,0x027e3b90
        expected=bool(((channels<<1)&0xffff)&enabled)
        expected_reads=[(STATUS+0x1f4,2)]
    else:
        pointer,size=values
        cpu.mem_write(REQUEST+4,struct.pack('<I',pointer))
        cpu.mem_write(REQUEST+8,struct.pack('<H',size))
        cpu.reg_write(ar.UC_ARM_REG_R8,REQUEST)
        start,yes,no=0x027e3bb4,0x027e3bf8,0x027e3bd4
        expected=pointer!=0 and pointer%4==0 and size>=64
        expected_reads=[(REQUEST+4,4)]+([(REQUEST+8,2)] if pointer!=0 and pointer%4==0 else [])
    pcs,reads=[],[]
    def code(machine,at,size,user):
        if at in (yes,no):machine.emu_stop()
        else:pcs.append(hex(at))
    cpu.hook_add(un.UC_HOOK_CODE,code)
    cpu.hook_add(un.UC_HOOK_MEM_READ,lambda machine,access,at,size,value,user:reads.append((at,size)))
    cpu.emu_start(start,0,count=16)
    if cpu.reg_read(ar.UC_ARM_REG_PC)!=(yes if expected else no) or reads!=expected_reads:
        raise ValueError(('Original conditional, exact offsets or widths differ',kind,values,reads))
    return dict(kind=kind,values=list(values),condition=expected,pcs=pcs,reads=[list(r) for r in reads],fullCallerExecutions=0,importExecutions=0)


def layout(entry,address):
    directory=WORK/'layout'/('%08x'%address)
    directory.mkdir(parents=True,exist_ok=True)
    headers=[]
    for pin in entry['sourceDependencies']:
        path=ROOT/pin['path'];target=directory/path.name;target.write_bytes(path.read_bytes());headers.append(target)
    text=''.join('#include "'+p.name+'"\n' for p in headers)
    assertions={0x027e0e08:'((u32)&((WMStatus*)0)->mp_ignoreFatalErrorMode==0x9a && sizeof(((WMStatus*)0)->mp_ignoreFatalErrorMode)==2 && (u32)&((WlMaFatalErrInd*)0)->errCode==0x10)',0x027e3a88:'((u32)&((WMStatus*)0)->enableChannel==0x1f4 && (u32)&((WMStartScanExReq*)0)->scanBuf==4 && (u32)&((WMStartScanExReq*)0)->scanBufSize==8)',0x027e524c:'((u32)&((WMStartMPReq*)0)->param==0x14 && sizeof(WMStartMPReq)==0x30)'}
    text+='typedef char native_layout['+assertions[address]+'?1:-1];\n'
    needle={0x027e0e08:'==0x9a',0x027e3a88:'==0x1f4',0x027e524c:'==0x14'}[address]
    cases=[('correct',text),('wrong-offset',text.replace(needle,'==0x7cc'))]
    results=[]
    for label,payload in cases:
        source,obj=directory/(label+'.c'),directory/(label+'.o');source.write_text(payload)
        command=[str(ROOT/entry['compiler']),*entry['compilerFlags'],'-c',str(source),'-o',str(obj)]
        run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        results.append(dict(label=label,exitCode=run.returncode,source=source.relative_to(ROOT).as_posix(),sha256=sha256(source)))
    if results[0]['exitCode']!=0 or results[1]['exitCode']==0:raise ValueError(('Typed-layout control failed',results))
    return dict(address=hex(address),controls=results)


def main():
    report=read_json(LANE/'packet-ready.json');rows={int(r['address'],0):r for r in report['matches']}
    image=(ROOT/'extract/utility/runtime/utility-child-arm7-main.bin').read_bytes();bodies={}
    for address,row in rows.items():
        native=image[address-BASE:address-BASE+row['bytes']]
        linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        if native!=linked:raise ValueError('Complete linked caller differs')
        bodies[address]=(native,linked)
    records=[]
    cases=[('fatal',0x027e0e08,[(m,e) for m in [0,1,2,65535] for e in [0,31,32,33,65535]]),('channel',0x027e3a88,[(c,e,m) for c in [0,1,2,32768,65535] for e in [0,1,2,32768,65535] for m in [0,1]]),('buffer',0x027e3a88,[(p,s) for p in [0,4,5,3] for s in [0,63,64,65535]])]
    for kind,address,vectors in cases:
        for values in vectors:
            original,linked=[fragment(image,address,b,kind,values) for b in bodies[address]]
            if original!=linked:raise ValueError('Original and linked fragment differ')
            records.append(dict(address=hex(address),original=original,recompiled=linked))
    order=[]
    for body in bodies[0x027e524c]:
        ins=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(body[0x108:0x120],0x027e5354))
        calls=[dict(address=hex(i.address),target=i.op_str,bytesHex=i.bytes.hex()) for i in ins if i.mnemonic=='bl']
        if [r['target'] for r in calls]!=['#0x27e7dc8','#0x27e8570','#0x37fe41c']:raise ValueError('Original parameter/interrupt order differs')
        order.append(calls)
    write_json(LANE/'native-condition-controls.json',dict(status='passed',fragments=len(records)*2,records=records,sourceLayoutControls=[layout(r,a) for a,r in rows.items()],nativeStartMPCallOrder=order,fullCallerExecutions=0,fullCallerReturns=0,actualNativeHelperExecutions=0,unicornVersion=un.__version__,limits=['Only bounded instruction fragments execute; all imported callbacks/helpers and complete callers remain unexecuted.','StartMP order is original-byte/decoded-control evidence; no import executes.']))
    print(dict(fragments=len(records)*2,layoutPositive=3,layoutNegative=3,fullCallerExecutions=0))


if __name__=='__main__':main()
