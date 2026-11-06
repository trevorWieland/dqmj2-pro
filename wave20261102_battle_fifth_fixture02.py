import struct

import ov001_selector917_machine_20261102 as B

STATE=0x022388EC
ACTOR=0x02540000
SIZES={0x021DF680:392,0x021DE40C:388}
PROVIDERS={0x021DF680:{0x021DCFA0:1,0x021D7E80:1,0x021F1294:2,0x021F1354:4,0x021F1438:1,0x021F14A4:0,0x021F14E4:0,0x021F1324:0},0x021DE40C:{0x0202A634:0,0x021F1798:0,0x021DCB44:0,0x021E8748:0,0x0220B6C4:0,0x02044424:1,0x02210DD0:0,0x021F165C:0,0x02210E08:0}}


def word(value):
    return value&0xFFFFFFFF


def signed_byte(value):
    value&=255
    return value-256 if value&128 else value


def profiles(entry):
    output=[]
    def add(**changes):
        p=dict(ordinal=len(output),target=entry,rawPhase=0,rawCounter=29,handle=0xFEDC5678,handleResult=0x81234567,slotByte=0xF1,wait=0,mode=2,gateByte=0,condition=0,pressed=0,rawResult=0xE7,rawTicks=0x12345678,controlCase=False,counter=0,phase=0,gate=0,seed=0x12345678,threshold=0,busy=0)
        p.update(changes)
        output.append(p)
    for phase in range(256):
        add(rawPhase=phase,wait=phase&1,controlCase=phase==255)
    if entry==0x021DF680:
        for counter in [0,28,29,30,126,127,128,255]:
            for handle in [0xFFFFFFFF,0,0x80000000,0x12345678]:
                add(rawPhase=10,rawCounter=counter,handleResult=handle,controlCase=True)
        for handle in [0xFFFFFFFF,0,0x80000000,0x12345678]:
            add(rawPhase=0,handleResult=handle,controlCase=True)
        add(rawPhase=20,wait=0,controlCase=True)
        add(rawPhase=20,wait=0xFFFFFFFF,controlCase=True)
        add(rawPhase=100,controlCase=True)
    else:
        for phase in [0,10]:
            for mode in [0,1,2,3,4,5,6,255]:
                for gate in [0,1]:
                    for condition in [0,0x80000000]:
                        add(rawPhase=phase,mode=mode,gateByte=gate,condition=condition,pressed=0xFFFFFFFF,controlCase=True)
        for pressed in [0,1]:
            add(rawPhase=10,mode=4,pressed=pressed,controlCase=True)
        for wait in [0,0xFFFFFFFF]:
            add(rawPhase=20,wait=wait,controlCase=True)
        add(rawPhase=100,controlCase=True)
    return output


def returned(p,address):
    return {0x021DCFA0:p['handleResult'],0x021F14E4:p['wait'],0x021E8748:p['condition'],0x02044424:p['pressed'],0x02210E08:p['wait']}.get(address,word(0xABCD0000+(address&0xFFFF)))


class Machine(B.Machine):
    def __init__(self,main,overlay,images,p):
        super().__init__(main,overlay,None,p)
        entry=p['target']
        self.ranges={entry:(SIZES[entry],0)}
        self.u.mem_write(STATE,bytes(0x9C))
        self.u.mem_write(STATE+8,bytes([0xE5]))
        self.u.mem_write(ACTOR,bytes(0x400))
        self.u.mem_write(ACTOR+0x31E,bytes([p['slotByte']]))
        if entry==0x021DF680:
            self.u.mem_write(STATE+0x30,bytes([p['rawCounter'],p['rawPhase']]))
            self.u.mem_write(STATE+0x3C,B.pack([p['handle']]))
            self.u.mem_write(STATE+0x48,B.pack([ACTOR]))
        else:
            self.u.mem_write(STATE+1,bytes([p['rawResult']]))
            self.u.mem_write(STATE+5,bytes([p['rawPhase'],p['mode']]))
            self.u.mem_write(STATE+9,bytes([p['gateByte']]))
            self.u.mem_write(STATE+0x38,B.pack([p['rawTicks']]))
        for address,image in(images or{}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.beforeState=bytes(self.u.mem_read(STATE,0x9C))
        self.beforeMemory=bytes(self.u.mem_read(0x02000000,0x800000))

    def code(self,u,pc,size,unused):
        providers=PROVIDERS[self.p['target']]
        if pc in providers:
            words=[u.reg_read(r)for r in B.REGS[:4]]
            value=returned(self.p,pc)
            self.provided.append(dict(target=hex(pc),consumedWords=words[:providers[pc]],rawCallerWords=words,returnWord=value))
            for index in[0,1,2,3,12]:
                u.reg_write(B.REGS[index],word(0xC0DE0000+len(self.provided)*0x100+index*17))
            u.reg_write(B.REGS[0],value)
            flags=u.reg_read(B.UC_ARM_REG_CPSR)
            u.reg_write(B.UC_ARM_REG_CPSR,(flags&0x0FFFFFFF)|((self.p['ordinal']&15)<<28))
            u.reg_write(B.UC_ARM_REG_PC,u.reg_read(B.REGS[14])&~1)
            return
        entry=self.p['target']
        if entry<=pc<entry+SIZES[entry]:
            self.pcs.add(pc)
        super().code(u,pc,size,unused)

    def run(self,entry):
        result=super().run(entry)
        result['stateHex']=bytes(self.u.mem_read(STATE,0x9C)).hex()
        return result


def model(vm,result):
    p=vm.p
    state=bytearray(vm.beforeState)
    calls=[]
    writes=[]
    expected_return=0
    def call(address,args):
        value=returned(p,address)
        calls.append(dict(target=hex(address),consumedWords=[word(value)for value in args],returnWord=value))
        return value
    def store(offset,value,width=1):
        value&=(1<<(width*8))-1
        state[offset:offset+width]=value.to_bytes(width,'little')
        writes.append([STATE+offset,width,value])
    if p['target']==0x021DF680:
        phase=p['rawPhase']
        if phase==0:
            handle=call(0x021DCFA0,[ACTOR])
            store(0x3C,handle,4)
            if handle!=0xFFFFFFFF:
                call(0x021D7E80,[ACTOR])
                call(0x021F1294,[16,2])
                call(0x021F1354,[1,5,handle&65535,1])
                call(0x021F1438,[p['slotByte']])
                store(0x30,0)
                store(0x31,10)
            else:
                store(0x31,100)
                expected_return=1
        elif phase==10:
            store(0x30,p['rawCounter']+1)
            if signed_byte(state[0x30])>=30:
                call(0x021F14A4,[])
                handle=call(0x021DCFA0,[ACTOR])
                store(0x3C,handle,4)
                store(0x31,20 if handle!=0xFFFFFFFF else 100)
                expected_return=int(handle==0xFFFFFFFF)
        elif phase==20:
            if call(0x021F14E4,[])==0:
                call(0x021F1354,[1,5,p['handle']&65535,1])
                call(0x021F1438,[p['slotByte']])
                store(0x31,10)
                store(0x30,0)
        elif phase==100:
            call(0x021F1324,[])
            store(8,0x18)
            store(0x31,0)
            expected_return=1
    else:
        call(0x0202A634,[])
        call(0x021F1798,[])
        if state[5]==0:
            call(0x021DCB44,[])
            store(5,10)
        selected=False
        if state[5]==10:
            if state[6]>=2:
                if state[9]==0 and call(0x021E8748,[])!=0 and state[6]!=4:
                    call(0x0220B6C4,[])
                    selected=True
                    store(9,1)
                    store(1,0x23)
                elif state[6]==2:
                    store(1,3)
                    selected=True
                elif state[6]==3:
                    store(1,0x13)
                    selected=True
                elif state[6]==4:
                    store(1,0x33 if call(0x02044424,[0x40])else 0x1D)
                    selected=True
                elif state[6]==5:
                    store(1,0x23)
                    selected=True
            if selected:
                call(0x02210DD0,[])
                call(0x021F165C,[])
                store(5,20)
            else:
                store(0x38,p['rawTicks']+1,4)
        if state[5]==20 and call(0x02210E08,[])==0:
            store(5,100)
        if state[5]==100:
            store(5,0)
            store(8,state[1])
    failures=[]
    contracts=[{key:row[key]for key in['target','consumedWords','returnWord']}for row in result['provided']]
    for name,actual,expected in [('raw state',result['stateHex'],state.hex()),('ordered writes',result['writes'],writes),('consumed boundary words',contracts,calls),('R0',result['registers'][0],expected_return)]:
        if actual!=expected:
            failures.append(name)
    expected=bytearray(vm.beforeMemory)
    expected[STATE-0x02000000:STATE-0x02000000+len(state)]=state
    low=result['privateStackStart']-0x02000000
    high=B.SP-0x02000000
    if result['memory'][:low]!=expected[:low]or result['memory'][high:]!=expected[high:]:
        failures.append('independent complete nonstack RAM')
    if result['nativeEntries']or result['nativePhysicalReturns']or result['rngState']!=p['seed']:
        failures.append('unexpected original helper or RNG execution')
    return failures
