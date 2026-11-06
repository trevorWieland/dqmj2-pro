import random
import struct
from ov001_recruit360_fixture_20261031 import STATE,TEMPLATE,ARCHIVE
BASE=0x02000000
RECORDS,WINDOW,CLEAR=0x021BD674,0x0223A7FC,0x0223DF3C

def read(raw,offset,size,signed=False):return int.from_bytes(raw[offset:offset+size],'little',signed=signed)

def put(raw,offset,size,value):raw[offset:offset+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')

def recipes():
    return[dict(seed=360000+i,phase=phase,groupCase=i%4,stride=[12,36,128][i%3],ioResult=[0,1,0xFFFFFFFF,0xA3600000][i%4])for i,phase in enumerate([-1,0,1,2,3,4,127,0,1,3,0,1,3,0,1,3])]

def setup(obj,recipe):
    rng=random.Random(recipe['seed'])
    state=bytearray(rng.randbytes(0x34))
    put(state,0x14,4,recipe['phase'])
    put(state,0x1C,4,101)
    obj.u.mem_write(STATE,bytes(state))
    obj.u.mem_write(TEMPLATE,rng.randbytes(132))
    obj.u.mem_write(TEMPLATE+0x67,bytes([1]))
    obj.u.mem_write(CLEAR,rng.randbytes(8))
    obj.u.mem_write(RECORDS,bytes(13200))
    for index in range(3):
        row=bytearray(rng.randbytes(132))
        put(row,20,4,101+2*index)
        put(row,24,2,367)
        obj.u.mem_write(RECORDS+132*index,bytes(row))
    groups=[[101,103,0,105,0,0],[0,0,0,0,0,0],[101,101,999,105,0,999],[105,103,101,101,103,105]][recipe['groupCase']]
    obj.u.mem_write(0x021BD540,struct.pack('<6I',*groups))
    archive=bytearray(0x1000)
    put(archive,0,4,16)
    for index in range(17):put(archive,4+4*index,4,0x80+index*recipe['stride'])
    obj.u.mem_write(ARCHIVE,bytes(archive))
    obj.ioResult=recipe['ioResult']

def model(before,after,result,provided,recipe):
    expected=bytearray(before)
    phase=recipe['phase']
    offset=STATE-BASE
    count=sum(read(before,0x021BD540-BASE+4*i,4)in[101,103,105]for i in range(6))
    pointer1=ARCHIVE+0x80+recipe['stride']
    pointer8=ARCHIVE+0x80+8*recipe['stride']
    events=[]
    def add(address,args):events.append((hex(address),args))
    if phase==0:
        add(0x0207E720,None)
        add(0x0206DCD0,[RECORDS])
        add(0x02041538,[0,2,16])
        row=before[RECORDS-BASE:RECORDS-BASE+132]
        want=dict(kind=1,species=read(row,24,2,True),variant=row[26],raw=row[27],namePointer=TEMPLATE+0x6D,length=16,last=0)
        if provided[0].get('descriptor')!=want or provided[0].get('nameBytes')!=before[TEMPLATE-BASE+0x6D:TEMPLATE-BASE+0x81].hex():raise ValueError('Recruit360 descriptor/name-byte model differs')
    if phase==1:
        for slot in range(4):add(0x02045680,[slot])
        for index in range(4):put(expected,offset+0x24+4*index,4,32)
        add(0x02068AE8,[])
        add(0x0203CC2C,[0x0222F0B0,2])
        add(0x02045490,[3,pointer1,0,recipe['stride']])
        put(expected,offset+0x30,4,recipe['stride'])
        add(0x02045994,[3,pointer8,0,2048])
        add(0x0202A498,[2,ARCHIVE])
        put(expected,CLEAR-BASE,1,0)
        put(expected,CLEAR-BASE+4,4,0)
        add(0x0220AAB8,[STATE+0x24])
        add(0x0220A5E0,[])
        add(0x0220AD70,[WINDOW])
        add(0x0220AF00,[WINDOW,0])
        add(0x0220AF68,[WINDOW])
        add(0x0220A6CC,[101])
        add(0x02068EB8,[2,0,0,count])
        add(0x0206BE08,[0,0])
        put(expected,offset+6,1,1)
        add(0x0206DE44,[1])
        add(0x02041538,[0,2,16])
    if phase==3:
        add(0x0220AF00,[WINDOW,0])
        add(0x0220AF68,[WINDOW])
        add(0x0220AFE4,[WINDOW,read(before,offset+0x18,4)])
        item=provided[-1]
        add(0x0220B0F0,None)
        coordinates=[read(before,0x0222E0E4-BASE+2*i,2)for i in range(2)]
        if item['arguments'][:2]!=[WINDOW,2]or item['arguments'][3:]!=[2,9,14]or item.get('coordinates')!=coordinates:raise ValueError('Recruit360 coordinate call model differs')
    if len(provided)!=len(events):raise ValueError('Recruit360 provider event count differs')
    for actual,(address,args)in zip(provided,events):
        if actual['entry']!=address or args is not None and actual['arguments']!=args:raise ValueError(('Recruit360 independent provider contract differs',address,actual,args))
        want=ARCHIVE if address=='0x203cc2c'else recipe['ioResult']
        if actual['providedReturnWord']!=want:raise ValueError('Recruit360 declared provider result differs')
    lo,hi=0x027E0000-BASE,0x027F1000-BASE
    if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]or result!=(4 if phase==3 else 1):raise ValueError('Recruit360 independent complete nonstack RAM/return model differs')
    return dict(returnWord=result,groupResolvedCount=count,providerCalls=len(events),completeIndependentNonstackRam=True,phase=phase,sharedAlias='STATE+0x30 is the fourth32-bit slot at223DF1C; final phase1 value is chunk1 size')
