import itertools
import struct
from wave20261104_main_front_eighth_common import Machine,RAM,STACK,STOP,STATUS,signed
from unicorn import UC_HOOK_CODE

INIT=0x0200bd04
OPEN=0x0200bfe4
READ=0x0200c180
SEEK=0x0200c190
CLOSE=0x0200c02c
HEAP=0x0202a250
ALLOC=0x0202a37c
FLUSH=0x02007308
TERMINATE=0x02008430


def cases():
    rows=[]
    for index,size,heap,read in itertools.product([0,1],[None,0,5],[3,0xffffffff],['full',0,-1,1]):
        rows.append(dict(index=index,size=size,heap=heap,read=read,open=True,invalid=None))
    rows.extend([dict(index=0,size=0,heap=3,read='full',open=False,invalid=None),dict(index=2,size=0,heap=3,read='full',open=True,invalid='index'),dict(index=0,size=0,heap=3,read='full',open=True,invalid='offset')])
    return rows


def run(address,code,case):
    memory=bytearray(0x8000);path=RAM+0x5000;sizeptr=RAM+0x5100 if case['size'] is not None else 0
    memory[0x5000:0x500b]=b'local.bin\0\0'
    if sizeptr:struct.pack_into('<i',memory,0x5100,case['size'])
    m=Machine(address,code,memory,[path,case['index'],case['heap'],sizeptr]);expected=bytearray(memory)
    offsets=[16,29,42]
    if case['invalid']=='offset':offsets=[29,16,42]
    contents=struct.pack('<4I',2,*offsets)+bytes((i*17+9)&255 for i in range(64))
    state=dict(file=None,position=0,allocated=False,stopped=None,reads=0)
    requested=case['size'] if case['size'] else 13
    report=requested if case['read']=='full' else case['read']
    expected_status=2 if not case['open'] else (0 if report>0 else 1)
    if case['invalid']:expected_status=0
    def step(uc,pc,size,unused):
        if pc==STOP:state['stopped']='return';uc.emu_stop();return
        if pc==TERMINATE:
            assert case['invalid'];state['stopped']='termination-entry';uc.emu_stop();return
        if pc in [INIT,OPEN,READ,SEEK,CLOSE,HEAP,ALLOC,FLUSH]:
            a=m.arguments();m.calls.append((pc,*a[:3]));result=1
            if pc==INIT:
                assert STACK<=a[0] and a[0]+72<=STACK+0x10000
                state['file']=a[0];m.provide(a[0],bytes(72))
            elif pc==HEAP:assert case['heap']==0xffffffff;result=3
            elif pc==ALLOC:
                assert a[:3]==[3,(requested+3)&~3,4]
                result=RAM+0x6000;state['allocated']=True
                block=bytes([0xa5])*a[1];m.provide(result,block);expected[0x6000:0x6000+len(block)]=block
            elif pc==FLUSH:assert a[:2]==[RAM+0x6000,requested] and report>0
            else:
                assert a[0]==state['file']
                if pc==OPEN:assert a[1]==path;result=int(case['open'])
                elif pc==SEEK:
                    assert a[2]==0;state['position']=signed(a[1])
                elif pc==READ:
                    length=signed(a[2]);assert length>=0
                    payload=state['allocated']
                    result=report if payload else 4
                    copied=min(length,max(0,result))
                    chunk=contents[state['position']:state['position']+copied]
                    assert len(chunk)==copied
                    if chunk:
                        m.provide(a[1],chunk)
                        if RAM<=a[1]<RAM+0x8000:expected[a[1]-RAM:a[1]-RAM+len(chunk)]=chunk
                    state['position']+=copied;state['reads']+=1
                elif pc==CLOSE:assert state['allocated']
            m.finish_call(result);return
        assert address<=pc<address+len(code),hex(pc)
    m.uc.hook_add(UC_HOOK_CODE,step);m.uc.emu_start(address,STOP+4,count=50000)
    assert state['stopped']==('termination-entry' if case['invalid'] else 'return')
    if case['open'] and not case['invalid'] and sizeptr and not case['size']:struct.pack_into('<i',expected,0x5100,13)
    out=m.snapshot(state['stopped']=='return')
    assert out['ram']==bytes(expected) and out['status']==expected_status
    if state['stopped']=='return':assert out['registers'][0]==(RAM+0x6000 if case['open'] else 0)
    assert len([x for x in m.calls if x[0]==FLUSH])==int(case['open'] and not case['invalid'] and report>0)
    return dict(snapshot=out,kind=state['stopped'])


def execute(address,native,source,bindings):
    vectors=cases();returned=stopped=wrong=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if a['kind']=='return':returned+=1
        else:stopped+=1
        if case['open'] and not case['invalid'] and case['read']==0:
            assert a['snapshot']['status']==1;wrong+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=returned,actualSourceReturns=returned,
        actualNativeTerminationEntryStops=stopped,actualSourceTerminationEntryStops=stopped,
        semanticModelControlsRejected=wrong,wrongModel='Treat a zero reported payload read as success',
        allGprsCpsrOrderedCallerAndProvidedWritesAndRamCompared=True,calleeSavedAndStackAbiCheckedOnReturnsOnly=True,
        providedFileImageAndSdkContracts=True,nativeCalleeBodiesExecuted=0,physicalFilesystemCacheAllocationOrGameExecutionCredit=0)
