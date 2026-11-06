import itertools
import struct
from wave20261104_main_front_eighth_common import Machine,RAM,STACK,STOP,signed
from unicorn import UC_HOOK_CODE

LOOKUP=0x020446cc
IDENTITY=0x02000ce8
ROTATION=0x02028044
TRANSFORM=0x0200103c
END=0x020283fc
START=0x020283dc


def tagged_matrix(angle):
    value=signed(angle)
    return [4096,value%97,17,31,4096,(value>>3)%89,(value>>4)%79,13,4096]


def transform(vector,matrix):
    return [signed(sum(signed(vector[j])*matrix[j*3+i] for j in range(3))>>12) for i in range(3)]


def cases():
    rows=[dict(null=True,active=0,loop=0,index=0,length=3,angle=0,publish=0,available=3)]
    rows.append(dict(null=False,active=0,loop=0,index=0,length=3,angle=0,publish=1,available=3))
    for loop,index,angle,publish,available in itertools.product([0,1],[0,2],[0,0x1000,-0x123],[0,1],[0,1,2,3]):
        rows.append(dict(null=False,active=1,loop=loop,index=index,length=3,angle=angle,publish=publish,available=available))
    return rows


def run(address,code,case):
    memory=bytearray((i*13+11)&255 for i in range(0x8000))
    a=[0x1234,-0x2468,0x3456];b=[-0x1357,0x3579,0x4567];offset=[-0x1000,0x2000,0x3000]
    memory[0]=case['active'];memory[1]=case['loop']
    struct.pack_into('<i',memory,4,case['index']);struct.pack_into('<3i',memory,0x20,*offset)
    struct.pack_into('<iI',memory,0x2c,case['angle'],RAM+0x300)
    struct.pack_into('<IiII',memory,0x300,0x8888,case['length'],0x400,0x410)
    struct.pack_into('<3i',memory,0x400,*a);struct.pack_into('<3i',memory,0x410,*b)
    m=Machine(address,code,memory,[0 if case['null'] else RAM,case['publish']])
    expected=bytearray(memory);expected_vectors=None
    if case['null'] or not case['active']:result=0xffffffff
    else:
        result=0
        if case['available']==3:
            matrix=tagged_matrix(case['angle'])
            aa=transform(a,matrix) if case['angle'] else a
            bb=transform(b,matrix) if case['angle'] else b
            start=[signed(x+y) for x,y in zip(aa,offset)];end=[signed(x+y) for x,y in zip(bb,offset)]
            struct.pack_into('<3i',expected,8,*start);struct.pack_into('<3i',expected,0x14,*end)
            expected_vectors=(start,end)
        next_index=case['index']+1
        if next_index>=case['length']:
            if case['loop']:next_index=0
            else:expected[0]=0;result=1
        struct.pack_into('<i',expected,4,next_index)
    state=dict(stopped=False,lookup=0,matrix=None,transformed=0,publication=[])
    def step(uc,pc,size,unused):
        if pc==STOP:state['stopped']=True;uc.emu_stop();return
        if pc in [LOOKUP,IDENTITY,ROTATION,TRANSFORM,END,START]:
            values=m.arguments();m.calls.append((pc,*values));answer=0
            if pc==LOOKUP:
                i=state['lookup'];assert values[:3]==[RAM+0x300,case['index'],i]
                answer=RAM+0x400+i*16 if case['available']&(1<<i) else 0
                state['lookup']+=1
            elif pc==IDENTITY:
                matrix=[4096,0,0,0,4096,0,0,0,4096]
                assert STACK<=values[0] and values[0]+36<STACK+0x10000
                state['matrix']=values[0];m.provide(values[0],struct.pack('<9i',*matrix))
            elif pc==ROTATION:
                assert values[:2]==[state['matrix'],case['angle']&0xffffffff]
                m.provide(values[0],struct.pack('<9i',*tagged_matrix(case['angle'])))
            elif pc==TRANSFORM:
                assert values[0]==values[2] and values[1]==state['matrix']
                assert values[0] in [state['matrix']+36,state['matrix']+48]
                vector=struct.unpack('<3i',uc.mem_read(values[0],12))
                assert list(vector)==(b if state['transformed']==0 else a)
                matrix=struct.unpack('<9i',uc.mem_read(values[1],36))
                assert list(matrix)==tagged_matrix(case['angle'])
                m.provide(values[2],struct.pack('<3i',*transform(vector,matrix)));state['transformed']+=1
            else:
                assert values[0]==0 and expected_vectors and case['publish']
                expected_vector=expected_vectors[1] if pc==END else expected_vectors[0]
                assert [signed(v) for v in values[1:4]]==expected_vector
                state['publication'].append(pc)
            m.finish_call(answer);return
        assert address<=pc<address+len(code),hex(pc)
    m.uc.hook_add(UC_HOOK_CODE,step);m.uc.emu_start(address,STOP+4,count=50000)
    assert state['stopped'];out=m.snapshot(True)
    assert out['registers'][0]==result and out['ram']==bytes(expected)
    active=bool(not case['null'] and case['active'])
    assert state['lookup']==(2 if active else 0)
    assert state['transformed']==(2 if active and case['available']==3 and case['angle'] else 0)
    assert state['publication']==([END,START] if active and case['available']==3 and case['publish'] else [])
    return out


def execute(address,native,source,bindings):
    vectors=cases();wrong=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if case['active'] and not case['null'] and case['available']==3 and case['angle']:
            matrix=tagged_matrix(case['angle']);swapped=transform([0x1234,-0x2468,0x3456],matrix)
            end=struct.unpack_from('<3i',a['ram'],0x14)
            assert list(end)!=[signed(x+y) for x,y in zip(swapped,[-0x1000,0x2000,0x3000])];wrong+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=len(vectors),actualSourceReturns=len(vectors),
        allGprsCpsrOrderedCallerAndProvidedWritesAndRamCompared=True,calleeSavedAndStackAbiChecked=True,
        semanticModelControlsRejected=wrong,wrongModel='Use the first transformed vector for the second endpoint',
        taggedRotationMatrixAndVectorProviders=True,nativeCalleeBodiesExecuted=0,trigonometryGraphicsHardwareOrGameExecutionCredit=0)
