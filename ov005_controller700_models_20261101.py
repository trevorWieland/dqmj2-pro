import itertools
import struct
import ov005_controller700_machine_20261101 as M


def profiles():
    settings=[]
    for selector,path,subpath,menu in itertools.product([0,41,44,45,46,47,51,53,0xFFFFFFFF,0x80000000],[0,1,2],[0,0x80000000],[0,255]):settings.append(dict(selector=selector,pathWord=path,subpathWord=subpath,menuByte=menu))
    for selector,menu in itertools.product([42,43,50,52],[0,255]):settings.append(dict(selector=selector,menuByte=menu))
    for special,resource,mode,menu in itertools.product([0,1,2,0x80000000,0xFFFFFFFF],[False,True],[0,1,255,0xFFFFFF80],[0,255]):settings.append(dict(selector=48,specialWord=special,resourcePresent=resource,modeWord=mode,menuByte=menu))
    for tag,menu in itertools.product([0,2,3,4,255],[0,255]):settings.append(dict(selector=49,actorByte=tag,menuByte=menu))
    result=[]
    for seed,setting in enumerate(settings):
        p=dict(name=f'controller-{seed}',selector=0,pathWord=0,subpathWord=0,menuByte=0,specialWord=2,resourcePresent=False,modeWord=0,actorByte=0,allocationPresent=bool(seed%3),auxWord=[0,255,0x80000000,0xFFFFFFFF][seed%4],infoWord=[0,0x7FFFFFFF,0x80000000,0xFFFFFFFF][seed%4],sentinelWord=(0xA7001234+seed)&0xFFFFFFFF,outputWords=[[0,1,1,0],[99,12,31,6],[0xFFFFFF80,0xFFFFFFFF,0x80000000,255],[0xFFFFFFFF,0,0,0xFFFFFFFF]][seed%4],initialContext=[(index*17+seed*31+7)&255 for index in range(128)])
        p.update(setting);result.append(p)
    return result


def expected(result):
    p=result['profile'];expected=bytearray(result['before']);calls=[]
    def word(address,value):struct.pack_into('<I',expected,address-M.BASE,value&0xFFFFFFFF)
    def byte(address,value):expected[address-M.BASE]=value&255
    def call(entry,*words):calls.append(dict(entry=entry,preparedWords=list(words)))
    call(0x0200F3E0,M.CONTEXT+0x4C)
    for index,value in enumerate(p['outputWords']):word(M.CONTEXT+0x4C+index*4,value)
    word(M.CONTEXT+0x4C,p['outputWords'][0]+2000)
    call(0x02089804)
    word(M.CONTEXT+0x18,0)
    expected[M.BUFFER-M.BASE:M.BUFFER-M.BASE+0x2300]=bytes(0x2300)
    call(0x02089AA4,M.BUFFER,0x2300)
    call(0x021DECB0)
    if p['menuByte']==0:call(0x02041538,0,2,10)
    call(0x02063F6C);word(M.CONTEXT+0x40,M.INFO);word(M.CONTEXT+0x38,p['auxWord'])
    call(0x021DFACC);call(0x020642DC)
    selector=p['selector']
    if selector in[42,43]:
        call(0x021E026C,3,1 if selector==42 else 2,0,26,0,3);call(0x021E155C,1);call(0x01FF8580,1)
    elif selector==48:
        call(0x021E1048,87);call(0x021E0DE0,0);call(0x02064340)
        if p['specialWord']==1:
            call(0x021E155C,33);call(0x021E00B4,19,0,8,1);call(0x020BF4D4);byte(M.CONTEXT+4,p['modeWord']);call(0x021E026C,8,p['modeWord']&255,0,0,0,2);word(M.CONTEXT+0x48,1);call(0x02064340);word(M.FLAG,0)
        else:
            call(0x021E0FB0,p['infoWord'])
            if p['resourcePresent']:call(0x02048094,0x02630000,0);call(0x021E0730,19,2,12)
            else:call(0x021E0730,19,2,13)
            call(0x021E155C,32);call(0x021E0DE0,0)
    elif selector==52:
        call(0x021E0DE0,1);call(0x021E026C,4,0,0,1,0,0);call(0x021E155C,0)
    elif selector==49:
        call(0x020BF218)
        if p['actorByte']==3:
            call(0x020BF218);call(0x02048034,M.ACTOR+0xB0,0);call(0x021E0708,19,2,14);call(0x021E155C,53);word(M.CONTEXT+0x64,60)
        else:call(0x021E155C,28);call(0x01FF8580,1)
    elif selector==50:
        word(M.SENTINEL,0xFFFFFFFF);call(0x021E155C,29);word(M.CONTEXT+0x64,44);call(0x01FF8580,1)
    else:
        call(0x02064340);word(M.FLAG,0);call(0x020BEF58)
        if p['pathWord']==1:
            call(0x020BF084)
            if p['subpathWord']!=0:word(M.CONTEXT+0x18,1)
            call(0x021E155C,26);call(0x021E0DE0,0)
        else:
            call(0x021E155C,0);call(0x021E0DE0,1);call(0x021E026C,4,0,0,1,0,0);call(0x021E155C,0);call(0x021E0DF8,50);call(0x01FF8580,0);call(0x01FF8580,1)
    call(0x021E0E28);call(0x020BEF48,0);call(0x020642CC,0);call(0x0202A37C,1,0xA000,0x20)
    word(M.CONTEXT+0x28,M.ALLOC if p['allocationPresent']else 0)
    for offset in[0x14,0x34,0x2C,0x30]:word(M.CONTEXT+offset,0)
    for offset,value in[(9,3),(5,0),(7,0),(0,255)]:byte(M.CONTEXT+offset,value)
    if result['connected']:
        word(M.CALLCTX+4,1);call(0x020851D4);call(0x02085200);word(M.CALLFLAG,1);call(0x0204176C)
    return bytes(expected),calls


def model(result):
    ram,calls=expected(result);actual=[dict(entry=p['entry'],preparedWords=p['preparedWords'])for p in result['providedCalls']]
    if actual!=calls:raise ValueError(('700 independent supplied call order/words differ',result['profile']['name'],actual,calls))
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if result['after'][:lo]!=ram[:lo]or result['after'][hi:]!=ram[hi:]:
        mismatch=[hex(M.BASE+i)for i,(a,b)in enumerate(zip(result['after'],ram))if a!=b and not lo<=i<hi]
        raise ValueError(('700 independent complete nonstack RAM differs',result['profile']['name'],mismatch[:20]))
    expected_r0=8 if result['connected']else 0xFFFFFFFF
    if result['coreRegistersAndCpsr'][0]!=expected_r0:raise ValueError(('700 physicalR0 differs',result['profile']['name'],hex(result['coreRegistersAndCpsr'][0]),hex(expected_r0)))
    date=[x for x in result['providedCalls']if x['entry']==0x0200F3E0]
    if len(date)!=1 or date[0]['ramEffects']!=[dict(address=M.CONTEXT+0x4C,bytes=struct.pack('<4I',*result['profile']['outputWords']).hex())]:raise ValueError('700 supplied raw output effect differs')
    if result['connected']:
        returns=[r for r in result['watchedNativeReturns']if r['entry']==M.ENTRY]
        if len(returns)!=1 or returns[0]['returnedWords'][0]!=0xFFFFFFFF or returns[0]['returnPc']!=0x021DF680:raise ValueError('700 actual constructor callback return/discard path differs')
    return dict(expectedPhysicalR0=expected_r0,suppliedCalls=len(calls),completeNonstackRamMatches=True,slot0ResultIgnored=result['connected'])
