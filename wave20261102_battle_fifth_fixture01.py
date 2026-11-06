import struct

import ov001_selector917_machine_20261102 as B

ENTRY=0x021DFF00
STATE=0x022388EC
TABLE=0x0223896C
OBJECT=0x02238988
ACTOR=0x02540000
OTHER=0x02541000
PROVIDERS={0x0202AC08:1,0x021EEA10:2,0x021D7E80:1,0x0205D790:1,0x021EEC7C:3,0x0205D6F4:1,0x021DC230:2,0x021DB788:2,0x021DBB9C:2,0x0205D718:1,0x021EEB70:1,0x0202AC4C:1}


def word(value):
    return value&0xFFFFFFFF


def signed_byte(value):
    value&=255
    return value-256 if value&128 else value


def profiles():
    output=[]
    def add(**changes):
        profile=dict(ordinal=len(output),rawPhase=0,index=1,word80=ACTOR,actorWord=ACTOR,nextWord=0,slotByte=0xFE,label=0xC0010080,handle=0xD0A00191,initialHandle=0xE7,wait=0,finished=0,counter=0,phase=0,gate=0,seed=0x12345678,threshold=0,busy=0)
        profile.update(changes)
        output.append(profile)
    for phase in range(256):
        for selected in range(2):
            add(rawPhase=phase,index=[0,1,5][phase%3],word80=[ACTOR,0][selected],actorWord=[ACTOR,OTHER][selected],nextWord=[0,OTHER][selected],slotByte=[0,255][selected],label=[0xC0010080,0xC001007F][selected],handle=[0xD0A00191,0xD0A00100][selected],wait=[0,0xFFFFFFFF][selected],finished=[0,0x100][selected])
    for index in [0,1,5]:
        for label in [0,0x7F,0x80,0xFF,0x81230080]:
            add(rawPhase=5,index=index,label=label)
    for phase in [0,6,10,100]:
        for value in [0,1,0x80000000,0xFFFFFFFF]:
            add(rawPhase=phase,word80=value,wait=value,finished=value,nextWord=OTHER if value else 0)
    return output


def returned(profile,address):
    return {0x0205D790:profile['label'],0x021EEC7C:profile['handle'],0x0205D6F4:profile['wait'],0x021DBB9C:profile['finished']}.get(address,word(0xABCD0000+(address&0xFFFF)))


class Machine(B.Machine):
    def __init__(self,main,overlay,images,profile):
        super().__init__(main,overlay,None,profile)
        self.ranges={ENTRY:(436,0)}
        self.u.mem_write(STATE,bytes(0x9C))
        self.u.mem_write(STATE+8,bytes([0xE5]))
        self.u.mem_write(STATE+0x2A,bytes([profile['initialHandle'],profile['index'],profile['rawPhase']]))
        self.u.mem_write(TABLE,B.pack([profile['word80']]))
        actor=profile['actorWord'] if profile['index'] else profile['word80']
        if profile['rawPhase']==10 and actor not in [ACTOR,OTHER]:
            raise ValueError('Active raw phase10 requires a mapped actor word')
        self.actor=actor
        self.nextActor=profile['nextWord']
        self.u.mem_write(TABLE+profile['index']*4,B.pack([actor,self.nextActor]))
        for address in [ACTOR,OTHER]:
            self.u.mem_write(address,bytes(0x400))
            self.u.mem_write(address+0x31E,bytes([profile['slotByte']]))
        for address,image in(images or{}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.beforeState=bytes(self.u.mem_read(STATE,0x9C))
        self.beforeMemory=bytes(self.u.mem_read(0x02000000,0x800000))

    def code(self,u,pc,size,unused):
        if pc in PROVIDERS:
            words=[u.reg_read(r)for r in B.REGS[:4]]
            value=returned(self.p,pc)
            self.provided.append(dict(target=hex(pc),consumedWords=words[:PROVIDERS[pc]],rawCallerWords=words,returnWord=value))
            for index in[0,1,2,3,12]:
                u.reg_write(B.REGS[index],word(0xC0DE0000+len(self.provided)*0x100+index*17))
            u.reg_write(B.REGS[0],value)
            flags=u.reg_read(B.UC_ARM_REG_CPSR)
            u.reg_write(B.UC_ARM_REG_CPSR,(flags&0x0FFFFFFF)|((self.p['ordinal']&15)<<28))
            u.reg_write(B.UC_ARM_REG_PC,u.reg_read(B.REGS[14])&~1)
            return
        if ENTRY<=pc<ENTRY+436:
            self.pcs.add(pc)
        super().code(u,pc,size,unused)

    def run(self,entry):
        result=super().run(entry)
        result['stateHex']=bytes(self.u.mem_read(STATE,0x9C)).hex()
        return result


def contracts(result):
    return[{key:row[key]for key in['target','consumedWords','returnWord']}for row in result['provided']]


def model(vm,result):
    profile=vm.p
    state=bytearray(vm.beforeState)
    calls=[]
    writes=[]
    def call(address,args):
        value=returned(profile,address)
        calls.append(dict(target=hex(address),consumedWords=[word(arg)for arg in args],returnWord=value))
        return value
    def store(offset,value):
        state[offset]=value&255
        writes.append([STATE+offset,1,value&255])
    phase=profile['rawPhase']
    if phase==0:
        if struct.unpack_from('<I',vm.beforeState,0x80)[0]==0:
            store(8,0x1B)
        else:
            call(0x0202AC08,[OBJECT])
            call(0x021EEA10,[0x5C,0])
            store(0x2C,5)
    elif phase==5:
        call(0x021D7E80,[vm.actor])
        label=call(0x0205D790,[0x5C])
        handle=call(0x021EEC7C,[0x5C,vm.actor,signed_byte(label)])
        store(0x2A,handle)
        store(0x2C,6)
    elif phase==6:
        if call(0x0205D6F4,[profile['initialHandle']])==0:
            store(0x2C,8)
    elif phase==8:
        call(0x021DC230,[vm.actor,1])
        call(0x021DB788,[vm.actor,0])
        store(0x2C,10)
    elif phase==10:
        if call(0x021DBB9C,[vm.actor,profile['slotByte']])!=0:
            store(0x2C,100)
    elif phase==100:
        store(0x2B,profile['index']+1)
        if vm.nextActor:
            store(0x2C,5)
        else:
            call(0x0205D718,[profile['initialHandle']])
            call(0x021EEB70,[0x5C])
            call(0x0202AC4C,[OBJECT])
            store(0x2C,0)
            store(0x2B,0)
            store(8,0x1B)
    failures=[]
    for name,actual,expected in [('raw state',result['stateHex'],state.hex()),('ordered own writes',result['writes'],writes),('complete consumed word boundaries',contracts(result),calls),('raw R0',result['registers'][0],0)]:
        if actual!=expected:
            failures.append(name)
    expected=bytearray(vm.beforeMemory)
    expected[STATE-0x02000000:STATE-0x02000000+len(state)]=state
    low=result['privateStackStart']-0x02000000
    high=B.SP-0x02000000
    if result['memory'][:low]!=expected[:low]or result['memory'][high:]!=expected[high:]:
        failures.append('complete independent nonstack RAM')
    if result['nativeEntries']or result['nativePhysicalReturns']or result['rngState']!=profile['seed']:
        failures.append('unexpected original callee or RNG execution')
    return failures
