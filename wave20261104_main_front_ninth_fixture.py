import itertools
from wave20261104_main_front_eighth_common import Machine,RAM,STOP,signed
from unicorn import UC_HOOK_CODE

MODE=0x0206533c
RANDOM=0x0203d294
QUERY=0x0220fed4
GATE=0x020f69c4
ORDER=0x020444ec
A=0x01ffa824
B=0x01ffa84c
SLOTS=0x021db438
TEST=0x021db8d0
APPLY=0x0220ed5c


def cases(address):
    if address==0x020438f4:
        values=[0xffffffff,0,7,31,32,0x80000000,0x7fffffff]
        rows=[dict(mode=0,values=[a,b],threshold=t) for a,b,t in itertools.product(values,[0xffffffff,0,32],[0,7,31])]
        rows += [dict(mode=mode,values=[a],threshold=t) for mode,a,t in itertools.product([1,2],values,[0,7,31])]
        rows += [dict(mode=mode,values=[],threshold=7) for mode in [3,4,0xffffffff]]
        return rows
    orders=[(0,0,0),(1,0x100,128),(1,0xff,128),(1,0x800000ff,255)]
    rows=[dict(flag=0,mode=mode,a=a,b=b,mask=mask) for (mode,a,b),mask in itertools.product(orders,[0,0xfff,0x555,0x800])]
    return rows+[dict(flag=flag,mode=1,a=0,b=0,mask=0xfff) for flag in [1,255]]


def expected_selector(case,greater_equal=False):
    mode=case['mode'];values=case['values'];threshold=case['threshold']
    predicate=lambda value:signed(value)>=threshold if greater_equal else signed(value)>threshold
    if mode==0:return 1 if predicate(values[0]) else (2 if predicate(values[1]) else 0)
    if mode in [1,2]:return mode if predicate(values[0]) else 0
    return 0


def run(address,code,case):
    memory=bytes((i*19+13)&255 for i in range(0x8000))
    m=Machine(address,code,memory,[]);m.uc.mem_map(0x01ff8000,0x8000);m.uc.mem_map(0x02200000,0x10000);state=dict(stopped=False,query=0,random=0,visits=0,groups=[])
    flags=[1<<i for i in range(11)]+[0x80000000]
    if address==0x02043e7c:
        gate=bytes([case['flag'],0xa5,0xa5,0xa5]);m.uc.mem_write(GATE,gate)
        order=[0,2,1,3] if not case['mode'] or (case['a']&255)<case['b'] else [1,3,0,2]
        expected=0 if case['flag'] else sum(value for i,value in enumerate(flags) if case['mask']&(1<<i))
    else:expected=expected_selector(case)
    def step(uc,pc,size,unused):
        if pc==STOP:state['stopped']=True;uc.emu_stop();return
        imports=[MODE,RANDOM,QUERY] if address==0x020438f4 else [ORDER,A,B,SLOTS,TEST,APPLY]
        if pc in imports:
            a=m.arguments();m.calls.append((pc,*a));result=0
            if pc==MODE:result=case['mode']
            elif pc==QUERY:
                index=state['query'];mode=case['mode']
                assert mode in [0,1,2] and index<len(case['values'])
                pair=[index,1] if mode==0 else ([0,12] if mode==1 else [1,27])
                assert a[:2]==pair and index==state['random']
                result=case['values'][index];state['query']+=1
            elif pc==RANDOM:
                assert a[0]==32 and state['query']==state['random']+1
                result=case['threshold'];state['random']+=1
            elif pc==ORDER:assert not case['flag'];result=case['mode']
            elif pc==A:assert case['mode'];result=case['a']
            elif pc==B:assert case['mode'];result=case['b']
            elif pc==SLOTS:
                group=order[len(state['groups'])];assert a[:2]==[group,0]
                state['groups'].append(group);result=RAM+0x1000+group*0x1000
            else:
                group,offset=divmod(a[0]-(RAM+0x1000),0x1000)
                index,remainder=divmod(offset,0x440)
                assert not remainder and 0<=group<4 and 0<=index<3
                global_index=group*3+index
                if pc==TEST:
                    assert state['groups'] and group==state['groups'][-1]
                    assert index==state['visits']%3;state['visits']+=1
                    result=int(bool(case['mask']&(1<<global_index)))
                else:
                    assert case['mask']&(1<<global_index);result=flags[global_index]
            m.finish_call(result);return
        assert address<=pc<address+len(code),hex(pc)
    m.uc.hook_add(UC_HOOK_CODE,step);m.uc.emu_start(address,STOP+4,count=50000)
    assert state['stopped'];out=m.snapshot(True)
    assert out['registers'][0]==expected and out['ram']==memory
    if address==0x020438f4:
        needed=2 if case['mode']==0 and signed(case['values'][0])<=case['threshold'] else int(case['mode'] in [0,1,2])
        assert state['query']==state['random']==needed
        assert sum(c[0]==MODE for c in out['calls'])==1
    else:
        assert bytes(m.uc.mem_read(GATE,4))==gate
        assert state['groups']==([] if case['flag'] else order)
        assert state['visits']==(0 if case['flag'] else 12)
        assert sum(c[0]==A for c in out['calls'])==int(not case['flag'] and bool(case['mode']))
        assert sum(c[0]==B for c in out['calls'])==int(not case['flag'] and bool(case['mode']))
    return out


def execute(address,native,source,bindings):
    vectors=cases(address);rejected=equivalent=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if address==0x020438f4:
            wrong=expected_selector(case,True)
            if wrong!=a['registers'][0]:rejected+=1
            else:equivalent+=1
        elif not case['flag']:
            assert a['calls'];rejected+=1
        else:equivalent+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=len(vectors),actualSourceReturns=len(vectors),
        allGprsCpsrOrderedStackWritesAndRamCompared=True,calleeSavedAndStackAbiChecked=True,
        semanticModelControlsRejected=rejected,semanticModelEquivalentInputs=equivalent,
        wrongModels='Use greater-or-equal thresholds; treat the byte gate plus nonzero adjacent bytes as a full-word gate',
        providedMainItcmAndOverlay001ContractsOnly=True,nativeCalleeBodiesExecuted=0,gameHardwareOrRngImplementationExecutionCredit=0)
