import struct
import ov001_selector917_machine_20261102 as B
ENTRY=0x021E00B4
STATE=0x022388EC
TABLE=0x02238950
OBJECT=0x02238988
ACTOR=0x02540000
PROVIDERS={0x021DDA80:0,0x021FF238:1,0x021DB8D0:1,0x0202AC08:1,0x021EEA10:2,0x021D7E80:1,0x0205D790:1,0x021EEC7C:3,0x021F1294:2,0x021F1354:4,0x021F1414:1,0x021F1438:1,0x0205D6F4:1,0x021F14A4:0,0x021DC230:2,0x021DB788:2,0x021DBB9C:2,0x021F1324:0,0x0205D718:1,0x021EEB70:1,0x0202AC4C:1}

def profiles():
    rows=[]
    for phase in range(256):
        for selected in range(2):
            rows.append(dict(ordinal=len(rows),rawPhase=phase,index=[0,5,12][phase%3],actorPresent=True if phase in [5,10]else not selected,nextPresent=not selected,slotByte=[0,255][selected],condition=[0,0xFFFFFFFF][selected],eligible=[0x80000000,0][selected],finished=[0,0x100][selected],wait=[0,0xFFFFFFFF][selected],label=0xC0010000+phase,handle=0xD0A00000+phase,ticket=0xBEEF0000+phase,counter=0,phase=0,gate=0,seed=0x12345678,threshold=0,busy=0))
    for phase in [0,5,6,8,10,100]:
        for condition in [0,1,0xFFFFFFFF]:
            for present in [False,True]:
                rows.append(dict(rows[phase*2],ordinal=len(rows),rawPhase=phase,actorPresent=present,nextPresent=present,slotByte=255 if present else 0,condition=condition,eligible=condition,finished=condition,wait=condition))
    return [r for r in rows if r['rawPhase']not in [5,10]or r['actorPresent']]

def returned(p,address):
    return {0x021DDA80:p['condition'],0x021DB8D0:p['eligible'],0x021DBB9C:p['finished'],0x0205D6F4:p['wait'],0x0205D790:p['label'],0x021EEC7C:p['handle'],0x021F1414:p['ticket']}.get(address,0xABCD0000+(address&0xFFFF))

class Machine(B.Machine):
    def __init__(self,main,overlay,body,p):
        super().__init__(main,overlay,None,p)
        self.ranges={ENTRY:(628,0)}
        self.u.mem_write(STATE,bytes(0x9C))
        self.u.mem_write(STATE+8,bytes([0xE5]))
        self.u.mem_write(STATE+0x28,bytes([p['index'],p['rawPhase']]))
        self.u.mem_write(STATE+0x44,B.pack([0x12345678]))
        self.u.mem_write(ACTOR,bytes(0x400))
        self.u.mem_write(ACTOR+0x31E,bytes([p['slotByte']]))
        self.u.mem_write(TABLE+p['index']*4,B.pack([ACTOR if p['actorPresent'] else 0]))
        self.u.mem_write(TABLE+(p['index']+1)*4,B.pack([ACTOR if p['nextPresent'] else 0]))
        for address,image in (body or {}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.beforeState=bytes(self.u.mem_read(STATE,0x64))
        self.beforeMemory=bytes(self.u.mem_read(0x02000000,0x800000))

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
        if ENTRY<=pc<ENTRY+628:self.pcs.add(pc)
        super().code(u,pc,size,unused)

    def run(self,entry):
        result=super().run(entry)
        result['stateHex']=bytes(self.u.mem_read(STATE,0x64)).hex()
        return result

def contracts(result):
    return [{key:r[key]for key in ['target','consumedWords','returnWord']}for r in result['provided']]

def model(vm,result):
    p=vm.p
    state=bytearray(vm.beforeState)
    phase=p['rawPhase']
    actor=ACTOR if p['actorPresent'] else 0
    calls=[]
    writes=[]
    def call(address,args):
        value=returned(p,address)
        calls.append(dict(target=hex(address),consumedWords=args,returnWord=value))
        return value
    def store(offset,value,width=1):
        state[offset:offset+width]=value.to_bytes(width,'little')
        writes.append([STATE+offset,width,value])
    def branch():
        if call(0x021DDA80,[])!=0:
            call(0x021FF238,[0])
            store(8,0x36)
        else:store(8,0x1C)
    if phase==0:
        if not actor:branch()
        elif call(0x021DB8D0,[actor])!=0:
            call(0x0202AC08,[OBJECT])
            call(0x021EEA10,[125,0])
            store(0x29,5)
        else:store(0x28,p['index']+1)
    elif phase==5:
        if not actor:return ['unsupported phase5 null actor dereference']
        call(0x021D7E80,[actor])
        label=call(0x0205D790,[125])
        handle=call(0x021EEC7C,[125,actor,label])
        store(0x44,handle,4)
        call(0x021F1294,[16,2])
        call(0x021F1354,[5,3,59,1])
        ticket=call(0x021F1414,[p['slotByte']])
        call(0x021F1438,[ticket])
        store(0x29,6)
    elif phase==6:
        if call(0x0205D6F4,[0x12345678])==0:
            store(0x29,8)
            call(0x021F14A4,[])
    elif phase==8:
        call(0x021DC230,[actor,1])
        call(0x021DB788,[actor,0])
        store(0x29,10)
    elif phase==10:
        if not actor:return ['unsupported phase10 null actor dereference']
        if call(0x021DBB9C,[actor,p['slotByte']])!=0:store(0x29,100)
    elif phase==100:
        store(0x28,p['index']+1)
        call(0x021F1324,[])
        if p['nextPresent']:store(0x29,5)
        else:
            call(0x0205D718,[0x12345678])
            call(0x021EEB70,[125])
            call(0x0202AC4C,[OBJECT])
            store(0x29,0)
            store(0x28,0)
            branch()
    failures=[]
    for name,actual,expected in [('state',result['stateHex'],state.hex()),('ordered own writes',result['writes'],writes),('consumed service contracts',contracts(result),calls),('raw R0',result['registers'][0],0)]:
        if actual!=expected:failures.append(name)
    expected=bytearray(vm.beforeMemory)
    expected[STATE-0x02000000:STATE-0x02000000+len(state)]=state
    low=result['privateStackStart']-0x02000000
    high=B.SP-0x02000000
    if result['memory'][:low]!=expected[:low]or result['memory'][high:]!=expected[high:]:failures.append('complete independent nonstack RAM')
    if result['rngState']!=p['seed']or result['nativeEntries']or result['nativePhysicalReturns']:failures.append('unexpected native/RNG effects')
    return failures
