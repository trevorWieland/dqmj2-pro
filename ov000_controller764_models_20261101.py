import struct
import ov000_controller764_machine_20261101 as M

def profiles():
    cases=[]
    def add(**changes):
        seed=len(cases);p=dict(name=f'controller-{seed}',seed=seed,state=0,mode=[0,3,22,37,128,255][seed%6],renderWord=[0,1,0x80000000,0xFFFFFFFF][seed%4],cleanup14=seed%2,cleanup18=(seed//2)%2,field30=0x12345678,field3c=(seed//3)%2,slot1=[0,128,255][seed%3],slot4=[0,1,255][seed%3],byte2=255,rowFlag=[0,255][seed%2],constructorGate=seed%3,waitGate=(seed//3)%2,uiGate=[0,1,2,255][seed%4],buttonGate=seed%3,exitGate=[0,1,2,255][(seed//2)%4],spriteCount=[-1,0,1,3,8][seed%5],spriteIds=[[0,127,128,255][(seed+i)%4]for i in range(8)],spriteValues=[[-128,-1,0,127][(seed+i)%4]for i in range(8)],reference=[[-0x8000000,0x80001,0x8000000][seed%3],0x12345678,[-0x8000000,0x60001,0x8000000][(seed+1)%3]]);p.update(changes);cases.append(p)
    for state in list(range(13))+[128,255]:
        for branch in range(4):add(state=state,constructorGate=branch%2,waitGate=branch//2,uiGate=branch%2,exitGate=branch)
    for flag in[0,255]:
        for cleanup in[0,1]:add(state=6,mode=3,field3c=0,exitGate=0,rowFlag=flag,cleanup14=cleanup,cleanup18=cleanup,slot4=0)
    for byte in[0,127,128,255]:add(state=2,slot4=255,exitGate=0,cleanup14=1,cleanup18=1,spriteCount=1,spriteIds=[byte]*8)
    add(state=0,constructorGate=2,exitGate=0,slot4=255)
    add(state=1,waitGate=255)
    add(state=8,exitGate=255,uiGate=0)
    add(state=11,exitGate=255,uiGate=0)
    add(state=2,slot4=255,exitGate=0,cleanup14=0x80000000,cleanup18=0xFFFFFFFF,spriteCount=-32768)
    add(state=6,mode=3,field3c=0x80000000,exitGate=1,rowFlag=255,slot4=0)
    return cases

def signed8(value):return value if value<128 else value-256

def model(result,strict_order=True):
    p=result['profile'];expected=bytearray(result['before']);calls=[];writes=[];invocations=0
    def get(address,size=4,signed=False):return int.from_bytes(expected[address-M.BASE:address-M.BASE+size],'little',signed=signed)
    def put(address,size,value):
        word=value&((1<<(size*8))-1);expected[address-M.BASE:address-M.BASE+size]=word.to_bytes(size,'little');writes.append([address,size,word])
    def field(offset,value,size=4):put(M.STATE+offset,size,value)
    def call(address,*args):calls.append(dict(entry=address,kind='native'if address in M.NATIVE else'provided',preparedWords=[value&0xFFFFFFFF if isinstance(value,int)else value for value in args]))
    def invoke():
        nonlocal invocations
        invocations+=1
        if invocations>16:raise ValueError('764 model recursion exceeds bound')
        call(0x0202A634);call(0x020404E0);call(0x022187B8);state=get(M.STATE+3,1);again=False;value=0;mode=signed8(p['mode'])
        if state==0:
            call(0x02214FF0)
            if p['constructorGate']==1:
                call(0x0205FC10,M.RESOURCE,0x0221930C,0x0221938C,0,18,8192,2,0)
                for offset in range(0,208,4):put(M.RESOURCE+offset,4,get(M.TEMPLATE+offset))
                call(0x0205FD0C,M.RESOURCE);field(3,1,1)
            else:
                call(0x0221930C,0);call(0x022189E4,255,get(M.SLOTS+1,1));call(0x02218B4C);call(0x02218B60);field(0x3C,0);field(0x30,0);field(3,2,1)
        elif state==1:
            call(0x0205FD60)
            if p['waitGate']==0:
                call(0x02214FF0)
                if p['constructorGate']==1:field(3,3,1)
                else:field(0x3C,0);field(3,2,1)
                again=True
        elif state==3:call(0x02041538,0,2,10);field(3,4,1)
        elif state==4:
            call(0x02041814)
            if p['uiGate']!=1:field(0x3C,0);field(3,2,1);again=True
        elif state==2:
            call(0x02219494);call(0x020406B8)
            if p['buttonGate']==1:call(0x02214FC8,1)
            if 22<=mode<=27:call(0x02214FC8,2);call(0x020418B0,2)
            if mode==37:call(0x02214FC8,2);call(0x02041538,1,2,10)
            if get(M.STATE+0x3C)==1:call(0x02214FC8,2)
            if get(M.SLOTS+4,1)!=255:call(0x02041538,1,2,30);field(3,5,1)
            call(0x02214FE0)
            if p['exitGate']!=0:field(3,8,1);again=True
        elif state==5:
            call(0x02041814)
            if p['uiGate']!=1:put(M.SLOTS+1,1,get(M.SLOTS+4,1));field(3,6,1)
        elif state==6:
            call(0x021DF3BC,get(M.SLOTS+4,1))
            take=False
            if get(M.STATE+0x3C)==1:
                call(0x02214FE0);take=p['exitGate']!=0
            if take:field(3,8,1);again=True
            else:
                call(0x020404E0)
                if mode==3:
                    for getter,buffer in zip([0x02003EDC,0x02003F80,0x02004078],M.BUFFERS):
                        call(getter);call(0x02008C58,0,buffer,8192)
                        for offset in range(0,8192,4):put(buffer+offset,4,0)
                    if p['rowFlag']==255:call(0x0204820C,'short-zero2',0,2);call(0x02048308)
                    else:
                        call(0x02218960);call(0x02218330,get(M.SLOTS+4,1));call(0x022188CC,get(M.SLOTS+4,1));call(0x02218B4C);call(0x022199B8);call(0x02219C6C)
                    field(3,7,1)
        elif state==7:put(M.SLOTS+4,1,255);call(0x02041538,0,2,30);field(3,2,1)
        elif state==8:
            call(0x02214FE0)
            if p['exitGate']==1:field(3,9,1);call(0x02045680,0)
            else:field(3,11,1)
            again=True
        elif state==9:call(0x02041538,1,2,10);field(3,10,1)
        elif state==10:
            call(0x02041814)
            if p['uiGate']!=1:call(0x022188AC);call(0x022185B4);call(0x02068AE8);call(0x021F7F9C);field(3,11,1);put(M.SLOTS+2,1,16);again=True
        elif state==11:
            call(0x02041814)
            if p['uiGate']!=1:call(0x022188AC);call(0x022185B4);field(3,12,1);call(0x02214FE0);value=p['exitGate']
        state=get(M.STATE+3,1)
        if state in[2,3,4,7]:
            if get(M.STATE+0x18)!=0:call(0x02218B74);field(0x18,0)
            if get(M.STATE+0x14)!=0:
                call(0x02063E38)
                for index in range(max(0,p['spriteCount'])):call(0x0204AEB4,get(M.STATE+4),1,2,1,1,signed8(p['spriteIds'][index]),p['spriteValues'][index],1)
                field(0x14,0)
        if state in[2,3,5]:
            call(0x022199B8);call(0x02219BA4);call(0x02219CE4,M.STATE+0x40);call(0x021DF1F0);call(0x021DF3BC,127)
            x,z=get(M.STATE+0x40,signed=True),get(M.STATE+0x48,signed=True)
            if x<0x80000:field(0x40,0x80000)
            if x>0x88000:field(0x40,0x88000)
            if z<0x60000:field(0x48,0x60000)
            if z>0x68000:field(0x48,0x68000)
            call(0x02219C88);call(0x02219728);call(0x022198E0);call(0x022198EC);call(0x0221994C)
        put(M.FLAG,4,1)
        if again:value=invoke()
        return value
    raw=invoke();actual=[]
    for row in result['calls']:
        args=row['preparedWords'][:]
        if row['entry']==0x0204820C:
            if row['bufferAtEntry']!='0000'or not M.STACK-65536<=args[0]<M.STACK:raise ValueError('764 source two-byte local view differs')
            args[0]='short-zero2'
        actual.append(dict(entry=row['entry'],kind=row['kind'],preparedWords=args))
    if actual!=calls:raise ValueError(('764 independent caller-word sequence differs',p['name'],actual,calls))
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError(('764 complete nonstack model differs',p['name']))
    observed=[row[1:]for row in result['nonstackWrites']]
    if strict_order and observed!=writes:raise ValueError(('764 original ordered write model differs',p['name']))
    if not strict_order and sorted(observed)!=sorted(writes):raise ValueError(('764 candidate write effects differ',p['name']))
    if result['coreRegistersAndCpsr'][0]!=raw or result['ownInvocations']!=invocations:raise ValueError(('764 actual recursion/raw return differs',p['name']))
    return dict(rawR0=raw,ownInvocations=invocations,finalState=get(M.STATE+3,1),orderedWritesEqual=observed==writes,nonstackWriteCount=len(writes),nativeReturnInstructions=len(result['actualNativeReturnEvents']),providedCalls=sum(row['kind']=='provided'for row in calls),completeNonstackModel=True)
