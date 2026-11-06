import itertools
import struct
import ov000_controller748_machine_20261101 as M
def profiles():
    result=[];words=[0,1,0x80000000,0xFFFFFFFF];shorts=[-32768,-1,0,1,32767];byteset=[0,1,127,128,255]
    def add(**changes):
        seed=len(result);p=dict(name=f'input-{seed}',seed=seed,index=[0,1,127,255][seed%4],recordFlag=0,width=255,height=255,guards={'3':0,'1':0,'2':0},flagByte=byteset[seed%5],offset=[shorts[seed%5],shorts[(seed+2)%5]],last=[shorts[(seed+1)%5],shorts[(seed+3)%5]],active=0,secondary=0,reference=[0x80000,0x12345678,0x60000],vector=[0x80000,-2147483648,0x60000],touch=[0,byteset[seed%5],byteset[(seed+1)%5]],buttons=0,mode=0,returnWord=words[seed%4]);p.update(changes);result.append(p)
    for flag,width,height in itertools.product([0,255],[31,32,33,255],[23,24,25,255]):add(recordFlag=flag,width=width,height=height)
    for tag,value in itertools.product([3,1,2],[1,0x80000000,0xFFFFFFFF]):g={'3':0,'1':0,'2':0};g[str(tag)]=value;add(guards=g)
    for status,mode,active in itertools.product([0,1,2,3,255],[0,5,128,255],words):add(touch=[status,byteset[len(result)%5],byteset[(len(result)+2)%5]],mode=mode,active=active)
    for buttons,active,secondary in itertools.product([1,0x8000,0xFFFF],words,words):add(buttons=buttons,active=active,secondary=secondary)
    distances=[-12289,-12288,-12287,0,12287,12288,12289]
    for dx,dz in itertools.product(distances,repeat=2):
        seed=len(result);width,height=[33,255][seed%2],[25,255][(seed//2)%2];x,z=[-0x8000000,0x80001,0x8000000][seed%3],[0,0x60001,0x8000000][(seed+1)%3];cx=min(max(x,0x80000),(max(width,32)*8-128)*4096);cz=min(max(z,0x60000),(max(height,24)*8-96)*4096)
        add(width=width,height=height,secondary=words[1+seed%3],active=words[seed%4],vector=[x,-2147483648,z],reference=[cx+dx,0x12345678,cz+dz])
    return result
def model(result):
    p=result['profile'];expected=bytearray(result['before']);calls=[];writes=[]
    def call(entry,kind,*words):calls.append(dict(entry=entry,kind=kind,preparedWords=list(words)))
    def put(address,size,value):
        word=value&((1<<(size*8))-1);expected[address-M.BASE:address-M.BASE+size]=word.to_bytes(size,'little');writes.append([address,size,word])
    def state(offset,size,value):put(M.STATE+offset,size,value)
    call(0x02066C3C,'native');call(0x0202A634,'native');call(0x021DF1F0,'native');call(0x021DF3BC,'native',p['index'])
    raw=None;branch=''
    if p['recordFlag']==255:raw=M.TABLE+14*p['index'];branch='row-byte3-FF'
    elif p['width']<=32 and p['height']<=24:raw=p['height'];branch='minimum-dimensions'
    else:
        for tag in[3,1,2]:
            call(0x02218800,'provided',tag)
            if p['guards'][str(tag)]!=0:raw=p['guards'][str(tag)];branch='provided-guard-'+str(tag);break
    if raw is None:
        status,x,y=p['touch']
        if status==1:call(0x020404E0,'native')
        if status==1 and p['mode']==5:
            state(0x1C,2,x);state(0x1E,2,y);state(0x10,2,0);state(0x12,2,0);state(0x20,4,1)
            call(0x02041510,'provided',1,2,4);call(0x02041560,'provided',10);call(0x020404F0,'native',46);put(M.MODE,1,46);call(0x021E7B9C,'provided',82);call(0x0221993C,'native',0);state(1,1,0);raw=0;branch='status1-mode5'
        elif status==1:
            state(0x1C,2,x);state(0x1E,2,y);raw=M.STATE;branch='status1-cache'
        elif status==3 and p['active']!=0:
            state(0x10,2,p['offset'][0]+x-p['last'][0]);state(0x12,2,p['offset'][1]+y-p['last'][1]);state(0x1C,2,x);state(0x1E,2,y);raw=y;branch='status3-active-delta'
        elif p['buttons']!=0:
            if p['active']==0:raw=0;branch='buttons-inactive'
            else:
                state(0x10,2,0);state(0x12,2,0);state(0x28,4,1);state(0x20,4,0);call(0x021E7B9C,'provided',83);raw=p['returnWord'];branch='buttons-active-reset'
        elif p['secondary']==0:raw=0;branch='secondary-zero'
        else:
            x=min(max(p['vector'][0],0x80000),(max(p['width'],32)*8-128)*4096);z=min(max(p['vector'][2],0x60000),(max(p['height'],24)*8-96)*4096)
            call(0x02219CE4,'native','local-vector12');call(0x021DF1F0,'native');call(0x021DF3BC,'native',p['index'])
            for ref,target,sign in[(p['reference'][0],x-12288,-1),(p['reference'][0],x+12288,1),(p['reference'][2],z-12288,-1),(p['reference'][2],z+12288,1)]:
                if(ref<target if sign<0 else ref>target):raw=target&0xFFFFFFFF;branch='outside-local-bound';break
            if raw is None:
                state(0x28,4,0);call(0x020404F0,'native',5);put(M.MODE,1,5);call(0x0221993C,'native',1);state(1,1,1);call(0x02041510,'provided',0,2,4);call(0x020418E8,'provided',4,10);raw=p['returnWord'];branch='inside-local-bounds'
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError(('748 independent complete nonstack model differs',p['name'],branch))
    if[row[1:]for row in result['nonstackWrites']]!=writes:raise ValueError(('748 independent ordered writes differ',p['name'],branch,[r[1:]for r in result['nonstackWrites']],writes))
    actual=[]
    for entry in result['calls']:
        words=entry['preparedWords']
        if entry['entry']==0x02219CE4:
            if entry['localVectorAtEntry']!=p['vector']or not M.STACK-65536<=words[0]<=M.STACK-12:raise ValueError('748 private copy/clamp argument differs')
            words=['local-vector12']
        actual.append(dict(entry=entry['entry'],kind=entry['kind'],preparedWords=words))
    if actual!=calls:raise ValueError(('748 independent call order/word views differ',p['name'],branch,actual,calls))
    if result['coreRegistersAndCpsr'][0]!=raw:raise ValueError(('748 physical nonsemantic R0 differs',p['name'],branch,hex(result['coreRegistersAndCpsr'][0]),hex(raw)))
    return dict(branch=branch,expectedRawR0=raw,orderedNonstackWrites=len(writes),actualNativeDependencyReturns=sum(c['kind']=='native'for c in calls),providedCalls=sum(c['kind']=='provided'for c in calls),completeNonstackModel=True)
