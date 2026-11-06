import struct
import ov003_config525_machine_20261101 as M
VALUES={0:[0,2,0,2,1,2],1:[1,2,1,1,1,2],2:[2,2,1,2,2,0]}


def profiles():
    rows=[]
    for kind in[0,1,2,3,4,255,256,0xFFFFFFFF]:
        for keys in[0,1,2,0x800,0x801,0x802,0x803,0xFFFF]:
            for seed in[0,0x89ABCDEF]:rows.append(dict(name=f'{kind:x}-{keys:x}-{seed:x}',kind=kind,keys=keys,seed=seed,mutateKind=None,selectionAfter=(kind+1)&3))
    for kind in range(4):
        for after in[0,3,256,0xFFFFFFFF]:
            for keys in[1,0x800]:rows.append(dict(name=f'mutated-{kind}-{after:x}-{keys:x}',kind=kind,keys=keys,seed=0x80000000,mutateKind=after,selectionAfter=0xDEADBEEF))
    return rows


def model(result,original):
    p=result['profile'];before=result['before'];want=bytearray(before);events=[];kind=p['kind'];config=list(struct.unpack_from('<6I',before,original['config']-M.BASE));returns=[0x0202A634,0x021DAD9C]
    def word(a,v):struct.pack_into('<I',want,a-M.BASE,v&0xFFFFFFFF)
    def event(a,prepared,configuration=None):
        e=dict(address=a,preparedWords=prepared)
        if configuration is not None:e['configuration']=configuration
        events.append(e)
    if kind<=3:
        values=VALUES[kind]if kind<3 else[3]+config[1:];returns.extend([0x020C36AC]*5 if kind==3 else[]);event(0x021DA3E4,[],values);event(0x021DA3D0,[])
        if p['mutateKind']is not None:kind=p['mutateKind'];word(original['kind'],kind)
    keys=p['keys'];returned=keys
    if keys&1:
        low=kind&255
        if low<=2:
            for a,v in zip(original['setters'],VALUES[low]):word(a,v)
            returns.extend(M.NATIVE[3:]);word(M.STATE+12,4)
        elif low==3:
            returns.extend([0x020C36AC]*2);word(original['config'],3)
            for i in range(6):word(M.COPY+i*4,struct.unpack_from('<I',want,original['config']-M.BASE+i*4)[0])
            word(M.STATE+4,1);want[M.STATE-M.BASE+1]=1;word(M.STATE+12,1);want[M.STATE-M.BASE]=0
        event(0x0205E7A8,[0xFFFFFFFF,0x52]);returned=0xB0550052
    elif keys&2:word(M.STATE+12,4);event(0x0205E7A8,[0xFFFFFFFF,0x53]);returned=0xB0550053
    elif keys&0x800:
        event(0x021DEAF8,[original['kind']]);word(original['kind'],p['selectionAfter']);value=want[M.TABLE-M.BASE+(kind&255)];event(0x021DEA38,[0x14,1,value,1,1,0x57]);word(M.STATE+12,3);returned=M.STATE
    actual=[]
    for e in result['providedEvents']:
        actual.append({k:v for k,v in e.items()if k in['address','preparedWords','configuration']})
        if e['address']==0x021DA3E4:actual[-1]['preparedWords']=[]
    if actual!=events:raise ValueError(('525 provider contracts differ',actual,events))
    if sorted(x['entry']for x in result['nativeReturns'])!=sorted(returns):raise ValueError('525 actual native return sequence membership differs')
    begin=M.ENTRY-M.BASE;end=begin+max(M.SIZE,result['extent']);cut=M.STACK-M.BASE
    if result['after'][:begin]!=bytes(want[:begin])or result['after'][end:cut-65536]!=bytes(want[end:cut-65536])or result['after'][cut+4096:]!=bytes(want[cut+4096:]):raise ValueError('525 independent complete RAM effects differ')
    if result['returnedR0']!=returned:raise ValueError(('525 independent physical R0 differs',hex(result['returnedR0']),hex(returned)))
    return dict(providerSequence=[e['address']for e in events],actualNativeDependencyReturns=len(returns),physicalR0=returned)
