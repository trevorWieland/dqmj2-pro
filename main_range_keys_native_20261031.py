import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

LEAF=0x02036830
CHAIN=0x0203694C
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000


def lookup(node,key):
    kind,first,last,words=node
    if kind==0:return (key-first+words[0])&65535
    if kind==1:
        assert 0<=key-first<len(words)
        return words[key-first]
    if kind==2:
        left=0;right=words[0]-1
        while left<=right:
            middle=(left+right)//2;found,value=words[1+middle*2:3+middle*2]
            if found<key:left=middle+1
            elif key<found:right=middle-1
            else:return value
    return 65535


def leaf_cases():
    for kind in [*range(256),256,0x7FFF,0x8000,0xFFFF]:
        if kind>2:yield [(kind,0,65535,[0x2345])],0x1234
    for first in [0,1,10,65535]:
        for word in [0,1,0x7FFF,0x8000,0xFFFF]:
            for key in [0,1,9,10,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF]:yield [(0,first,65535,[word])],key
    for first in [0,8,65532]:
        for words in [[0,1,0x8000,65535],[65535,0x7FFF,42,3]]:
            for index in range(4):yield [(1,first,first+3,words)],first+index
    for count in [0,1,2,3,4,8,9,17,63]:
        entries=[(i*997,(i*7919+0x8000)&65535) for i in range(count)]
        words=[count]+[v for pair in entries for v in pair]
        for key in sorted({0,1,65535,65536,0xFFFFFFFF,*[x for k,v in entries for x in [max(0,k-1),k,k+1]]}):yield [(2,0,65535,words)],key
    words=[4,1,10,1,20,2,30,65535,0x8000]
    for key in [0,1,2,3,65535,65536]:yield [(2,0,65535,words)],key


def chain_cases():
    layouts=[[],[(0,10,20,[123])],[(0,10,9,[123])],[(1,10,13,[0,1,0x8000,65535])],[(2,0,65535,[3,10,1,11,0x8000,20,65535])],[(3,0,65535,[42])],[(0,10,20,[100]),(0,0,65535,[1000])],[(1,10,13,[0,1,0x8000,65535]),(2,0,65535,[2,0,1,65535,123])]]
    keys=[0,1,9,10,11,12,13,14,20,21,65534,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF]
    for nodes in layouts:
        for key in keys:yield nodes,key


def execute(arm,entry,case,tag,check=True):
    nodes,key=case;arena=bytearray((i*29+tag)&255 for i in range(0x4000));holder=DATA+0x20;base=DATA+0x100
    pointers=[DATA+0x400+i*0x400 for i in range(len(nodes))];struct.pack_into('<I',arena,0x20,base);struct.pack_into('<I',arena,0x110,pointers[0] if pointers else 0)
    extents=[]
    for i,(kind,first,last,words) in enumerate(nodes):
        at=pointers[i]-DATA;payload=struct.pack('<HHHHI',first,last,kind,0xA5A5,pointers[i+1] if i+1<len(nodes) else 0)+struct.pack('<'+'H'*len(words),*words);arena[at:at+len(payload)]=payload;extents.append((pointers[i],pointers[i]+len(payload)))
    called=0;expected=65535
    if entry==LEAF:assert len(nodes)==1;expected=lookup(nodes[0],key)
    else:
        for node in nodes:
            if node[1]<=key<=node[2]:called=1;expected=lookup(node,key);break
    pointer=pointers[0] if entry==LEAF else holder
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address,size in [(0x02036000,4096),(DATA,0x4000),(STACK,4096),(STOP,4096)]:uc.mem_map(address,size)
    uc.mem_write(0x02036000,arm[0x36000:0x37000]);uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096)
    uc.mem_protect(0x02036000,4096,UC_PROT_READ|UC_PROT_EXEC);uc.mem_protect(DATA,0x4000,UC_PROT_READ)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    uc.reg_write(REGISTERS[0],pointer);uc.reg_write(REGISTERS[1],key);uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(r) for r in REGISTERS[4:12]];pcs=set();pending=[];reads=[];writes=[];state={'actualTopReturns':0,'nestedEntries':0,'nestedReturns':0,'instructions':0}
    def code(machine,address,size,user):
        state['instructions']+=1
        if pending and address==pending[-1]:pending.pop();state['nestedReturns']+=1
        if address==STOP:state['actualTopReturns']+=1;machine.emu_stop();return
        assert LEAF<=address<LEAF+196 or CHAIN<=address<CHAIN+68,hex(address);pcs.add(address)
        if address==LEAF and entry==CHAIN:pending.append(machine.reg_read(UC_ARM_REG_LR)&~1);state['nestedEntries']+=1
    def read(machine,access,address,size,value,user):
        if DATA<=address<DATA+0x4000:
            reads.append((address,size));assert address==holder and size==4 or address==base+16 and size==4 or any(a<=address and address+size<=b for a,b in extents),(hex(address),case)
    def write(machine,access,address,size,value,user):
        assert STACK<=address and address+size<=STACK+4096;writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(entry,STOP+4,count=1000)
    assert state['actualTopReturns']==1 and not pending and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(r) for r in REGISTERS[4:12]]==saved and state['nestedEntries']==state['nestedReturns']
    memory=bytes(uc.mem_read(DATA,0x4000));passed=memory==bytes(arena) and uc.reg_read(REGISTERS[0])==expected and state['nestedReturns']==called
    if check:assert passed,(case,state,uc.reg_read(REGISTERS[0]),expected)
    return {'actualReturn':True,'modelPassed':passed,'state':state,'pcs':sorted(pcs),'memorySha256':hashlib.sha256(memory).hexdigest(),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest(),'registers':[uc.reg_read(r) for r in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'reads':reads,'writes':writes}
