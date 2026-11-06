import struct
import ov001_selector917_machine_20261102 as B
ENTRY=0x021FB7AC
PROVIDERS={0x021FAD98:0,0x021F1354:4,0x021F1414:1,0x021F1438:1,0x0205F210:2,0x02063D40:0,0x0205E7A8:2,0x021FB75C:0,0x021DC99C:1,0x021F14A4:0,0x021F14E4:0,0x021FB214:1}


def profiles():
    rows=[]
    for timer in range(256):
        for waitIndex,wait in enumerate([0,1,0xFFFFFFFF]):
            rows.append(dict(ordinal=len(rows),timer=timer,wait=wait,actor=[0,0x02540000,0xFFFFFFFF][waitIndex],ticket=(0x12340000+timer)&0xFFFFFFFF,builderReturn=0xC001CAFE,phase=30,counter=0xED,gate=0,seed=0x12345678,threshold=0,busy=0,selector=13))
    return rows


class Machine(B.Machine):
    def __init__(self,main,overlay,body,p):
        super().__init__(main,overlay,None,p)
        self.ranges[ENTRY]=(296,0)
        self.u.mem_write(B.STATE+1,bytes([p['timer']]))
        self.u.mem_write(B.STATE+0x40,B.pack([p['actor']]))
        for address,image in (body or {}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.beforeState=bytes(self.u.mem_read(B.STATE,0x200))

    def code(self,u,pc,size,unused):
        if pc in PROVIDERS:
            arity=PROVIDERS[pc]
            words=[u.reg_read(r)for r in B.REGS[:4]]
            stack=u.reg_read(B.REGS[13])
            actualReturn=self.p['ticket']if pc==0x021F1414 else self.p['wait']if pc==0x021F14E4 else self.p['builderReturn']if pc==0x021FB214 else(0xABCD0000+(pc&0xFFFF))
            self.provided.append(dict(target=hex(pc),consumedWords=words[:arity],rawCallerWords=words,stackPointer=hex(stack),returnWord=actualReturn))
            for index in [0,1,2,3,12]:u.reg_write(B.REGS[index],(0xC0DE0000+len(self.provided)*0x100+index*17)&0xFFFFFFFF)
            u.reg_write(B.REGS[0],actualReturn)
            flags=u.reg_read(B.UC_ARM_REG_CPSR)
            u.reg_write(B.UC_ARM_REG_CPSR,(flags&0x0FFFFFFF)|((self.p['ordinal']&15)<<28))
            u.reg_write(B.UC_ARM_REG_PC,u.reg_read(B.REGS[14])&~1)
            return
        if ENTRY<=pc<ENTRY+296:self.pcs.add(pc)
        super().code(u,pc,size,unused)


def contracts(result):
    return[{k:r[k]for k in ['target','consumedWords','returnWord']}for r in result['provided']]


def model(vm,result):
    p=vm.p
    state=bytearray(vm.beforeState)
    timer=p['timer']
    calls=[]
    writes=[]
    def call(address,args):
        value=p['ticket']if address==0x021F1414 else p['wait']if address==0x021F14E4 else p['builderReturn']if address==0x021FB214 else(0xABCD0000+(address&0xFFFF))
        calls.append(dict(target=hex(address),consumedWords=args,returnWord=value))
        return value
    def store(offset,value):
        state[offset]=value
        writes.append([B.STATE+offset,1,value])
    if timer==0:
        call(0x021FAD98,[])
        call(0x021F1354,[1,2,3,1])
        value=call(0x021F1414,[0])
        call(0x021F1438,[value])
        call(0x0205F210,[1,0])
        call(0x02063D40,[])
        call(0x0205E7A8,[0xFFFFFFFF,0x3A])
        call(0x021FB75C,[])
        call(0x021DC99C,[p['actor']])
        store(1,10)
    elif timer<40:store(1,timer+1)
    elif timer==40:
        call(0x021F1354,[1,2,5,0])
        store(1,50)
    elif timer<90:store(1,timer+1)
    elif timer==90:
        call(0x021F14A4,[])
        store(1,95)
    elif timer==95:
        if call(0x021F14E4,[])==0:
            call(0x021FB214,[p['actor']])
            store(1,110)
    elif timer==110:
        store(1,0)
        store(0xA,15)
    failures=[]
    for name,actual,expected in [('independent state',result['stateHex'],state.hex()),('ordered writes',result['writes'],writes),('consumed service contracts',contracts(result),calls),('raw R0',result['registers'][0],0)]:
        if actual!=expected:failures.append(name)
    if result['rngState']!=p['seed']:failures.append('unexpected RNG change')
    if result['nativeEntries']or result['nativePhysicalReturns']:failures.append('unexpected native dependency')
    return failures
