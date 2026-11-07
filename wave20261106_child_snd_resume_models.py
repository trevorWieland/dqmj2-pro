import struct
from pathlib import Path
import utility_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT
from wave20261106_child_snd_resume_bindings import TARGETS

ENTRY=0x2006eb8
STACK=0x3009000
STOP=0x2400000
HANDLE=0x3100000
SOUND=0x3101000
ARCHIVE=0x3102000
BANK=0x3103000
PLAYER=0x3104000
HEAP=0x3105000


def case_list():
    return[dict(playerPresent=present,bankResult=result,playerNo=n%16,bankNo=3+n,playerPriority=127-n,soundOffset=(0x10203040+n*0x10001)&0xffffffff,volume=v,channelPriority=(255-v),baseOffset=32+4*n,sequenceArchive=0x80000000+n,index=0x7fffffff-n)for n,v in enumerate([0,1,127,128,254,255])for present,result in[(False,0),(True,4),(True,0)]]


def expected(c):
    trace=[(0x2005884,(HANDLE,c['playerNo'],c['playerPriority']))]
    if not c['playerPresent']:return 0,trace
    trace.extend([(0x200577c,(c['playerNo'],PLAYER)),(0x2006d70,(c['bankNo'],6,HEAP,0,STACK-28))])
    if c['bankResult']:
        trace.append((0x2005878,(PLAYER,)));return 0,trace
    trace.extend([(0x2005820,(PLAYER,ARCHIVE+c['baseOffset'],c['soundOffset'],BANK)),(0x2005bb4,(HANDLE,c['volume'])),(0x2005b8c,(HANDLE,c['channelPriority'])),(0x2005b64,(HANDLE,c['sequenceArchive'],c['index']))])
    return 1,trace


def execute(code,c):
    code=bytes(code)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x100000);uc.mem_map(STOP,0x1000);uc.mem_map(0x3000000,0x10000);uc.mem_map(0x3100000,0x10000)
    uc.mem_write(ENTRY,code);uc.mem_write(STOP,b'\x1e\xff\x2f\xe1');uc.mem_write(0x3000000,bytes([0x69])*0x10000)
    uc.mem_write(SOUND,struct.pack('<I4B',c['soundOffset'],1,2,c['volume'],c['channelPriority']));uc.mem_write(ARCHIVE+24,struct.pack('<I',c['baseOffset']))
    uc.mem_write(STACK,struct.pack('<4I',SOUND,ARCHIVE,c['sequenceArchive'],c['index']))
    registers=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
    for reg,value in zip(registers,[HANDLE,c['playerNo'],c['bankNo'],c['playerPriority']]):uc.reg_write(reg,value)
    saved={reg:0x44220000+index*0x101 for index,reg in enumerate([UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11])}
    for reg,value in saved.items():uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,0x10);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP);trace=[];instructions=0;returned=False
    arities={0x2005884:3,0x200577c:2,0x2006d70:5,0x2005878:1,0x2005820:4,0x2005bb4:2,0x2005b8c:2,0x2005b64:3}
    def hook(engine,address,size,data):
        nonlocal instructions,returned
        if address==STOP:returned=True;engine.emu_stop();return
        if address in arities:
            count=arities[address];args=[engine.reg_read(r)&0xffffffff for r in registers[:min(count,4)]]
            if count>4:args.append(struct.unpack('<I',engine.mem_read(engine.reg_read(UC_ARM_REG_SP),4))[0])
            trace.append((address,tuple(args)))
            if address==0x2006d70:engine.mem_write(args[4],struct.pack('<I',BANK))
            result={0x2005884:PLAYER if c['playerPresent']else 0,0x200577c:HEAP,0x2006d70:c['bankResult']}.get(address,0x4bad0000)
            for i,reg in enumerate([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):engine.reg_write(reg,0xbad10000+i)
            engine.reg_write(UC_ARM_REG_R0,result);engine.reg_write(UC_ARM_REG_PC,engine.reg_read(UC_ARM_REG_LR));return
        if not ENTRY<=address<ENTRY+len(code):raise ValueError('Caller escaped exact body/qualified supplied provider boundaries')
        instructions+=1
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(ENTRY,STOP+4,count=2000)
    if not returned or uc.reg_read(UC_ARM_REG_SP)!=STACK or any(uc.reg_read(reg)!=value for reg,value in saved.items()):raise ValueError('Caller return/SP/callee-saved ABI failed')
    return dict(result=uc.reg_read(UC_ARM_REG_R0)&0xffffffff,trace=trace,instructions=instructions)


def check(rows,flats,negative=False):
    layout,files=utility_runtime.derive();module=next(m for m in layout['modules']if m['id']=='utility-child-arm9-main');raw=files[ROOT/module['binary']];native=raw[ENTRY-int(module['base'],0):ENTRY-int(module['base'],0)+196];cases=[]
    for row,flat in zip(rows,flats):
        code=flat if isinstance(flat,bytes)else Path(flat).read_bytes()
        for index,c in enumerate(case_list()):
            oracle,trace=expected(c);original=execute(native,c);compiled=execute(code,c)
            if original['result']!=oracle or original['trace']!=trace:raise ValueError('Original caller differs from independent scoped eight-argument oracle')
            if(compiled['result'],compiled['trace'])!=(oracle,trace):
                if negative:return dict(rejected=True,firstCase=index,original=original,wrongC=compiled)
                raise ValueError(('Actual C/native caller return/provider arguments differ',index,original,compiled))
            cases.append(dict(case=index,input=c,original=original,compiled=compiled))
    if negative:raise ValueError('Wrong C passed actual native caller model')
    return dict(passed=True,cases=cases,actualCallerReturns=2*len(cases),actualImportedBodyExecutions=0,suppliedProviderCalls=sum(len(x[k]['trace'])for x in cases for k in['original','compiled']),limits='Only complete original/C196B caller bodies execute. All eight supplied service hooks receive zero body credit. No audio hardware, real archive/heap/player implementation, whole-game execution, or transitive application reachability is proved.')
