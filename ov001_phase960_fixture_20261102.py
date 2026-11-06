import struct
import ov001_selector917_machine_20261102 as B
ENTRY=0x021F9B54
STATE=B.STATE
OBJECT=0x02239A5C
ACTOR=0x02540000
GETTER=0x02041800
LEAF=0x020417F8
RAWBYTE=0x020F6102
PROVIDERS={0x02041510:3,0x021F9AC8:0,0x0202AC08:1,0x021EEA10:2,0x0205C904:1,0x021DB438:2,0x021DB8D0:1,0x021EEC7C:3,0x021F94D8:2,0x021F949C:2,0x021F14A4:0,0x021EEB70:1,0x0202AC4C:1}

def profiles():
    rows=[]
    def add(phase,count,flag,raw):
        rows.append(dict(ordinal=len(rows),rawPhase=phase,count=count,flag=flag,rawByte=raw,condition=[0,1,0xFFFFFFFF][len(rows)%3],handle=0xC0010000+len(rows),ticket=0xBEEF0000+len(rows),counter=0,phase=0,gate=0,seed=0x12345678,threshold=0,busy=0))
    for phase in range(256):
        for raw in [0,1,255]:add(phase,[0,2,15,255][phase%4],phase&1,raw)
    for phase in [40,55]:
        for count in range(256):add(phase,count,count&1,255)
    for flag in range(256):add(36,2,flag,0)
    return rows

def returned(p,address):
    return {0x021DB438:ACTOR,0x021DB8D0:p['condition'],0x021EEC7C:p['handle'],0x021F949C:p['ticket']}.get(address,0xABCD0000+(address&0xFFFF))

class Machine(B.Machine):
    def __init__(self,main,overlay,body,p):
        super().__init__(main,overlay,None,p)
        self.ranges={ENTRY:(624,0),GETTER:(20,0),LEAF:(8,1)}
        self.u.mem_write(STATE,bytes(0x200))
        self.u.mem_write(STATE,bytes([p['count']]))
        self.u.mem_write(STATE+3,bytes([p['rawPhase'],p['flag']]))
        self.u.mem_write(STATE+0xA,bytes([7]))
        self.u.mem_write(RAWBYTE,bytes([p['rawByte']]))
        self.u.mem_write(ACTOR,bytes([0x7A])*0x400)
        for address,image in (body or {}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.beforeState=bytes(self.u.mem_read(STATE,0x200))
        self.beforeMemory=bytes(self.u.mem_read(0x02000000,0x800000))
        self.tailEntries=[]

    def code(self,u,pc,size,unused):
        if pc in PROVIDERS:
            words=[u.reg_read(r)for r in B.REGS[:4]]
            value=returned(self.p,pc)
            self.provided.append(dict(target=hex(pc),consumedWords=words[:PROVIDERS[pc]],rawCallerWords=words,stackPointer=hex(u.reg_read(B.REGS[13])),returnWord=value))
            for index in [0,1,2,3,12]:u.reg_write(B.REGS[index],(0xC0DE0000+len(self.provided)*0x100+index*17)&0xFFFFFFFF)
            u.reg_write(B.REGS[0],value)
            flags=u.reg_read(B.UC_ARM_REG_CPSR)
            u.reg_write(B.UC_ARM_REG_CPSR,(flags&0x0FFFFFFF)|((self.p['ordinal']&15)<<28))
            u.reg_write(B.UC_ARM_REG_PC,u.reg_read(B.REGS[14])&~1)
            return
        if ENTRY<=pc<ENTRY+624:self.pcs.add(pc)
        if pc==LEAF:
            self.tailEntries.append(dict(entry=hex(pc),rawWords=[u.reg_read(r)for r in B.REGS[:4]],logicalParent=hex(GETTER)))
            saved=self.entry
            self.entry=LEAF
            try:super().code(u,pc,size,unused)
            finally:self.entry=saved
            return
        super().code(u,pc,size,unused)

    def run(self,entry):
        result=super().run(entry)
        result['tailEntries']=self.tailEntries
        result['actorHex']=bytes(self.u.mem_read(ACTOR,0x400)).hex()
        return result

def contracts(result):
    return [{key:r[key]for key in ['target','consumedWords','returnWord']}for r in result['provided']]

def model(vm,result):
    p=vm.p
    state=bytearray(vm.beforeState)
    actor=bytearray([0x7A])*0x400
    calls=[]
    writes=[]
    getterCalls=0
    def call(address,args):
        value=returned(p,address)
        calls.append(dict(target=hex(address),consumedWords=args,returnWord=value))
        return value
    def store(offset,value):
        value&=255
        state[offset]=value
        writes.append([STATE+offset,1,value])
    def actorStore(offset,value):
        value&=255
        actor[offset]=value
        writes.append([ACTOR+offset,1,value])
    if state[3]==0:
        call(0x02041510,[0,3,20])
        call(0x021F9AC8,[])
        call(0x0202AC08,[OBJECT])
        call(0x021EEA10,[7,0])
        store(3,10)
    if state[3]==10:
        getterCalls+=1
        if p['rawByte']!=1:
            call(0x0205C904,[7])
            store(3,20)
    if state[3]==20:
        store(0,0)
        store(3,30)
    if state[3]==30:
        selected=call(0x021DB438,[0,state[0]])
        store(3,35 if call(0x021DB8D0,[selected])!=0 else 40)
    elif state[3]==35:
        selected=call(0x021DB438,[0,state[0]])
        call(0x021EEC7C,[7,selected,0])
        call(0x021F94D8,[74,1])
        actorStore(0x324,0)
        store(3,state[3]+1)
    elif state[3]==36:
        selected=call(0x021DB438,[0,state[0]])
        actorStore(0x358,call(0x021EEC7C,[8,selected,2]))
        if state[4]==0:
            actorStore(0x324,call(0x021F949C,[234,1]))
            store(4,state[4]+1)
        store(3,40)
    elif state[3]==40:
        store(0,state[0]+1)
        store(3,50 if state[0]>=3 else 30)
    elif state[3]<50:store(3,state[3]+1)
    if state[3]==50:
        store(0,0)
        store(3,55)
    if state[3]==55:
        store(0,state[0]+1)
        if state[0]>15:store(3,100)
    if state[3]==100:
        call(0x021F14A4,[])
        call(0x021EEB70,[7])
        call(0x0202AC4C,[OBJECT])
        store(3,0)
        store(4,0)
        store(0xA,4)
    failures=[]
    for name,actual,expected in [('state',result['stateHex'],state.hex()),('actor bytes',result['actorHex'],actor.hex()),('ordered writes',result['writes'],writes),('consumed service contracts',contracts(result),calls),('raw R0',result['registers'][0],0)]:
        if actual!=expected:failures.append(name)
    expected=bytearray(vm.beforeMemory)
    expected[STATE-0x02000000:STATE-0x02000000+len(state)]=state
    expected[ACTOR-0x02000000:ACTOR-0x02000000+len(actor)]=actor
    low=result['privateStackStart']-0x02000000
    high=B.SP-0x02000000
    if result['memory'][:low]!=expected[:low]or result['memory'][high:]!=expected[high:]:failures.append('complete independent nonstack RAM')
    if result['rngState']!=p['seed']:failures.append('unexpected RNG effect')
    if len(result['nativeEntries'])!=getterCalls or len(result['nativePhysicalReturns'])!=getterCalls or len(result['tailEntries'])!=getterCalls:failures.append('getter/tail physical-return count')
    if any(r['entry']!=hex(GETTER)for r in result['nativeEntries']):failures.append('unexpected native helper')
    if any(r['rawWords'][0]!=0x020F6100 for r in result['tailEntries']):failures.append('getter actual data pointer')
    if any(r['rawReturnWords'][0]!=p['rawByte']or r['returnPc']!='0x20417fc'for r in result['nativePhysicalReturns']):failures.append('getter actual raw byte/physical leaf return')
    return failures
