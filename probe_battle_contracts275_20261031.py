import hashlib
import json
import random
import struct
import match_runtime
from link_runtime_unit import measured_module
from project import ROOT, configuration, sha256, write_json
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

STOP, SP, TABLE, OUT = 0x08000000, 0x0301F000, 0x02102E2C, 0x02300004
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
BODY = [(0x0205D790,60,60,'main'), (0x0205D764,44,40,'main'), (0x0205CA0C,56,52,'main'), (0x021D8B4C,44,40,'ov001')]

def execute(main, overlay, seed, entry, args, initials, effects, expected, native):
    rng = random.Random(seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for a,n in [(0x02000000,0x400000),(0x03000000,0x20000),(STOP,0x1000)]:
        machine.mem_map(a,n)
    machine.mem_write(0x02000000,main)
    machine.mem_write(0x021D7240,overlay)
    machine.mem_write(0x03000000,rng.randbytes(0x20000))
    for a,b in initials:
        machine.mem_write(a,b)
    ram = bytearray(machine.mem_read(0x02000000,0x400000))
    for a,b in effects:
        ram[a-0x02000000:a-0x02000000+len(b)] = b
    values = [rng.getrandbits(32)for r in REGS]
    values[:len(args)] = args
    for r,v in zip(REGS,values):
        machine.reg_write(r,v)
    machine.reg_write(UC_ARM_REG_CPSR,rng.getrandbits(4)<<28|0x10)
    machine.reg_write(UC_ARM_REG_SP,SP)
    machine.reg_write(UC_ARM_REG_LR,STOP)
    frames, returns, trace, writes = [],[],[],[]
    def step(vm,pc,width,data):
        while frames and pc==frames[-1]['returnAddress']:
            frame=frames.pop()
            if vm.reg_read(UC_ARM_REG_SP)!=frame['sp'] or [vm.reg_read(r)for r in REGS[4:12]]!=frame['preserved'] or vm.reg_read(REGS[0])!=frame['result']:
                raise ValueError('Contracts275 actual helper return/frame differs')
            returns.append(dict(address=hex(frame['address']),result=vm.reg_read(REGS[0])))
        if pc==STOP:
            vm.emu_stop()
            return
        if vm.reg_read(UC_ARM_REG_CPSR)&255!=0x10 or not any(a<=pc<a+c for a,n,c,m in BODY):
            raise ValueError(('Contracts275 unexpected code/mode',hex(pc)))
        if pc in native:
            frames.append(dict(address=pc,returnAddress=vm.reg_read(UC_ARM_REG_LR)&~1,sp=vm.reg_read(UC_ARM_REG_SP),preserved=[vm.reg_read(r)for r in REGS[4:12]],result=native[pc]))
        trace.append(pc)
    def written(vm,access,a,n,value,data):
        if not (0x03000000<=a and a+n<=SP or any(base<=a and a+n<=base+len(b)for base,b in effects)):
            raise ValueError('Contracts275 unexpected native memory write')
        writes.append([a,n,value])
    machine.hook_add(UC_HOOK_CODE,step)
    machine.hook_add(UC_HOOK_MEM_WRITE,written)
    machine.emu_start(entry,STOP+4,count=600)
    actual=[machine.reg_read(r)for r in REGS]
    if machine.reg_read(UC_ARM_REG_PC)!=STOP or machine.reg_read(UC_ARM_REG_SP)!=SP or frames or actual[4:12]!=values[4:12] or actual[0]!=expected or len(returns)!=len(native) or bytes(machine.mem_read(0x02000000,0x400000))!=ram:
        raise ValueError('Contracts275 actual top return/frame/RAM differs')
    return dict(actualResult=actual[0],actualReturn=True,nativeReturns=returns,instructions=len(trace),traceSha256=hashlib.sha256(struct.pack('<'+'I'*len(trace),*trace)).hexdigest(),writes=writes)

def run():
    main_meta,main,_=measured_module('main')
    overlay_meta,overlay,_=measured_module('ov001')
    bodies=[]
    for a,n,c,m in BODY:
        data=main if m=='main'else overlay
        base=0x02000000 if m=='main'else 0x021D7240
        bodies.append(dict(processor='arm9',program='',module=m,mode='arm',address=hex(a),bytes=n,instructionBytes=c,spanSha256=hashlib.sha256(data[a-base:a-base+n]).hexdigest(),moduleSha256=(main_meta if m=='main'else overlay_meta)['sha256']))
    results=[]
    for value in range(256):
        rng=random.Random(275000+value)
        table=bytearray(rng.randbytes(32*0xAC))
        ids=[0x10000000+i*0x10231 for i in range(32)]
        ids[31]=0xFFFFFFFF
        ids[4]=ids[19]=0x80000000
        for i,uid in enumerate(ids):
            struct.pack_into('<I',table,i*0xAC+4,uid)
            table[i*0xAC+0x7A]=value
        signed=value if value<128 else value-256
        for query in[ids[0],ids[31],ids[4],0x7F000001]:
            index=ids.index(query)if query in ids else -1
            result=signed if index>=0 else -1
            mapped=result-1 if result in[1,2,3]else -1
            row=execute(main,overlay,275000+len(results),0x0205D790,[query],[(TABLE,bytes(table))],[],mapped&0xFFFFFFFF,{0x0205D764:result&0xFFFFFFFF,0x0205CA0C:index&0xFFFFFFFF})
            results.append(dict(query=hex(query),rawField7A=value,firstIndex=index,tableSha256=hashlib.sha256(table).hexdigest(),**row))
    copy=[]
    vectors=[(0,0,0),(1,2,3),(0xFFFFFFFF,0x80000000,0x7FFFFFFF),(0x12345678,0x76543210,0x87654321)]
    for index in[3,11]:
        address=0x0223161C+index*16
        for values in vectors:
            payload=struct.pack('<IIII',*values,0xA17C00DE)
            data=payload[:12]
            for nullable in[True,False]:
                initial=bytes(range(32))
                row=execute(main,overlay,275200+len(copy),0x021D8B4C,[index,0 if nullable else OUT],[(OUT-4,initial),(address,payload)],[]if nullable else[(OUT,data)],address,{})
                copy.append(dict(index=index,nullDestination=nullable,sourceAddress=hex(address),suppliedBssBytesHex=payload.hex(),copiedBytesHex=data.hex(),**row))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],generatorSha256=sha256(__file__),bodies=bodies,actualTopReturns=len(results)+len(copy),actualNestedNativeReturns=sum(len(r['nativeReturns'])for r in results),providers=0,sourceCredit=0,instructionBound=600,freshMachinePerExecution=True,mapperResults=results,copyResults=copy,contracts=[dict(address='0x0205d790',inputWords=1,returnWord='FFFFFFFF except mapped raw signed8 values1/2/3 become0/1/2',originalPrototypeProven=False),dict(address='0x021d8b4c',inputWords=2,destination='Nullable; three32-bit words written when nonnull',minimumNonNullOutputBytes=12,returnWord='0223161C + (index << 4) within tested indices3/11',originalPrototypeProven=False)],limitations=['Synthetic32-row ID/type table at02102E2C; no game initialization, record meaning or lifecycle claim','All256 raw signed8 type encodings, first/last/duplicate/absent queries and high-bit full-word IDs tested; not every32-bit query enumerated','Copy source0223161C is outside initialized overlay end0222FD20; supplied synthetic BSS records are not ROM values or observed live state','Copy indices3/11 follow the ordinary BF54 caller; no other index bounds or vector meaning inferred','Frozen accepted void source and historical projected declarations remain unchanged; this packet adds no source bytes'])
    write_json(ROOT/'evidence/verification/battle-contracts275-20261031.json',report)
    print(json.dumps(dict(actualTopReturns=report['actualTopReturns'],actualNestedNativeReturns=report['actualNestedNativeReturns'],providers=0,sourceCredit=0)))

if __name__=='__main__':
    run()
