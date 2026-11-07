import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT
from wave20261106_overlay_strict_reuse_source_bindings import inputs

STACK=0x3009000
DATA=0x3100000
STOP=0x4000000


def signed(value,bits=32):return((value&((1<<bits)-1))^(1<<(bits-1)))-(1<<(bits-1))
def word(value):return value&0xffffffff
def quotient(value,divisor):return(abs(value)//divisor)*(-1 if value<0 else 1)


def cases(row):
    if row['module']=='ov003':return[dict(number=n,previousActive=active,index0=n%4,index1=(n//2)%4,allocationResult=word(result),arguments=[word(0x10203040+i*0x10101+n)for i in range(6)],initialValues=[0xffffffe0,0,0x7fffffe0,0x80000020],targetFlags=word(0x8f00aa10+n))for n,result in enumerate([0,1,-1,0x80000000,0x7fffffff,0x4000000])for active in[False,True]]
    return[dict(number=n,nonnull=present,level=level,count=word(count),handle=word(0x80000000+n),values=([255]*256 if n%2 else[(i*71+1)&255 for i in range(256)]))for n,(level,count)in enumerate([(-1,1),(0,0),(1,1),(3,-1),(130,1),(140,5),(255,0x7fffffff),(255,0x80000000),(255,0xffffffff)])for present in[False,True]]


def execute(row,code,case):
    address=int(row['address'],0);code=bytes(code);engine=Uc(UC_ARCH_ARM,UC_MODE_ARM);engine.mem_map(0x2000000,0x300000);engine.mem_map(0x3000000,0x10000);engine.mem_map(DATA,0x10000);engine.mem_map(STOP,0x1000);engine.mem_write(address,code);engine.mem_write(STOP,b'\x1e\xff\x2f\xe1');engine.reg_write(UC_ARM_REG_CPSR,0x10|((case['number']%16)<<28));engine.reg_write(UC_ARM_REG_SP,STACK);engine.reg_write(UC_ARM_REG_LR,STOP)
    registers=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3];saved={r:0x55aa0000+i*0x101 for i,r in enumerate([UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11])}
    for reg,value in saved.items():engine.reg_write(reg,value)
    trace=[];expected=[];steps=0;returned=False;get_calls=0;index_calls=0;original_args=[];observed=[]
    def put(address,values):engine.mem_write(address,struct.pack('<%dI'%len(values),*[word(v)for v in values]))
    if row['module']=='ov003':
        args=case['arguments'];original_args=args;put(STACK,args[4:]);previous=DATA+0x1000;current=[DATA+0x2000,DATA+0x3000,DATA+0x4000];values=DATA+0x5000;targets=[DATA+0x6000,DATA+0x7000,DATA+0x8000];old_pointer=0x2112340 if case['previousActive']else 0;put(previous,[old_pointer,0x3110010]);put(values,case['initialValues'])
        for p,t in zip(current,targets):put(p,[0,t])
        put(targets[1]+24,[case['targetFlags']]);arities={0x2049ae4:0,0x21dadb8:0,0x2048f7c:1,0x2049af0:7,0x20853c8:2,0x21dfd18:1,0x2086b14:2}
        offset=signed(case['initialValues'][case['index0']])>>5;expected=[(0x2049ae4,()),(0x21dadb8,()),(0x2048f7c,(1,)),(0x2049af0,tuple([*args[:3],word(offset),*args[3:]])),(0x2048f7c,(1,))]
        if case['previousActive']:expected.append((0x20853c8,(0x3110010,old_pointer)))
        expected.extend([(0x21dfd18,(0,)),(0x2049ae4,()),(0x2086b14,(targets[0],10)),(0x2049ae4,()),(0x2049ae4,())]);answer=targets[2];new_values=list(case['initialValues']);new_values[case['index1']]=word(case['allocationResult']<<5);expected_memory=dict(values=new_values,targetFlags=case['targetFlags']|2)
    else:
        args=[word(case['level']),case['count'],case['handle']];values=DATA+0x1000;engine.mem_write(values,bytes(case['values']));arities={0x203cc2c:2,0x203cf9c:2};expected=[(0x203cc2c,(0x220d010,case['handle']))];total=0
        if case['nonnull']:
            for value in case['values'][:max(0,case['level'])]:total=signed(total+value,16)
            scaled=signed(word(total*case['count']+4));answer=word(signed(quotient(scaled,5),16));expected.append((0x203cf9c,(case['handle'],values)))
        else:answer=0
        expected_memory=dict(values=case['values'])
    for reg,value in zip(registers,args):engine.reg_write(reg,value)
    def hook(uc,pc,size,data):
        nonlocal steps,returned,get_calls,index_calls
        if pc==STOP:returned=True;uc.emu_stop();return
        if pc in arities:
            count=arities[pc];arguments=[word(uc.reg_read(r))for r in registers[:min(count,4)]]
            if count>4:arguments.extend(struct.unpack('<%dI'%(count-4),uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4*(count-4))))
            trace.append((pc,tuple(arguments)));result=0x7bad0000
            if row['module']=='ov003':
                if pc==0x2049ae4:
                    result=previous if get_calls==0 else current[get_calls-1];get_calls+=1
                elif pc==0x21dadb8:result=values
                elif pc==0x2048f7c:result=case['index0']if index_calls==0 else case['index1'];index_calls+=1
                elif pc==0x2049af0:result=case['allocationResult']
            elif pc==0x203cc2c:result=values if case['nonnull']else 0
            for i,r in enumerate([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):uc.reg_write(r,0xabc10000+i)
            uc.reg_write(UC_ARM_REG_R0,result);uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(code):raise ValueError('Caller escaped exact body/qualified supplied boundaries')
        steps+=1
    engine.hook_add(UC_HOOK_CODE,hook);engine.emu_start(address,STOP+4,count=20000)
    if not returned or engine.reg_read(UC_ARM_REG_SP)!=STACK or any(engine.reg_read(r)!=v for r,v in saved.items()):raise ValueError('Original/C caller return/SP/callee-saved ABI failed')
    if row['module']=='ov003':memory=dict(values=list(struct.unpack('<4I',engine.mem_read(values,16))),targetFlags=struct.unpack('<I',engine.mem_read(targets[1]+24,4))[0])
    else:memory=dict(values=list(engine.mem_read(values,256)))
    result=dict(returnValue=word(engine.reg_read(UC_ARM_REG_R0)),trace=trace,memory=memory,instructions=steps)
    return result,dict(returnValue=answer,trace=expected,memory=expected_memory)


def check(rows,flats,negative=False):
    value,images,inventories,records=inputs();records=[]
    for row,flat in zip(rows,flats):
        address=int(row['address'],0);base=int(value['images'][row['module']]['base'],0);native=images[row['module']][address-base:address-base+row['bytes']]
        for number,case in enumerate(cases(row)):
            original,oracle=execute(row,native,case);compiled,unused=execute(row,flat,case)
            if any(original[key]!=oracle[key]for key in oracle):raise ValueError(('Independent original caller oracle failed',row['address'],number,original,oracle))
            if any(compiled[key]!=oracle[key]for key in oracle):
                if negative:return dict(rejected=True,address=row['address'],case=number,original=original,wrongC=compiled)
                raise ValueError(('Complete C caller differs from independent native oracle',row['address'],number,compiled,oracle))
            records.append(dict(address=row['address'],case=number,input=case,original=original,compiled=compiled))
    if negative:raise ValueError('Wrong C passed independent original caller model')
    return dict(passed=True,records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeHelperInvocations=0,suppliedServiceCalls=sum(len(r[k]['trace'])for r in records for k in['original','compiled']),limits='Only complete original/C192B and140B callers execute. Every external helper is a supplied boundary with zero body credit. Target32bit modulo operations, s16 narrowing, signed division and arithmetic right shift are measured; full object storage, provider implementations, real game reachability and native Windows execution remain unproved.')
