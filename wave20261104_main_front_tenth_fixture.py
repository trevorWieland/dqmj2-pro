import itertools
import struct
from wave20261104_main_front_eighth_common import Machine,RAM,STOP,STACK
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_SP

GET=0x020649c0
RANDOM=0x0203d294
BUILD=0x02044ff4
QUERY=0x02087544
LOAD=0x0204535c
PALETTE_A=0x020481b8
PALETTE_B=0x0204820c
CONFIG=0x020faaec
BANK_A=0x020fab2c
BANK_B=0x020fab30


class CallerMachine(Machine):
    def store(self,uc,kind,where,size,value,unused):
        if size==4 and any(where==base+i*144 for base in [BANK_A,BANK_B] for i in range(3)):
            self.writes.append(('caller',where,size,value));return
        super().store(uc,kind,where,size,value,unused)


def cases(address):
    if address==0x02043570:return [dict(kinds=kinds) for kinds in itertools.product([-32768,-1,0,32767],repeat=3)]
    return [dict(index=i,palette=p,flags=flags,wide=wide) for i,p,flags,wide in itertools.product(range(3),[False,True],[(0,0),(1,1),(0,1),(1,0)],[False,True])]


def run(address,code,case):
    memory=bytearray((i*7+23)&255 for i in range(0x8000));expected=bytearray(memory)
    if address==0x02043570:
        args=[];result=sum(k>=0 for k in case['kinds'])
        for i,kind in enumerate(case['kinds']):
            struct.pack_into('<h',memory,0x1000+i*0x210+0x2e,kind)
            memory[0x1000+i*0x210+0x30]=[0,1,255][i]
        expected=bytearray(memory)
    else:
        index=case['index'];screen=0x10001 if case['wide'] else index
        tile=0x80000001 if case['wide'] else 9+index
        args=[index,screen,tile];result=None
    m=CallerMachine(address,code,memory,args);state=dict(stopped=False,slot=-1,rng=0,lookup=0,queries=0,built=[])
    if address==0x020462e0:
        palette=RAM+0x6000 if case['palette'] else 0
        config=struct.pack('<IIiiI',RAM+0x5000,palette,17+index,8+index*4,0x88776655)
        m.uc.mem_write(CONFIG+index*20,config)
        for base in [BANK_A,BANK_B]:
            for i in range(3):m.uc.mem_write(base+i*144,struct.pack('<I',0x55550000+i))
    def step(uc,pc,size,unused):
        if pc==STOP:state['stopped']=True;uc.emu_stop();return
        allowed=[GET,RANDOM,BUILD] if address==0x02043570 else [QUERY,LOAD,PALETTE_A,PALETTE_B]
        if pc in allowed:
            a=m.arguments();m.calls.append((pc,*a));answer=0
            if pc==GET:
                assert a[0]==state['lookup'];state['slot']=a[0];state['lookup']+=1;state['rng']=0
                answer=RAM+0x1000+a[0]*0x210
            elif pc==RANDOM:
                assert a[0]==249 and state['rng']<3
                i=state['slot'];assert case['kinds'][i]>=0
                answer=[0,127,248][state['rng']]
                expected[0x1000+i*0x210+12+state['rng']]=(answer+7)&255
                state['rng']+=1
            elif pc==BUILD:
                i=state['slot'];kind=case['kinds'][i];value=[0,1,255][i]
                assert state['rng']==3 and a[:3]==[RAM+0x1000+i*0x210+0xb6,kind,value]
                block=bytes([0xa0+i,kind&255,value,0]);m.provide(a[0],block)
                offset=a[0]-RAM;expected[offset:offset+4]=block;state['built'].append(i);answer=a[0]
            elif pc==QUERY:
                assert a[0]==index and state['queries']<2
                answer=case['flags'][state['queries']];state['queries']+=1
            elif pc==LOAD:
                fifth=struct.unpack('<I',uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4))[0]
                assert a[:4]==[0 if case['flags'][0] else 1,screen&255,RAM+0x5000,(tile<<5)&0xffffffff]
                assert fifth==17+index
                m.calls[-1]=(*m.calls[-1],fifth)
            else:
                assert pc==(PALETTE_A if case['flags'][1] else PALETTE_B)
                assert a[:3]==[palette,128,8+index*4]
            m.finish_call(answer);return
        assert address<=pc<address+len(code),hex(pc)
    m.uc.hook_add(UC_HOOK_CODE,step);m.uc.emu_start(address,STOP+4,count=50000)
    assert state['stopped'];out=m.snapshot(True)
    assert out['ram']==bytes(expected)
    if address==0x02043570:
        assert out['registers'][0]==result and state['lookup']==3
        assert state['built']==[i for i,k in enumerate(case['kinds']) if k>=0]
    else:
        assert state['queries']==1+int(case['palette'])
        assert bytes(m.uc.mem_read(CONFIG+index*20,20))==config
        for base,wanted in [(BANK_A,screen),(BANK_B,tile)]:
            for i in range(3):assert struct.unpack('<I',m.uc.mem_read(base+i*144,4))[0]==(wanted if i==index else 0x55550000+i)
    return out


def execute(address,native,source,bindings):
    vectors=cases(address);wrong=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if address==0x02043570:
            if any(k>=0 for k in case['kinds']):
                assert all(call[1]==249 and call[1]!=248 for call in a['calls'] if call[0]==RANDOM);wrong+=1
        else:
            load=next(call for call in a['calls'] if call[0]==LOAD)
            assert load[-1]!=8+case['index']*4;wrong+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=len(vectors),actualSourceReturns=len(vectors),
        allGprsCpsrOrderedCallerAndProvidedWritesAndRamCompared=True,calleeSavedAndStackAbiChecked=True,
        semanticModelControlsRejected=wrong,wrongModels='Random bound248 or replace the fifth loader word with palette bytes',
        threeWordBuilderAndFiveWordResourceLoaderContracts=True,nativeCalleeBodiesExecuted=0,
        graphicsRngBuilderHardwareOrGameExecutionCredit=0)
